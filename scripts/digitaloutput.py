#!/usr/bin/env python3
""" module docstring, yo! """

import sys
import json
import requests
import rospy
from ros_robotino_rest_pkg.msg import DigitalReadings

# api-endpoint
URL = "http://127.0.0.1/data/digitaloutputarray"
PARAMS = {'sid': 'ros_robotino_rest_pkg'}


def callback(data):
    """ function docstring, yo! """
    try:
        result = requests.post(url=URL, params=PARAMS, data=json.dumps(data.values))
        if result.status_code != 200:
            rospy.logwarn("post to %s with params %s failed", URL, PARAMS)
    except requests.exceptions.RequestException as exception_e:
        rospy.logerr("%s", exception_e)


def listener():
    """ function docstring, yo! """
    rospy.init_node('robotino_digitaloutput', anonymous=True)
    rospy.Subscriber("digitaloutput", DigitalReadings, callback)
    rospy.spin()


if __name__ == '__main__':
    MYARGV = rospy.myargv(argv=sys.argv)
    if len(MYARGV) > 1:
        URL = URL.replace("127.0.0.1", MYARGV[1])
    rospy.loginfo("connecting to: %s", URL)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
