#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 01:40:34 2020

@author: ivanderjmw
"""

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

servo_pin = 20
solenoid_pin = 21


GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(solenoid_pin, GPIO.OUT)

p = GPIO.PWM(servo_pin, 50)

p.start (7.5)
        
def servodothething ():
    x = input(int)
    if x<0 or x>180:
            print ("wrong value fuck")
            return
    else:
            p.ChangeDutyCycle (2.5 + (5 * x/90))
            time.sleep (1)


try:
    while True:
        servodothething();
        GPIO.output(solenoid_pin, 1)
        print("GPIO HIGH (on)")
        time.sleep(1)
        GPIO.output(solenoid_pin, 0)
        print("GPIO HIGH (off)")
        time.sleep(1)
        
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()