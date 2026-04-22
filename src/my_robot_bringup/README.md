# Robot Movement Control System

## Overview
This package provides complete robot control setup with launch files and movement publishers for your differential drive robot.

## Components

### 1. Launch Files

#### `robot_control.launch.py` (Original)
Launches the basic robot control system:
- Robot State Publisher
- Controller Manager
- Joint State Broadcaster & Diff Drive Controller
- RViz2 visualization

**Usage:**
```bash
ros2 launch my_robot_bringup robot_control.launch.py
```

#### `complete_system.launch.py` (New - Enhanced)
Launches the complete system with optional features:
- All components from robot_control.launch.py
- Optional movement publisher
- Configurable RViz visualization

**Usage:**
```bash
# Basic launch (without automatic movement)
ros2 launch my_robot_bringup complete_system.launch.py

# Launch with automatic robot movement
ros2 launch my_robot_bringup complete_system.launch.py enable_movement:=true

# Launch without RViz (for headless mode)
ros2 launch my_robot_bringup complete_system.launch.py use_rviz:=false

# Both options together
ros2 launch my_robot_bringup complete_system.launch.py enable_movement:=true use_rviz:=false
```

### 2. Movement Publisher Script

**File:** `scripts/movement_publisher.py`

This is a standalone ROS2 node that publishes velocity commands to move the robot. It provides several movement methods:

- `move_forward(duration, speed)` - Move forward
- `move_backward(duration, speed)` - Move backward
- `rotate(duration, angular_speed)` - Rotate in place
- `move_circle(duration, linear_speed, angular_speed)` - Move in circular path
- `stop()` - Stop the robot

**Standalone Usage (after launching with robot_control.launch.py):**
```bash
# In a new terminal
source /path/to/install/setup.bash
ros2 run my_robot_bringup movement_publisher.py
```

**Full example with separate terminals:**

Terminal 1 - Start the robot control system:
```bash
cd ~/ros2_ws_urdf
source install/setup.bash
ros2 launch my_robot_bringup robot_control.launch.py
```

Terminal 2 - Start movement publisher:
```bash
cd ~/ros2_ws_urdf
source install/setup.bash
ros2 run my_robot_bringup movement_publisher.py
```

## Configuration

### Robot Parameters
Edit `/config/my_robot_controller.yaml`:
- `wheel_separation`: 0.54m (distance between wheel centers)
- `wheel_radius`: 0.1m
- `linear.x.max_velocity`: 1.0 m/s
- `angular.z.max_velocity`: 1.0 rad/s
- `cmd_vel_timeout`: 0.5s (safety timeout)

### Custom Movement Sequence
Edit `scripts/movement_publisher.py` in the `main()` function to customize the movement pattern.

## Topic Information

### Subscribed Topics
- `/diff_drive_controller/cmd_vel` (TwistStamped) - Velocity commands

### Published Topics
- `/joint_states` - Joint state information
- `/odom` - Odometry (robot position/velocity)
- `/tf` - Transform tree

### Frame Information
- `base_footprint` - Robot base reference
- `base_link` - Robot body
- `odom` - Odometry frame
- `map` - (optional global frame)

## Troubleshooting

### Controllers not spawning
- Ensure controller manager has fully started (wait 2-3 seconds)
- Check `/controller_manager` is responding: `ros2 service list | grep controller_manager`

### Robot not moving
- Verify teleop or publisher is connected: `ros2 topic list | grep cmd_vel`
- Check odometry topic: `ros2 topic echo /odom`
- Verify wheel parameters in YAML match URDF

### RViz showing incorrect robot
- Ensure `robot_description` parameter is set correctly
- Check TF tree: `ros2 run tf2_tools view_frames.py`

## Building

```bash
cd ~/ros2_ws_urdf
colcon build --packages-select my_robot_bringup my_robot_description
source install/setup.bash
```

## Testing

### Option 1: Automatic Movement (Recommended for testing)
```bash
ros2 launch my_robot_bringup complete_system.launch.py enable_movement:=true
```
Watch the robot move automatically in RViz!

### Option 2: Manual Control with Keyboard
```bash
# Terminal 1
ros2 launch my_robot_bringup robot_control.launch.py

# Terminal 2
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args \
  -r /cmd_vel:=/diff_drive_controller/cmd_vel -p stamped:=true
```
Then use arrow keys to control the robot.

## Notes
- Robot simulation uses mock_components/GenericSystem
- No actual hardware is being controlled (mock only)
- All movements are visualized in RViz
- Odometry is calculated from wheel velocities
