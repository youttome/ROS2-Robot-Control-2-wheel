import cv2

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class CameraPublisher(Node):

    def __init__(self):
        super().__init__('camera_publisher')
        self.cameraDeviceNumber = 0
        self.camera = cv2.VideoCapture(self.cameraDeviceNumber)
        if not self.camera.isOpened():
            self.get_logger().error('Failed to open camera device')
            return
        self.bridgeObject = CvBridge()
        self.topicNameFrame = '/camera/image_raw'
        self.queueSize = 10
        self.publisher_ = self.create_publisher(Image, self.topicNameFrame, self.queueSize)
        self.communicationPeriod = 0.1
        self.timer = self.create_timer(self.communicationPeriod, self.timer_callback)
        self.i = 0
    
    def timer_callback(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
            Ros2ImageMessage = self.bridgeObject.cv2_to_imgmsg(frame, encoding='bgr8')
            Ros2ImageMessage.header.stamp = self.get_clock().now().to_msg()
            Ros2ImageMessage.header.frame_id = 'camera_link'
            self.publisher_.publish(Ros2ImageMessage)
            self.get_logger().info('Publishing video frame %d' % self.i)
            self.i += 1
        else:
            self.get_logger().warn('Failed to read frame from camera')
    
    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()

def main(args=None):
    rclpy.init(args=args)
    cameraPublisherObject = CameraPublisher()
    rclpy.spin(cameraPublisherObject)
    cameraPublisherObject.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()