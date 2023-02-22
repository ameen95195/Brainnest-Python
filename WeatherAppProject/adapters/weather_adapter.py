# collaborate weather json with model class
from models.weather_model import *


def current_weather_adapter(current_weather_json) -> BaseWeatherModel:
    """
    get current weather data as json and return it as BaseWeatherModel object
    :param current_weather_json: json object of current weather response json
    :return: BaseWeatherModel object from key "main"
    """
    if current_weather_json is None:
        raise ValueError("No data in current_weather_json object #current_weather_adapter()")

    weather = WeatherModel(current_weather_json["weather"][0]["id"],
                           current_weather_json["weather"][0]["main"],
                           current_weather_json["weather"][0]["description"],
                           current_weather_json["weather"][0]["icon"])

    return BaseWeatherModel(current_weather_json["main"]["temp"],
                            current_weather_json["main"]["feels_like"],
                            current_weather_json["main"]["temp_min"],
                            current_weather_json["main"]["temp_max"],
                            current_weather_json["main"]["pressure"],
                            current_weather_json["main"]["humidity"],
                            weather)


def weather_adapter(weather_json) -> WeatherModel:
    """
    collaborate weather status from json into WeatherModel
    :param weather_json: json object of key "weather" in element of key "list" in forcast response json
    :return: WeatherModel object from key "weather"
    """

    if weather_json is None:
        raise ValueError("No data in weather_json object #weather_adapter()")

    return WeatherModel(weather_json["id"],
                        weather_json["main"],
                        weather_json["description"],
                        weather_json["icon"])


def forcast_weather_adapter(forcast_weather_json) -> ForcastWeatherModel:
    """
    get forcast weather data as json and return it as ForcastWeatherModel object
    :param forcast_weather_json: json object of element in key "list" in forcast weather response json
    :return: ForcastWeatherModel object from element in key "list"
    """

    if forcast_weather_json is None:
        raise ValueError("No data in forcast_weather_json object #forcast_weather_adapter()")

    return ForcastWeatherModel(forcast_weather_json["dt"],
                               current_weather_adapter(forcast_weather_json))


