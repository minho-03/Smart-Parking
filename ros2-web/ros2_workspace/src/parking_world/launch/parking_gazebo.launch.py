import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    
    pkg_parking_world = get_package_share_directory('parking_world')
    world_file = os.path.join(pkg_parking_world, 'worlds', 'parking_lot.world')

    urdf_file = os.path.join(
        get_package_share_directory('turtlebot3_description'),
        'urdf',
        'turtlebot3_burger.urdf'
    )
    with open(urdf_file, 'r') as f:
        robot_description = f.read().replace('${namespace}', '')

    # 🔥 이그니션 가제보(Ignition) 전용 모터 및 라이다 센서 플러그인 주입!
    ignition_plugins = """
    <gazebo>
      <plugin filename="libignition-gazebo-diff-drive-system.so" name="ignition::gazebo::systems::DiffDrive">
        <left_joint>wheel_left_joint</left_joint>
        <right_joint>wheel_right_joint</right_joint>
        <wheel_separation>0.160</wheel_separation>
        <wheel_radius>0.033</wheel_radius>
        <odom_publish_frequency>30</odom_publish_frequency>
        <topic>cmd_vel</topic>
        <odom_topic>odom</odom_topic>
        <tf_topic>tf</tf_topic>
        <frame_id>odom</frame_id>
        <child_frame_id>base_footprint</child_frame_id>
      </plugin>
      <plugin filename="libignition-gazebo-joint-state-publisher-system.so" name="ignition::gazebo::systems::JointStatePublisher">
        <topic>joint_states</topic>
      </plugin>
    </gazebo>
    
    <gazebo reference="base_scan">
      <sensor name="gpu_lidar" type="gpu_lidar">
        <always_on>true</always_on>
        <visualize>true</visualize>
        <update_rate>20</update_rate>
        <topic>scan</topic>
        <ignition_frame_id>base_scan</ignition_frame_id>
        <ray>
          <scan>
            <horizontal>
              <samples>360</samples>
              <resolution>1.0</resolution>
              <min_angle>0.0</min_angle>
              <max_angle>6.28</max_angle>
            </horizontal>
          </scan>
          <range>
            <min>0.12</min>
            <max>3.5</max>
            <resolution>0.015</resolution>
          </range>
          <noise>
            <type>gaussian</type>
            <mean>0.0</mean>
            <stddev>0.01</stddev>
          </noise>
        </ray>
      </sensor>
    </gazebo>
    """
    
    # 기본 URDF 파일의 맨 끝 </robot> 태그 바로 앞에 위 플러그인 코드를 끼워 넣습니다.
    robot_description_ign = robot_description.replace('</robot>', ignition_plugins + '\n</robot>')

    # 1. 가제보 실행
    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', world_file, '-r', '-v', '4'],
        additional_env={
            'IGN_GAZEBO_RESOURCE_PATH': os.path.join(
                get_package_share_directory('turtlebot3_description'), '..'
            )
        },
        output='screen'
    )

    # 2. 로봇 상태(TF) 퍼블리시
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_ign, 'use_sim_time': True}]
    )

    # 3. 로봇 스폰 (이제 토픽 대신 문자열 자체를 전달하여 완벽하게 생성시킵니다)
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'turtlebot3_burger',
            '-string', robot_description_ign, 
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.05',
        ],
        output='screen'
    )

    # 4. 통신 브리지
    ign_bridge = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist',
            '/scan@sensor_msgs/msg/LaserScan@ignition.msgs.LaserScan',
            '/odom@nav_msgs/msg/Odometry@ignition.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage@ignition.msgs.Pose_V',
            '/clock@rosgraph_msgs/msg/Clock@ignition.msgs.Clock'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        ign_bridge,
    ])