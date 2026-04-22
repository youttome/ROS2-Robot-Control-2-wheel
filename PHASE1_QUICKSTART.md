# ROS2 Robot Project - Quick Start Guide

## Getting Started with Phase 1: Custom Messages

This guide will help you implement the first phase of the project - creating custom ROS2 message definitions.

---

## Step 1: Create the robot_interfaces Package

### 1.1 Create the package directory

```bash
cd ~/ros2_ws_urdf/src
ros2 pkg create --build-type ament_cmake robot_interfaces
cd robot_interfaces
```

### 1.2 Update package.xml

Edit `src/robot_interfaces/package.xml` and add dependencies:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>robot_interfaces</name>
  <version>0.0.0</version>
  <description>Custom message and service definitions for robot</description>
  <maintainer email="youtemail@example.com">your_name</maintainer>
  <license>Apache License 2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>rosidl_default_generators</buildtool_depend>

  <build_depend>geometry_msgs</build_depend>
  <build_depend>sensor_msgs</build_depend>
  <build_depend>std_msgs</build_depend>

  <exec_depend>rosidl_default_runtime</exec_depend>
  <exec_depend>geometry_msgs</exec_depend>
  <exec_depend>sensor_msgs</exec_depend>
  <exec_depend>std_msgs</exec_depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <member_of_group>rosidl_interface_packages</member_of_group>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

### 1.3 Update CMakeLists.txt

Edit `src/robot_interfaces/CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.8)
project(robot_interfaces)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)

set(msg_files
  "msg/Detection.msg"
  "msg/DetectionArray.msg"
  "msg/ObstacleStatus.msg"
  "msg/RobotSignal.msg"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  DEPENDENCIES geometry_msgs sensor_msgs std_msgs
)

ament_package()
```

---

## Step 2: Create Message Definitions

### 2.1 Create msg directory

```bash
mkdir -p src/robot_interfaces/msg
```

### 2.2 Create Detection.msg

Create file: `src/robot_interfaces/msg/Detection.msg`

```
# Single detected object
string object_type          # "car", "box", "pedestrian", etc.
float32 confidence          # Detection confidence (0.0 to 1.0)
int32 x_min                 # Bounding box top-left x
int32 y_min                 # Bounding box top-left y
int32 x_max                 # Bounding box bottom-right x
int32 y_max                 # Bounding box bottom-right y
float32 center_x            # Center point x
float32 center_y            # Center point y
float32 width               # Object width in pixels
float32 height              # Object height in pixels
float32 distance            # Estimated distance (meters)
string description          # Additional info
```

### 2.3 Create DetectionArray.msg

Create file: `src/robot_interfaces/msg/DetectionArray.msg`

```
# Array of detected objects
std_msgs/Header header
robot_interfaces/Detection[] detections    # Array of detections
int32 image_width
int32 image_height
float32 processing_time     # Time taken for detection (seconds)
string status               # "success", "failed", "processing"
```

### 2.4 Create ObstacleStatus.msg

Create file: `src/robot_interfaces/msg/ObstacleStatus.msg`

```
# Current obstacle detection status
std_msgs/Header header
bool detected               # Is any obstacle detected
string primary_obstacle    # Type of main obstacle
float32 front_distance     # Distance to obstacle in front (meters)
float32 left_distance      # Distance to left obstacle
float32 right_distance     # Distance to right obstacle
float32 center_x           # Obstacle center x position
float32 center_y           # Obstacle center y position
float32 confidence         # Confidence of detection
string action              # Current avoidance action
```

### 2.5 Create RobotSignal.msg

Create file: `src/robot_interfaces/msg/RobotSignal.msg`

```
# Robot operational signal and status
std_msgs/Header header
bool is_moving              # Is robot currently moving
bool is_autonomous          # Is autonomous mode enabled
bool obstacle_detected      # Obstacle present
bool emergency_stop         # Emergency stop activated
float32 linear_velocity     # Current linear velocity (m/s)
float32 angular_velocity    # Current angular velocity (rad/s)
string current_action       # "idle", "moving", "turning", "avoiding", "stopped"
string operation_mode       # "autonomous", "manual", "monitoring"
float32 battery_level       # Battery level (0-100%)
```

