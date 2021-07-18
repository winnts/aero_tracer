from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
kit.servo[0].angle = 88


def move_to_angle(angle):
    kit.servo[0].angle = angle
