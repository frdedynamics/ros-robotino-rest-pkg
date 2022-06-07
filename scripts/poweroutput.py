#!/usr/bin/env python3
""" This script does not work at the moment. It is just for controlling the gripper. Current problem is power_response = {"current" : 20} returns response 400. """

import sys
import json
import requests
import rospy
from ros_robotino_rest_pkg.msg import DigitalReadings
from std_msgs.msg import Int16

# api-endpoint
URL = "http://127.0.0.1/data/poweroutputcurrent"
PARAMS = {'sid': 'ros_robotino_rest_pkg'}


def callback(msg):
    """ function docstring, yo! """
    power_response = {"current" : 20}
    
    try:
        result = requests.post(url=URL, params=PARAMS, data=json.dumps(power_response))
        rospy.loginfo(result)
        if result.status_code != 200:
            rospy.logwarn("post to %s with params %s failed", URL, PARAMS)
    except requests.exceptions.RequestException as exception_e:
        rospy.logerr("%s", exception_e)


def listener():
    """ function docstring, yo! """
    rospy.init_node('robotino_poweroutput', anonymous=True)
    rospy.Subscriber("poweroutput", Int16, callback)
    rospy.spin()


if __name__ == '__main__':
    MYARGV = rospy.myargv(argv=sys.argv)
    if len(MYARGV) > 1:
        URL = URL.replace("127.0.0.1", MYARGV[1])
    rospy.loginfo("connecting to: %s", URL)
    try:
        listener()
        rospy.loginfo("here")
    except rospy.ROSInterruptException:
        pass
