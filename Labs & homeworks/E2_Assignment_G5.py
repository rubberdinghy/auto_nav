#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 01:40:34 2020

@author: ivanderjmw
"""

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#servo_pin = 20
#solenoid_pin = 21

class servo:
    
    # Initializer / Instance attributes
    def __init__(self, pinnum):
        self.pin = pinnum
    
    def start (self):
        GPIO.setup(self.pin, GPIO.OUT)
        global p 
        p = GPIO.PWM(self.pin, 50)
        p.start (7.5)
        print(p)
        
    def move (self, x):
        global p
        print(p)
        if x<0 or x>180:
                print ("wrong value fuck")
                return
        else:
                p.ChangeDutyCycle (2.5 + (5 * x/90))
                time.sleep (1)
                return
            
class solenoid:
    
    # Initializer / Instance attributes
    def __init__(self, pinnum):
        self.pin = pinnum
    
    def start (self):
        GPIO.setup(self.pin, GPIO.OUT)
        return
        
    def toggle (self, toggle_time):
        GPIO.output(self.pin, 1)
        print("GPIO HIGH (on)")
        time.sleep(toggle_time)
        GPIO.output(self.pin, 0)
        print("GPIO HIGH (off)")
        time.sleep(toggle_time)
        return

# Initialize the two components
servo = servo(16)
servo.start()
solenoid = solenoid(21)
solenoid.start()


try:
    while True:
        servo.move(input(int))
        solenoid.toggle(.5)
        
        
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()