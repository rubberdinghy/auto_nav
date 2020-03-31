#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 22:30:44 2020

@author: tuandung
"""

from time import sleep 
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM)

class dc_motor(object):
    def __init__(self,pin):
        self.p = pin
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(self.p, 100)
        pwm.start(100)
    
    def change_pwm(self, value): 
        self.ChangeDutyCycle(value)
    
    def run(self): 
        GPIO.output(self.p, GPIO.HIGH)
        sleep(2)
        
    def stop(self):
        GPIO.output(self.p, GPIO. LOW)
        self.pwm.stop()
        
        
        
        