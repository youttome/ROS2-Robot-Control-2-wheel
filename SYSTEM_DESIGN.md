# ROS2 Robot Project - System Architecture & Design

## System Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        ROBOT HARDWARE                           │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐          │
│  │   USB/IP    │  │   Motor      │  │  Encoders   │          │
│  │   Camera    │  │  Controllers │  │   (IMU)     │          │
│  └──────────────┘  └──────────────┘  └─────────────┘          │
└─────────┬──────────────────┬──────────────────────┬─────────────┘
          │                  │                      │
          ▼                  ▼                      ▼
┌──────────────────────────────────────────────────────────────────┐
│              ROS2 MIDDLEWARE (DDS)                               │
│  Provides distributed communication between all nodes            │
└──────────────────────────────────────────────────────────────────┘
          │
    ┌─────┴─────────────────────────────────────────────┐
    │                                                     │
    ▼                                                     ▼
┌─────────────────────────────┐          ┌──────────────────────────┐
│   PERCEPTION NODE CLUSTER   │          │  CONTROL NODE CLUSTER    │
│                             │          │                          │
│  ┌──────────────────────┐   │          │  ┌──────────────────┐    │
│  │ Camera Publisher     │   │          │  │ Movement Manager │    │
│  │ Topic: /camera/      │   │          │  │ Input: /avoidance│    │
│  │ image_raw            │   │          │  │ /command        │    │
│  └──────────┬───────────┘   │          │  │ Output: /diff_   │    │
│             │               │          │  │ drive_controller/│    │
│             ▼               │          │  │ cmd_vel         │    │
│  ┌──────────────────────┐   │          │  └──────────────────┘    │
│  │ Vision Detector Node │   │          │          ▲               │
│  │ (Object Detection)   │   │          │          │               │
│  │ Input: /camera/      │   │          │          │               │
│  │ image_raw            │   │          │  ┌──────────────────┐    │
│  │ Output: /vision/     │   │          │  │ Obstacle Avoid   │    │
│  │ detections,          │   │          │  │ Node             │    │
│  │ /vision/obstacles    │   │          │  │ Input: /vision/  │    │
│  └──────────┬───────────┘   │          │  │ detections       │    │
│             │               │          │  │ Output: /avoidance│   │
│             │               │          │  │ /command         │    │
│             │               │          │  └──────────────────┘    │
│             │               │          │          ▲               │
│  ┌──────────────────────┐   │          │          │               │
│  │ Status Aggregator    │   │          └──────────┼───────────────┘
│  │ Input: All topics    │   │                     │
│  │ Output: /robot/      │   │                     │
│  │ status, /robot/      │   │    ┌────────────────┘
│  │ signal               │   │    │
│  └──────────────────────┘   │    │
│                             │    │
└─────────────────────────────┘    │
                                   │
                   ┌───────────────┤
                   │               │
                   ▼               ▼
          ┌──────────────────┐  ┌──────────────────────┐
          │  MONITORING APP  │  │  RViz2 Visualization │
          │  (GUI - PyQt5)   │  │  (Native ROS2)       │
          │  - Live camera   │  │  - Robot TF frames   │
          │  - Detections    │  │  - Sensor markers    │
          │  - Obstacles     │  │  - Path visualization│
          │  - Robot status  │  │  - Manual control    │
          │  - Manual control│  └──────────────────────┘
          └──────────────────┘
```

---

## Node Communication Flow

### Scenario 1: Normal Autonomous Navigation

```
[Camera] 
    ▼
[Camera Publisher] → Topic: /camera/image_raw
    ▼
[Vision Detector]
    ├─→ Topic: /vision/detections (Detection data)
    └─→ Topic: /vision/obstacles (Obstacle info)
    ▼
[Obstacle Avoidance]
    ├─→ Topic: /avoidance/command (Movement command)
    └─→ Topic: /avoidance/status (Avoidance info)
    ▼
[Movement Manager]
    ├─→ Topic: /diff_drive_controller/cmd_vel (To motors)
    └─→ Topic: /robot/signal (Robot status)
    ▼
