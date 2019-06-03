#!/usr/bin/env python
""" module docstring, yo! """

import sys
import requests
import rospy
from nav_msgs.msg import Odometry

# api-endpoint
URL = "http://127.0.0.1/data/odometry"
PARAMS = {'sid': 'robotino_rest_node'}


def talker():
    """ docsctring, yo! """
    odometry_pub = rospy.Publisher('odometry_readings', Odometry, queue_size=1)
    rospy.init_node('robotino_odometry', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        try:
            result = requests.get(url=URL, params=PARAMS)
            if result.status_code == 200:
                data = result.json()
                rospy.loginfo(data)
                msg = Odometry()
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
                # sequence number data[6]

                odometry_pub.publish(msg)
            else:
                rospy.logwarn("get from %s with params %s failed", URL, PARAMS)
        except requests.exceptions.RequestException as exception_e:
            rospy.logerr("%s", exception_e)
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
