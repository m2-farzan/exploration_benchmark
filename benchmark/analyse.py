import subprocess
import re

import numpy as np

from .get_map_info import get_map_info
from .get_similarity_score import get_similarity_score

def analyse(rosbag_file):
        print(f'Analyzing {rosbag_file}')
        rosbag_file_noext = re.findall(r'(.*)\.bag', rosbag_file)[0]
        env_name, exp_pkg_name, robot_name, x0, y0, Y0 = rosbag_file_noext.split(':')
        duration = get_duration(rosbag_file)
        cov_times, covs, final_map = get_map_info(rosbag_file, env_name)
        cov_90 = np.interp(0.9, covs, cov_times, left=np.NaN, right=np.NaN)
        similarity_score = get_similarity_score(final_map, env_name)
        row = {
            'bag_file': rosbag_file,
            'env': env_name,
            'pkg': exp_pkg_name,
            'robot': robot_name,
            'x0': x0,
            'y0': y0,
            'Y0': Y0,
            'duration_seconds': duration,
            'final_coverage': covs[-1],
            'cov_90': cov_90,
            'similarity_score': similarity_score,
        }
        return row

def get_duration(rosbag_file):
    rosbag_info = subprocess.check_output(['rosbag', 'info', rosbag_file]).decode('utf-8')
    for line in rosbag_info.split('\n'):
        if 'duration' in line:
            duration_line = line
            break
    if '(' in duration_line:
        return float(re.findall(r'\(([\d\.]+)s\)', duration_line)[0])
    else:
        return float(re.findall(r'([\d\.]+)s', duration_line)[0])
