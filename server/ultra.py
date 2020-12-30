#!/usr/bin/python3
# File name   : Ultrasonic.py
# Description : Detection distance and tracking with ultrasonic
# Website     : www.gewbot.com
# Author      : William
# Date        : 2019/02/23
import time

import RPi.GPIO as GPIO

TRANSMITTER_PIN = 11
READER_PIN = 8
SPEED_OF_SOUND_MpS = 340


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMITTER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(READER_PIN, GPIO.IN)


def checkdist():
    """
    Backwards compatibility, remove when not used anymore.
    """
    return get_distance()

def get_distance() -> float:
    """
    Returns the current measured distance to what's in front of the sensor.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMITTER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(READER_PIN, GPIO.IN)

    GPIO.output(TRANSMITTER_PIN, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TRANSMITTER_PIN, GPIO.LOW)
    while not GPIO.input(READER_PIN):
        pass

    t1 = time.time()
    while GPIO.input(READER_PIN):
        pass

    t2 = time.time()
    return round((t2 - t1) * SPEED_OF_SOUND_MpS / 2, 2)


if __name__ == "__main__":
    while True:
        print(get_distance())
        time.sleep(1)
