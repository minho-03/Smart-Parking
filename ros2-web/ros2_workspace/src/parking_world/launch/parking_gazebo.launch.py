import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    
    # Paths
    pkg_parking_world = get_package_share_directory('parking_world')
    world_file = os.path.join(pkg_parking_world, 'worlds', 'parking_lot.world')
    
    # Gazebo launch
    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', world_file, '-r', '-v', '4'],
        output='screen'
    )
    
    # Bridge for cmd_vel topic
    bridge_cmd_vel = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        arguments=['/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist'],
        output='screen'
    )
    
    # Bridge for scan topic
    bridge_scan = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        arguments=['/scan@sensor_msgs/msg/LaserScan@ignition.msgs.LaserScan'],
        output='screen'
    )
    
    # Bridge for odom topic
    bridge_odom = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        arguments=['/odom@nav_msgs/msg/Odometry@ignition.msgs.Odometry'],
        output='screen'
    )
    
    return LaunchDescription([
        gazebo,
        bridge_cmd_vel,
        bridge_scan,
        bridge_odom,
    ])