#!/usr/bin/env python3

import math
import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler

def get_rotation (msg):
    global roll, pitch, yaw
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

rospy.init_node('gps_waypoint_follower')

sub_odom = rospy.Subscriber ('/odom', Odometry, get_rotation)
sub_gps = rospy.Subscriber ('/navsat/fix', NavSatFix, get_gps_coordinates)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(10)

rospy.loginfo("GPS waypoint follower node has started!")

cellLength=0.18 #in meters

# Example waypoints [latitude, longitude]
waypoints = [[47.47908802923231, 19.05774719012997],
             [47.47905809688768, 19.05774697410133],
             [47.47907097650916, 19.05779319890401],
             [47.47907258024465, 19.05782379884820]]

cmd_vel = Twist()
cmd_vel.linear.x = 0
cmd_vel.angular.z = 0

waypointIndex = 0


maze=[[0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0]]

#cellTypes
#    0= none    1 =|     2= ‾  3=  |
#    4= _       5 =|‾    6=| | 7=|_  
#    8= ‾|       9= ‾_   10= _| 11=|‾| 
#    12=|‾_       13=|_|   14=‾_| 15=|_‾|
#
#
#


while not rospy.is_shutdown():
    distance, bearing = haversine(latitude, longitude, waypoints[waypointIndex][0], waypoints[waypointIndex][1])

        # calculate heading error from yaw and bearing
    headingError = bearing - yaw
    if headingError > math.pi:
        headingError = headingError - (2 * math.pi) 
    if headingError < -math.pi:
        headingError = headingError + (2 * math.pi)

    rospy.loginfo("Distance: %.3f m, heading error: %.3f rad." % (distance, headingError))
    #rospy.loginfo("Bearing: %.3f rad, yaw: %.3f rad, error: %.3f rad" % (bearing, yaw, headingError))

    # Heading error, threshold is 0.1 rad
    if abs(headingError) > 0.1:
        # Only rotate in place if there is any heading error
        cmd_vel.linear.x = 0

        if headingError < 0:
            cmd_vel.angular.z = -0.3
        else:
            cmd_vel.angular.z = 0.3
    else:
        # Only straight driving, no curves
        cmd_vel.angular.z = 0
        # Distance error, threshold is 0.2m
        if distance > 0.2:
            cmd_vel.linear.x = 0.5
        else:
            cmd_vel.linear.x = 0
            rospy.loginfo("Target waypoint reached!")
            waypointIndex += 1

    pub.publish(cmd_vel)

    if waypointIndex == len(waypoints):
        rospy.loginfo("Last target waypoint reached!")
        break
    else:
        rate.sleep()