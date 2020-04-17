#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 05:56:04 2020

@author: juinhwaye
"""

#!/usr/bin/env python
import cv2
import numpy as np
import rospy
from std_msgs.msg import Float32
from collections import deque
import argparse
import imutils
import sys


def talker():
	rospy.init_node('ball_tracking1', anonymous=True)
	pubx=rospy.Publisher('coordinates_x',Float32,queue_size=1)
	puby=rospy.Publisher('coordinates_y',Float32,queue_size=1)
	rate = rospy.Rate(20) # 10hz
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", dest="/home/arabinda/catkin_ws/src/ros_seminar/scripts/ball_tracking_example.mp4",help="path")
	ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
	args = vars(ap.parse_args())

	redLower = (161, 110, 84)
	redUpper = (179, 255, 255)
	pts = deque(maxlen=64)
	if not args.get("video", False):
		camera = cv2.VideoCapture(0)
	else:
		camera = cv2.VideoCapture('args["video"]')

	while not rospy.is_shutdown():
		(grabbed, frame) = camera.read()
		if args.get("video") and not grabbed:
			break
		frame = imutils.resize(frame, width=600)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		# mask = cv2.erode(mask, None, iterations=2)
		# mask = cv2.dilate(mask, None, iterations=2)
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None
		if len(cnts) > 0:
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			if (M["m00"] != 0):
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
				#print(center)
				pubx.publish(int(M["m10"] / M["m00"]))
				puby.publish(int(M["m01"] / M["m00"]))
				rospy.loginfo(str('x')+str(int(M["m10"] / M["m00"])) + str('y') + str(int(M["m01"] / M["m00"])))
			rate.sleep()
			# if radius > 10:
			# 	cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			# 	cv2.circle(frame, center, 5, (0, 0, 255), -1)
		pts.appendleft(center)

		# cv2.imshow("Frame", frame)
		# if cv2.waitKey(1) & 0xFF==ord('q'):
		# 	break

	rospy.spin()


if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		video_capture.release()
		cv2.destroyAllWindows()
		pass
