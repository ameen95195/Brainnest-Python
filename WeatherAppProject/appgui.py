# GUI class file
import tkinter

from PIL import Image as PILImage
from PIL import ImageTk
from tkinter import *

from adapters.weather_adapter import *
from models.weather_model import *
from urllib.request import urlopen
from weathercall import *
from io import BytesIO
import datetime

# constants
FORCAST_DAYS = 4

# colors of program background
header_color = "#ffffff"
body_color = "#f2f2f2"

# fonts
h1_font = ("Arial", 25)
h2_font = ("Arial", 21)
h3_font = ("Arial", 17)
h4_font = ("Arial", 13)

root = Tk()
root.geometry("1000x750")
root.config(bg=body_color)

# global search text for city that will get its weather information
search_text = StringVar()

# current weather texts variables
temp_text = StringVar()  # hold temperature value for widget Label
feels_like_text = StringVar()  # will hold feels like temp and weather description for widget Label
humidity_with_min_max_temp_text = StringVar()  # will hold humidity, min and max temp for widget Label

# forcast weather texts variables
forcast_dates = [StringVar()] * FORCAST_DAYS
forcast_min_max_temp = [StringVar()] * FORCAST_DAYS
forcast_weather_description = [StringVar()] * FORCAST_DAYS

# weather icon
icon = None


def get_icon_url(icon_name: str):
    return f"http://openweathermap.org/img/wn/{icon_name}@2x.png"


def get_weather():
    weather = Weather(search_text.get())

    current_weather = current_weather_adapter(weather.get_weather())
    current_weather_assign_data(current_weather)

    forcast_weather_list = []
    # for loop to set forecast list into forcast adapter
    for forcast_weather_json in weather.get_forecast()["list"]:
        forcast_data = forcast_weather_adapter(forcast_weather_json)
        forcast_data.convert_to_c()
        forcast_weather_list.append(forcast_data)
    forcast_weather_assign_data(forcast_weather_list)  # send the list of forcast


def show_more_details():
    pass


def header_search_box(h_frame: Frame):
    """
    header search box for cities
    :param h_frame: header frame
    :return: none
    """
    global search_text, header_color
    search_frame = Frame(h_frame, bg=header_color)
    search_frame.pack(side=TOP, ipady=5, ipadx=10)

    search_btn = Button(search_frame, text="Search", bg="#48484a", fg="white", command=get_weather)
    search_btn.grid_configure(row=0, column=0, pady=10, padx=2)

    search_entry = Entry(search_frame, textvariable=search_text, width=30, bg="#f4f4f4", font=h3_font)
    search_entry.grid_configure(row=0, column=1, pady=10, padx=2)


def current_weather_assign_data(current_weather_data: BaseWeatherModel):
    """
    show current weather widgets
    :param current_weather_data: weather data
    :return: none
    """
    current_weather_data.convert_to_c()

    temp_text.set(f"{current_weather_data.temp:.0f}°C")
    feels_like_text.set(
        f"Feels like {current_weather_data.feels_like:.0f}°C. {current_weather_data.weather_model.description}")

    minmax = f"{current_weather_data.temp_max:.0f} / {current_weather_data.temp_min:.0f}°C"
    humidity_with_min_max_temp_text.set(f"Humidity: {current_weather_data.humidity}% --- {minmax}")

    im = PILImage.open(urlopen(get_icon_url(current_weather_data.weather_model.icon)))
    img = ImageTk.PhotoImage(im)
    icon.config(image=img)


def forcast_weather_assign_data(forcast_weather_data: [ForcastWeatherModel]):
    """
    show forcast weather widgets
    :param forcast_weather_data: forcast weather data
    :return:
    """
    # because forcast is giving list of weather data every 4 hours for 4 days and I need only one for each day
    # So we will define day variable to compare the incoming day with previous
    prev_day = datetime.date.today().day
    index = 0
    for forcast in forcast_weather_data:
        temp_date = datetime.datetime.fromtimestamp(forcast.dt)
        if temp_date.day == prev_day:
            continue
        if index >= len(forcast_dates):
            break

        prev_day = temp_date.day
        forcast_dates[index].set(temp_date.strftime("%d-%B-%Y"))

        minmax = f"{forcast.temp_max:.0f} / {forcast.temp_min:.0f}°C"
        forcast_min_max_temp[index].set(minmax)

        forcast_weather_description[index].set(forcast.weather_model.description)
        index += 1


def forcast_line_widget(frame_: Frame, index):
    global forcast_dates, forcast_min_max_temp, forcast_weather_description
    forcast_dates[index] = StringVar()
    forcast_min_max_temp[index] = StringVar()
    forcast_weather_description[index] = StringVar()
    Label(frame_, textvariable=forcast_dates[index], font=h4_font) \
        .grid_configure(row=index + 1, column=0)  # label for date

    Label(frame_, textvariable=forcast_min_max_temp[index], font=h4_font) \
        .grid_configure(row=index + 1, column=1)  # label for min max temp

    Label(frame_, textvariable=forcast_weather_description[index], font=h4_font) \
        .grid_configure(row=index + 1, column=2)  # label for weather status


header_frame = Frame(root, bg=header_color, padx=50)
header_frame.pack(fill="x")

body_frame = Frame(root, bg=body_color, padx=50, pady=25)
body_frame.pack(fill="both")

header_search_box(header_frame)

# frame of current weather widgets
current_weather_frame = Frame(body_frame, bg=body_color)
current_weather_frame.pack(side=LEFT, ipady=5, ipadx=5)

# frame of forcast weather widgets
bottom_frame = Frame(body_frame, bg=body_color)
bottom_frame.pack(side=BOTTOM, ipady=5, ipadx=5)
forcast_weather_frame = Frame(bottom_frame, bg=body_color)
forcast_weather_frame.pack(side=RIGHT, ipady=5, ipadx=5)

# =================current weather widgets====================
# icon of weather status
icon = Label(current_weather_frame)
icon.grid_configure(row=0, column=0)

# current date
date = datetime.date.today()
Label(current_weather_frame, text=date.strftime("%d-%B-%Y"), font=h4_font, fg="red") \
    .grid_configure(row=0, column=0)

# temp label and icon frame
temp_icon_frame = Frame(current_weather_frame)
temp_icon_frame.grid_configure(row=1, column=0, padx=2, pady=2)
# temp label
Label(temp_icon_frame, font=h1_font, textvariable=temp_text).grid_configure(row=1, column=1, padx=2, pady=2)

# Feels like label
Label(current_weather_frame, textvariable=feels_like_text, font=h3_font).grid_configure(row=2, column=0, padx=2, pady=2)

# Humidity and min_max temp widget
Label(current_weather_frame, textvariable=humidity_with_min_max_temp_text, font=h4_font).grid_configure(row=3, column=0,
                                                                                                        padx=2, pady=2)
# =====================================

# =================forcast weather widgets====================
Label(forcast_weather_frame, text="4-day forcast", font=h2_font).grid_configure(row=0, column=1, pady=2,
                                                                                padx=2)  # title label

forcast_line_widget(forcast_weather_frame, 0)
forcast_line_widget(forcast_weather_frame, 1)
forcast_line_widget(forcast_weather_frame, 2)
forcast_line_widget(forcast_weather_frame, 3)

# =====================================

root.mainloop()
