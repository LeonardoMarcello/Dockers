#!/bin/bash
# File: ros_entrypoint.sh

# Shell B:
source ${ROS1_INSTALL_PATH}/setup.bash
# Or, on OSX, something like:
# . ~/ros_catkin_ws/install_isolated/setup.bash
source ${ROS2_INSTALL_PATH}/setup.bash
#export ROS_MASTER_URI=http://localhost:11311
ros2 run ros1_bridge dynamic_bridge

# Execute whatever command is passed to the container
exec "$@"
