#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 01:07:53 2020

@author: ivanderjmw
"""
import rospy
import G5_dc_motor
import G5_stepper
import time
import RPi.GPIO as GPIO
from std_msgs.msg import Bool

def shoot():

    rospy.loginfo("[SHOOTER] Initialising shooting sequence")
    rospy.loginfo("[SHOOTER] Turning on Motors")
    
    
    G5_dc_motor.dc_right.change_pwm(100)
    G5_dc_motor.dc_left.change_pwm(100)

    time.sleep(5)

    rospy.loginfo("[SHOOTER] Loading the ball")
    G5_stepper.left(300)

    dc_right.stop()
    dc_left.stop()

def callback(msg):
  rospy.loginfo("[SHOOTER] Received shoot_signal " + str(msg))
  if msg.data == True:
    shoot()

def waiting():
  GPIO.setwarnings(False)
  rospy.init_node('waiting', anonymous=True)

  rospy.Subscriber("shoot_signal", Bool, callback)
  rospy.spin()
    

if __name__ == '__main__' :
  try:
    waiting()
  except KeyboardInterrupt():
    pass