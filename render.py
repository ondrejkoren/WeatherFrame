from WeatherScreens.RingScreen import RingScreen
from WeatherScreens.QuadrantScreen import QuadrantScreen
from WeatherScreens.ImageScreen import ImageScreen
from WeatherScreens.ScreenBase import ScreenBase
from datetime import datetime, timedelta
from suntime import Sun, SunTimeException
from dateutil import tz
import pyowm
import argparse


if __name__ == "__main__":

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

    latitude = args.lat
    longitude = args.long
    owm_token = args.owm
    screen_type = args.type
    image_path = args.image

    # MOCK data
    weather_data = {
        'wind': {'speed': 33.5, 'deg': 190, 'gust': 42.12},
        'humidity': 100,
        'humidity_indoor': 47,
        'temp': {'temp': -33.77, 'temp_max': 0.56, 'temp_min': -2.0},
        'temp_indoor': 24.12,
        'status': 'Mist',
        'clouds': 90,
        'pressure': {'press': 1009, 'sea_level': 1038.381},
        'observation_time': "2020-01-25 09:04:34+00",
        'forecast': [
            {'status': 'Clouds', 'temp': {'temp': -0.52, 'temp_max': 0.83, 'temp_min': -0.52, 'temp_kf': -1.35}, 'wind': {'speed': 2.21, 'deg': 88}, 'date': "2020-01-26 15:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': -1.69, 'temp_max': -0.68, 'temp_min': -1.69, 'temp_kf': -1.01}, 'wind': {'speed': 1.73, 'deg': 80}, 'date': "2020-01-26 18:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': -1.75, 'temp_max': -1.07, 'temp_min': -1.75, 'temp_kf': -0.68}, 'wind': {'speed': 1.42, 'deg': 45}, 'date': "2020-01-26 21:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': -1.66, 'temp_max': -1.32, 'temp_min': -1.66, 'temp_kf': -0.34}, 'wind': {'speed': 1.32, 'deg': 8}, 'date': "2020-01-27 00:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': -1.56, 'temp_kf': -273.15, 'temp_max': -1.56, 'temp_min': -1.56}, 'wind': {'speed': 0.83, 'deg': 17}, 'date': "2020-01-27 03:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': -1.48, 'temp_kf': -273.15, 'temp_max': -1.48, 'temp_min': -1.48}, 'wind': {'speed': 1.09, 'deg': 317}, 'date': "2020-01-27 06:00:00+00"},
            {'status': 'Clear', 'temp': {'temp': 1.78, 'temp_kf': -273.15, 'temp_max': 1.78, 'temp_min': 1.78}, 'wind': {'speed': 1.53, 'deg': 302}, 'date': "2020-01-27 09:00:00+00"},
            {'status': 'Clear', 'temp': {'temp': 4.87, 'temp_kf': -273.15, 'temp_max': 4.87, 'temp_min': 4.87}, 'wind': {'speed': 1.39, 'deg': 267}, 'date': "2020-01-27 12:00:00+00"},
            {'status': 'Clear', 'temp': {'temp': 3.01, 'temp_kf': -273.15, 'temp_max': 3.01, 'temp_min': 3.01}, 'wind': {'speed': 1.96, 'deg': 187}, 'date': "2020-01-27 15:00:00+00"},
            {'status': 'Clear', 'temp': {'temp': 1.33, 'temp_kf': -273.15, 'temp_max': 1.33, 'temp_min': 1.33}, 'wind': {'speed': 3.08, 'deg': 141}, 'date': "2020-01-27 18:00:00+00"},
            {'status': 'Clear', 'temp': {'temp': 1.25, 'temp_kf': -273.15, 'temp_max': 1.25, 'temp_min': 1.25}, 'wind': {'speed': 3.64, 'deg': 140}, 'date': "2020-01-27 21:00:00+00"},
            {'status': 'Clear', 'temp': {'temp': 1.46, 'temp_kf': -273.15, 'temp_max': 1.46, 'temp_min': 1.46}, 'wind': {'speed': 5.11, 'deg': 138}, 'date': "2020-01-28 00:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 2.65, 'temp_kf': -273.15, 'temp_max': 2.65, 'temp_min': 2.65}, 'wind': {'speed': 6.79, 'deg': 142}, 'date': "2020-01-28 03:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 3.88, 'temp_kf': -273.15, 'temp_max': 3.88, 'temp_min': 3.88}, 'wind': {'speed': 5.3, 'deg': 164}, 'date': "2020-01-28 06:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 5.47, 'temp_kf': -273.15, 'temp_max': 5.47, 'temp_min': 5.47}, 'wind': {'speed': 5.01, 'deg': 143}, 'date': "2020-01-28 09:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 6.44, 'temp_kf': -273.15, 'temp_max': 6.44, 'temp_min': 6.44}, 'wind': {'speed': 3.59, 'deg': 335}, 'date': "2020-01-28 12:00:00+00"},
            {'status': 'Rain', 'temp': {'temp': 5.16, 'temp_kf': -273.15, 'temp_max': 5.16, 'temp_min': 5.16}, 'wind': {'speed': 3.21, 'deg': 264}, 'date': "2020-01-28 15:00:00+00"},
            {'status': 'Rain', 'temp': {'temp': 3.55, 'temp_kf': -273.15, 'temp_max': 3.55, 'temp_min': 3.55}, 'wind': {'speed': 3.59, 'deg': 321}, 'date': "2020-01-28 18:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 3.97, 'temp_kf': -273.15, 'temp_max': 3.97, 'temp_min': 3.97}, 'wind': {'speed': 7.12, 'deg': 301}, 'date': "2020-01-28 21:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 2.98, 'temp_kf': -273.15, 'temp_max': 2.98, 'temp_min': 2.98}, 'wind': {'speed': 6.25, 'deg': 277}, 'date': "2020-01-29 00:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 1.37, 'temp_kf': -273.15, 'temp_max': 1.37, 'temp_min': 1.37}, 'wind': {'speed': 3.69, 'deg': 263}, 'date': "2020-01-29 03:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 2.09, 'temp_kf': -273.15, 'temp_max': 2.09, 'temp_min': 2.09}, 'wind': {'speed': 5.82, 'deg': 213}, 'date': "2020-01-29 06:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 4.53, 'temp_kf': -273.15, 'temp_max': 4.53, 'temp_min': 4.53}, 'wind': {'speed': 3.18, 'deg': 260}, 'date': "2020-01-29 09:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 5.56, 'temp_kf': -273.15, 'temp_max': 5.56, 'temp_min': 5.56}, 'wind': {'speed': 11.16, 'deg': 291}, 'date': "2020-01-29 12:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 4.4, 'temp_kf': -273.15, 'temp_max': 4.4, 'temp_min': 4.4}, 'wind': {'speed': 9.39, 'deg': 296}, 'date': "2020-01-29 15:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 3.49, 'temp_kf': -273.15, 'temp_max': 3.49, 'temp_min': 3.49}, 'wind': {'speed': 12.78, 'deg': 298}, 'date': "2020-01-29 18:00:00+00"},
            {'status': 'Clear', 'temp': {'temp': 2.37, 'temp_kf': -273.15, 'temp_max': 2.37, 'temp_min': 2.37}, 'wind': {'speed': 6.79, 'deg': 288}, 'date': "2020-01-29 21:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 2.59, 'temp_kf': -273.15, 'temp_max': 2.59, 'temp_min': 2.59}, 'wind': {'speed': 8.32, 'deg': 292}, 'date': "2020-01-30 00:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 1.8, 'temp_kf': -273.15, 'temp_max': 1.8, 'temp_min': 1.8}, 'wind': {'speed': 7.83, 'deg': 294}, 'date': "2020-01-30 03:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 1.06, 'temp_kf': -273.15, 'temp_max': 1.06, 'temp_min': 1.06}, 'wind': {'speed': 5.74, 'deg': 303}, 'date': "2020-01-30 06:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 3.67, 'temp_kf': -273.15, 'temp_max': 3.67, 'temp_min': 3.67}, 'wind': {'speed': 9.05, 'deg': 305}, 'date': "2020-01-30 09:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 5.38, 'temp_kf': -273.15, 'temp_max': 5.38, 'temp_min': 5.38}, 'wind': {'speed': 9.72, 'deg': 299}, 'date': "2020-01-30 12:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 4.55, 'temp_kf': -273.15, 'temp_max': 4.55, 'temp_min': 4.55}, 'wind': {'speed': 4.51, 'deg': 294}, 'date': "2020-01-30 15:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 3.21, 'temp_kf': -273.15, 'temp_max': 3.21, 'temp_min': 3.21}, 'wind': {'speed': 4.77, 'deg': 298}, 'date': "2020-01-30 18:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 1.39, 'temp_kf': -273.15, 'temp_max': 1.39, 'temp_min': 1.39}, 'wind': {'speed': 1.37, 'deg': 269}, 'date': "2020-01-30 21:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 0.23, 'temp_kf': -273.15, 'temp_max': 0.23, 'temp_min': 0.23}, 'wind': {'speed': 1.08, 'deg': 155}, 'date': "2020-01-31 00:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': -0.07, 'temp_kf': -273.15, 'temp_max': -0.07, 'temp_min': -0.07}, 'wind': {'speed': 0.35, 'deg': 28}, 'date': "2020-01-31 03:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': -0.09, 'temp_kf': -273.15, 'temp_max': -0.09, 'temp_min': -0.09}, 'wind': {'speed': 0.47, 'deg': 342}, 'date': "2020-01-31 06:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 3.67, 'temp_kf': -273.15, 'temp_max': 3.67, 'temp_min': 3.67}, 'wind': {'speed': 1.49, 'deg': 286}, 'date': "2020-01-31 09:00:00+00"},
            {'status': 'Clouds', 'temp': {'temp': 6.95, 'temp_kf': -273.15, 'temp_max': 6.95, 'temp_min': 6.95}, 'wind': {'speed': 1.9, 'deg': 258}, 'date': "2020-01-31 12:00:00+00"}
        ]
    }
    # correct weather data forecast dates
    fixed_forecast = []
    now = datetime.now()
    datapoint_datetime = datetime.strptime(weather_data["forecast"][0]["date"], "%Y-%m-%d %H:%M:%S+00")
    diff = now - datapoint_datetime
    for x in weather_data["forecast"]:
        x_date = datapoint_datetime = datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S+00")
        x["date"] = x_date + timedelta(days=diff.days+1)
        x["date"] = x["date"].strftime("%Y-%m-%d %H:%M:%S+00")
        fixed_forecast.append(x)
    weather_data["forecast"] = fixed_forecast

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
        'observation_time': observation.get_reception_time(timeformat="iso")
    }
    screen = None
    if screen_type == "ring":
        screen = RingScreen(coordinates=(latitude, longitude),
                            weather_data=weather_data)
    elif screen_type == "quadrant":
        screen = QuadrantScreen(coordinates=(latitude, longitude),
                                weather_data=weather_data)
    elif screen_type == "image":
        screen = ImageScreen(path=image_path)
    else:
        screen = ScreenBase()

    image = screen.render()
    image.show()
