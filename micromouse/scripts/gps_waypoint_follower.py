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

def get_gps_coordinates(msg):
    global latitude, longitude
    latitude = msg.latitude
    longitude = msg.longitude
    #print(msg.latitude, msg.longitude)

def haversine(lat1, lon1, lat2, lon2):
    # Calculate distance
    R = 6378.137 # Radius of earth in km
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c * 1000 # in meters

    # Calculate heading
    y = math.sin(dLon) * math.cos(dLon)
    x = math.cos(lat1 * math.pi / 180) * math.sin(lat2 * math.pi / 180) - math.sin(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.cos(dLon)
    bearing = -math.atan2(y,x)

    return d, bearing

latitude, longitude = 0, 0
roll, pitch, yaw = 0, 0, 0
positionX, positionY=0.155,0.155
ranges= [0]*720
bearing =0
isRotating=False
isMoving=False
rospy.init_node('gps_waypoint_follower')

sub_odom = rospy.Subscriber ('/odom', Odometry, get_rotation)
sub_gps = rospy.Subscriber ('/navsat/fix', NavSatFix, get_gps_coordinates)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(10)

rospy.loginfo("GPS waypoint follower node has started!")

cellLength=0.18 #in meters

# Example waypoints [latitude, longitude]
waypoints = [[0.155, 0.155]]

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



maze=np.zeros((17,17))
#print(maze)
#cellTypes
#    0= none    1 =|     2= ‾  3=  |
#    4= _       5 =|‾    6=| | 7=|_  
#    8= ‾|       9= ‾_   10= _| 11=|‾| 
#    12=|‾_       13=|_|   14=‾_| 15=|_‾|
#
#    01010
#    1A0B1
#    01010
#    1C1D1
#    01010 
def check_walls(yaw_in):
    global backWall, rightWall, frontWall, leftWall 
    backWall = 1 if ranges[4] < 0.3 else 2
    rightWall = 1 if ranges[0] < 0.3 else 2
    frontWall = 1 if ranges[1] < 0.3 else 2
    leftWall = 1 if ranges[2] < 0.3 else 2
    
    if yaw < 0.1 or yaw > 6.283:
        return [backWall, rightWall, frontWall, leftWall]
    elif yaw_in > 1.4708 or yaw_in < 1.6708:
        return [rightWall, frontWall, leftWall, backWall]
    elif yaw_in > 4.6124 or yaw_in < 4.8124:
        return [frontWall, leftWall, backWall, rightWall]
    elif yaw > 4.6124 or yaw < 4.8124:
        return [leftWall, backWall, rightWall, frontWall]
    

    #print(backWall, rightWall, frontWall, leftWall)
def maze_fill(mazeIndexX_in, mazeIndexY_in, maze_in, yaw_in):
    maze_in[mazeIndexX_in][mazeIndexY_in-1] = check_walls(yaw_in)[0]
    maze_in[mazeIndexX_in-1][mazeIndexY_in] = check_walls(yaw_in)[1]
    maze_in[mazeIndexX_in][mazeIndexY_in+1] = check_walls(yaw_in)[2]
    maze_in[mazeIndexX_in+1][mazeIndexY_in] = check_walls(yaw_in)[3]
    print(maze_in)
    return maze_in

while not rospy.is_shutdown():
    print(positionY, positionX)

    distanceX, distanceY = waypoints[waypointIndex][0]-positionX,waypoints[waypointIndex][1]-positionY #haversine(latitude, longitude, waypoints[waypointIndex][0], waypoints[waypointIndex][1])

        # calculate heading error from yaw or bearing
    
    headingError = bearing - yaw
    if headingError > math.pi:
        headingError = headingError - (2 * math.pi) 
    if headingError < -math.pi:
        headingError = headingError + (2 * math.pi)

    #rospy.loginfo("Distance: %.3f m, heading error: %.3f rad." % (distanceX+distanceY, headingError))
    #rospy.loginfo("Bearing: %.3f rad, yaw: %.3f rad, error: %.3f rad" % (bearing, yaw, headingError))
    # print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    # print(distanceX, distanceY)
    # print(positionX, positionY)
    # print("-----------")
    # print(waypoints)
    # print("#####################")
    # print(yaw)
    print(check_walls(yaw))
    # Heading error, threshold is 0.1 rad
    if abs(headingError) > 0.01:
        # Only rotate in place if there is any heading error
        cmd_vel.linear.x = 0
        isRotating=True
        if headingError >0:
            cmd_vel.angular.z = -0.3
        else:
            cmd_vel.angular.z = 0.3
    else:
        # Only straight driving, no curves
        cmd_vel.angular.z = 0
        isRotating=False
        # Distance error, threshold is 0.2m
        if abs(distanceY)+abs(distanceX) > 0.01 :
            cmd_vel.linear.x = -0.2
            isMoving=True
        else:
            cmd_vel.linear.x = 0
            isMoving=False
            rospy.loginfo("Target waypoint reached!")
            waypointIndex += 1
    pub.publish(cmd_vel)

    if waypointIndex == len(waypoints) and not(isRotating)and not(isMoving):
        if yaw < 0.1 or yaw > 6.283:
            mazeIndexX+=2
            maze=maze_fill(mazeIndexX, mazeIndexY, maze, yaw)
        elif yaw > 1.4708 or yaw < 1.6708:
            mazeIndexY+=2
            maze=maze_fill(mazeIndexX, mazeIndexY, maze, yaw)
        elif yaw < 3.2415 or yaw > 3.0415:
            mazeIndexX-=2
            maze=maze_fill(mazeIndexX, mazeIndexY, maze, yaw)
        elif yaw > 4.6124 or yaw < 4.8124:
            mazeIndexY-=2
            maze=maze_fill(mazeIndexX, mazeIndexY, maze, yaw)
        if check_walls(0)[3]==2:
            if yaw < 0.01 or yaw > 6.2:
                bearing = 0
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]+0.31])
            elif yaw > 1.4708 or yaw < 1.6708:
                bearing = 1.5708
                waypoints.append([waypoints[waypointIndex-1][0]+0.31,waypoints[waypointIndex-1][1]])
            elif yaw < 3.2415 or yaw > 3.0415:
                bearing = 3.1415
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]-0.31])
            elif yaw > 4.6124 or yaw < 4.8124:
                bearing = 4.7124
                waypoints.append([waypoints[waypointIndex-1][0]-0.31,waypoints[waypointIndex-1][1]])
            
        elif check_walls(0)[2]==2:
            if yaw < 0.01 or yaw > 6.2:
                bearing = 0
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]+0.31])
            elif yaw > 1.4708 or yaw < 1.6708:
                bearing = 1.5708
                waypoints.append([waypoints[waypointIndex-1][0]+0.31,waypoints[waypointIndex-1][1]])
            elif yaw < 3.2415 or yaw > 3.0415:
                bearing = 3.1415
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]-0.31])
            elif yaw > 4.6124 or yaw < 4.8124:
                bearing = 4.7124
                waypoints.append([waypoints[waypointIndex-1][0]-0.31,waypoints[waypointIndex-1][1]])
            
        elif check_walls(0)[1]==2:
            if yaw < 0.01 or yaw > 6.2:
                bearing = 0
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]+0.31])
            elif yaw > 1.4708 or yaw < 1.6708:
                bearing = 1.5708
                waypoints.append([waypoints[waypointIndex-1][0]+0.31,waypoints[waypointIndex-1][1]])
            elif yaw < 3.2415 or yaw > 3.0415:
                bearing = 3.1415
                waypoints.append([waypoints[waypointIndex-1][0],waypoints[waypointIndex-1][1]-0.31])
            elif yaw > 4.6124 or yaw < 4.8124:
                bearing = 4.7124
                waypoints.append([waypoints[waypointIndex-1][0]-0.31,waypoints[waypointIndex-1][1]])
            
                
        rospy.loginfo("Last target waypoint reached!")
        waypointIndex -= 1
    else:
        rate.sleep()