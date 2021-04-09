from flask import Flask
from flask import send_file
from aero_tracer import AeroTracer


app = Flask(__name__)
trace = AeroTracer()
trace.camera_rotating_start()


@app.route('/picture')
def send_picture():
    return send_file("image.jpg", mimetype='image/jpg')
