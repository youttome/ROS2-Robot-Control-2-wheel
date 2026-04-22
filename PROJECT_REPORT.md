# ROS2 Robot Vision & Control System - Project Report

**Project Name:** Autonomous Mobile Robot with Camera-Based Vision and Obstacle Avoidance  
**Date:** April 2026  
**Purpose:** College Project - Autonomous Navigation System  
**Status:** In Development

---

## 1. PROJECT OVERVIEW

This project implements a ROS2-based autonomous mobile robot system that integrates:
- **Camera Vision Processing** - Real-time object detection using OpenCV
- **Robot Control System** - Differential drive movement control
- **Obstacle Avoidance** - Real-time detection and avoidance of obstacles
- **Remote Monitoring** - GUI application for real-time monitoring
- **Signal Management** - Custom topics for sensor data and control signals

### Project Objectives
1. Develop a fully functional autonomous mobile robot
2. Implement real-time camera-based object detection
3. Create obstacle avoidance logic for autonomous navigation
4. Build a user-friendly monitoring application
5. Establish ROS2 topic communication system

---

## 2. CURRENT PROJECT STRUCTURE

```
ros2_ws_urdf/
├── src/
│   ├── my_robot_bringup/
│   │   ├── launch/
│   │   │   ├── complete_system.launch.py
│   │   │   └── robot_control.launch.py
│   │   ├── scripts/
│   │   │   └── movement_publisher.py (Basic movement control)
│   │   ├── config/
│   │   └── package.xml
│   │
│   ├── my_robot_description/
│   │   ├── urdf/
│   │   │   ├── my_robot.urdf.xacro
│   │   │   ├── mobile_base.xacro
│   │   │   ├── mobile_base.ros2_control.xacro
│   │   │   └── common_properties.xacro
│   │   ├── rviz/
│   │   │   └── urdf_config.rviz
│   │   ├── launch/
│   │   └── package.xml
│   │
│   └── ros2_opencv/
│       ├── ros2_opencv/
│       │   ├── camera_publisher_cv.py (Camera feed publisher)
│       │   ├── camera_subscriber_cv.py (Camera feed subscriber)
│       │   └── __init__.py
│       ├── setup.py
│       └── package.xml
│
├── build/ (Build output)
├── install/ (Installation files)
└── log/ (Build logs)
```

### Existing Components

#### 2.1 Robot Movement Control (`movement_publisher.py`)
- **Status:** ✓ Basic implementation exists
- **Functions:**
  - `move_forward()` - Forward movement
  - `move_backward()` - Backward movement
  - `rotate()` - In-place rotation
  - `move_circle()` - Circular path movement
  - `stop()` - Emergency stop
- **Output Topic:** `/diff_drive_controller/cmd_vel`

#### 2.2 Camera System (`ros2_opencv` package)
- **Publisher:** Streams camera frames to `/camera/image_raw`
- **Subscriber:** Receives and displays camera frames
- **Resolution:** 640x480 pixels
- **Frame Rate:** 10Hz (0.1s period)

#### 2.3 Robot Description (`my_robot_description`)
- URDF/Xacro files for robot model definition
- Mobile base configuration
- ROS2 control integration
- RViz visualization configuration

---

