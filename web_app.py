from flask import Flask
from flask import send_file
from aero_tracer import AeroTracer
import threading


app = Flask(__name__)


@app.route('/picture')
def send_picture():
    return send_file("image.jpg", mimetype='image/jpg', as_attachment=True)


@app.route('/start')
def start():
    trace = AeroTracer()
    x = threading.Thread(target=trace.camera_rotating_start(), daemon=True)
