import random

import cv2

from . import config

def generate_initial_poses(
    map_file,
    res=config.pgm_resolution,
    origin_x=config.pgm_origin_x,
    origin_y=config.pgm_origin_y,
    origin_z=config.pgm_origin_z,
    num_poses=config.num_poses
):
    # Keep it simple, stupid
    img = cv2.imread(map_file, 0)
    poses = []
    while len(poses) < num_poses:
        x = random.randint(0, img.shape[0]-1)
        y = random.randint(0, img.shape[1]-1)
        Y = random.random() * 2 * 3.14159
        r = 0.3  # safe distance from the wall
        if \
            img[x, y] != 128 or \
            img[min(img.shape[0]-1, x+int(r/res)), y] != 128 or \
            img[x, min(img.shape[1]-1, y+int(r/res))] != 128 or \
            img[max(0, x-int(r/res)), y] != 128 or \
            img[x, max(0, y-int(r/res))] != 128 or \
            img[min(img.shape[0]-1, x+int(r/res)), min(img.shape[1]-1, y+int(r/res))] != 128 or \
            img[min(img.shape[0]-1, x+int(r/res)), max(0, y-int(r/res))] != 128 or \
            img[max(0, x-int(r/res)), min(img.shape[1]-1, y+int(r/res))] != 128 or \
            img[max(0, x-int(r/res)), max(0, y-int(r/res))] != 128 \
        :
            continue  # thanks, copilot!
        poses.append((x * res + origin_x, y * res + origin_y, origin_z, Y))
    return poses
