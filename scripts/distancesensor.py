#!/usr/bin/env python3
""" module docstring, yo!"""

import sys
import requests
import rospy
from ros_robotino_rest_pkg.msg import AnalogReadings


# api-endpoint
URL = "http://127.0.0.1/data/distancesensorarray"
PARAMS = {'sid': 'ros_robotino_rest_pkg'}


def talker():
    """ docstring, yo! """
    distancesensor_readings_pub = rospy.Publisher('distancesensor_readings', AnalogReadings, queue_size=1)
    rospy.init_node('robotino_distancesensor', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        try:
            result = requests.get(url=URL, params=PARAMS)
            if result.status_code == 200:
                data = result.json()
                
                msg = AnalogReadings()
                msg.stamp = rospy.get_rostime()
                msg.values = data
                distancesensor_readings_pub.publish(msg)
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
