import cv2
import random

def generate_initial_poses(map_file, res=0.01, origin_x=-15, origin_y=-15, origin_z=0.0, num_poses=10):
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
            img[max(0, x-int(r/res)), max(0, y-int(r/res))] != 128:  # thanks, copilot!
            continue
        poses.append((x * res + origin_x, y * res + origin_y, origin_z, Y))  # swap x, y
    return poses
