#!/usr/bin/env python3
# File name   : switch.py
# Production  : HAT
# Website     : www.gewbot.com
# Author      : William
# Date        : 2018/08/22

import RPi.GPIO as GPIO

ON = True
OFF = False

PORTS_TO_PIN = {
    1: 5,
    2: 6,
    3: 13,
}


def switchSetup() -> None:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)


def switch(port: int, status: bool) -> None:
    pin = PORTS_TO_PIN.get(port, None)
    if pin is None:
        raise Exception(f"Wrong Command, only ports {list(ports.keys())} allowed.")

    if status is ON:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)


def set_all_switch_off():
    switch(port=1, status=OFF)
    switch(port=2, status=OFF)
    switch(port=3, status=OFF)
