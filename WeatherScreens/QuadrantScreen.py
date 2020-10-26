from PIL import Image, ImageDraw, ImageFont
from suntime import Sun, SunTimeException
from dateutil import tz
from datetime import datetime, date, timedelta, timezone
import pyowm
import math
from random import randrange
from . import constants
import dateutil.parser
from . import ScreenBase


class QuadrantScreen(ScreenBase.ScreenBase):
    weather_font = ImageFont.truetype('weathericons-regular-webfont.ttf', 80)
    weather_forecast_font = ImageFont.truetype('weathericons-regular-webfont.ttf', 120)
    regular_font = ImageFont.truetype('Font.ttc', 80)
    regular_font_small = ImageFont.truetype('Font.ttc', 24)
    forecast_regular_font = ImageFont.truetype('Font.ttc', 50)
    fontawesome_font = ImageFont.truetype('fa-solid-900.ttf', 80)

    def __init__(self,
                 coordinates: tuple,
                 weather_data,
                 screen_resolution: tuple = (800, 480),
                 datetime=datetime.now().astimezone(tz.tzlocal())):
        ScreenBase.ScreenBase.__init__(self)
        self.weather_data = weather_data
        self.resolution = screen_resolution
        self.image = Image.new('L', screen_resolution, 255)
        self.location_coordinates = coordinates

    def render(self):
        draw = ImageDraw.Draw(self.image)
        draw.line((0, self.resolution[1] / 2, self.resolution[0], self.resolution[1] / 2), width=4)
        draw.line((self.resolution[0] / 2, 0, self.resolution[0] / 2, self.resolution[1]/2), width=4)
        self.paint_top_left(draw)
        self.paint_top_right(draw)
        self.paint_bottom(draw)
        return self.image

    def paint_top_left(self, draw: ImageDraw.ImageDraw):
        draw.text((10, 10), "OUTDOOR", font=self.regular_font_small)
        weather_icon_text = constants.WEATHER_ICONS[self.weather_data["status"]]
        weather_icon_w, weather_icon_h = draw.textsize(weather_icon_text, font=self.weather_font)
        draw.text((10, weather_icon_h/4), weather_icon_text, font=self.weather_font)
        draw.text((10 + weather_icon_w + 10, weather_icon_h/2), f'{self.weather_data["temp"]["temp"]:.1f}°C', font=self.regular_font)

        # Humidity
        hum_icon_text = u'\uf07a'
        hum_icn_txt_w, hum_icn_txt_h = draw.textsize(hum_icon_text, font=self.weather_font)
        draw.text((10, hum_icn_txt_w + weather_icon_h/2 + 10), hum_icon_text, font=self.weather_font)
        draw.text((10 + weather_icon_w + 10, weather_icon_h + hum_icn_txt_w - 20), f'{self.weather_data["humidity"]}%', font=self.regular_font)

    def paint_top_right(self, draw: ImageDraw.ImageDraw):
        draw.text((self.resolution[0]/2 + 10 + 5, 10), "INDOOR", font=self.regular_font_small)
        home_icon_text = u'\uf015'
        home_icon_w, home_icon_h = draw.textsize(home_icon_text, font=self.fontawesome_font)
        draw.text((self.resolution[0]/2 + 10 + 5, 10 + home_icon_h/2), home_icon_text, font=self.fontawesome_font)
        draw.text((self.resolution[0]/2 + 10 + home_icon_w + 10 + 5, 10 + home_icon_h/2), f'{self.weather_data["temp_indoor"]:.1f}°C', font=self.regular_font)

        # Humidity
        hum_icon_text = u'\uf07a'
        hum_icn_txt_w, hum_icn_txt_h = draw.textsize(hum_icon_text, font=self.weather_font)
        weather_icon_text = constants.WEATHER_ICONS[self.weather_data["status"]]
        weather_icon_w, weather_icon_h = draw.textsize(weather_icon_text, font=self.weather_font)
        draw.text((self.resolution[0]/2 + 10 + 5, hum_icn_txt_w + weather_icon_h / 2 + 10), hum_icon_text, font=self.weather_font)
        draw.text((self.resolution[0]/2 + home_icon_w + 10 + 10, weather_icon_h + hum_icn_txt_w - 20), f'{self.weather_data["humidity_indoor"]}%',
                  font=self.regular_font)

    def paint_bottom(self, draw: ImageDraw.ImageDraw):
        now = datetime.now()
        daily_forecast = {}
        for w in self.weather_data["forecast"]:
            w_date = dateutil.parser.parse(w['date'])
            if w_date.date() == now.date():
                continue
            date_key = w_date.strftime("%Y-%m-%d")
            if date_key not in daily_forecast:
                daily_forecast[date_key] = []
            daily_forecast[date_key].append(w)
        for i in range(1, 6):
            d = (datetime.now() + timedelta(days=i))
            d_key = d.strftime("%Y-%m-%d")

            icon_font = ImageFont.truetype('weathericons-regular-webfont.ttf', 90)
            d_icon = constants.WEATHER_ICONS[daily_forecast[d_key][0]["status"]]
            d_icon_w, d_icon_h = draw.textsize(d_icon, font=icon_font)
            draw.text(((i-1)*(d_icon_w+70)+10, self.resolution[1] - 120*2), d_icon, font=icon_font)

            d_temp = daily_forecast[d_key][0]["temp"]["temp"]
            d_temp_w, d_temp_h = draw.textsize(f'{d_temp:.0f}°C', font=self.forecast_regular_font)
            draw.text(((i-1)*(d_icon_w+70)+10+25, self.resolution[1]/2 + 120), f'{d_temp:.0f}°C', font=self.forecast_regular_font)

            d_dow = d.strftime("%a")
            d_dow_w, d_dow_h = draw.textsize(d_dow, font=self.forecast_regular_font)
            draw.text(((i-1)*(d_icon_w+70)+10+25, self.resolution[1]/2 + 180), d_dow, font=self.forecast_regular_font)
