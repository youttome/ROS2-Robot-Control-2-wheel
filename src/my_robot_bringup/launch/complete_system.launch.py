#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # -------------------------------------------------
    # Packages
    # -------------------------------------------------
    description_pkg = FindPackageShare("my_robot_description")
    bringup_pkg = FindPackageShare("my_robot_bringup")

    # -------------------------------------------------
    # Launch Arguments
    # -------------------------------------------------
    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Launch RViz2"
    )

    enable_movement_arg = DeclareLaunchArgument(
        "enable_movement",
        default_value="false",
        description="Run movement publisher node"
    )

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation clock"
    )

    use_rviz = LaunchConfiguration("use_rviz")
    enable_movement = LaunchConfiguration("enable_movement")
    use_sim_time = LaunchConfiguration("use_sim_time")

    # -------------------------------------------------
    # File Paths
    # -------------------------------------------------
    urdf_file = PathJoinSubstitution(
        [description_pkg, "urdf", "my_robot.urdf.xacro"]
    )

    robot_description = Command(
        ["xacro ", urdf_file]
    )

    rviz_config = PathJoinSubstitution(
        [description_pkg, "rviz", "urdf_config.rviz"]
    )

    controller_yaml = PathJoinSubstitution(
        [bringup_pkg, "config", "my_robot_controller.yaml"]
    )

    # -------------------------------------------------
    # Nodes
    # -------------------------------------------------

    # Publish TF from URDF
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": use_sim_time,
            }
        ],
    )

    # ros2_control
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        output="screen",
        parameters=[
            {"robot_description": robot_description},
            controller_yaml,
            {"use_sim_time": use_sim_time},
        ],
    )

    # Joint State Broadcaster
    joint_state_broadcaster = TimerAction(
        period=2.0,
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                output="screen",
                arguments=[
                    "joint_state_broadcaster",
                    "--controller-manager",
                    "/controller_manager",
                ],
            )
        ],
    )

    # Diff Drive Controller
    diff_drive_controller = TimerAction(
        period=4.0,
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                output="screen",
                arguments=[
                    "diff_drive_controller",
                    "--controller-manager",
                    "/controller_manager",
                ],
            )
        ],
    )

    # RViz2
    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        parameters=[{"use_sim_time": use_sim_time}],
        condition=IfCondition(use_rviz),
    )

    # Optional movement node
    movement_node = TimerAction(
        period=6.0,
        actions=[
            Node(
                package="my_robot_bringup",
                executable="movement_publisher.py",
                output="screen",
                condition=IfCondition(enable_movement),
            )
        ],
    )

    # -------------------------------------------------
    # Launch Description
    # -------------------------------------------------
    return LaunchDescription([
        use_rviz_arg,
        enable_movement_arg,
        use_sim_time_arg,

        robot_state_publisher,
        controller_manager,
        joint_state_broadcaster,
        diff_drive_controller,
        rviz2,
        movement_node,
    ])