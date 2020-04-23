#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 18:13:21 2020

@author: ivanderjmw
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 20:35:52 2020
@author: tuandung
"""

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
import RPi.GPIO as GPIO
import time

servo_pin = 21
solenoid_pin = 22
l2i = = np.array([])

def run_lidar() # Need to reference to mover() in auto_nav.py
    global l2i
    # create numpy array
    l2i = np.array([msg.ranges])


def action(): #carry out requirements
    run_lidar()
    if l2i[0] == 1:
        rotation(45)
        solenoid_punch(1)
        time.sleep(1)
    elif l2i[0] == 0:
        print('Distance out of range')
        time.sleep(1)
    else:
        print('Distance not 1m')
        time.sleep(1)


def servo_setup(servo_pin): #set up servo motor
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    global p
    p = GPIO.PWM(servo_pin, 50)
    p.start(2.5)

def rotation(angle): #rotate servo 
    dc = angle/18 +2.5 #convert angle to duty cycle
    global p
    p.ChangeDutyCycle(dc) #rotate motor to needed angle 
    time.sleep(0.1)

def solenoid_setup(solenoid_pin): #setup solenoid
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(solenoid_pin, GPIO.OUT) 

def solenoid_punch(n): #make solenoid punch n times
    for i in range(0,n):
        GPIO.output(solenoid_pin, 1)
        time.sleep(0.2)
        GPIO.output(solenoid_pin, 0)
        time.sleep(0.2)

try:
    servo_setup(servo_pin)
    solenoid_setup(solenoid_pin)
    while True: 
        action()
        
except KeyboardInterrupt:
    lidar.StopScanning()
    lidar.Disconnect()
    p.stop()
    GPIO.cleanup()
