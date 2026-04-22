import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class CameraSubscriber(Node):

    def __init__(self):
        super().__init__('camera_subscriber')
        self.bridgeObject = CvBridge()
        self.topicNameFrame = '/camera/image_raw'
        self.queueSize = 10
        self.subscription = self.create_subscription(
            Image,
            self.topicNameFrame,
            self.listener_callback,
            self.queueSize)
        self.subscription
        self.frameCount = 0
        self.get_logger().info('Camera subscriber initialized')

    def listener_callback(self, imageMessage):
        try:
            frame = self.bridgeObject.imgmsg_to_cv2(imageMessage, desired_encoding='bgr8')
            self.frameCount += 1
            
            # Display the frame
            cv2.imshow('Camera Feed', frame)
            cv2.waitKey(1)
            
            self.get_logger().info(f'Received and displayed frame {self.frameCount}')
        except Exception as e:
            self.get_logger().error(f'Error processing frame: {str(e)}')


def main(args=None):
    rclpy.init(args=args)
    cameraSubscriberObject = CameraSubscriber()
    rclpy.spin(cameraSubscriberObject)
    cv2.destroyAllWindows()
    cameraSubscriberObject.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