## 3. SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────┐
│         ROBOT HARDWARE LAYER                        │
│  ├─ Camera (USB or Onboard)                        │
│  ├─ Motor Controllers                              │
│  ├─ Wheel Encoders                                 │
│  └─ Power Management                               │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│         ROS2 NODE LAYER                             │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ Camera Publisher (ros2_opencv)               │   │
│  │ Topic: /camera/image_raw                     │   │
│  └──────────────────────────────────────────────┘   │
│           ↓                                          │
│  ┌──────────────────────────────────────────────┐   │
│  │ Vision Processing Node (TO BE IMPLEMENTED)   │   │
│  │ • Object Detection                           │   │
│  │ • Obstacle Classification                    │   │
│  │ • Publish detection results                  │   │
│  │ Topics:                                      │   │
│  │  - /vision/detections (Custom Msg)           │   │
│  │  - /vision/obstacles (Bool array)            │   │
│  └──────────────────────────────────────────────┘   │
│           ↓                                          │
│  ┌──────────────────────────────────────────────┐   │
│  │ Obstacle Avoidance Node (TO BE IMPLEMENTED)  │   │
│  │ • Subscribe to detections                    │   │
│  │ • Generate avoidance paths                   │   │
│  │ • Publish movement commands                  │   │
│  │ Topics:                                      │   │
│  │  - /avoidance/command (Twist)                │   │
│  │  - /avoidance/status (String)                │   │
│  └──────────────────────────────────────────────┘   │
│           ↓                                          │
│  ┌──────────────────────────────────────────────┐   │
│  │ Movement Controller (movement_publisher.py)  │   │
│  │ Topic: /diff_drive_controller/cmd_vel        │   │
│  └──────────────────────────────────────────────┘   │
│           ↓                                          │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│    MONITORING & VISUALIZATION LAYER                 │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ Monitor Application (TO BE IMPLEMENTED)       │   │
│  │ • Real-time camera feed display               │   │
│  │ • Obstacle visualization                      │   │
│  │ • Robot status display                        │   │
│  │ • Manual control interface                    │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ├─ RViz2 (Robot visualization)                    │
│  └─ ROS2 Dashboard (System monitoring)             │
└─────────────────────────────────────────────────────┘
```

---

## 4. ROS2 TOPICS DEFINITION

| Topic Name | Message Type | Direction | Purpose |
|-----------|---------|-----------|---------|
| `/camera/image_raw` | `sensor_msgs/Image` | Publisher | Raw camera frames |
| `/vision/detections` | `Custom DetectionMsg` | Publisher | Object detection results |
| `/vision/obstacles` | `std_msgs/Float32MultiArray` | Publisher | Obstacle positions and sizes |
| `/vision/status` | `std_msgs/String` | Publisher | Vision system status |
| `/avoidance/command` | `geometry_msgs/Twist` | Publisher | Movement commands with avoidance |
| `/avoidance/status` | `std_msgs/String` | Publisher | Avoidance system status |
| `/diff_drive_controller/cmd_vel` | `geometry_msgs/TwistStamped` | Subscriber | Motor velocity commands |
| `/robot/status` | `std_msgs/String` | Publisher | Overall robot status |
| `/robot/signal` | `std_msgs/Bool` | Publisher | Emergency signal status |

---

## 5. KEY FEATURES TO IMPLEMENT

### Phase 1: Vision System Enhancement
- [ ] Implement object detection using YOLO or MobileNet
- [ ] Classify obstacles (cars, boxes, pedestrians)
- [ ] Create custom ROS2 message for detection data
- [ ] Implement real-time detection topic

### Phase 2: Obstacle Avoidance
- [ ] Implement obstacle detection algorithm
- [ ] Create avoidance path planning logic
- [ ] Integrate with movement controller
- [ ] Add safety margins and collision detection

### Phase 3: Robot Control Enhancement
- [ ] Implement real-time control node
- [ ] Add sensor integration (encoders, IMU)
- [ ] Implement feedback control loops
- [ ] Add emergency stop mechanisms

### Phase 4: Monitoring Application
- [ ] Create GUI with camera feed display
- [ ] Implement real-time obstacle visualization
- [ ] Add robot status monitoring
- [ ] Implement manual control interface

### Phase 5: Integration & Testing
- [ ] Full system integration testing
- [ ] Performance optimization
- [ ] Safety testing and validation
- [ ] Documentation completion

---

## 6. TECHNICAL SPECIFICATIONS

### Hardware Requirements
- Ubuntu 20.04 / 22.04 LTS
- ROS2 Humble or newer
- USB Camera / Onboard Camera
- Motor controllers (PWM capable)
- Differential drive robots (2-3 wheels)

### Software Requirements
- ROS2 (with controller_manager, geometry_msgs)
- OpenCV 4.x
- Python 3.8+
- cv_bridge
- Additional: YOLO/TensorFlow (for object detection)

### Dependencies
```xml
<!-- Core ROS2 -->
<buildtool_depend>ament_cmake</buildtool_depend>
<exec_depend>rclpy</exec_depend>
<exec_depend>geometry_msgs</exec_depend>
<exec_depend>sensor_msgs</exec_depend>

