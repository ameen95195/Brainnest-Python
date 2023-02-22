# give every weather data a class model to make it eazier to use weather components as object

# temp static convert to °C
TEMP_CONVERTER_NUMBER = 273.15


class WeatherModel:
    """ Model for weather status like (cloudy)"""

    def __init__(self, ignored_id: str, main: str, description: str, icon: str):
        self.id = ignored_id
        self.main = main
        self.description = description
        self.icon = icon


class BaseWeatherModel:
    """Model for basic weather data """

    def __init__(self, temp, feels_like, temp_min, temp_max, pressure, humidity, weather_model: WeatherModel):
        self.temp = temp
        self.feels_like = feels_like
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.pressure = pressure
        self.humidity = humidity
        self.weather_model = weather_model

    def convert_to_c(self):
        self.temp -= TEMP_CONVERTER_NUMBER
        self.temp_min -= TEMP_CONVERTER_NUMBER
        self.temp_max -= TEMP_CONVERTER_NUMBER
        self.feels_like -= TEMP_CONVERTER_NUMBER

class ForcastWeatherModel(BaseWeatherModel):
    """ Model for forcast weather data """

    def __init__(self, dt, base_weather: BaseWeatherModel):
        self.dt = dt
        BaseWeatherModel.__init__(self, base_weather.temp, base_weather.feels_like, base_weather.temp_min,
                                  base_weather.temp_max, base_weather.pressure, base_weather.humidity,
                                  base_weather.weather_model)
