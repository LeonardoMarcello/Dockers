# Start from docker image with ros-noetic
FROM ros:rolling-ros1-bridge

# ====================================================================
# 	SETUP USER
# ====================================================================
# Add "allegro" user with same UID and GID as your host system 
# (copied from https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user)
ARG USERNAME=rosbridge
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
	&& useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
	&& apt-get update \
	&& apt-get install -y sudo \
	&& echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
	&& chmod 0440 /etc/sudoers.d/$USERNAME
# switch from root to user
USER $USERNAME

# Add user to video group to allow acces to webcam
RUN sudo usermod --append --groups video $USERNAME

# Update all packages
RUN sudo apt-get update && sudo apt upgrade -y

# Install terminator
RUN sudo DEBIAN_FRONTEND=noninteractive apt-get install terminator -y 


# ====================================================================
# 	INSTALL ROS LIBRARIES
# ====================================================================
# Add here additional ros-libraries
# - MoveIt!
# - candriver
# - USB Camera
# - RealSense
# - AprilTag
# - Vision_msgs (yolov7)
RUN sudo apt-get install -y \
	ros-noetic-sensor-msgs 



# Remove temporary apt files to lower the image size.
# To use apt install command while running a container
# they must be added again with: sudo apt update 
RUN sudo rm -rf /var/lib/apt/lists/*

# ====================================================================
# 	SETUP ENV
# ====================================================================
ENV ROS1_INSTALL_PATH=/opt/ros/noetic
ENV ROS2_INSTALL_PATH=/opt/ros/rolling

WORKDIR /home/$USERNAME
COPY ./ros_entrypoint.sh ros_entrypoint.sh
RUN sudo chmod +x ros_entrypoint.sh

# Use the entrypoint
ENTRYPOINT ["./ros_entrypoint.sh"]
CMD ["bash"]


