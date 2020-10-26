WEATHER_ICONS = {
    'Thunderstorm': u'\uf01e',
    'Drizzle': u'\uf04e',
    'Rain': u'\uf019',
    'Snow': u'\uf01b',
    'Mist': u'\uf014',
    'Smoke': u'\uf062',
    'Haze': u'\uf014',
    'Dust': u'\uf063',
    'Fog': u'\uf014',
    'Sand': u'\uf063',
    'Dust': u'\uf063',
    'Ash': u'\uf063',
    'Squall': u'\uf063',
    'Tornado': u'\uf056',
    'Clear': u'\uf00d',
    'Clouds': u'\uf041'
}

DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 480
REGULAR_FONT = "Font.ttc"


def get_wind_icon(degrees: int):
    if 0 <= degrees < 45:
        return u'\uf044'
    if 45 <= degrees < 90:
        return u'\uf043'
    if 90 <= degrees < 135:
        return u'\uf048'
    if 135 <= degrees < 180:
        return u'\uf058'
    if 180 <= degrees < 225:
        return u'\uf057'
    if 225 <= degrees < 270:
        return u'\uf04d'
    if 270 <= degrees < 315:
        return u'\uf088'
    if 315 <= degrees <= 359:
        return u'\uf044'
    return u'\uf044'


class Colors(object):
    WHITE: tuple = (255, 255, 255)
