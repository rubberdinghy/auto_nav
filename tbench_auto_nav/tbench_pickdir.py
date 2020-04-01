#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 18:45:56 2020

@author: ivanderjmw
"""

import sys

import cmath
import math
import numpy as np
import time

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

# create global variables
rotated_size = 384
clear_color = 134
wall_color = 0
unmap_color = 65
square_size = 5

def check_region(x, y, arr):
    blocked = False
    unmapped = False
    
    for n in (-square_size, square_size):
        for m in (-square_size, square_size):
            if (arr[y + n][x + m][0] == wall_color):
                blocked = True
            if (arr[y + n][x + m][0] == unmap_color):
                unmapped = True
    
    if (blocked):
        return wall_color
    elif (unmapped):
        return unmap_color
    else: 
        return clear_color

def pick_direction(n, rotated): # NEED TO MODIFY THIS #
    
    
    print(['[PICKDIRECTION] '+'Picking direction...'])
    
    
    # Initialise found and angle
    found = False
    blocked_angle = False
    angle = 0.0
    angle2 = 180.0
    current = 0
    s_prev = 0
    
#    plt.imshow(rotated)
#    plt.pause(1)
    
    # Convert rotated map back to numpy array
    radar_map = np.array(rotated)
    
    time.sleep(1)
    
    # Check every 30 degrees.
    for i in range(0, 360, 1):
        # Initialize the line parameter
#        print(['[PICKDIRECTION] ' + 'Checking for angle at ' + str(i) + ' degrees'])
        
        s = 6.5
        
        # Using polar coordinates to index numpy array
        x_val = int(rotated_size/2 + s * math.sin(math.radians(i)))
        y_val = int(rotated_size/2 + s * math.cos(math.radians(i)))
        current = check_region(x_val, y_val, radar_map)
        
        radar_map[y_val][x_val][0] = 255
        
        for s in range (7, 500, 1):
            
#            sys.stdout.write(str(current))
            
            if (current == wall_color):
                blocked_angle = True
                break
            
            
            if (current == unmap_color):
                angle = i
                found = True
                break
            
            # Using polar coordinates to index numpy array
            x_val = int(rotated_size/2 + s * math.sin(math.radians(i))/2)
            y_val = int(rotated_size/2 + s * math.cos(math.radians(i))/2)
            current = check_region(x_val, y_val, radar_map)
            
            radar_map[y_val][x_val][0] = 255
        
#        print('')
        if (abs(s - s_prev) > square_size*5):
            angle2 = i
            
        s_prev = s
        
        if (blocked_angle):
            blocked_angle = False
            continue
        
        if (found):
            break
        
        time.sleep(.005)
        
    
     # create image from 2D array using PIL
    img = Image.fromarray(radar_map)
    plt.imshow(img)
    plt.pause(1)
    
    if (found):
        print(['[PICKDIRECTION] '+'Picked direction: ' + str(angle) + ' '])
    else:
        print(['[PICKDIRECTION] '+'Using angle2: ' + str(angle2)])
#        print(['[PICKDIRECTION] '+'Direction not found'])
        

#    # rotate to that direction
#    rotatebot(float(angle))
#
#    # start moving
#    rospy.loginfo(['Start moving'])
#    twist.linear.x = linear_speed
#    twist.angular.z = 0.0
    # not sure if this is really necessary, but things seem to work more
    # reliably with this
    time.sleep(1)
#    pub.publish(twist)
    
if __name__ == '__main__':
    try:
        for n in range (1, 5):
#            img = Image.open("maps/" + "map" + str(n) + ".png")
            img = Image.open("maps/" + "map" + str(n) + ".png").convert('LA')
            plt.imshow(img)
            plt.pause(0.5)
            pick_direction(n, img)
    except KeyboardInterrupt:
        pass