---

## Step 3: Build the Package

### 3.1 Verify file structure

```bash
tree src/robot_interfaces/
# Should show:
# robot_interfaces/
# ├── CMakeLists.txt
# ├── package.xml
# └── msg/
#     ├── Detection.msg
#     ├── DetectionArray.msg
#     ├── ObstacleStatus.msg
#     └── RobotSignal.msg
```

### 3.2 Build the package

```bash
cd ~/ros2_ws_urdf
colcon build --packages-select robot_interfaces
source install/setup.bash
```

### 3.3 Verify message creation

```bash
ros2 interface list | grep robot_interfaces
```

You should see:
```
robot_interfaces/msg/Detection
robot_interfaces/msg/DetectionArray
robot_interfaces/msg/ObstacleStatus
robot_interfaces/msg/RobotSignal
```

---

## Step 4: Test Message Definitions

### 4.1 Test message interface

```bash
ros2 interface show robot_interfaces/msg/DetectionArray
```

This should display your message structure.

### 4.2 Create a simple test publisher

Create file: `src/robot_interfaces/test_publisher.py`

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from robot_interfaces.msg import Detection, DetectionArray, ObstacleStatus, RobotSignal
from std_msgs.msg import Header

class TestPublisher(Node):
    def __init__(self):
        super().__init__('test_message_publisher')
        
        # Create publishers for each message type
        self.detection_pub = self.create_publisher(DetectionArray, '/vision/detections', 10)
        self.obstacle_pub = self.create_publisher(ObstacleStatus, '/vision/obstacles', 10)
        self.signal_pub = self.create_publisher(RobotSignal, '/robot/signal', 10)
        
        self.timer = self.create_timer(1.0, self.publish_test_messages)
        self.get_logger().info('Test publisher started')
    
    def publish_test_messages(self):
        # Test DetectionArray
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = 'camera'
        
        detection = Detection()
        detection.object_type = 'car'
        detection.confidence = 0.95
        detection.x_min = 100
        detection.y_min = 50
        detection.x_max = 300
        detection.y_max = 250
        detection.center_x = 200.0
        detection.center_y = 150.0
        detection.width = 200.0
        detection.height = 200.0
        detection.distance = 5.0
        detection.description = 'Test car detection'
        
        det_array = DetectionArray()
        det_array.header = header
        det_array.detections = [detection]
        det_array.image_width = 640
        det_array.image_height = 480
        det_array.processing_time = 0.033
        det_array.status = 'success'
        
        self.detection_pub.publish(det_array)
        self.get_logger().info('Published DetectionArray')
        
        # Test ObstacleStatus
        obstacle = ObstacleStatus()
        obstacle.header = header
        obstacle.detected = True
        obstacle.primary_obstacle = 'car'
        obstacle.front_distance = 3.5
        obstacle.left_distance = 5.0
        obstacle.right_distance = 4.5
        obstacle.center_x = 320.0
        obstacle.center_y = 240.0
        obstacle.confidence = 0.92
        obstacle.action = 'avoiding_left'
        
        self.obstacle_pub.publish(obstacle)
        self.get_logger().info('Published ObstacleStatus')
        
        # Test RobotSignal
        signal = RobotSignal()
        signal.header = header
        signal.is_moving = True
        signal.is_autonomous = True
        signal.obstacle_detected = True
        signal.emergency_stop = False
        signal.linear_velocity = 0.3
        signal.angular_velocity = 0.1
        signal.current_action = 'avoiding'
        signal.operation_mode = 'autonomous'
        signal.battery_level = 85.0
        
        self.signal_pub.publish(signal)
        self.get_logger().info('Published RobotSignal')

def main(args=None):
    rclpy.init(args=args)
    node = TestPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 4.3 Run the test publisher

In terminal 1:
```bash
cd ~/ros2_ws_urdf
source install/setup.bash
python3 src/robot_interfaces/test_publisher.py
```

In terminal 2 (monitor the topics):
```bash
cd ~/ros2_ws_urdf
source install/setup.bash
ros2 topic list
ros2 topic echo /vision/detections
```

---

## Step 5: Update Existing Packages

### 5.1 Update my_robot_bringup package.xml

