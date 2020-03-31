#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:20:58 2020

@author: tuandung
"""

from time import sleep 
import RPi.GPIO as GPIO  

GPIO.setmode(GPIO.BOARD)

class Stepper_Motor(object):
    def __init__(self,pins):
        self.IN1 = pins[0]
        self.IN2 = pins[1]
        self.IN3 = pins[2]
        self.IN4 = pins[3] 
        self.time = 0.001 
        self.pins = pins
    
    def Motor_setup(self):
        GPIO.setup(self.IN1,GPIO.OUT)
        GPIO.setup(self.IN2,GPIO.OUT)
        GPIO.setup(self.IN3,GPIO.OUT)
        GPIO.setup(self.IN4,GPIO.OUT)

        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, False)
        GPIO.output(self.IN4, False)
    
    def Step1(self):
        GPIO.output(self.IN4, True)
        sleep (self.time)
        GPIO.output(self.IN4, False)

    def Step2(self):
        GPIO.output(self.IN4, True)
        GPIO.output(self.IN3, True)
        sleep (self.time)
        GPIO.output(self.IN4, False)
        GPIO.output(self.IN3, False)

    def Step3(self):
        GPIO.output(self.IN3, True)
        sleep (self.time)
        GPIO.output(self.IN3, False)
    
    def Step4(self):
        GPIO.output(self.IN2, True)
        GPIO.output(self.IN3, True)
        sleep (self.time)
        GPIO.output(self.IN2, False)
        GPIO.output(self.IN3, False)

    def Step5(self):
        GPIO.output(self.IN2, True)
        sleep (self.time)
        GPIO.output(self.IN2, False)

    def Step6(self):
        GPIO.output(self.IN1, True)
        GPIO.output(self.IN2, True)
        sleep (self.time)
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, False)

    def Step7(self):
        GPIO.output(self.IN1, True)
        sleep (self.time)
        GPIO.output(self.IN1, False)

    def Step8(self):
        GPIO.output(self.IN4, True)
        GPIO.output(self.IN1, True)
        sleep (self.time)
        GPIO.output(self.IN4, False)
        GPIO.output(self.IN1, False)
        
    def left(self, step):
        for i in range (step):    
            Step1(self)
            Step2(self)
            Step3(self)
            Step4(self)
            Step5(self)
            Step6(self)
            Step7(self)
            Step8(self)  
            
    
    def right(self,step):
        for i in range (step):    
            Step8(self)
            Step7(self)
            Step6(self)
            Step5(self)
            Step4(self)
            Step3(self)
            Step2(self)
            Step1(self)