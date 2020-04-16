#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 01:05:56 2020

@author: ivanderjmw
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 22:30:44 2020

@author: tuandung
"""

from time import sleep 
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM)

class dc_motor(object):
    def __init__(self,pin):
        self.p = pin
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.p, 100)
        self.pwm.start(0)
    
    def change_pwm(self, value): 
        self.pwm.ChangeDutyCycle(value)
        self.pwm.start(value)

    def run(self): 
        GPIO.output(self.p, GPIO.HIGH)
        sleep(2)
        
    def stop(self):
        self.pwm.stop()
        
        
dc_left = dc_motor(18)
dc_right = dc_motor(12)


if __name__ == '__main__' :
    try:
        r_pwm = 0
        l_pwm = 0
        while  (True) :
            x = str(input('Enter direction (L/R):'))
            
            if(x == "R"):
                r_pwm = 100 - r_pwm
                print("r_pwm :" + str(r_pwm))

                dc_right.change_pwm(r_pwm)
            elif (x == "L"):
                l_pwm = 100 - l_pwm
                print("l_pwm :" + str(l_pwm))
                dc_left.change_pwm(l_pwm)
    
    		#dc_left.change_pwm(100)
           		#sleep(2)
            	#dc_left.stop()
            	#dc_right.change_pwm(50)
            	#sleep(1)
            	#dc_right.stop()
    except KeyboardInterrupt() :
        GPIO.cleanup()
    
        

