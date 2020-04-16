#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 01:07:53 2020

@author: ivanderjmw
"""


import rospy
from nav_msgs.msg import Odometry
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
import math
import cmath
import numpy as np
import time


laser_range = np.array([])
occdata = np.array([])
target_x = 0
target_y = 0

yaw = 0.0
rotate_speed = 0.4
linear_speed = 0.17
stop_distance = 0.65
occ_bins = [-1, 0, 100, 101]
front_angle = 20
front_angles = range(-front_angle,front_angle+1,1)

shoot_distance = .5
distance_threshold = .02


def get_odom_dir(msg):
    global yaw

    orientation_quat =  msg.pose.pose.orientation
    orientation_list = [orientation_quat.x, orientation_quat.y, orientation_quat.z, orientation_quat.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)


def get_laserscan(msg):
    global laser_range

    # create numpy array
    laser_range = np.array(msg.ranges)
    # replace 0's with nan's
    # could have replaced all values below msg.range_min, but the small values
    # that are not zero appear to be useful
    laser_range[laser_range==0] = np.nan
    
def rotatebot(rot_angle):
    global yaw

    # create Twist object
    twist = Twist()
    # set up Publisher to cmd_vel topic
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    # set the update rate to 20 Hz
    rate = rospy.Rate(20)

    # get current yaw angle
    current_yaw = np.copy(yaw)
    # log the info
    rospy.loginfo(['Current: ' + str(math.degrees(current_yaw))])
    # we are going to use complex numbers to avoid problems when the angles go from
    # 360 to 0, or from -180 to 180
    c_yaw = complex(math.cos(current_yaw),math.sin(current_yaw))
    # calculate desired yaw
    target_yaw = current_yaw + math.radians(rot_angle)
    # convert to complex notation
    c_target_yaw = complex(math.cos(target_yaw),math.sin(target_yaw))
    rospy.loginfo(['Desired: ' + str(math.degrees(cmath.phase(c_target_yaw)))])
    # divide the two complex numbers to get the change in direction
    c_change = c_target_yaw / c_yaw
    # get the sign of the imaginary component to figure out which way we have to turn
    c_change_dir = np.sign(c_change.imag)
    # set linear speed to zero so the TurtleBot rotates on the spot
    twist.linear.x = 0.0
    # set the direction to rotate
    twist.angular.z = c_change_dir * rotate_speed
    # start rotation
    pub.publish(twist)

    # we will use the c_dir_diff variable to see if we can stop rotating
    c_dir_diff = c_change_dir
    # rospy.loginfo(['c_change_dir: ' + str(c_change_dir) + ' c_dir_diff: ' + str(c_dir_diff)])
    # if the rotation direction was 1.0, then we will want to stop when the c_dir_diff
    # becomes -1.0, and vice versa
    while(c_change_dir * c_dir_diff > 0):
        # get current yaw angle
        current_yaw = np.copy(yaw)
        # get the current yaw in complex form
        c_yaw = complex(math.cos(current_yaw),math.sin(current_yaw))
        rospy.loginfo('While Yaw: %f Target Yaw: %f', math.degrees(current_yaw), math.degrees(target_yaw))
        # get difference in angle between current and target
        c_change = c_target_yaw / c_yaw
        # get the sign to see if we can stop
        c_dir_diff = np.sign(c_change.imag)
        # rospy.loginfo(['c_change_dir: ' + str(c_change_dir) + ' c_dir_diff: ' + str(c_dir_diff)])
        rate.sleep()

   rospy.loginfo(['End Yaw: ' + str(math.degrees(current_yaw))])
    # set the rotation speed to 0
    twist.angular.z = 0.0
    # stop the rotation
    time.sleep(0.1)
    pub.publish(twist)
    
    stopbot()
    
    
def stopbot():
    # publish to cmd_vel to move TurtleBot
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    twist = Twist()
    twist.linear.x = 0.0
    twist.angular.z = 0.0
    time.sleep(1)
    pub.publish(twist)
    
def reversebot():
    # publish to cmd_vel to move TurtleBot
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    twist = Twist()
    twist.linear.x = -0.1
    twist.angular.z = 0.0
    time.sleep(1)
    pub.publish(twist)
    stopbot()
    
def forwardbot():
    # publish to cmd_vel to move TurtleBot
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    twist = Twist()
    twist.linear.x = 0.1
    twist.angular.z = 0.0
    time.sleep(1)
    pub.publish(twist)
    stopbot()



def takeaim():

    global laser_range
    
    #check_size
    #   if it is too big then move backwards, too small then move fowrards. Can also use the lidar data
    
#     lr0 = laser_range[0]
    
#     while (abs(lr0 - shoot_distance) < distance_threshold):
#         if (lr0 > shoot_distance):
#             reversebot()
#         elif (lr0 < shoot_distance):
#             forwardbot()
    
    rate = rospy.Rate(5) # Rate of 5 Hz

    # check_dir
    #   see the red target on camera. If it is not center, then rotate the bot slowly to center it.
    while (abs(target_x - 300) > 5):
        time.sleep(0.5)
        rospy.loginfo(str(target_x) + " " + str(target_y))

        if (target_x > 300):
            rospy.loginfo("left")
            rotatebot(-0.5)
        elif (target_x < 300):
            rospy.loginfo("right")
            rotatebot(0.5)

        rate.sleep()
    
    # When everything is aligned, rotate the bot 180 degrees to shoot.
    rotatebot(180.0)
    shooting = rospy.Publisher('shoot_signal', bool, queue_size=1)
    shooting.publish(bool(True))
    rospy.loginfo ('Running GUN!')


def searchshoot():
    
    global laser_range

    rospy.init_node('searchshoot', anonymous=True)

    # subscribe to odometry data
#     rospy.Subscriber('odom', Odometry, get_odom_dir)
#     # subscribe to LaserScan data
#     rospy.Subscriber('scan', LaserScan, get_laserscan)
    
    rospy.Subscriber('coordinates_y', Float32, get_target_y)
    rospy.Subscriber('coordinates_x', Float32, get_target_x)
    
    rate = rospy.Rate(1) # Rate of 1 Hz

    rotatebot(90)

    while not rospy.is_shutdown():
        rospy.loginfo("Now taking aim")
        takeaim()

        rate.sleep()
    
                     
def get_target_y(msg):
    global target_y
    target_y = float(str(msg).split(" ")[1])
         
def get_target_x(msg):
    global target_x
    target_x = float(str(msg).split(" ")[1])

    

if __name__ == '__main__':
    try:
        searchshoot()
    except rospy.ROSInterruptException:
        pass
