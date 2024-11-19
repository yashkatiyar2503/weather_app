from flask import Flask, render_template, request, jsonify
import requests
from PIL import Image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    city = request.form.get('city')
    result = get_weather(city)
    if result is None:
        return jsonify({'error': 'City not found'})

    return jsonify(result)


def get_weather(city):
    API_Key = '1479be5ef5c043fc857140638231810'
    url = f"http://api.weatherapi.com/v1/forecast.json?Key={API_Key}&q={city}&days=2&aqi=no&alerts=no"
    response = requests.get(url)

    if response.status_code == 404:
        return None

    weather = response.json()

    icon_id = weather['current']['condition']['icon']
    temperature = weather['current']['temp_c']
    description = weather['current']['condition']['text']
    city = weather['location']['name']
    country = weather['location']['country']
    humidity = weather['current']['humidity']
    wind = weather['current']['wind_kph']
    uv = weather['current']['uv']
    forecast_date = weather['forecast']['forecastday'][0]['date']
    max_temp = weather['forecast']['forecastday'][0]['day']['maxtemp_c']
    min_temp = weather['forecast']['forecastday'][0]['day']['mintemp_c']
    avg_temp = weather['forecast']['forecastday'][0]['day']['avgtemp_c']

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return {
        'temperature': temperature,
        'avg_temp': avg_temp,
        'description': description,
        'city': city,
        'country': country,
        'humidity': humidity,
        'wind': wind,
        'uv': uv,
        'forecast_date': forecast_date,
        'max_temp': max_temp,
        'min_temp': min_temp,
    }


@app.route('/weather')
def temp():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
        if weather_data is None:
            return render_template('error.html', message='City not found')

        # Render the template and pass weather data
        return render_template('weather.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run(debug=True)