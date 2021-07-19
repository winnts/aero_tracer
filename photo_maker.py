from picamera import PiCamera


class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.rotation = 180

    def take_full_picture(self, picture_name):
        self.camera.resolution = (3280, 1930)
        self.camera.capture(picture_name)

    def take_small_picture(self, picture_name):
        self.camera.resolution = (640, 375)
        self.camera.capture(picture_name)