Add dependency to `src/my_robot_bringup/package.xml`:

```xml
<exec_depend>robot_interfaces</exec_depend>
```

### 5.2 Update my_robot_description package.xml

Add dependency to `src/my_robot_description/package.xml`:

```xml
<exec_depend>robot_interfaces</exec_depend>
```

### 5.3 Update ros2_opencv package.xml

Edit `src/ros2_opencv/package.xml` and add:

```xml
<exec_depend>robot_interfaces</exec_depend>
```

### 5.4 Rebuild all packages

```bash
cd ~/ros2_ws_urdf
colcon build
source install/setup.bash
```

---

## Step 6: Create Integration Script

Create a script to verify all messages work together: `src/robot_interfaces/integration_test.py`

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from robot_interfaces.msg import Detection, DetectionArray, ObstacleStatus, RobotSignal
from std_msgs.msg import Header

class IntegrationTest(Node):
    def __init__(self):
        super().__init__('integration_test')
        
        # Create subscriptions to all message types
        self.create_subscription(DetectionArray, '/vision/detections', self.detection_callback, 10)
        self.create_subscription(ObstacleStatus, '/vision/obstacles', self.obstacle_callback, 10)
        self.create_subscription(RobotSignal, '/robot/signal', self.signal_callback, 10)
        
        self.detection_count = 0
        self.obstacle_count = 0
        self.signal_count = 0
        
        self.get_logger().info('Integration test node started - listening to all topics')
    
    def detection_callback(self, msg: DetectionArray):
        self.detection_count += 1
        self.get_logger().info(
            f'Detection #{self.detection_count}: {len(msg.detections)} objects detected, '
            f'Status: {msg.status}, Processing time: {msg.processing_time:.3f}s'
        )
        for det in msg.detections:
            self.get_logger().info(
                f'  - {det.object_type}: confidence={det.confidence:.2f}, '
                f'distance={det.distance:.2f}m'
            )
    
    def obstacle_callback(self, msg: ObstacleStatus):
        self.obstacle_count += 1
        self.get_logger().info(
            f'Obstacle #{self.obstacle_count}: detected={msg.detected}, '
            f'type={msg.primary_obstacle}, front={msg.front_distance:.2f}m, '
            f'action={msg.action}'
        )
    
    def signal_callback(self, msg: RobotSignal):
        self.signal_count += 1
        self.get_logger().info(
            f'Signal #{self.signal_count}: moving={msg.is_moving}, '
            f'autonomous={msg.is_autonomous}, velocity={msg.linear_velocity:.2f}m/s, '
            f'battery={msg.battery_level:.1f}%'
        )

def main(args=None):
    rclpy.init(args=args)
    node = IntegrationTest()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## Checklist for Phase 1 Completion

- [ ] Created `robot_interfaces` package
- [ ] Updated `package.xml` with proper dependencies
- [ ] Updated `CMakeLists.txt` with message generation
- [ ] Created all 4 message definition files (.msg)
- [ ] Built the `robot_interfaces` package successfully
- [ ] Verified messages with `ros2 interface show`
- [ ] Created and ran test publisher
- [ ] Verified topics with `ros2 topic list`
- [ ] Updated all other packages to depend on `robot_interfaces`
- [ ] Rebuilt entire workspace
- [ ] Ran integration test and verified message flow

---

## Troubleshooting

### Issue: colcon build fails

**Solution:**
```bash
rm -rf build/ install/ log/
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release
```

### Issue: "robot_interfaces" not found when importing

**Solution:**
```bash
# Make sure you've sourced the setup file
source install/setup.bash
```

### Issue: Message doesn't appear in `ros2 interface list`

**Solution:**
1. Verify CMakeLists.txt has correct message files listed
2. Rebuild: `colcon build --packages-select robot_interfaces`
3. Source again: `source install/setup.bash`
4. Check: `ros2 interface list | grep robot_interfaces`

---

## Next Steps

After completing Phase 1:
1. Start with **Task 2.1** - Create Vision Detection Node
2. Use the custom messages you just created
3. Subscribe to `/camera/image_raw` and publish to `/vision/detections`

---

**Document Version:** 1.0  
**Created:** April 2026