<!-- Robot Control -->
<exec_depend>robot_state_publisher</exec_depend>
<exec_depend>controller_manager</exec_depend>
<exec_depend>diff_drive_controller</exec_depend>

<!-- Vision -->
<exec_depend>cv_bridge</exec_depend>
<exec_depend>opencv</exec_depend>

<!-- Visualization -->
<exec_depend>rviz2</exec_depend>
```

---

## 7. IMPLEMENTATION ROADMAP

### Week 1: Foundation Setup
- Review existing code structure
- Set up development environment
- Create custom message definitions
- Implement basic vision pipeline

### Week 2: Vision Processing
- Implement object detection system
- Create detection topic publishers
- Test with camera feed
- Optimize detection performance

### Week 3: Obstacle Avoidance
- Develop avoidance algorithm
- Integrate with movement controller
- Test obstacle detection and avoidance
- Implement safety constraints

### Week 4: Monitoring Application
- Design GUI interface
- Implement real-time visualization
- Add control features
- Integrate all components

### Week 5: Integration & Testing
- Full system integration
- Performance testing
- Safety validation
- Documentation and finalization

---

## 8. CUSTOM MESSAGE DEFINITIONS (To Be Created)

### DetectionMsg
```
# Detected objects and their properties
string[] object_types      # Type of objects detected
float32[] confidence       # Confidence scores
int32[] x_positions        # X coordinates
int32[] y_positions        # Y coordinates
int32[] widths            # Bounding box widths
int32[] heights           # Bounding box heights
time timestamp            # Detection timestamp
```

### RobotSignalMsg
```
# Robot signal and status
bool is_moving            # Robot moving status
bool obstacle_detected    # Obstacle presence
float32 front_distance    # Distance to front obstacle
float32 left_distance     # Distance to left obstacle
float32 right_distance    # Distance to right obstacle
string current_action     # Current robot action
```

---

## 9. TESTING STRATEGY

### Unit Tests
- Vision detection accuracy
- Obstacle avoidance calculations
- Movement command validation

### Integration Tests
- Camera to vision node communication
- Vision to avoidance node communication
- Avoidance to movement controller communication

### System Tests
- Full autonomous navigation
- Obstacle avoidance in real environment
- Performance under various lighting conditions
- Safety and emergency stop functionality

### Validation Tests
- Accuracy of object detection (90%+ target)
- Avoidance success rate (100% safety target)
- Real-time performance (<100ms latency)

---

## 10. CHALLENGES & SOLUTIONS

| Challenge | Solution |
|-----------|----------|
| Real-time vision processing latency | Use optimized detection models (YOLO-tiny, MobileNet) |
| Lighting variation effects | Implement adaptive preprocessing, histogram equalization |
| False positive detections | Implement tracking and temporal filtering |
| Complex obstacle scenarios | Combine multiple sensor inputs, add safety margins |
| Scalability issues | Optimize node communication, use message compression |

---

## 11. SAFETY CONSIDERATIONS

- **Emergency Stop:** Implement hard stop on critical obstacle detection
- **Safety Margins:** Keep 30-50cm distance from detected obstacles
- **Speed Limits:** Limit maximum speed during autonomous operation
- **Manual Override:** Always allow manual control override
- **Watchdog Timer:** Implement timeout for lost sensor signals

---

## 12. DELIVERABLES

1. ✓ Complete source code with documentation
2. ✓ Custom message definitions
3. ✓ ROS2 launch files and configurations
4. ✓ Vision processing pipeline
5. ✓ Obstacle avoidance algorithm
6. ✓ Monitoring application
7. ✓ Test suite and validation results
8. ✓ Project documentation and user manual
9. ✓ Video demonstration

---

## 13. CONCLUSION

This ROS2-based autonomous robot system integrates vision processing with intelligent navigation to create a fully autonomous mobile platform. The modular design allows for easy testing, debugging, and future enhancements.

### Expected Outcomes
- Autonomous navigation with real-time obstacle avoidance
- 90%+ detection accuracy for target objects
- <100ms response time for obstacle detection
- Safe operation in dynamic environments
- Intuitive monitoring interface

---

**Document Version:** 1.0  
**Last Updated:** April 2026  
**Author:** Robot Engineering Team
