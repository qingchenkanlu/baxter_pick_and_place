# -*- coding: utf-8 -*-

"""Module for hardware interfaces.

Implements interfaces to the Baxter research robot (using the Baxter SDK
found at https://github.com/BRML/baxter_interface) and the Kinect V2 in ROS
(using the ROS bridge found at https://github.com/code-iai/iai_kinect2).
"""

from base import (
    img_to_imgmsg,
    imgmsg_to_img,
    remove_default_loghandler as cam_remove_default_loghandler
)

from baxter import (
    Baxter,
    remove_default_loghandler as baxter_remove_default_loghandler
)

from kinect import (
    Kinect,
    remove_default_loghandler as kinect_remove_default_loghandler
)