[Motors]
    ▼
[Robot Moves with Avoidance]
```

**Latency Path:**
- Camera capture: ~30ms
- Frame transmission: ~10ms
- Vision detection: ~50-100ms
- Avoidance planning: ~20ms
- Movement command: ~10ms
- Motor response: ~20-50ms
- **Total: 140-220ms**

---

### Scenario 2: Emergency Stop

```
[Manual Override / Emergency Button]
    ▼
[Monitoring App]
    ├─→ Topic: /robot/emergency_stop
    └─→ Topic: /robot/signal (emergency flag)
    ▼
[Movement Manager] (Highest Priority)
    ├─→ Topic: /diff_drive_controller/cmd_vel (ZERO velocity)
    └─→ Watchdog timeout: 100ms
    ▼
[Robot Stops Immediately]
```

**Maximum latency:** ~50ms

---

## Topic Specifications

### Input Topics (Subscribers)

| Topic | Message Type | Node | Frequency | Purpose |
|-------|-------------|------|-----------|---------|
| `/camera/image_raw` | `sensor_msgs/Image` | Vision Detector | 30 Hz | Camera frame input |
| `/vision/detections` | `robot_interfaces/DetectionArray` | Obstacle Avoidance | Variable | Object detection |
| `/robot/emergency_stop` | `std_msgs/Bool` | Movement Manager | Event-driven | Emergency stop signal |
| `/manual/cmd_vel` | `geometry_msgs/Twist` | Movement Manager | Variable | Manual control |

### Output Topics (Publishers)

| Topic | Message Type | Node | Frequency | Purpose |
|-------|-------------|------|-----------|---------|
| `/vision/detections` | `robot_interfaces/DetectionArray` | Vision Detector | 10 Hz | Detected objects |
| `/vision/obstacles` | `robot_interfaces/ObstacleStatus` | Vision Detector | 10 Hz | Obstacle analysis |
| `/avoidance/command` | `geometry_msgs/Twist` | Obstacle Avoidance | 10 Hz | Movement command |
| `/avoidance/status` | `std_msgs/String` | Obstacle Avoidance | 1 Hz | Status updates |
| `/diff_drive_controller/cmd_vel` | `geometry_msgs/TwistStamped` | Movement Manager | 20 Hz | Motor commands |
| `/robot/status` | `std_msgs/String` | Status Aggregator | 1 Hz | Overall status |
| `/robot/signal` | `robot_interfaces/RobotSignal` | Status Aggregator | 10 Hz | Signal info |

---

## Node Specifications

### 1. Camera Publisher Node
- **Package:** `ros2_opencv`
- **File:** `camera_publisher_cv.py`
- **Language:** Python
- **Dependencies:** OpenCV, cv_bridge, rclpy
- **Inputs:** USB/IP Camera device
- **Outputs:** `/camera/image_raw` (Image frames)
- **Processing:** Frame capture, resize to 640x480
- **Frequency:** 10 Hz
- **Resources:** Medium (depends on resolution)

### 2. Vision Detector Node (TO IMPLEMENT)
- **Package:** `ros2_opencv`
- **File:** `vision_detector.py`
- **Language:** Python
- **Dependencies:** OpenCV, robot_interfaces, rclpy
- **Inputs:** `/camera/image_raw`
- **Outputs:**
  - `/vision/detections` (DetectionArray)
  - `/vision/obstacles` (ObstacleStatus)
  - `/vision/annotated_image` (Image with boxes)
- **Processing:**
  - Object detection (YOLO, HOG, or Cascade)
  - Confidence filtering
  - Bounding box calculation
  - Distance estimation
- **Frequency:** 10 Hz
- **Resources:** High (GPU recommended)

### 3. Obstacle Avoidance Node (TO IMPLEMENT)
- **Package:** `my_robot_bringup`
- **File:** `obstacle_avoidance.py`
- **Language:** Python
- **Dependencies:** geometry_msgs, robot_interfaces, rclpy
- **Inputs:**
  - `/vision/detections`
  - `/vision/obstacles`
- **Outputs:**
  - `/avoidance/command` (Twist)
  - `/avoidance/status` (String)
- **Processing:**
  - Path planning
  - Avoidance decision making
  - Velocity ramping
- **Frequency:** 10 Hz
- **Resources:** Low-Medium

### 4. Movement Manager Node (TO ENHANCE)
- **Package:** `my_robot_bringup`
- **File:** `movement_manager.py`
- **Language:** Python
- **Dependencies:** geometry_msgs, robot_interfaces, rclpy
- **Inputs:**
  - `/avoidance/command`
  - `/manual/cmd_vel`
  - `/robot/emergency_stop`
- **Outputs:**
  - `/diff_drive_controller/cmd_vel` (TwistStamped)
- **Processing:**
  - Command arbitration
  - Safety checks
  - Velocity limiting
- **Frequency:** 20 Hz
- **Resources:** Low

### 5. Status Aggregator Node (TO IMPLEMENT)
- **Package:** `my_robot_bringup`
- **File:** `robot_status_monitor.py`
- **Language:** Python
- **Dependencies:** All message types, rclpy
- **Inputs:** All sensor/status topics
- **Outputs:**
  - `/robot/status` (String)
  - `/robot/signal` (RobotSignal)
- **Processing:**
  - Status aggregation
  - Watchdog monitoring
  - Alert generation
- **Frequency:** 1-10 Hz
- **Resources:** Low

### 6. Monitoring Application (TO IMPLEMENT)
- **Package:** `monitor_app` (New)
- **File:** `monitor_app_gui.py`
- **Language:** Python
- **GUI Framework:** PyQt5
- **Dependencies:** All message types, rclpy, cv_bridge, opencv
- **Inputs:** All ROS2 topics
- **Outputs:**
  - `/manual/cmd_vel` (for manual control)
  - `/robot/emergency_stop` (emergency signal)
- **Features:**
  - Real-time camera display
  - Detection visualization
  - Obstacle visualization
  - Status dashboard
  - Manual control interface
- **Resources:** Medium-High

---

## Communication Patterns

### Pattern 1: Request-Response (Service)
Used for configuration changes:

```python
client = node.create_client(SetParameter, '/vision/set_confidence')
request = SetParameter.Request()
request.threshold = 0.85
future = client.call_async(request)
```

### Pattern 2: Publish-Subscribe (Topic)
Used for continuous sensor data:

```python
# Publisher
publisher = node.create_publisher(Message, '/topic/name', queue_size)
publisher.publish(message)

