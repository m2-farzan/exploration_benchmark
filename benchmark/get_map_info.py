import datetime
import subprocess

import cv2
import numpy as np
import rospy
from nav_msgs.msg import OccupancyGrid

from . import config
from .envs import envs

def get_map_info(rosbag_file, env_name):
    global img
    times = []
    coverages = []
    # create ros1 node
    rospy.init_node('get_map_info', anonymous=True)
    t0 = datetime.datetime.now().timestamp()
    # load ground truth
    ground_truth_img = cv2.imread(envs[env_name]['map_file'], 0)
    # count ground truth non-occupied cells
    zeros_gt = np.count_nonzero(ground_truth_img == 128)
    # calculate area
    area_gt = zeros_gt * config.pgm_resolution**2
    # create map subscriber
    def map_callback(msg):
        global img
        img = np.asarray(msg.data)
        img = img.reshape((msg.info.height, msg.info.width))
        resolution = msg.info.resolution
        # count detected non-occupied cells i.e. count zeros
        zeros = np.count_nonzero(img == 0)
        # calculate area
        area = zeros * resolution**2
        # calculate coverage
        coverage = area / area_gt  # Note: this assumes no false-positive free cells in the generated map. Use in conjuction with ground truth ORB similarity.
        # save data
        t = datetime.datetime.now().timestamp()
        times.append(config.playback_speed * (t - t0))
        coverages.append(coverage)
    
    map_sub = rospy.Subscriber('/map', OccupancyGrid, map_callback)
    # play rosbag
    subprocess.call(['rosbag', 'play', rosbag_file, '-r', str(config.playback_speed)])

    return times, coverages, img