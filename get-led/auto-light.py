import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

led = 26

GPIO.setup(led, GPIO.OUT)

photo_sensor = 6

GPIO.setup(photo_sensor, GPIO.IN)

try:
    while True:
        GPIO.output(led, not GPIO.input(photo_sensor))
except KeyboardInterrupt:
    GPIO.cleanup()
