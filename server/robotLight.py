#!/usr/bin/env python3
# File name   : servo.py
# Description : Control lights
# Author      : William
# Date        : 2019/02/23
import sys
import threading
import time
from dataclasses import dataclass
from typing import List

from RPi import GPIO
from rpi_ws281x import Adafruit_NeoPixel, Color


@dataclass
class FrontLed:
    R_pin: int
    G_pin: int
    B_pin: int

    def setup(self):
        GPIO.setup(self.R_pin, GPIO.OUT)
        GPIO.setup(self.G_pin, GPIO.OUT)
        GPIO.setup(self.B_pin, GPIO.OUT)

    def off(self):
        GPIO.output(self.R_pin, GPIO.HIGH)
        GPIO.output(self.G_pin, GPIO.HIGH)
        GPIO.output(self.B_pin, GPIO.HIGH)

    def on(self):
        GPIO.output(self.R_pin, GPIO.LOW)
        GPIO.output(self.G_pin, GPIO.LOW)
        GPIO.output(self.B_pin, GPIO.LOW)

    def blue(self):
        GPIO.output(self.R_pin, GPIO.HIGH)
        GPIO.output(self.G_pin, GPIO.HIGH)
        GPIO.output(self.B_pin, GPIO.LOW)

    def green(self):
        GPIO.output(self.R_pin, GPIO.HIGH)
        GPIO.output(self.G_pin, GPIO.LOW)
        GPIO.output(self.B_pin, GPIO.HIGH)

    def red(self):
        GPIO.output(self.R_pin, GPIO.LOW)
        GPIO.output(self.G_pin, GPIO.HIGH)
        GPIO.output(self.B_pin, GPIO.HIGH)

    def white(self):
        self.on()

    def cyan(self):
        GPIO.output(self.R_pin, GPIO.HIGH)
        GPIO.output(self.G_pin, GPIO.LOW)
        GPIO.output(self.B_pin, GPIO.LOW)

    def pink(self):
        GPIO.output(self.R_pin, GPIO.LOW)
        GPIO.output(self.G_pin, GPIO.HIGH)
        GPIO.output(self.B_pin, GPIO.LOW)

    def yellow(self):
        GPIO.output(self.R_pin, GPIO.LOW)
        GPIO.output(self.G_pin, GPIO.LOW)
        GPIO.output(self.B_pin, GPIO.HIGH)


class LedStrip:
    # Number of LED pixels.
    LED_COUNT = 12
    # GPIO pin connected to the pixels (18 uses PWM!).
    LED_PIN = 12
    # LED signal frequency in hertz (usually 800khz)
    LED_FREQ_HZ = 800000
    # DMA channel to use for generating signal (try 10)
    LED_DMA = 10
    # Set to 0 for darkest and 255 for brightest
    LED_BRIGHTNESS = 255
    # True to invert the signal (when using NPN transistor level shift)
    LED_INVERT = False
    # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_CHANNEL = 0

    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(
            self.LED_COUNT,
            self.LED_PIN,
            self.LED_FREQ_HZ,
            self.LED_DMA,
            self.LED_INVERT,
            self.LED_BRIGHTNESS,
            self.LED_CHANNEL,
        )
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def setColor(self, R: int, G: int, B: int) -> None:
        """Change color across display a pixel at a time."""
        color = Color(int(R), int(G), int(B))
        for pixel in range(self.strip.numPixels()):
            self.strip.setPixelColor(pixel, color)
            self.strip.show()

    def off(self) -> None:
        self.setColor(0, 0, 0)


class RobotLightController(threading.Thread):
    def __init__(self, *args, **kwargs):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.colorBreathR = 0
        self.colorBreathG = 0
        self.colorBreathB = 0
        self.breathSteps = 10

        self.left_led = FrontLed(R_pin=22, G_pin=23, B_pin=24)
        self.right_led = FrontLed(R_pin=10, G_pin=9, B_pin=25)
        self.left_led.setup()
        self.right_led.setup()
        self.strip = LedStrip()

        self.lightMode = "none"  #'none' 'police' 'breath'

        super().__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()

    def front_off(self):
        self.left_led.off()
        self.right_led.off()

    def front_on(self):
        self.left_led.on()
        self.right_led.on()

    def front_red(self):
        self.left_led.red()
        self.right_led.red()

    def front_green(self):
        self.left_led.green()
        self.right_led.green()

    def front_blue(self):
        self.left_led.blue()
        self.right_led.blue()

    def front_yellow(self):
        self.left_led.yellow()
        self.right_led.yellow()

    def front_pink(self):
        self.left_led.pink()
        self.right_led.pink()

    def front_cyan(self):
        self.left_led.cyan()
        self.right_led.cyan()

    def turnLeft(self):
        self.left.yellow()

    def turnRight(self):
        self.right.yellow()

    def pause(self):
        self.lightMode = "none"
        self.strip.setColor(0, 0, 0)
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def police(self):
        self.lightMode = "police"
        self.resume()

    def all_blue(self):
        self.strip.setColor(0, 0, 255)
        self.front_blue()

    def all_off(self):
        self.strip.off()
        self.front_off()

    def all_red(self):
        self.strip.setColor(255, 0, 0)
        self.front_red()

    def policeProcessing(self):
        while self.lightMode == "police":
            for i in range(0, 3):
                self.all_blue()
                time.sleep(0.05)

                self.all_off()
                time.sleep(0.05)

            if self.lightMode != "police":
                break

            time.sleep(0.1)
            for i in range(0, 3):
                self.all_red()
                time.sleep(0.05)

                self.all_off()
                time.sleep(0.05)

            time.sleep(0.1)

    def breath(self, R_input, G_input, B_input):
        self.lightMode = "breath"
        self.colorBreathR = R_input
        self.colorBreathG = G_input
        self.colorBreathB = B_input
        self.resume()

    def breathProcessing(self):
        while self.lightMode == "breath":
            for i in range(0, self.breathSteps):
                if self.lightMode != "breath":
                    break

                self.strip.setColor(
                    self.colorBreathR * i / self.breathSteps,
                    self.colorBreathG * i / self.breathSteps,
                    self.colorBreathB * i / self.breathSteps,
                )
                time.sleep(0.03)

            for i in range(0, self.breathSteps):
                if self.lightMode != "breath":
                    break
                self.strip.setColor(
                    self.colorBreathR - (self.colorBreathR * i / self.breathSteps),
                    self.colorBreathG - (self.colorBreathG * i / self.breathSteps),
                    self.colorBreathB - (self.colorBreathB * i / self.breathSteps),
                )
                time.sleep(0.03)

    def lightChange(self):
        if self.lightMode == "none":
            self.pause()
        elif self.lightMode == "police":
            self.policeProcessing()
        elif self.lightMode == "breath":
            self.breathProcessing()

    def run(self):
        while 1:
            self.__flag.wait()
            self.lightChange()
            pass


if __name__ == "__main__":
    RL = RobotLightController()
    RL.start()
    try:
        RL.front_on()
        input("Hit enter to continue...")
        RL.left_led.yellow()
        input("Hit enter to continue...")
        RL.left_led.cyan()
        input("Hit enter to continue...")
        RL.breath(70, 70, 255)
        input("Hit enter to continue...")
        RL.pause()
        input("Hit enter to continue...")
        RL.police()
        while True:
            time.sleep(1)

    finally:
        print("turning off...")
        RL.pause()
        RL.all_off()
