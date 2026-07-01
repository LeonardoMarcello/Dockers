
ARG ROS_DISTRO=noetic
FROM ros:${ROS_DISTRO}-ros-core

# Use bash for all RUN commands
SHELL ["/bin/bash", "-c"]

# ---------------------------
# Install dependencies
# ---------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-catkin-tools \
    python3-pyqt5 \
    python3-tk \
    python3-pip \
    ros-${ROS_DISTRO}-roscpp \
    ros-${ROS_DISTRO}-std-msgs \
    ros-${ROS_DISTRO}-message-generation \
    ros-${ROS_DISTRO}-message-runtime \
    && rm -rf /var/lib/apt/lists/*
RUN pip install matplotlib 
# ---------------------------
# Create workspace
# ---------------------------
WORKDIR /ros1_ws
RUN mkdir -p src

# ---------------------------
# Copy your package
# ---------------------------
COPY ros1/src/papillarray_ros_v2 src/papillarray_ros_v2
COPY ros1/src/papillarray_interface src/papillarray_interface

# ---------------------------
# Build workspace
# ---------------------------
RUN source /opt/ros/$ROS_DISTRO/setup.bash && \
    catkin_make


# ---------------------------
# Default entrypoint
# ---------------------------
ENTRYPOINT ["/bin/bash", "-c", "source /opt/ros/$ROS_DISTRO/setup.bash && source /ros1_ws/devel/setup.bash && exec \"$@\"", "--"]

# ---------------------------
# Default command
# ---------------------------
#CMD ["roslaunch", "papillarray_ros", "papillarray.launch"]
