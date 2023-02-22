"""
This module is responsible for making the API call to OpenWeatherMap.org
Probably needs more testing, but it works for now.
use Weather(location) to create a new weather object
use get_temperature() to get the temperature in Celsius
use get_humidity() to get the humidity in %
"""

try:
    import requests
except ImportError:
    from time import sleep
    print("Requests module not found, installing...")
    sleep(3)
    import os
    os.system("pip install requests")
    import requests


api_key = "8eecf449bc7b6049b0aff522cb7526f5"


class Weather:
    def __init__(self, location: str):
        global api_key
        self.location = location
        self.api_key = api_key

    def get_weather(self):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={self.location}&appid={self.api_key}'
        response = requests.get(url)
        return response.json()

    def get_lat_lon_coordinates(self):
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={self.location}&limit=5&appid={self.api_key}'
        response = requests.get(url).json()
        lat = response[0]['lat']
        lon = response[0]['lon']
        return [lat, lon]

    def get_forecast(self):
        coordinates = self.get_lat_lon_coordinates()
        lat = coordinates[0]
        lon = coordinates[1]
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}'
        response = requests.get(url)
        return response.json()

    def get_temperature(self):
        weather = self.get_weather()
        temp = weather['main']['temp']
        temp = temp - 273.15
        return f"{temp:.2f}°C"

    def get_humidity(self):
        weather = self.get_weather()
        humidity = weather['main']['humidity']
        return f"{humidity}%"


