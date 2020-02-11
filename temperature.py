#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 20:38:08 2020

@author: ivanderjmw
"""
# Temperature Sensor

import time
import smbus

i2c_ch = 1

# Define I2C address 
i2c_address = 0x48

# Define register addresses
reg_temp = 0x00

# Read temperature registers and convert to degrees celsius
def read_temp():
        # Read 2 bytes of temperature register data
        regVal = bus.read_i2c_block_data(i2c_address, reg_temp, 2)
        print("1st byte", bin(regVal[0])) #print in binary
        print("2nd byte", bin(regVal[1]))
        
        # Combine both bytes to form 12-bit temperature valuie
        temp_combined = (regVal[0] << 4) | (regVal[1] >> 4)
        print ("combined", bin(temp_combined))
        
        # Convert 12-bit value to readable temperature in degrees C
        temp_degC = temp_combined * 400
        
        return temp_degC