# Subscriber
subscription = node.create_subscription(
    Message, '/topic/name', callback, queue_size
)
```

### Pattern 3: Action (Goal-Oriented)
Used for robot movements:

```python
# Client sends goal
action_client.send_goal_async(goal)

# Server processes goal
# Sends feedback periodically
# Sends result when done
```

---

## Data Flow Timing

### Worst-Case Scenario
```
Time    Event
0ms     Camera captures frame
~30ms   Frame encoded to ROS message
~40ms   Vision node receives frame
~140ms  Vision processing complete, publishes detections
~160ms  Avoidance node receives detections
~180ms  Avoidance planning complete, publishes command
~190ms  Movement manager receives command
~200ms  Motor command sent
~250ms  Motors start moving
───────────────────────
~250ms  Total latency (CRITICAL: < 300ms for safety)
```

### Best-Case Scenario
```
0ms     Camera captures frame
~15ms   Frame transmitted
~35ms   Vision processing (optimized)
~50ms   Detections available
~60ms   Avoidance command
~70ms   Motor command sent
~100ms  Total latency
```

---

## Resource Allocation

### CPU Usage Estimates
- Camera Publisher: ~5-10%
- Vision Detector: ~40-60% (with GPU: ~10-15%)
- Obstacle Avoidance: ~3-5%
- Movement Manager: ~1-2%
- Status Aggregator: ~1-2%
- Monitoring App: ~10-20%
- **Total: 60-100%** (Single CPU core)

### Memory Usage Estimates
- Camera frame (640x480, RGB8): ~0.9 MB
- ROS nodes (typical): ~20-50 MB each
- Message queue buffers: ~10-20 MB
- **Total: 150-250 MB**

---

## Safety Architecture

### Safety Levels

**Level 1: Hardware Safety**
- Mechanical brakes
- Physical speed limiters
- Power cutoff switches

**Level 2: ROS2 Watchdog**
- Message timeout detection
- Heartbeat monitoring
- Automatic stop on timeout

**Level 3: Software Safety**
- Obstacle detection confidence check
- Speed limitation
- Collision avoidance
- Emergency stop override

**Level 4: Monitoring Layer**
- Real-time visualization
- Operator oversight
- Manual intervention capability
- Logging and diagnostics

### Safety Constraints
```
Maximum Linear Velocity: 0.5 m/s
Maximum Angular Velocity: 1.0 rad/s
Minimum Obstacle Distance: 0.3 m (30cm)
Maximum Detection Latency: 300ms
Watchdog Timeout: 500ms
Emergency Stop Response: <50ms
```

---

## Development Workflow

### 1. Local Testing
```bash
# Terminal 1: Run node
ros2 run ros2_opencv camera_publisher_cv

