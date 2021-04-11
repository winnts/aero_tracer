from flask import Flask
from flask import send_file
from flask import render_template
from aero_tracer import AeroTracer
import threading


app = Flask(__name__)


@app.route('/picture')
def send_picture():
    return render_template("/opt/aero_tracer/templates/photo.html")


@app.route('/start')
def start():
    trace = AeroTracer()
    x = threading.Thread(target=trace.camera_rotating_start(), daemon=True)
