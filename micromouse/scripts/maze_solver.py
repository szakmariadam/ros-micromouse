#!/usr/bin/env python3

import rospy
import math
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from sensor_msgs.msg import LaserScan
import numpy as np

def get_rotation (msg):
    global roll, pitch, yaw, positionX, positionY
    positionX  = msg.pose.pose.position.x
    positionY  = msg.pose.pose.position.y
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)

latitude, longitude = 0, 0
roll, pitch, yaw = 0, 0, 0
positionX, positionY=0.155,0.155
ranges= [0]*720
bearing =0
isRotating=False
isMoving=False

rospy.init_node('basic_node')  # Init the node with name "basic_node"

sub_odom = rospy.Subscriber ('/odom', Odometry, get_rotation)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(20)

rospy.loginfo("Maze solver node has started!")

cmd_vel = Twist()
cmd_vel.linear.x = 0
cmd_vel.angular.z = 0

waypointIndex = 1

#x --->
#y |
#  |
#  V

#megoldott labirintus fileból kiolvasása

matrix = [[]]

f=open("temp.txt","r")

temp=f.read()

f.close()

rows=0

for i in range(0,len(temp)):
    if temp[i]=="\n":
        rows=rows+1
        matrix.append([])
    elif temp[i]!="," and temp[i]!="\n":
        if temp[i+1]!="," and temp[i]!="\n":
            matrix[rows].append(temp[i]+temp[i+1])
        elif temp[i-1]=="," or temp[i-1]=="\n":
            matrix[rows].append(temp[i])

for i in range(0, len(matrix)):
    for j in range(0, len(matrix[0])):
         if matrix[i][j]!="x" and matrix[i][j]!="s" and matrix[i][j]!="g":
            matrix[i][j]=int(matrix[i][j])

for i in range(0,len(matrix)):
    print(matrix[i])


#waypointok kiszámolása

maze = matrix

start = [1,1]
goal = [9,9]

position = start

waypoints = [[0.155, 0.155]]

if maze[position[0]-1][position[1]]!='x' and maze[position[0]-1][position[1]]!=0:
    distance=maze[position[0]-2][position[1]]
    position[0]=position[0]-2
    waypoints.append([waypoints[len(waypoints)-1][0],round(waypoints[len(waypoints)-1][1]-0.31,3)])
elif maze[position[0]+1][position[1]]!='x' and maze[position[0]+1][position[1]]!=0:
    distance=maze[position[0]+2][position[1]]
    position[0]=position[0]+2
    waypoints.append([waypoints[len(waypoints)-1][0],round(waypoints[len(waypoints)-1][1]+0.31,3)])
elif maze[position[0]][position[1]-1]!='x' and maze[position[0]][position[1]-1]!=0:
    distance=maze[position[0]][position[1]-2]
    position[1]=position[1]-2
    waypoints.append([round(waypoints[len(waypoints)-1][0]-0.31,3),waypoints[len(waypoints)-1][1]])
elif maze[position[0]][position[1]+1]!='x' and maze[position[0]][position[1]+1]!=0:
    distance=maze[position[0]][position[1]+2]
    position[1]=position[1]+2
    waypoints.append([round(waypoints[len(waypoints)-1][0]+0.31,3),waypoints[len(waypoints)-1][1]])

while position!=goal:
    if maze[position[0]-1][position[1]]==distance-1:
        distance=maze[position[0]-2][position[1]]
        position[0]=position[0]-2
        waypoints.append([waypoints[len(waypoints)-1][0],round(waypoints[len(waypoints)-1][1]-0.31,3)])
    elif maze[position[0]+1][position[1]]==distance-1:
        distance=maze[position[0]+2][position[1]]
        position[0]=position[0]+2
        waypoints.append([waypoints[len(waypoints)-1][0],round(waypoints[len(waypoints)-1][1]+0.31,3)])
    elif maze[position[0]][position[1]-1]==distance-1:
        distance=maze[position[0]][position[1]-2]
        position[1]=position[1]-2
        waypoints.append([round(waypoints[len(waypoints)-1][0]-0.31,3),waypoints[len(waypoints)-1][1]])
    elif maze[position[0]][position[1]+1]==distance-1:
        distance=maze[position[0]][position[1]+2]
        position[1]=position[1]+2
        waypoints.append([round(waypoints[len(waypoints)-1][0]+0.31,3),waypoints[len(waypoints)-1][1]])

print(waypoints)

while not rospy.is_shutdown():
    #print(positionY, positionX)
    # print(yaw)

    distanceX, distanceY = waypoints[waypointIndex][0]-positionX,waypoints[waypointIndex][1]-positionY #haversine(latitude, longitude, waypoints[waypointIndex][0], waypoints[waypointIndex][1])

        # calculate heading error from yaw or bearing
    
    headingError = bearing - yaw
    if headingError > math.pi:
        headingError = headingError - (2 * math.pi) 
    if headingError < -math.pi:
        headingError = headingError + (2 * math.pi)

    #rospy.loginfo("Distance: %.3f m, heading error: %.3f rad." % (distanceX+distanceY, headingError))
    #rospy.loginfo("Bearing: %.3f rad, yaw: %.3f rad, error: %.3f rad" % (bearing, yaw, headingError))
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    # print(distanceX, distanceY)
    print(abs(distanceX)+abs(distanceY))
    # print(positionX, positionY)
    # print("-----------")
    print(waypoints[waypointIndex])
    # print("#####################")
    # print(yaw)
    # print(check_walls(yaw))
    # Heading error, threshold is 0.1 rad
    print(headingError)
    print(bearing)
    if abs(headingError) > 0.01:
        # Only rotate in place if there is any heading error
        cmd_vel.linear.x = 0
        isRotating=True
        if headingError >0.1:
            cmd_vel.angular.z = -0.2
        elif headingError < -0.1:   
            cmd_vel.angular.z = 0.2
        elif headingError> 0:
            cmd_vel.angular.z=-0.05
        elif headingError< 0:
            cmd_vel.angular.z=0.05
    else:
        # Only straight driving, no curves
        cmd_vel.angular.z = 0
        isRotating=False
        # Distance error, threshold is 0.2m
        if abs(distanceY)+abs(distanceX) < 0.15 and abs(distanceY)+abs(distanceX)>0.14:
            bearing=math.atan2((positionX-waypoints[waypointIndex][0]), (-positionY+waypoints[waypointIndex][1]))

        if abs(distanceY)+abs(distanceX) > 0.02 :
            cmd_vel.linear.x = -0.2
            isMoving=True
        else:
            cmd_vel.linear.x = 0
            isMoving=False

            cmd_vel.angular.z = 0
            isRotating=False

            rospy.loginfo("Target waypoint reached!")
            print(waypoints[waypointIndex][0], waypoints[waypointIndex][1])
            #bearing=math.atan2((positionX-waypoints[len(waypoints)-1][0]), (-positionY+waypoints[len(waypoints)-1][1]))
            print(bearing)
            print(yaw)
            print(isRotating)
            print(isMoving) 
            waypointIndex += 1
            print(waypointIndex)
            print(len(waypoints))
            bearing=math.atan2((positionX-waypoints[waypointIndex][0]), (-positionY+waypoints[waypointIndex][1]))
    pub.publish(cmd_vel)

    rate.sleep()