#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:20:58 2020

@author: tuandung
"""

from time import sleep 
import RPi.GPIO as GPIO  


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
    
    def right(self, angle):
        step = int ((angle/360)*512)
        for i in range (step):
            self.Step8(self)
            self.Step7(self)
            self.Step6(self)
            self.Step5(self)
            self.Step4(self)
            self.Step3(self)
            self.Step2(self)
            self.Step1(self)
            print "Step left: " + str(i)
        
    def left(self,angle):
        step = int((angle/360)*512)
        for i in range (step):    
            self.Step1(self)
            self.Step2(self)
            self.Step3(self)
            self.Step4(self)
            self.Step5(self)
            self.Step6(self)
            self.Step7(self)
            self.Step8(self)  
            print "Step left: " + str(i)


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    m = Stepper_Motor([31,33,35,37])
    m.Motor_setup()
    m.right(90)
    sleep(1)
    m.left(270)
    sleep(1)
    GPIO.cleanup()