# Terminal 2: Monitor topic
ros2 topic echo /camera/image_raw

# Terminal 3: RViz visualization
ros2 run rviz2 rviz2 -d config/visualization.rviz
```

### 2. Integration Testing
```bash
# Build all packages
colcon build

# Source workspace
source install/setup.bash

# Run launch file
ros2 launch my_robot_bringup complete_system.launch.py
```

### 3. Simulation (Future)
```bash
# With Gazebo
ros2 launch my_robot_bringup complete_system.launch.py use_sim_time:=true
```

---

## Monitoring & Debugging Commands

### Check Node Status
```bash
ros2 node list
ros2 node info /node_name
```

### Monitor Topics
```bash
ros2 topic list
ros2 topic echo /topic_name
ros2 topic info /topic_name
```

### Check Message Sizes
```bash
ros2 bag record -a -o robot_run1
ros2 bag info robot_run1
```

### Visualize TF Tree
```bash
ros2 run tf2_tools view_frames
```

### Measure Performance
```bash
ros2 node list --include-hidden
ros2 service call /node_name/get_parameters ros2srvs/GetParameters
```

---

## Scalability Considerations

### Adding New Nodes
1. Define custom messages in `robot_interfaces`
2. Create node in appropriate package
3. Update launch file
4. Rebuild workspace
5. Test communication

### Adding New Sensors
1. Create publisher node for new sensor
2. Define custom message (if needed)
3. Subscribe in relevant processing nodes
4. Update topic documentation
5. Test sensor integration

### Multi-Robot Setup
```
Robot 1: /robot1/vision/detections
Robot 2: /robot2/vision/detections

Coordinator Node: Subscribes to both
```

---

## Future Enhancements

### Planned Features
- [ ] Multi-robot coordination
- [ ] SLAM implementation
- [ ] Deep learning models (YOLO v8)
- [ ] LiDAR integration
- [ ] IMU-based localization
- [ ] Path planning (A*, RRT)
- [ ] Web-based monitoring
- [ ] Distributed nodes on multiple machines

### Research Areas
- Improved avoidance algorithms
- Machine learning for detection
- Edge computing optimization
- Real-time scheduling
- Network optimization

---

## Documentation Standards

### Code Documentation
- Docstrings for all functions
- Inline comments for complex logic
- Type hints for all parameters
- Examples in docstrings

### File Headers
```python
#!/usr/bin/env python3
"""
Brief description of node.

Longer description explaining functionality,
inputs, outputs, and usage.
"""

# Author: Your Name
# Date: 2026-04-22
# Version: 1.0
```

---

## Contact & Support

For issues or questions:
1. Check the project documentation
2. Review ROS2 official docs: https://docs.ros.org/
3. Search existing issues
4. Create detailed bug report

---

**Document Version:** 1.0  
**Created:** April 2026  
**Scope:** ROS2 Robot Vision & Control System
