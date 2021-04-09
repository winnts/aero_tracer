from picamera import PiCamera


class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.rotation = 18

    def take_picture(self):
        self.camera.capture("image.jpg")
