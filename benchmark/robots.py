robots = {
    'waffle': lambda x, y, z, Y: [
        f'xacro /opt/ros/noetic/share/turtlebot3_description/urdf/turtlebot3_waffle.urdf.xacro | rosrun gazebo_ros spawn_model -urdf -stdin -model waffle -x {x} -y {y} -z {z} -Y {Y}',
        'TURTLEBOT3_MODEL=waffle roslaunch turtlebot3_slam turtlebot3_slam.launch',
        'TURTLEBOT3_MODEL=waffle roslaunch turtlebot3_navigation move_base.launch',
    ],
    # 'Robot-2': lambda x, y, z, Y: [
        
    # ],
}
