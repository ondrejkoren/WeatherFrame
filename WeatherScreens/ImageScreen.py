from PIL import Image, ImageDraw, ImageFont
from suntime import Sun, SunTimeException
from dateutil import tz
from datetime import datetime, date, timedelta
import pyowm
import math
from random import randrange
from . import constants
import dateutil.parser
from . import ScreenBase


class ImageScreen(ScreenBase.ScreenBase):

    def __init__(self,
                 path: str,
                 resolution: tuple = (constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT)):
        ScreenBase.ScreenBase.__init__(self)
        self.path = path
        self.resolution = resolution
    
    def render(self):
        image_file = Image.open(self.path)  # open colour image
        width, height = image_file.size  # Get dimensions
        scale = width/self.resolution[0]
        print("scale: ", scale)
        image_file = image_file.resize((int(width/scale), int(height/scale)), Image.ANTIALIAS)
        width, height = image_file.size  # Get dimensions
        new_x, new_y = 800, 480
        if width < height:
            new_x, new_y = new_y, new_x
        left = (width - new_x) / 2
        top = (height - new_y) / 2
        right = (width + new_x) / 2
        bottom = (height + new_y) / 2

        # Crop the center of the image
        image_file = image_file.crop((left, top, right, bottom))
        self.image = image_file.convert('1')  # convert image to black and white
        draw = ImageDraw.Draw(self.image)
        return self.image
