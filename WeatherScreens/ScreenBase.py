from PIL import Image, ImageDraw
from . import constants


class ScreenBase(object):

    def __init__(self):
        self.resolution = (constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT)
        self.image = Image.new('RGB',
                               self.resolution,
                               constants.Colors.WHITE)
    
    def render(self):
        draw = ImageDraw.Draw(self.image)
        draw.text((0, 0), "ScreenBase")
        return self.image
