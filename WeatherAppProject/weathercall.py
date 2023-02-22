"""
This module is responsible for making the API call to OpenWeatherMap.org
Probably needs more testing, but it works for now.
use Weather(location) to create a new weather object
use get_temperature() to get the temperature in Celsius
use get_humidity() to get the humidity in %
temperature and humidity are stored as strings in the object
so you can use them as such object_name.temperature for temperature and object_name.humidity for humidity
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
        self.temperature = self.get_temperature()
        self.humidity = self.get_humidity()

    def get_weather(self):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={self.location}&appid={self.api_key}'
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



