#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from waveshare_epd import epd7in5_V2
from WeatherScreens.RingScreen import RingScreen
from WeatherScreens.QuadrantScreen import QuadrantScreen
from WeatherScreens.ImageScreen import ImageScreen
from datetime import datetime
from suntime import Sun, SunTimeException
from dateutil import tz
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
import argparse


parser = argparse.ArgumentParser(description="WeatherFrame CLI Utility")
parser.add_argument("--lat", type=float,
                    help="Latitude in decimal form")
parser.add_argument("--long", type=float,
                    help="Longitude in decimal form")
parser.add_argument("--owm", type=str,
                    help="OpenWeatherMap API Token")
parser.add_argument("--type", type=str,
                    help="Screen type")
parser.add_argument("--image", type=str,
                    help="Image path")
args = parser.parse_args()

owm_token = args.owm
screen_type = args.type

owm = pyowm.OWM(owm_token)
observation = owm.weather_at_coords(latitude, longitude)
w = observation.get_weather()
weather_data = {
    'wind': w.get_wind(),
    'humidity': w.get_humidity(),
    'temp': w.get_temperature('celsius'),
    'clouds': w.get_clouds(),
    'pressure': w.get_pressure(),
    'status': w.get_status(),
    'observation_time'; observation.get_reception_time(timeformat="iso")
}


try:
    latitude = args.lat
    longitude = args.long

    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    screen = None
    if screen_type == "ring":
        screen = RingScreen(coordinates=(latitude, longitude),
                            weather_data=weather_data)
    elif screen_type == "quadrant":
        screen = QuadrantScreen(coordinates=(latitude, longitude),
                                weather_data=weather_data)

    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()
    image = screen.get_image()
    epd.display(epd.getbuffer(image))
    epd.sleep()
except IOError as e:
    print(e)
