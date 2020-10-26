import io
import os
from flask import Flask, render_template, send_file, flash, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
from WeatherScreens.RingScreen import RingScreen
from WeatherScreens.QuadrantScreen import QuadrantScreen
from WeatherScreens.ImageScreen import ImageScreen
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
# TODO: Change this to your location
latitude = 32.132323
longitude = -100.764232


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/refresh")
def refresh():
    print("Refreshing...")
    from waveshare_epd import epd7in5_V2
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()
    screen = RingScreen((latitude, longitude))
    image = screen.get_image()
    epd.display(epd.getbuffer(image))
    epd.sleep()
    return {
        "success": True,
        "refresh": "OK",
        "change": 1
    }


@app.route("/api/preview/ringscreen")
def preview_ring():
    screen = RingScreen((latitude, longitude), mock_data=True)
    img_io = io.BytesIO()
    screen.get_image().save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route("/api/preview/quadrantscreen")
def preview_quadrant():
    screen = QuadrantScreen((latitude, longitude), mock_data=True)
    img_io = io.BytesIO()
    screen.get_image().save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route("/api/uploadImage", methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        print(f'file not in request.files')
        abort(500)
    file = request.files['file']
    if file.filename == '':
        print(f'filename empty')
        abort(500)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        screen = ImageScreen(file_path)
        screen.get_image().save(os.path.join(app.config['UPLOAD_FOLDER'], f'transformed_{filename}'), 'JPEG', quality=100)
        return {
            'imageUrl': f'transformed_{filename}'
        }


@app.route("/api/getimage/<image_name>")
def getimage(image_name):
    path = os.path.join(app.config['UPLOAD_FOLDER'], f'{image_name}')
    image_file = Image.open(path)
    img_io = io.BytesIO()
    image_file.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route("/api/display/<image_name>")
def display_image(image_name):
    path = os.path.join(app.config['UPLOAD_FOLDER'], f'{image_name}')
    image_file = Image.open(path)
    from waveshare_epd import epd7in5_V2
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()
    epd.display(epd.getbuffer(image_file))
    epd.sleep()
    return {
        "success": True,
        "refresh": "OK",
        "change": 1
    }
