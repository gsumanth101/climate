from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

WEATHERAPI_KEY = '3035c7e3f75347e68d352530241007'


RAIN_THRESHOLD = 10.0  # mm
TEMP_THRESHOLD = 35.0  # Celsius
WIND_SPEED_THRESHOLD = 74.0 # km/h

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET','POST'])
def predict():
    try:
        data = request.get_json()
        location = data['location']
        date = data['date']
        
        # Fetch future weather data
        weather_url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHERAPI_KEY}&q={location}&dt={date}"
        response = requests.get(weather_url)
        weather_data = response.json()

        print(f"Weather API Response: {weather_data}")  # Debugging line

        with open("data.json", "w") as f:
            json.dump(weather_data, f)

        if response.status_code == 200 and 'forecast' in weather_data:
            forecast_day = weather_data['forecast']['forecastday'][0]['day']
            prediction = {

                'condition': forecast_day['condition']['text'],
                'temperature': forecast_day['avgtemp_c'],
                'humidity': forecast_day['avghumidity'],
                'rainfall': forecast_day.get('totalprecip_mm', 0),
                'wind_speed': forecast_day.get('maxwind_mph', 0),
                'sunrise': weather_data['forecast']['forecastday'][0]['astro']['sunrise'],
                'sunset': weather_data['forecast']['forecastday'][0]['astro']['sunset'],
                'moonrise': weather_data['forecast']['forecastday'][0]['astro']['moonrise'],
                'moonset': weather_data['forecast']['forecastday'][0]['astro']['moonset']
                
            }
            
            # Check if alarm conditions are met
            cyclone_condition = (prediction['wind_speed'] > WIND_SPEED_THRESHOLD and prediction['rainfall'] > RAIN_THRESHOLD)
            alarm = (prediction['rainfall'] > RAIN_THRESHOLD or prediction['temperature'] > TEMP_THRESHOLD)
        else:
            prediction = "Unable to fetch weather data"
            alarm = False
            cyclone_condition = False

        return jsonify({'prediction': prediction, 'alarm': alarm, 'cyclone_condition': cyclone_condition})
        #return render_template('result.html')

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'prediction': 'Error occurred', 'alarm': False}), 500

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
