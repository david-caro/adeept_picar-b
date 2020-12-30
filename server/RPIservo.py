#!/usr/bin/env python3
# File name   : servo.py
# Description : Control Servos
# Author      : William
# Date        : 2019/02/23
import random
import sys
import threading
import time
import logging
from typing import List
from dataclass import dataclass

from enum import Enum, auto

import Adafruit_PCA9685
from RPi import GPIO

"""
change this form 1 to -1 to reverse servos
"""
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


LOGGER = logging.getLogger(__name__)


class Servos(Enum):
    HEAD_VERTICAL = 0
    HEAD_HORIZONTAL = 1
    DIRECTION = 2


class ScMode(Enum):
    INIT = auto()
    AUTO = auto()
    CERTAIN = auto()
    QUICK = auto()
    WIGGLE = auto()


@dataclass
class Servo:
    pin: int
    name: str
    min_pos: int = 100
    max_pos: int = 560
    init_pos: int = 300
    buffer_pos: float = 300.0
    now_pos: int = 300
    last_pos: int = 300
    goal_pos: int = 300
    sc_speed: int = 0
    sc_direction: int = 1
    ing_goal: int = 300

    def move_to(self, new_position: int) -> None:
        """
        The position is an integer that corresponds to the 'angle' of the
        rotation, usually starting from 100 and to a maximum of 560.
        """
        pwm.set_pwm(servo.pin, 0, new_position)
        servo.last_pos = servo.init_pos
        servo.now_pos = servo.init_pos
        servo.buffer_pos = float(servo.init_pos)
        servo.goal_pos = servo.init_pos

    def move_to_angle(self, new_angle: int) -> None:
        """
        Given an angle between 0-180 move the servo there.
        """
        new_position = int(
            round((self.max_pos - self.min_pos) / 180 * new_angle, 0)
        )
        self.move_to(new_position)



