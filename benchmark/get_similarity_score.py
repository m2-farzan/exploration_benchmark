import cv2
import numpy as np

from .envs import envs

def get_similarity_score(img, env_name):
    # Convert to mapfile to ros map
    map_img = cv2.imread(envs[env_name]['map_file'], 0)
    map_img[map_img == 255] = -1
    map_img[map_img == 128] = 0
    map_img[map_img == 0] = 100
    # Measure orb similarity
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img.astype(np.uint8), None)
    kp2, des2 = orb.detectAndCompute(map_img.astype(np.uint8), None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    # Sort matches by score
    matches.sort(key=lambda x: x.distance)
    # Calculate similarity score
    score = 0
    for match in matches:
        score += 1.0 / match.distance
    return score
