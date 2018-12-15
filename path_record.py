#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped

global last_x
last_x = 0
global last_y
last_y = 0
global init
init = 0

def callback(data):
    pose = PoseStamped()

    pose.header.frame_id = data.header.frame_id
    pose.header.stamp = data.header.stamp
    pose.pose.position.x = float(data.pose.pose.position.x)
    pose.pose.position.y = float(data.pose.pose.position.y)
    pose.pose.orientation.x = float(data.pose.pose.orientation.x)
    pose.pose.orientation.y = float(data.pose.pose.orientation.y)
    pose.pose.orientation.z = float(data.pose.pose.orientation.z)
    pose.pose.orientation.w = float(data.pose.pose.orientation.w)

    if init == 0:
        global last_x
        last_x = pose.pose.position.x
        global last_y
        last_y = pose.pose.position.y
        global init
        init = 1
        path.header.frame_id = pose.header.frame_id
        path.header.stamp=rospy.Time.now()
        path.poses.append(pose)

    else:
        if (last_x != pose.pose.position.x) or (last_y != pose.pose.position.y):
            path.header.frame_id = pose.header.frame_id
            path.header.stamp=rospy.Time.now()
            path.poses.append(pose)

    pub.publish(path)
    return

if __name__ == '__main__':
    rospy.init_node('path_record')
    path = Path()
    rospy.Subscriber("odom_groundtruth", Odometry, callback)
    pub = rospy.Publisher("odom_path", Path, queue_size=1)
    rospy.spin()