class ServoCtrl(threading.Thread):
    NUM_SERVOS = 16
    INIT_VALUE = 300
    MAX_POS = 560
    MIN_POS = 100

    def __init__(self, *args, **kwargs) -> None:
        logging.debug("ServoCtrl.__init__")
        self.servos = [
            Servo(pin=Servos.HEAD_VERTICAL, name="HEAD_VERTICAL"),
            Servo(pin=Servos.HEAD_HORIZONTAL, name="HEAD_HORIZONTAL"),
            Servo(pin=Servos.DIRECTION, name="HEAD_VERTICAL"),
        ]
        self.ctrlRangeMax = self.MAX_POS
        self.ctrlRangeMin = self.MIN_POS
        self.angleRange = 180

        self.scMode = ScMode.AUTO
        self.scTime = 2.0
        self.scSteps = 30

        self.scDelay = 0.037
        self.scMoveTime = 0.037

        self.goalUpdate = 0
        self.wiggleID = 0
        self.wiggleDirection = 1

        super().__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()

    def pause(self) -> None:
        logging.debug("ServoCtrl.pause")
        print("......................pausing..........................")
        self.__flag.clear()

    def resume(self) -> None:
        logging.debug("ServoCtrl.resume")
        print("resuming")
        self.__flag.set()

    def handleMoveInit(self) -> None:
        logging.debug("ServoCtrl.handleMoveInit")
        for servo in self.servos:
            pwm.set_pwm(servo.pin, 0, servo.init_pos)
            servo.last_pos = servo.init_pos
            servo.now_pos = servo.init_pos
            servo.buffer_pos = float(servo.init_pos)
            servo.goal_pos = servo.init_pos

        self.pause()

    def initConfig(self, servo: Servo, initInput: int, moveTo: int) -> None:
        logging.debug("ServoCtrl.initConfig")
        if initInput > servo.min_pos and initInput < servo.max_pos:
            servo.init_pos = initInput
            if moveTo:
                pwm.set_pwm(ID, 0, serrvo.init_pos)
        else:
            print("initPos Value Error.")

    def moveInit(self) -> None:
        logging.debug("ServoCtrl.moveInit")
        self.scMode = ScMode.INIT

    def posUpdate(self) -> None:
        logging.debug("ServoCtrl.posUpdate")
        self.goalUpdate = 1
        for servo in self.servos:
            servo.last_pos = servo.now_pos

        self.goalUpdate = 0

    def speedUpdate(self, servos: List[Servo], speedInputs: List[int]) -> None:
        logging.debug("ServoCtrl.speedUpdate")
        for servo, speed in zip(servos, speedInputs):
            servo.sc_speed = speed

    def moveAuto(self) -> int:
        logging.debug("ServoCtrl.moveAuto")
        for servo in self.servos:
            servo.ing_goal = servo.goal_pos

        for step in range(0, self.scSteps):
            for servo in self.servos:
                if not self.goalUpdate:
                    servo.now_pos = int(
                        round(
                            (
                                servo.last_pos
                                + (
                                    (
                                        (servo.goal_pos - servo.last_pos)
                                        / self.scSteps
                                    )
                                    * (step + 1)
                                )
                            ),
                            0,
                        )
                    )
                    pwm.set_pwm(servo.pin, 0, servo.now_pos)

                if self.ingGoal != self.goalPos:
                    self.posUpdate()
                    time.sleep(self.scTime / self.scSteps)
                    return 1

            time.sleep((self.scTime / self.scSteps - self.scMoveTime))

        self.posUpdate()
        self.pause()
        return 0

    def moveCert(self) -> int:
        logging.debug("ServoCtrl.moveCert")
        for i in range(0, self.NUM_SERVOS):
        for servo in self.servos:
            servo.ing_geal = servo.goal_pos
            servo.buffer_pos = servo.last_pos

        while self.nowPos != self.goalPos:
            for servo in self.servos:
                if servo.last_pos < servo.goal_pos:
                    servo.buffer_pos += self.pwmGenOut(servo.sc_speed) / (
                        1 / self.scDelay
                    )
                    newNow = int(round(servo.buffer_pos[i], 0))
                    if newNow > servo.goal_pos:
                        newNow = servo.goal_pos

                    servo.now_pos = newNow

                elif servo.last_pos > servo.goal_pos:
                    servo.buffer_pos -= self.pwmGenOut(servo.sc_speed) / (
                        1 / self.scDelay
                    )
                    newNow = int(round(servo.buffer_pos, 0))
                    if newNow < servo.goal_pos:
                        newNow = servo.goal_pos

                    servo.now_pos = newNow

                if not self.goalUpdate:
                    pwm.set_pwm(i, 0, servo.now_pos)

                if self.ingGoal != self.goalPos:
                    self.posUpdate()
                    return 1

            self.posUpdate()
            time.sleep(self.scDelay - self.scMoveTime)

        else:
            self.pause()
            return 0

    def pwmGenOut(self, angleInput: int) -> int:
        """
        Given an angle between 0-180 return the 'position' the servo must move
        to.
        """
        logging.debug("ServoCtrl.pwmGenOut")
        return int(
            round(
                (
                    (self.ctrlRangeMax - self.ctrlRangeMin)
                    / self.angleRange
                    * angleInput
                ),
                0,
            )
        )

    def setAutoTime(self, autoSpeedSet: int) -> None:
        logging.debug("ServoCtrl.setAutoTime")
        self.scTime = autoSpeedSet

    def setDelay(self, delaySet: int) -> None:
        logging.debug("ServoCtrl.setDelay")
        self.scDelay = delaySet

    def autoSpeed(self, servos: List[Servo], angleInputs: List[int]):
        logging.debug("ServoCtrl.autoSpeed")
        self.scMode = ScMode.AUTO
        self.goalUpdate = 1
        for servo, angle in zip(servos, angleInputs):
            newGoal = (
                servo.init_pos
                + self.pwmGenOut(angle) * servo.sc_direction
            )
            if newGoal > servo.max_pos:
                newGoal = servo.max_pos
            elif newGoal < servo.min_pos:
                newGoal = servo.min_pos

            servo.goal_pos = newGoal

        self.goalUpdate = 0
        self.resume()

    def certSpeed(
        self, servos: List[Servo], angleInputs: List[int], speeds: List[int]
    ):
        logging.debug("ServoCtrl.certSpeed")
        self.scMode = ScMode.CERTAIN
        self.goalUpdate = 1
        for servo, angle in zip(servos, angleInputs):
            newGoal = (
                servo.init_pos
                + self.pwmGenOut(angle) * servo.sc_direction
            )
            if newGoal > servo.max_pos:
                newGoal = servo.max_pos
            elif newGoal < servo.min_pos:
                newGoal = servo.min_pos

            servo.goalPos = newGoal
        self.speedUpdate(servos, speeds)
        self.goalUpdate = 0
        self.resume()

    def moveWiggle(self) -> None:
        logging.debug("ServoCtrl.moveWiggle")
        servo = self.servos[self.wiggleID]
        servo.buffer_pos += (
            self.wiggleDirection
            * servo.sc_direction
            * self.pwmGenOut(servo.sc_speed)
            / (1 / self.scDelay)
        )
        newNow = int(round(servo.buffer_pos, 0))
        if servo.buffer_pos > servo.max_pos:
            servo.buffer_pos = servo.max_pos

        elif servo.buffer_pos < servo.min_pos:
            servo.buffer_pos = servo.min_pos

        servo.now_pos = newNow
        servo.last_pos = newNow
        if (
            servo.buffer_pos < servo.max_pos
            and servo.buffer_pos > servo.min_pos
        ):
            pwm.set_pwm(servo.pin, 0, servo.now_pos)
        else:
            self.stopWiggle()

        time.sleep(self.scDelay - self.scMoveTime)

    def stopWiggle(self) -> None:
        logging.debug("ServoCtrl.stopWiggle")
        self.pause()
        self.posUpdate()

    def singleServo(self, ID: int, direcInput: int, speedSet: int):
        logging.debug("ServoCtrl.singleServo")
        self.wiggleID = ID
        self.wiggleDirection = direcInput
        self.servos[ID].sc_speed = speedSet
        self.scMode = ScMode.WIGGLE
        self.posUpdate()
        self.resume()

    def moveAngle(self, servo: Servo, angleInput: float) -> None:
        logging.debug("ServoCtrl.moveAngle")
        servo.now_pos = int(
            servo.init_pos + servo.sc_direction * self.pwmGenOut(angleInput)
        )
        if servo.now_pos > servo.max_pos:
            servo.now_pos = servo.max_pos

        elif servo.now_pos < servo.min_pos:
            servo.now_pos = servo.min_pos

        servo.last_pos = servo.now_pos
        pwm.set_pwm(servo.pin, 0, servo.now_pos)

    def scMove(self) -> None:
        logging.debug("ServoCtrl.scMove")
        if self.scMode == ScMode.INIT:
            self.handleMoveInit()
        elif self.scMode == ScMode.AUTO:
            self.moveAuto()
        elif self.scMode == ScMode.CERTAIN:
            self.moveCert()
        elif self.scMode == ScMode.WIGGLE:
            self.moveWiggle()

    def setPWM(self, servo: Servo, PWM_input: int) -> None:
        logging.debug("ServoCtrl.setPWM")
        servo.last_pos = PWM_input
        servo.now_pos = PWM_input
        servo.buffer_pos = float(PWM_input)
        servo.goal_pos = PWM_input
        pwm.set_pwm(servo.pin, 0, PWM_input)
        self.pause()

    def run(self):
        logging.debug("ServoCtrl.run")
        while True:
            self.__flag.wait()
            self.scMove()
            pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sc = ServoCtrl()
    sc.start()
    sc.moveInit()
    input("Hit enter to continue...")
    while 1:
        print("Starting loop")
        #sc.moveWiggle()
        new_angle = random.random() * 100 - 50
        print(f"  moving vertical head to angle {new_angle}")
        sc.moveAngle(ServoPins.HEAD_VERTICAL, new_angle)
        time.sleep(1)
        new_angle = random.random() * 100 - 50
        print(f"  moving horizontal head to angle {new_angle}")
        sc.moveAngle(ServoPins.HEAD_HORIZONTAL, new_angle)
        time.sleep(1)
        input("Hit enter to continue...")
        print("Ending loop")
        """
        sc.singleServo(0, 1, 5)
        time.sleep(6)
        sc.singleServo(0, -1, 30)
        time.sleep(1)
        """
        """
        delaytime = 5
        sc.certSpeed([0,7], [60,0], [40,60])
        print('xx1xx')
        time.sleep(delaytime)

        sc.certSpeed([0,7], [0,60], [40,60])
        print('xx2xx')
        time.sleep(delaytime+2)

        # sc.moveServoInit([0])
        # time.sleep(delaytime)
        """
        """
        pwm.set_pwm(0,0,560)
        time.sleep(1)
        pwm.set_pwm(0,0,100)
        time.sleep(2)
        """
        pass
    pass
