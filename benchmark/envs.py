from .generate_initial_poses import generate_initial_poses

envs = {
    'simple': {
        # 'gazebo -s libgazebo_ros_api_plugin.so /usr/share/gazebo-11/worlds/willowgarage.world',
        # 'roslaunch gazebo_ros willowgarage_world.launch',  # try this if hits the walls
        'cmds': [
            'roslaunch gazebo_ros empty_world.launch world_name:=$(pwd)/assets/worlds/01-simple/world.xml'
        ],
        'initial_poses': generate_initial_poses('assets/worlds/01-simple/map.png'),
    },
    'wide-open': {
        'cmds': [
            'roslaunch gazebo_ros empty_world.launch world_name:=$(pwd)/assets/worlds/05-office/world.xml'
        ],
        'initial_poses': generate_initial_poses('assets/worlds/05-office/map.png'),
    }
}
