#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 19:48:04 2020

@author: tuandung
"""

from time import sleep 
import RPi.GPIO as GPIO 

class Stepper_Motor(object):
    def __init__(self, pins, mode=3):
        self.p1 = pins[0]
        self.p2 = pins[1]
        self.p3 = pins[2]
        self.p4 = pins[3] 
        self.mode = mode 
        self.deg_per_step = 0.9 
        self.steps_per_rev = int(360/0.9)
        self.step_angle = 0 # assume the way it is positioning is 0 degree 
        for p in pins: 
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)
    
    def _set_rpm(self, rpm): 
        """set rotation speed of stepper motor"""
        self._rpm = rpm 
        self._T = (60/rpm)/ self.steps_per_rev # amount of time to stop between signal
        
    rpm = property(lambda self: self.rpm, _set_rpm())
    def move_to(self, angle):
        """take the shortest route to chosen angle"""
        target_steps = int(angle/self.deg_per_step)
        steps = target_steps - self.step_angle
        steps = steps % self.steps_per_rev 
        
        if steps > self.steps_per_rev:
            steps -= self.steps_per_rev
            print "moving " + str(steps) + " steps"
            if self.mode == 2: 
                self._move_acw_2(-steps/8)
            else: 
                self._move_acw_3(-steps/8)
        else: 
            print "moving " + str(steps) + " steps" 
            if self.mode == 2: 
                self._move_cw_2(steps/8)
            else: 
                self._move_cw_3(steps/8)
        
        self.step_angle = target_steps
    
    def __clear(self):
        GPIO.output(self.p1, 0)
        GPIO.output(self.p2, 0)
        GPIO.output(self.p3, 0)
        GPIO.output(self.p4, 0)
    
    def _move_acw_2(self, big_steps): 
        self.__clear()
        for i in range(big_steps): 
            GPIO.output(self.p3, 0)
            GPIO.output(self.p1, 1)
            sleep(self._T * 2)
            GPIO.output(self.p2, 0)
            GPIO.output(self.p4, 1)
            sleep(self._T * 2)
            GPIO.output(self.p1, 0)
            GPIO.output(self.p3, 1)
            sleep(self._T * 2)
            GPIO.output(self.p4, 0)
            GPIO.output(self.p2, 1)
            sleep(self._T * 2)
            
    def _move_cw_2(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.p4, 0)
            GPIO.output(self.p2, 1)
            sleep(self._T * 2)
            GPIO.output(self.p1, 0)
            GPIO.output(self.p3, 1)
            sleep(self._T * 2)
            GPIO.output(self.p2, 0)
            GPIO.output(self.p4, 1)
            sleep(self._T * 2)
            GPIO.output(self.p3, 0)
            GPIO.output(self.p1, 1)
            sleep(self._T * 2)
    
    def _move_acw_3(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P1, 0)
            sleep(self._T)
            GPIO.output(self.P3, 1)
            sleep(self._T)
            GPIO.output(self.P4, 0)
            sleep(self._T)
            GPIO.output(self.P2, 1)
            sleep(self._T)
            GPIO.output(self.P3, 0)
            sleep(self._T)
            GPIO.output(self.P1, 1)
            sleep(self._T)
            GPIO.output(self.P2, 0)
            sleep(self._T)
            GPIO.output(self.P4, 1)
            sleep(self._T)

    def _move_cw_3(self, big_steps):
        self.__clear()
        for i in range(big_steps):
            GPIO.output(self.P3, 0)
            sleep(self._T)
            GPIO.output(self.P1, 1)
            sleep(self._T)
            GPIO.output(self.P4, 0)
            sleep(self._T)
            GPIO.output(self.P2, 1)
            sleep(self._T)
            GPIO.output(self.P1, 0)
            sleep(self._T)
            GPIO.output(self.P3, 1)
            sleep(self._T)
            GPIO.output(self.P2, 0)
            sleep(self._T)
            GPIO.output(self.P4, 1)
            sleep(self._T)
        
        
try:
    while True: 
        GPIO.setmode(GPIO.BOARD)
        m = Stepper_Motor([18,22,24,26])
        m.rpm = 5
        print ("Pause in seconds: " + str(m._T))
        m.move_to(90)
        sleep(1)
        m.move_to(0)
        sleep(1)
        m.mode = 2
        m.move_to(90)
        sleep(1)
        m.move_to(0)
        GPIO.cleanup()