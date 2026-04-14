import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

leds = [16, 12, 25, 17, 27, 23, 22, 24]

up_button = 5
down_button = 6

GPIO.setup(leds, GPIO.OUT)
GPIO.setup(up_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(down_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

num = 0
sleep_time = 0.2

def dec2bin(value):
    return [int(element) for element in bin(value % 256)[2:].zfill(8)]

try:
    while True:
        up_pressed = GPIO.input(up_button)
        down_pressed = GPIO.input(down_button)

        if up_pressed and down_pressed:
            num = 255
            print("Double push! Max value:", num, dec2bin(num))
            time.sleep(sleep_time)
        
        elif up_pressed:
            num += 1
            if num > 255: num = 0
            print(num, dec2bin(num))
            time.sleep(sleep_time)

        elif down_pressed:
            num -= 1
            if num < 0: num = 0
            print(num, dec2bin(num))
            time.sleep(sleep_time)

        GPIO.output(leds, dec2bin(num))

except KeyboardInterrupt:
    print("\nStopped by user")
finally:
    GPIO.output(leds, 0)
    GPIO.cleanup()
