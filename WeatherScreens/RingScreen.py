from PIL import Image, ImageDraw, ImageFont
from suntime import Sun, SunTimeException
from dateutil import tz
from datetime import datetime, date
import pyowm
import math
from random import randrange
from . import constants
from . import ScreenBase

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
LIGHT_GREY = (200, 200, 200)


class RingScreen(ScreenBase.ScreenBase):
    ring_padding = 10

    def __init__(self,
                 coordinates: tuple,
                 weather_data,
                 screen_resolution: tuple = (800, 480),
                 datetime=datetime.now().astimezone(tz.tzlocal())):
        ScreenBase.ScreenBase.__init__(self)
        self.weather_data = weather_data
        self.res = screen_resolution
        self.latitude, self.longitude = coordinates
        self.sun = Sun(self.latitude, self.longitude)

        # Get today's sunrise and sunset in UTC
        self.sunrise = self.sun.get_local_sunrise_time(datetime).astimezone(tz.tzlocal())
        self.sunset = self.sun.get_local_sunset_time(datetime).astimezone(tz.tzlocal())
        self.sunrise_angle, self.sunset_angle = RingScreen.get_sun_angles(self.sunrise, self.sunset)
        self.now = datetime.now().astimezone(tz.tzlocal())
        self.now_angle = (self.now.hour + (((100/60) * self.now.minute) / 100)) * 15

        print(f'Observation time: {weather_data["observation_time"]}')
        print(f'wind: {weather_data["wind"]}')
        print(f'humidity: {weather_data["humidity"]}')
        print(f'temp: {weather_data["temp"]}')
        print(f'status: {weather_data["status"]}')

    def draw_on_ring(self, theta: int, text: str, draw: ImageDraw, radius: int = constants.DISPLAY_HEIGHT / 2, rotate: int = 0):
        # forecast_font = ImageFont.truetype('weathericons-regular-webfont.ttf', size=80)
        forecast_font = ImageFont.truetype('Font.ttc', size=48)
        # correction for different frames of reference - right angle rotation
        theta = theta - 90 - rotate

        # First calculate x and y in reference to unit circle
        x_o = radius * math.cos(math.radians(theta))
        y_o = radius * math.sin(math.radians(theta))

        # Next transform x and y to square reference frame
        x_s = radius + x_o
        y_s = radius - y_o

        # transform to absolute reference frame
        # x = x_s + DISPLAY_WIDTH - (radius*2)
        # y = y_s
        x_abs = x_o + 400
        y_abs = y_o + radius

        # correct for render size
        text_width, text_height = draw.textsize(text, font=forecast_font)
        x = x_abs - (text_width/2)+(self.res[0]-self.res[1])/2
        y = y_abs + 10 + self.ring_padding

        # child_img = Image.new('RGBA', (text_height + 10, text_width + 10), (255, 255, 255, 0))
        # child_draw = ImageDraw.Draw(child_img)
        draw.text((x+2, y), text, fill=BLACK, font=forecast_font)
        draw.text((x, y+2), text, fill=BLACK, font=forecast_font)
        draw.text((x-2, y), text, fill=BLACK, font=forecast_font)
        draw.text((x, y-2), text, fill=BLACK, font=forecast_font)
        draw.text((x, y), text, fill=WHITE, font=forecast_font)

        # child_draw.text((0 + 2, 0), text, fill=(0,0,0,100), font=forecast_font)
        # child_draw.text((0, 0 + 2), text, fill=(0,0,0,100), font=forecast_font)
        # child_draw.text((0 - 2, 0), text, fill=(0,0,0,100), font=forecast_font)
        # child_draw.text((0, 0 - 2), text, fill=(0,0,0,100), font=forecast_font)
        # child_draw.text((0, 0), text, fill=(255,255,255,100), font=forecast_font)
        # child_img = child_img.rotate(angle=360-theta-90, expand=False)
        # mask = Image.new('RGBA', child_img.size, (0,0,0,100))
        # mask.rotate(angle=360-theta-90, expand=True)
        # return child_img, mask, x, y

    def render(self):
        draw = ImageDraw.Draw(self.image)
        font24 = ImageFont.truetype(constants.REGULAR_FONT, size=80)
        font18 = ImageFont.truetype(constants.REGULAR_FONT, 35)
        fa_font = ImageFont.truetype('fa-solid-900.ttf', 50)
        weather_font = ImageFont.truetype('weathericons-regular-webfont.ttf', 80)
        ring_thickness = 80

        # arc from sunrise to sunset (night portion)
        draw.pieslice((self.res[0]-self.res[1]+self.ring_padding, 0+self.ring_padding, self.res[0]-self.ring_padding, self.res[1]-self.ring_padding), start=self.sunset_angle - 90 - self.now_angle, end=self.sunrise_angle - 90 - self.now_angle,
                      fill=GREY, width=2)

        # arc from sunrise to sunset (night portion)
        draw.pieslice((self.res[0] - self.res[1] + self.ring_padding, 0 + self.ring_padding,
                       self.res[0] - self.ring_padding, self.res[1] - self.ring_padding),
                      start=self.sunset_angle - 90 - self.now_angle + 18, end=self.sunrise_angle - 90 - self.now_angle - 18,
                      fill=BLACK, width=2)

        # basic outer ring
        draw.ellipse((self.res[0] - self.res[1] + self.ring_padding, 0 + self.ring_padding,
                      self.res[0] - self.ring_padding, self.res[1] - self.ring_padding), width=2, outline=BLACK)

        # draw inner white circle so we can draw text
        draw.ellipse((self.res[0]-self.res[1]+ring_thickness+self.ring_padding, ring_thickness+self.ring_padding, self.res[0]-ring_thickness-self.ring_padding, self.res[1]-ring_thickness-self.ring_padding), fill=WHITE)

        # wind direction
        wind_ring_size = 0
        arc = 5
        draw.pieslice((self.res[0] - self.res[1] + self.ring_padding - wind_ring_size + ring_thickness, 0 + self.ring_padding - wind_ring_size + ring_thickness,
                       self.res[0] - self.ring_padding + wind_ring_size - ring_thickness, self.res[1] - self.ring_padding + wind_ring_size - ring_thickness),
                      start=self.weather_data["wind"]["deg"] - arc - 90 - self.now_angle, end=self.weather_data["wind"]["deg"] + arc - 90 - self.now_angle,
                      fill=LIGHT_GREY, width=2)
        # offset = 15
        # draw.ellipse((self.res[0]-self.res[1]+ring_thickness+self.ring_padding + offset, ring_thickness+self.ring_padding + offset,
        #               self.res[0]-ring_thickness-self.ring_padding - offset, self.res[1]-ring_thickness-self.ring_padding - offset),
        #              fill=WHITE)

        # draw inner circle outline
        draw.ellipse((self.res[0]-self.res[1]+ring_thickness+self.ring_padding, ring_thickness+self.ring_padding, self.res[0]-ring_thickness-self.ring_padding, self.res[1]-ring_thickness-self.ring_padding), width=2, outline=BLACK)

        temperature_text = f'{self.weather_data["temp"]["temp"]:.1f}°C'
        w, h = draw.textsize(temperature_text, font=font24)
        draw.text(((constants.DISPLAY_WIDTH-w)/2+(self.res[0]-self.res[1])/2, (constants.DISPLAY_HEIGHT-h)/2), temperature_text, font=font24, fill=BLACK)

        weather_icon = constants.WEATHER_ICONS[self.weather_data["status"]]
        w2, h2 = draw.textsize(weather_icon, font=weather_font)
        draw.text(((constants.DISPLAY_WIDTH-w2)/2+(self.res[0]-self.res[1])/2, ((constants.DISPLAY_HEIGHT-h2)/2)-h-25+self.ring_padding), weather_icon, font=weather_font, fill=BLACK)

        time_now_icon = u'\uf0d8'
        w3, h3 = draw.textsize(time_now_icon, font=fa_font)
        draw.text(((constants.DISPLAY_WIDTH-w3)/2+(self.res[0]-self.res[1])/2, ring_thickness-12+self.ring_padding), time_now_icon, font=fa_font, fill=BLACK)

        temperature_range_text = f'{self.weather_data["temp"]["temp_max"]:.0f}°C / {self.weather_data["temp"]["temp_min"]:.0f}°C'
        temp_r_txt_w, temp_r_txt_h = draw.textsize(temperature_range_text, font=font18)
        draw.text(((constants.DISPLAY_WIDTH-temp_r_txt_w)/2+(self.res[0]-self.res[1])/2, (constants.DISPLAY_HEIGHT-temp_r_txt_h)/2 + h + 15-self.ring_padding), temperature_range_text, font=font18, fill=BLACK)

        # Sunrise and sunset
        sun_font = ImageFont.truetype('weathericons-regular-webfont.ttf', 60)
        font = ImageFont.truetype(constants.REGULAR_FONT, size=60)
        sunrise_icon_text = u'\uf051'
        sun_icn_txt_w, sun_icn_txt_h = draw.textsize(sunrise_icon_text, font=sun_font)
        draw.text((10, 10), sunrise_icon_text, font=sun_font, fill=BLACK)
        sunrise_text = f'{self.sunrise.strftime("%H:%M")}'
        draw.text((10+sun_icn_txt_w+10, 10+5), sunrise_text, font=font, fill=BLACK)

        sunset_icon_text = u'\uf052'
        sun_icn_txt_w, sun_icn_txt_h = draw.textsize(sunset_icon_text, font=sun_font)
        draw.text((10, 10+sun_icn_txt_h+10), sunset_icon_text, font=sun_font, fill=BLACK)
        sunset_text = f'{self.sunset.strftime("%H:%M")}'
        draw.text((10 + sun_icn_txt_w + 10, 10 + 10 + sun_icn_txt_w + 5), sunset_text, font=font, fill=BLACK)

        sun_font = ImageFont.truetype('weathericons-regular-webfont.ttf', 60)
        font = ImageFont.truetype(constants.REGULAR_FONT, size=60)

        # Wind
        wind_font = ImageFont.truetype(constants.REGULAR_FONT, size=43)
        wind_icon_font = ImageFont.truetype('weathericons-regular-webfont.ttf', 40)
        if "deg" not in self.weather_data["wind"]:
            self.weather_data["wind"]["deg"] = 45
        wind_icon_text = u'\uf050'
        wind_icn_txt_w, wind_icn_txt_h = draw.textsize(wind_icon_text, font=wind_icon_font)
        draw.text((10, constants.DISPLAY_HEIGHT - 10 - wind_icn_txt_h), wind_icon_text, font=wind_icon_font, fill=BLACK)
        wind_text = ''
        if "gust" in self.weather_data["wind"]:
            wind_text = f'{(self.weather_data["wind"]["speed"] * 3.6):.1f} ({(self.weather_data["wind"]["gust"] * 3.6):.1f}) km/h'
        else:
            wind_text = f'{(wind["speed"] * 3.6):.1f} km/h'
        draw.text((10 + 15 + wind_icn_txt_h, constants.DISPLAY_HEIGHT - 10 - wind_icn_txt_h),
                  wind_text, font=wind_font, fill=BLACK)

        # Humidity
        hum_icon_text = u'\uf07a'
        hum_icn_txt_w, hum_icn_txt_h = draw.textsize(hum_icon_text, font=sun_font)
        draw.text((10, constants.DISPLAY_HEIGHT - 10 - hum_icn_txt_h - wind_icn_txt_h), hum_icon_text, font=sun_font, fill=BLACK)
        hum_text = f'{self.weather_data["humidity"]} %'
        draw.text((10 + hum_icn_txt_w + 5, constants.DISPLAY_HEIGHT - 5 - hum_icn_txt_h - wind_icn_txt_h + 5), hum_text, font=font, fill=BLACK)

        # Time
        refresh_icon = u'\uf021'
        refresh_icon_w, refresh_icon_h = draw.textsize(refresh_icon, font=fa_font)
        draw.text((10, constants.DISPLAY_HEIGHT/2 - 20), refresh_icon, font=fa_font, fill=GREY)
        time_text = self.now.strftime("%H:%M")
        time_text_w, time_text_h = draw.textsize(time_text, font=font)
        draw.text((10 + refresh_icon_w + 10, constants.DISPLAY_HEIGHT/2 - 30), time_text, font=font, fill=GREY)

        time=0
        for i in range(0, 360, 15):
            txt = str(time) if time % 3 == 0 else "·"
            # img, mask, x, y = self.draw_on_ring(theta=i, text=txt, draw=draw, radius=DISPLAY_HEIGHT/2 - ring_thickness/2, rotate=now_angle)
            self.draw_on_ring(theta=i, text=txt, draw=draw, radius=(constants.DISPLAY_HEIGHT / 2 - ring_thickness / 2)-self.ring_padding/2, rotate=self.now_angle)
            # self.image.paste(img, (int(x), int(y)), mask)
            time += 1

        self.image = self.image.convert('L')
        return self.image

    @staticmethod
    def get_sun_angles(sunrise_datetime: datetime, sunset_datetime:datetime):
        sunrise_decimal = sunrise_datetime.hour + (((100/60) * sunrise_datetime.minute) / 100)
        sunset_decimal = sunset_datetime.hour + (((100/60) * sunset_datetime.minute) / 100)
        sunrise_angle = sunrise_decimal * 15
        sunset_angle = sunset_decimal * 15
        return sunrise_angle, sunset_angle
