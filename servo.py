import RPi.GPIO as GPIO
import time

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
p.start(92/16.3+1)  # Initialization


def move_to_angle(angle):
    try:
        p.ChangeDutyCycle(angle/16.3+1)
        time.sleep(1)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
