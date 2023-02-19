"""
This module is responsible for making the API call to OpenWeatherMap.org
Probably needs more testing, but it works for now.
use Weather(location) to create a new weather object
use get_temperature() to get the temperature in Celsius
use get_humidity() to get the humidity in %
"""
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

    def get_temperature(self):
        weather = self.get_weather()
        temp = weather['main']['temp']
        temp = temp - 273.15
        return temp

    def get_humidity(self):
        weather = self.get_weather()
        humidity = weather['main']['humidity']
        return humidity

