#!/bin/bash
set -e

# 1. Source the base ROS 2 distribution
source "/opt/ros/${ROS_DISTRO}/setup.bash"

# 2. Source your specific workspace
if [ -f "/home/${USER}/ros2_ws/install/setup.bash" ]; then
    source "/home/${USER}/ros2_ws/install/setup.bash"
fi

# 3. Execute the command passed from Docker (CMD or docker-compose command)
exec "$@"