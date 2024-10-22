import requests
from datetime import datetime
from .config import OPENWEATHERMAP_API_KEY, TEMPERATURE_UNIT

class OpenWeatherMapClient:
    BASE_URL = "http://api.openweathermap.org/data/2.5"

    def __init__(self):
        if not OPENWEATHERMAP_API_KEY:
            raise ValueError("OpenWeatherMap API key is not set")
        self.api_key = OPENWEATHERMAP_API_KEY

    def get_weather_data(self, city):
        """Get current weather data"""
        params = {
            'q': f"{city},IN",
            'appid': self.api_key,
            'units': 'metric' if TEMPERATURE_UNIT == 'celsius' else 'imperial'
        }
        try:
            response = requests.get(f"{self.BASE_URL}/weather", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            raise

    def get_forecast_data(self, city, days=5):
        """Get weather forecast data"""
        params = {
            'q': f"{city},IN",
            'appid': self.api_key,
            'units': 'metric' if TEMPERATURE_UNIT == 'celsius' else 'imperial'
        }
        try:
            response = requests.get(f"{self.BASE_URL}/forecast", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data: {e}")
            raise

    def parse_weather_data(self, data):
        """Parse current weather data with extended parameters"""
        return {
            'city': data['name'],
            'main': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind'].get('deg', 0),
            'clouds': data['clouds']['all'],
            'visibility': data.get('visibility', 0),
            'rain_1h': data.get('rain', {}).get('1h', 0),
            'snow_1h': data.get('snow', {}).get('1h', 0),
            'dt': data['dt']
        }

    def parse_forecast_data(self, data):
        """Parse forecast data"""
        forecasts = []
        for item in data['list']:
            forecast = {
                'city': data['city']['name'],
                'dt': item['dt'],
                'date_time': datetime.fromtimestamp(item['dt']),
                'main': item['weather'][0]['main'],
                'description': item['weather'][0]['description'],
                'temp': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'temp_min': item['main']['temp_min'],
                'temp_max': item['main']['temp_max'],
                'pressure': item['main']['pressure'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'wind_direction': item['wind'].get('deg', 0),
                'clouds': item['clouds']['all'],
                'pop': item.get('pop', 0),  # Probability of precipitation
                'rain_3h': item.get('rain', {}).get('3h', 0),
                'snow_3h': item.get('snow', {}).get('3h', 0)
            }
            forecasts.append(forecast)
        return forecasts