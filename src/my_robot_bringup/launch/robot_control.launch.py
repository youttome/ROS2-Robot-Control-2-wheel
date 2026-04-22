#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, PathJoinSubstitution, LaunchConfiguration


def generate_launch_description():
    # Package shares
    my_robot_description_share = FindPackageShare("my_robot_description")
    my_robot_bringup_share = FindPackageShare("my_robot_bringup")

    # File paths using substitutions
    urdf_model_path = Command(
        [
            "xacro ",
            PathJoinSubstitution(
                [my_robot_description_share, "urdf", "my_robot.urdf.xacro"]
            ),
        ]
    )
    
    rviz_config_path = PathJoinSubstitution(
        [my_robot_description_share, "rviz", "urdf_config.rviz"]
    )
    
    controller_config_path = PathJoinSubstitution(
        [my_robot_bringup_share, "config", "my_robot_controller.yaml"]
    )

    return LaunchDescription(
        [
            # Robot State Publisher to publish TF from robot_description URDF
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                output="screen",
                parameters=[
                    {
                        "robot_description": urdf_model_path,
                        "use_sim_time": False,
                    }
                ],
            ),
            
            # ROS2 Control Node - Controller Manager
            Node(
                package="controller_manager",
                executable="ros2_control_node",
                output="screen",
                parameters=[controller_config_path],
            ),
            
            # Spawn controllers after controller manager has started
            TimerAction(
                period=2.0,
                actions=[
                    Node(
                        package="controller_manager",
                        executable="spawner",
                        output="screen",
                        arguments=[
                            "joint_state_broadcaster",
                            "diff_drive_controller",
                            "--controller-manager",
                            "/controller_manager",
                        ],
                    ),
                ],
            ),
            
            # RViz2 Visualization
            Node(
                package="rviz2",
                executable="rviz2",
                output="screen",
                arguments=["-d", rviz_config_path],
            ),
        ]
    )
