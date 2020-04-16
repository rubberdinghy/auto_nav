import cv2
import numpy as np 
import rospy
from picamera.array import PiRGBArray
from picamera import PiCamera 


def nothing(x):
    pass
 
cv2.namedWindow("Trackbars")
 
cv2.createTrackbar("B", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("G", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("R", "Trackbars", 0, 255, nothing)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(640, 480))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	B = cv2.getTrackbarPos("B", "Trackbars")
	G = cv2.getTrackbarPos("G", "Trackbars")
	R = cv2.getTrackbarPos("R", "Trackbars")

	green = np.uint8([[[B, G, R]]])
	hsvGreen = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
	lowerLimit = np.uint8([hsvGreen[0][0][0]-10,100,100])
	upperLimit = np.uint8([hsvGreen[0][0][0]+10,255,255])

	mask = cv2.inRange(hsv, lowerLimit, upperLimit)
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

	result = cv2.bitwise_and(image	, image	, mask=mask)

	cv2.imshow("frame", image)
	cv2.imshow("mask", mask)
	cv2.imshow("result", result)

	key = cv2.waitKey(1)
	rawCapture.truncate(0)
	if key == 27:
		break

cv2.destroyAllWindows()
