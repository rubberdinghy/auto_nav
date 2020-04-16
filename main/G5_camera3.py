#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 05:56:04 2020
@author: juinhwaye
"""

#!/usr/bin/env python
# import the necessary packages

from imutils.video import WebcamVideoStream
class VideoStream:
	def __init__(self, src=0, usePiCamera=False, resolution=(320, 240), framerate=32):
		# check to see if the picamera module should be used
		if usePiCamera:
			# only import the picamera packages unless we are
			# explicity told to do so -- this helps remove the
			# requirement of `picamera[array]` from desktops or
			# laptops that still want to use the `imutils` package
			from pivideostream import PiVideoStream
			# initialize the picamera stream and allow the camera
			# sensor to warmup
			self.stream = PiVideoStream(resolution=resolution, framerate=framerate)
		# otherwise, we are using OpenCV so initialize the webcam
		# stream
		else:
			self.stream = WebcamVideoStream(src=src)
            
	def start(self):
		# start the threaded video stream
		return self.stream.start()
	def update(self):
		# grab the next frame from the stream
		self.stream.update()
	def read(self):
		# return the current frame
		return self.stream.read()
	def stop(self):
		# stop the thread and release any resources
		self.stream.stop()
		
		
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
	pub=rospy.Publisher('coordinates',Float32,queue_size=1)
	rate = rospy.Rate(20) # 10hz
        ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", dest="/home/arabinda/catkin_ws/src/ros_seminar/scripts/ball_tracking_example.mp4",help="path")
	ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
	args = vars(ap.parse_args())

	greenLower = (155, 103, 82)
	greenUpper = (178, 255, 255)
	pts = deque(maxlen=64)
	if not args.get("video", False):
		camera = VideoStream()
	else:
		camera = VideoStream('args["video"]')

	while not rospy.is_shutdown():
		(grabbed, frame) = camera.read()
		if args.get("video") and not grabbed:
			break
		frame = imutils.resize(frame, width=600)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None
		if len(cnts) > 0:
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			#print(center)
			pub.publish(int(M["m01"] / M["m00"]))
			rospy.loginfo(int(M["m01"] / M["m00"]))
			rate.sleep()
			if radius > 10:
				cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
		pts.appendleft(center)
		for i in xrange(1, len(pts)):
			if pts[i - 1] is None or pts[i] is None:
				continue
			thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
			cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

		cv2.imshow("Frame", frame)
		if cv2.waitKey(1) & 0xFF==ord('q'):
			break

	rospy.spin()
    
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
	camera.stop()
	cv2.destroyAllWindows()
	pass
