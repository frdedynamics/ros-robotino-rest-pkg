#!/usr/bin/env python3
""" module docstring, yo!"""

import sys
import requests
import rospy
from ros_robotino_rest_pkg.msg import PowerReadings


# api-endpoint
URL = "http://127.0.0.1/data/digitalinputarray"
PARAMS = {'sid': 'ros_robotino_rest_pkg'}


def talker():
    """ docstring, yo! """
    poweroutputcurrent_readings_pub = rospy.Publisher('poweroutputcurrent_readings', PowerReadings, queue_size=1)
    rospy.init_node('robotino_powercurrent', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        # try:
        result = requests.get(url=URL, params=PARAMS)
        result.raise_for_status()
        if result.status_code == 200:
            # data = result.json()
            # rospy.loginfo(result)
            try:
                return result.json()
            except ValueError as e:
                rospy.loginfo(e)
                # decide how to handle a server that's misbehaving to this extent
            
            # msg = PowerReadings()
            # msg.stamp = rospy.get_rostime()
            # # msg.current = data["current"]
            # print(data)
            # rospy.loginfo(str(data))
            # poweroutputcurrent_readings_pub.publish(msg)
        else:
            rospy.logwarn("get from %s with params %s failed", URL, PARAMS)
        # except requests.exceptions.RequestException as exception_e:
        #     rospy.logerr("%s", exception_e)
        rate.sleep()


if __name__ == '__main__':
    MYARGV = rospy.myargv(argv=sys.argv)
    if len(MYARGV) > 1:
        URL = URL.replace("127.0.0.1", MYARGV[1])
    print("connecting to: ", URL)
    try:
        talker()
        print("here")
    except rospy.ROSInterruptException:
        pass
