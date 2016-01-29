#!/usr/bin/env python

# Copyright (c) 2015--2016, BRML
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import argparse
import cv2
import os
import rospkg
import rospy
import sys
import tty
import termios

from sensor_msgs.msg import Image

from baxter_pick_and_place.image import write_imgmsg, _imgmsg2img
from baxter_pick_and_place.rand import rand_x_digit_num
from baxter_pick_and_place.robot import Robot


class Images(object):
    def __init__(self, limb, outpath):
        """ Image recorder.
        :param limb: the limb to record images with
        :param outpath: the path to write the images to
        """
        self._arm = limb
        self._outpath = outpath

        self.robot = Robot(self._arm, self._outpath)
        self._imgmsg = None
        self._cam_sub = None

    def record(self):
        """ Records an image each time key 'r' is pressed. Stops upon pressing
        key 's'.
        """
        s = '/cameras/' + self._arm + '_hand_camera/image'
        self._cam_sub = rospy.Subscriber(s, Image, callback=self._camera_callback)
        print "\nRecording images ..."
        while not rospy.is_shutdown():
            # pose = self.robot._perturbe_pose(self.robot._top_pose)
            # self.robot._move_to_pose(pose)
            self.robot._move_to_pose(self.robot._top_pose)
            print " Press 'r' to record image, 's' to stop."
            ch = self.getch()
            if ch == 'r':
                fname = os.path.join(self._outpath, rand_x_digit_num(12))
                write_imgmsg(self._imgmsg, fname)
                print " Recorded image '%s.jpg'." % fname
            elif ch == 's':
                self._cam_sub.unregister()
                break

    @staticmethod
    def getch():
        """ getch()-like unbuffered character reading from stdin.
        See http://code.activestate.com/recipes/134892/.
        :return: a single character
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def _camera_callback(self, data):
        """
        Callback routine for the camera subscriber.
        """
        self._imgmsg = data
        img = _imgmsg2img(self._imgmsg)
        h, w, = img.shape[:2]
        img = cv2.resize(img, (w/2, h/2))
        cv2.imshow('%s image' % self._arm, img)
        cv2.waitKey(3)


def main():
    """Image recorder software

    Records an image each time the key 'r' (for 'record') is pressed.
    Upon pressing the key 's' (for 'stop'), the program exits.
    """
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__)
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        '-l', '--limb', required=True, choices=['left', 'right'],
        help='limb to record images with'
    )
    args = parser.parse_args(rospy.myargv()[1:])

    rospack = rospkg.RosPack()
    ns = rospack.get_path('baxter_pick_and_place')
    ns = os.path.join(ns, 'data', 'sdd')
    if not os.path.exists(ns):
        os.makedirs(ns)

    print("Initializing node... ")
    rospy.init_node("image_recording_%s" % (args.limb,))

    images = Images(args.limb, outpath=ns)
    rospy.on_shutdown(images.robot.clean_shutdown)
    images.record()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()