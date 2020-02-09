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

def callback(msg):
    # create numpy array
	laser_range = np.array([msg.ranges])
    #get wanted distance 
    distance = laser_range[0]
	#log info 
        rospy.loginfo ("Distance at 0 degree is %i", distance)
    
    return distance 

def scanner():
	# initialize node
	rospy.init_node('scanner', anonymous=True)

	# set the update rate to 1 Hz
	rate = rospy.Rate(1) # 1 Hz

	# subscribe to LaserScan data
	rospy.Subscriber('scan', LaserScan, callback)
    
	# wait until it is time to run again
	rate.sleep()

	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
    return callback(msg)


def servo_setup(servo_pin): #set up servo motor
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    p = GPIO.PWM(servo_pin, 50)
    p.start(2.5)

def rotation(angle): #rotate servo 
    dc = angle/18 +2.5 #convert angle to duty cycle
    p.ChangeDutyCycle(dc) #rotate motor to needed angle 
    time.sleep(0.1)

def solenoid_setup(solenoid_pin): #setup solenoid
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(solenoid_pin, GPIO.OUT) 

def solenoid_punch(n): #make solenoid punch n times
    for i in range(1,n):
        GPIO.output(solenoid_pin, 1)
        time.sleep(0.2)
        GPIO.output(solenoid_pin, 0)
        time.sleep(0.2)
        
try:
    servo_setup(servo_pin)
    solenoid_setup(solenoid_pin)
    while True: 
        if scanner() == 1:
            rotation(45)
            solenoid_punch(1)
        else:
            continue 
except rospy.ROSInterruptException:
    p.stop()
    GPIO.cleanup()
            
        
        
        
    
    