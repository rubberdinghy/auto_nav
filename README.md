#The codes used for the video are under main folder. Please refer to the readme.md under that folder for inspection of those codes.

# The Turtle-Bot Project for EG2310  - Group 5 AY1920
This is a student project utilising the Robot Operating Syestem (ROS) on a turtlebot-burger. The code is written in python and is run in a Raspberry Pi 3 Model B+.
- Nguyen Tuan Dung
- Juin Hwaye Mong
- Ivander Jonathan
- Luo Yikai
- Keng Wei

## Goals of the Project
- Navigate and Map and unknown area no larger than 8mx8m
- Autonomously identify, aim, and fire a ping-pong ball projectile at a target from
the turtlebot no further than 2m away

## The details of the Maze
- Bounded Start and End points
- Walled obstacles
- Branches and cul-de-sacs
- No larger than 8mx8m
- No firing at targets until mapping is completed

## The details of the Targets
- Visual RGB and IR
- No bigger than A5, no smaller than A6 (paper size)
- Mission ends once target is hit or when rounds are expended
- Robot can carry a minimum of 1 ball, a maximum of 5 balls

## Scoring
- Speed of completion
- Dimensional accuracy of the map drawn
- Input-less navigation
