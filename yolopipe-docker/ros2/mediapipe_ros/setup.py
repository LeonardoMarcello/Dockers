from setuptools import setup
import os

package_name = 'mediapipe_ros'

model_data = []
if os.path.exists('model'):
    for root, _, files in os.walk('model'):
        files = [os.path.join(root, f) for f in files]
        if files:
            target_dir = os.path.join('share', package_name, root)
            model_data.append((target_dir, files))

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ] + model_data,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Leonardo Marcello',
    maintainer_email='leonardo.marcello_99@hotmail.com',
    description='MediaPipe for ROS 2',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mediapipe_node = mediapipe_ros.mediapipe_node:main',
        ],
    },
)