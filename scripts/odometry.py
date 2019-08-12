#!/usr/bin/env python
""" module docstring, yo! """

import sys
import requests
import rospy
import tf2_ros
import tf_conversions
import geometry_msgs.msg
from nav_msgs.msg import Odometry

# api-endpoint
URL = "http://127.0.0.1/data/odometry"
PARAMS = {'sid': 'ros_robotino_rest_pkg'}


def talker():
    """ docsctring, yo! """
    odometry_pub = rospy.Publisher('odometry_readings', Odometry, queue_size=1)
    rospy.init_node('robotino_odometry', anonymous=True)
    rate = rospy.Rate(10)  # 10hz

    br = tf2_ros.TransformBroadcaster()
    t = geometry_msgs.msg.TransformStamped()

    msg = Odometry()
    msg.header.frame_id = 'odom'
    msg.child_frame_id = 'base_link'

    while not rospy.is_shutdown():
        try:
            result = requests.get(url=URL, params=PARAMS)
            if result.status_code == 200:
                data = result.json()

                msg.header.stamp = rospy.get_rostime()

                msg.pose.pose.position.x = data[0]  # [m]
                msg.pose.pose.position.y = data[1]  # [m]
                msg.pose.pose.position.z = 0.0

                msg.pose.pose.orientation.w = data[2]  # [rad]
                msg.pose.pose.orientation.x = 0.0
                msg.pose.pose.orientation.y = 0.0
                msg.pose.pose.orientation.z = 0.0

                msg.twist.twist.linear.x = data[3]  # [m/s]
                msg.twist.twist.linear.y = data[4]  # [m/s]
                msg.twist.twist.linear.z = 0.0

                msg.twist.twist.angular.x = 0.0
                msg.twist.twist.angular.y = 0.0
                msg.twist.twist.angular.z = data[5]  # [rad/s]

                odometry_pub.publish(msg)
            else:
                rospy.logwarn("get from %s with params %s failed", URL, PARAMS)
        except requests.exceptions.RequestException as exception_e:
            rospy.logerr("%s", exception_e)

        t.header.stamp = msg.header.stamp

        t.header.frame_id = "world"
        t.child_frame_id = msg.header.frame_id

        t.transform.translation = msg.pose.pose.position

        q = tf_conversions.transformations.quaternion_from_euler(0, 0, msg.pose.pose.orientation.w)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        br.sendTransform(t)

        rate.sleep()


if __name__ == '__main__':
    MYARGV = rospy.myargv(argv=sys.argv)
    if len(MYARGV) > 1:
        URL = URL.replace("127.0.0.1", MYARGV[1])
    print("connecting to: ", URL)
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
