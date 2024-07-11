document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const location = document.getElementById('location').value;
    const date = document.getElementById('date').value;
    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ location, date })
        });
        const result = await response.json();
        if (typeof result.prediction === 'string' && result.prediction === 'Error occurred') {
            document.getElementById('result').textContent = `Prediction: ${result.prediction}. Please check the console for more details.`;
        } else if (typeof result.prediction === 'string') {
            document.getElementById('result').textContent = `Prediction: ${result.prediction}`;
        } else {
            document.getElementById('result').innerHTML = `
                Condition: ${result.prediction.condition}<br>
                Temperature: ${result.prediction.temperature} °C<br>
                Humidity: ${result.prediction.humidity} %<br>
                Rainfall: ${result.prediction.rainfall} mm
            `;
            if (result.alarm) {
                document.getElementById('alarm').innerHTML = `
                    <div style="color: red; font-weight: bold;">
                        Warning: Severe weather conditions expected!
                    </div>
                `;
            } else {
                document.getElementById('alarm').innerHTML = '';
            }
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'An error occurred';
    }
});
