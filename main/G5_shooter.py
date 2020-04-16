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

def shoot():
    dc_left = G5_dc_motor.dc_motor(18)
    dc_right = G5_dc_motor.dc_motor(12)
        
    time.sleep(5)

    dc_right.change_pwm(100)
    dc_left.change_pwm(100)

    G5_stepper.left(300)

    dc_right.stop()
    dc_left.stop()

def callback(msg):
  if msg.data == True:
    shoot()

def waiting():
  rospy.Subscriber("shoot_signal", Bool, callback)
  rospy.spin()
    

if __name__ == '__main__' :
  try:
    waiting()
  except KeyboardInterrupt():
    pass