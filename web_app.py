from flask import Flask
from flask import send_file
from flask import make_response
from flask import render_template
from aero_tracer import AeroTracer
import threading


app = Flask(__name__)


@app.route('/picture')
def send_picture():
    response = make_response(render_template('picture.html'))
    response.headers['Content-type'] = 'image/jpg'
    return response


@app.route('/start')
def start():
    trace = AeroTracer()
    x = threading.Thread(target=trace.camera_rotating_start(), daemon=True)
