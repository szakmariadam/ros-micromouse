#!/usr/bin/env python3

import math
import rospy
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
rospy.init_node('gps_waypoint_follower')

sub_odom = rospy.Subscriber ('/odom', Odometry, get_rotation)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(20)

rospy.loginfo("GPS waypoint follower node has started!")

cellLength=0.31

# Example waypoints [latitude, longitude]
waypoints = [[0.155, 0.155+cellLength]]

cmd_vel = Twist()
cmd_vel.linear.x = 0
cmd_vel.angular.z = 0

waypointIndex = 0
mazeIndexY, mazeIndexX=0,0
def get_lidar_data(msg):
    global ranges
    ranges=msg.ranges
    #print(ranges)

sub_lidar = rospy.Subscriber('/scan', LaserScan, get_lidar_data)



#maze=np.zeros((17,17))

maze = [[]]
for i in range(0,17):
    maze.append([])

for i in range(0,17):
    for j in range(0,17):
        maze[i].append([' '])

for i in range(0,17):
    for j in range(0,17):
        maze[i][j]=0


def check_walls(yaw_in):
    global backWall, rightWall, frontWall, leftWall 
    backWall = 'x' if ranges[1] < 0.3 else 2
    rightWall = 'x' if ranges[2] < 0.3 else 2
    frontWall = 'x' if ranges[3] < 0.3 else 2
    leftWall = 'x' if ranges[0] < 0.3 else 2
    print(yaw_in)
    if yaw_in < 0.2 and yaw_in > -0.2:
        # print("egyenesen")
        return [backWall, rightWall, frontWall, leftWall]
    elif yaw_in > 1.3708 and yaw_in < 1.7708:
        # print("bal")
        return [rightWall, frontWall, leftWall, backWall]
    elif yaw_in > 2.9415 or yaw_in < -2.9415:
        # print("hátra")
        return [frontWall, leftWall, backWall, rightWall]
    elif yaw_in < -1.3708 and yaw_in > -1.7708:
        # print("jobb")
        return [leftWall, backWall, rightWall, frontWall]
    

    #print(backWall, rightWall, frontWall, leftWall)
def maze_fill(mazeIndexX_in, mazeIndexY_in, maze_in, yaw_in):
    maze_in[mazeIndexX_in][mazeIndexY_in-1] = check_walls(yaw_in)[0]
    maze_in[mazeIndexX_in-1][mazeIndexY_in] = check_walls(yaw_in)[1]
    maze_in[mazeIndexX_in][mazeIndexY_in+1] = check_walls(yaw_in)[2]
    maze_in[mazeIndexX_in+1][mazeIndexY_in] = check_walls(yaw_in)[3]
    # print(maze_in)
    print("MAZEFILL MEG LETT HIVVA? WAYPOINT ELERVE")
    return maze_in

while not rospy.is_shutdown():
    #print(positionY, positionX)
    # print(yaw)

    distanceX, distanceY = waypoints[len(waypoints)-1][0]-positionX,waypoints[len(waypoints)-1][1]-positionY #haversine(latitude, longitude, waypoints[waypointIndex][0], waypoints[waypointIndex][1])

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
    print(waypoints[len(waypoints)-1])
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
            bearing=math.atan2((positionX-waypoints[len(waypoints)-1][0]), (-positionY+waypoints[len(waypoints)-1][1]))

        if abs(distanceY)+abs(distanceX) > 0.02 :
            cmd_vel.linear.x = -0.2
            isMoving=True
        else:
            cmd_vel.linear.x = 0
            isMoving=False

            cmd_vel.angular.z = 0
            isRotating=False

            rospy.loginfo("Target waypoint reached!")
            print(waypoints[len(waypoints)-1][0], waypoints[len(waypoints)-1][1])
            #bearing=math.atan2((positionX-waypoints[len(waypoints)-1][0]), (-positionY+waypoints[len(waypoints)-1][1]))
            print(bearing)
            print(yaw)
            print(isRotating)
            print(isMoving) 
            waypointIndex += 1
            print(waypointIndex)
            print(len(waypoints))
    pub.publish(cmd_vel)

    if waypointIndex == len(waypoints) and not(isRotating)and not(isMoving): #error: nincs mindig meghívva a valamiért
        
        if yaw < 0.2 and yaw > -0.2:
            mazeIndexX+=2
            maze=maze_fill(mazeIndexX, mazeIndexY, maze, yaw)
        elif yaw > 1.3708 and yaw < 1.7708:
            mazeIndexY+=2
            maze=maze_fill(mazeIndexX, mazeIndexY, maze, yaw)
        elif yaw < -2.9415 or yaw > 2.9415:
            mazeIndexX-=2
            maze=maze_fill(mazeIndexX, mazeIndexY, maze, yaw)
        elif yaw < -1.3708 and yaw >-1.7708:
            mazeIndexY-=2
            maze=maze_fill(mazeIndexX, mazeIndexY, maze, yaw)
        print(check_walls(0))
        if check_walls(0)[3]==2:   #ha robot saját koord rendszere szerint a bal oldalán nincs fal akkor:
            print("balra fog menni")
            if yaw < 0.2 and yaw > -0.2:
                
                waypoints.append([waypoints[waypointIndex-1][0]-cellLength,waypoints[waypointIndex-1][1]])
            elif yaw > 1.3708 and yaw < 1.7708:
               
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]-cellLength])
            elif yaw < -2.9415 or yaw > 2.9415:
                waypoints.append([waypoints[waypointIndex-1][0]+cellLength,waypoints[waypointIndex-1][1]])
            elif yaw < -1.3708 and yaw >-1.7708:
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]+cellLength])
            
        elif check_walls(0)[2]==2: #ha robot saját koord rendszere szerint előtte nincs fal akkor:
            print("egyenesen fog menni")
            if yaw < 0.2 and yaw > -0.2:
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]+cellLength])
            elif yaw > 1.3708 and yaw < 1.7708:
                waypoints.append([waypoints[waypointIndex-1][0]+cellLength,waypoints[waypointIndex-1][1]])
            elif yaw < -2.9415 or yaw > 2.9415:
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]-cellLength])
            elif yaw < -1.3708 and yaw >-1.7708:
                waypoints.append([waypoints[waypointIndex-1][0]-cellLength,waypoints[waypointIndex-1][1]])
            
        elif check_walls(0)[1]==2: #ha robot saját koord rendszere szerint a jobb oldalán nincs fal akkor:
            print("jobbra fog menni")
            if yaw < 0.2 and yaw > -0.2:
                waypoints.append([waypoints[waypointIndex-1][0]+cellLength,waypoints[waypointIndex-1][1]])
            elif yaw > 1.3708 and yaw < 1.7708:
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]+cellLength])
            elif yaw < -2.9415 or yaw > 2.9415:
                waypoints.append([waypoints[waypointIndex-1][0]-cellLength,waypoints[waypointIndex-1][1]])
            elif yaw < -1.3708 and yaw >-1.7708:
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]-cellLength])
       
        bearing=math.atan2((positionX-waypoints[len(waypoints)-1][0]), (-positionY+waypoints[len(waypoints)-1][1]))

        rospy.loginfo("Last target waypoint reached!")
        waypointIndex -= 1
    
    else:
        rate.sleep()
    
 