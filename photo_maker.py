from picamera import PiCamera


class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution(3280, 2464)

    def take_picture(self):
        self.camera.capture("image.jpg")
