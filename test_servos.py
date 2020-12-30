#!/usr/bin/env python3
import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


# servo 1 -> 100 <> 560
# servo 0 -> 280 - 580
# servo 2 -> 

while True:
    step = 10
    maxnum = 700
    minnum = 100
    curnum = minnum
    while True:
        print(f"Step {curnum}")
        pwm.set_pwm(2, 0, curnum)
        curnum += step
        if curnum > maxnum:
            curnum = minnum

        time.sleep(1)
