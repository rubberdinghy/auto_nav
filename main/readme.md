# Main Code of the Ninja-Turtlebot
The robot is set to accomplish two fairly different tasks. First being auto-navigation inside an enclosed maze, second being target detection and shooting.
## TurtleBot Package Requirements
These code is meant to run in a [TurtleBot3 - Burger](http://emanual.robotis.com/docs/en/platform/turtlebot3/specifications/) along with [ROS Kinetic Kame](http://wiki.ros.org/kinetic) running on Ubuntu 16.04.
Before using these python scripts, a pre-installation of the following programs must be done:
* [TurtleBot3 Setup](http://emanual.robotis.com/docs/en/platform/turtlebot3/setup/#setup) - Hardware setup for the Turtlebot
* [TurtleBot3 Bringup](http://emanual.robotis.com/docs/en/platform/turtlebot3/bringup/#ros-1-bringup) - Software to run to initialise the Turtlebot every boot up
* [SLAM with Rviz](http://emanual.robotis.com/docs/en/platform/turtlebot3/slam/#ros-1-slam) - Visualisation software to run in Ubuntu 16.04
* [Python 2.7](https://www.python.org/download/releases/2.7/) - To run the scripts both on Main Computer and on the Turtlebot
* Create a catkin workspace through `catkin_make`, then clone this repo to `~/catkin_ws/src/auto_nav/scripts/` and again `catkin_make`

## Auto Navigation
Accomplished using running `G5_auto_nav3.py`
### Preparation
* Run ROS Master in the Main Computer
```roscore```
* SSH to RaspBerry Pi and Launch TurtleBot3 Bringup
```roslaunch turtlebot3_bringup turtlebot3_robot.launch```
### Usage
The use of this code is for the Turtlebot to map an enclosed maze, and the turtlebot will move autonomously to try mapping all sections of the maze. When the mapping is complete, the computer will play a sound.
* Launch Rviz
```roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping```
* Run Auto_Nav code
```rosrun auto_nav G5_auto_nav3.py```

## Target Detection and Shooting
Accomplished using G5_go_and_shoot4.py, G5_shooter.py, and G5_camera.py
### Usage
