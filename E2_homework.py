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
laser_range = np.array([])

def get_laserscan(msg):
    global laser_range

    # create numpy array
    laser_range = np.array([msg.ranges])

def action():
    global laser_range 
    #start a node 
    rospy.init_node('action', anonymous = True)
    # subcribe to LaserScan Data 
    rospy.Subscriber('scan', LaserScan, get_laserscan)
    
    rate = rospy.Rate(5) # 5 Hz
    
    rospy.loginfo(['Distance in front is ' + str(laser_range[0])])
    
    if laser_range[0] == 1:
        rotation(45)
        solenoid_punch(1)
        time.sleep(1)
    else: 
        rate.sleep()


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
except rospy.ROSInterruptException:
    p.stop()
    GPIO.cleanup()
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()



        
        
    
    
