from picamera import PiCamera


class Camera:
    def take_picture(self):
        camera = PiCamera()
        camera.rotation = 180
        camera.capture('image.jpg')
