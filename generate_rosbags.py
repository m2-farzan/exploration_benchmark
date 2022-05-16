#!/usr/bin/env python3

import itertools
import logging
import subprocess
import time

from benchmark import (
    config,
    envs,
    exp_packages,
    robots,
)


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    subprocess.run('killall -s9 gzserver gzclient rviz; rosnode kill -a', shell=True)
    for (env_name, env_props), (exp_package_name, exp_package_cmds), (robot_name, robot_cmds_functor) in itertools.product(envs.items(), exp_packages.items(), robots.items()):
        for initial_pose in env_props['initial_poses']:
            logging.info(f'Item: ({env_name}:{exp_package_name}:{robot_name}:{initial_pose})')
            procs = []
            rosbag_proc = subprocess.Popen(f'rosbag record --bz2 /map /tf /tf_static -O {env_name}:{exp_package_name}:{robot_name}:{initial_pose[0]:.2f}:{initial_pose[1]:.2f}.bag', shell=True)
            procs.append(rosbag_proc)
            for cmd in env_props['cmds']:
                proc = subprocess.Popen(cmd, shell=True)
                procs.append(proc)
            time.sleep(3)  # wait for gazebo to stabilize
            for cmd in robot_cmds_functor(*initial_pose):
                proc = subprocess.Popen(cmd, shell=True)
                procs.append(proc)
                time.sleep(3)
            time.sleep(10)
            for cmd in exp_package_cmds:
                proc = subprocess.Popen(cmd, shell=True)
                procs.append(proc)
            time.sleep(config.timeout)  # wait for the experiment to finish
            for proc in procs:
                proc.kill()
                while proc.poll() is None:
                    time.sleep(1)
            subprocess.run('killall -s9 gzserver gzclient rviz; rosnode kill -a', shell=True)
            time.sleep(5)



if __name__ == '__main__':
    main()