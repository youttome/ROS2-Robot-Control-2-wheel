#!/usr/bin/env python3

import rclpy
from geometry_msgs.msg import TwistStamped
import time
from rclpy.node import Node


class RobotMovementPublisher(Node):
    def __init__(self):
        super().__init__('robot_movement_publisher')
        self.publisher = self.create_publisher(
            TwistStamped,
            '/diff_drive_controller/cmd_vel',
            10
        )
        self.get_logger().info('Movement Publisher Node Started')

    def move_forward(self, duration=2.0, speed=0.5):
        """Move robot forward"""
        self.get_logger().info(f'Moving forward at {speed} m/s for {duration}s')
        msg = TwistStamped()
        msg.twist.linear.x = speed
        msg.twist.angular.z = 0.0
        
        end_time = time.time() + duration
        while time.time() < end_time:
            msg.header.stamp = self.get_clock().now().to_msg()
            self.publisher.publish(msg)
            time.sleep(0.1)
        
        # Stop robot
        msg.twist.linear.x = 0.0
        msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(msg)

    def move_backward(self, duration=2.0, speed=-0.5):
        """Move robot backward"""
        self.get_logger().info(f'Moving backward at {speed} m/s for {duration}s')
        msg = TwistStamped()
        msg.twist.linear.x = speed
        msg.twist.angular.z = 0.0
        
        end_time = time.time() + duration
        while time.time() < end_time:
            msg.header.stamp = self.get_clock().now().to_msg()
            self.publisher.publish(msg)
            time.sleep(0.1)
        
        # Stop robot
        msg.twist.linear.x = 0.0
        msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(msg)

    def rotate(self, duration=2.0, angular_speed=0.5):
        """Rotate robot"""
        self.get_logger().info(f'Rotating at {angular_speed} rad/s for {duration}s')
        msg = TwistStamped()
        msg.twist.linear.x = 0.0
        msg.twist.angular.z = angular_speed
        
        end_time = time.time() + duration
        while time.time() < end_time:
            msg.header.stamp = self.get_clock().now().to_msg()
            self.publisher.publish(msg)
            time.sleep(0.1)
        
        # Stop robot
        msg.twist.angular.z = 0.0
        msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(msg)

    def move_circle(self, duration=5.0, linear_speed=0.3, angular_speed=0.3):
        """Move robot in a circle"""
        self.get_logger().info(f'Moving in circle for {duration}s')
        msg = TwistStamped()
        msg.twist.linear.x = linear_speed
        msg.twist.angular.z = angular_speed
        
        end_time = time.time() + duration
        while time.time() < end_time:
            msg.header.stamp = self.get_clock().now().to_msg()
            self.publisher.publish(msg)
            time.sleep(0.1)
        
        # Stop robot
        msg.twist.linear.x = 0.0
        msg.twist.angular.z = 0.0
        msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(msg)

    def stop(self):
        """Stop robot"""
        self.get_logger().info('Stopping robot')
        msg = TwistStamped()
        msg.twist.linear.x = 0.0
        msg.twist.angular.z = 0.0
        msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    
    node = RobotMovementPublisher()
    
    try:
        # Give time for all nodes to connect
        time.sleep(3)
        
        # Execute movements
        node.move_forward(duration=3.0, speed=0.5)
        time.sleep(1)
        
        node.rotate(duration=2.0, angular_speed=0.5)
        time.sleep(1)
        
        node.move_backward(duration=2.0, speed=-0.3)
        time.sleep(1)
        
        node.move_circle(duration=4.0, linear_speed=0.3, angular_speed=0.3)
        
        node.stop()
        node.get_logger().info('Movement sequence completed')
        
        # Keep node alive briefly before shutdown
        time.sleep(1)
        
    except KeyboardInterrupt:
        node.stop()
        node.get_logger().info('Movement interrupted by user')
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
