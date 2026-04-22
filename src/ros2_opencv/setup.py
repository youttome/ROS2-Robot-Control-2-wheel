from setuptools import find_packages, setup

package_name = 'ros2_opencv'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abso',
    maintainer_email='youttome@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
                    entry_points={
                        'console_scripts': [
                            'camera_publisher_cv = ros2_opencv.camera_publisher_cv:main',
                            'camera_subscriber_cv = ros2_opencv.camera_subscriber_cv:main',
                        ],
                    },

)
