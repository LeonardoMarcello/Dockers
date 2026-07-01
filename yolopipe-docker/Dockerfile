ARG ROS_DISTRO=humble
FROM ros:${ROS_DISTRO}-ros-core AS deps

# ====================================================================
# 	SETUP USER
# ====================================================================
# Add "yolopipe" user with same UID and GID as your host system 
# (copied from https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user)
ARG USERNAME=yolopipe
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
	&& useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
	&& apt-get update \
	&& apt-get install -y sudo \
	&& echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
	&& chmod 0440 /etc/sudoers.d/$USERNAME

# Add user to video group to allow acces to webcam
RUN sudo usermod --append --groups video $USERNAME

# Update all packages
RUN sudo apt update && sudo apt upgrade -y

# Install terminator
RUN sudo DEBIAN_FRONTEND=noninteractive apt-get install terminator -y



# ====================================================================
# 	INSTALL DEPENDENCIES
# ====================================================================
# Install system dependencies early for better caching
RUN apt update && apt install -y --no-install-recommends \
    git \
    nano \
    build-essential \
    python3-pip \
    python3-rosdep \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

# ====================================================================
# 	INSTALL YOLO and MediaPipe DEPENDENCIES
# ====================================================================
# Create ros2_ws and copy files with proper ownership
WORKDIR /home/${USERNAME}/ros2_ws
COPY --chown=${USERNAME}:${USERNAME} ./ros2 /home/${USERNAME}/ros2_ws/src


# Copy only package files to resolve dependencies
#WORKDIR /${USERNAME}/ros2_ws
#COPY --chown=${USERNAME}:${USERNAME} ./ros2/mediapipe_ros/package.xml src/mediapipe_ros/package.xml
#COPY --chown=${USERNAME}:${USERNAME} ./ros2/yolo_ros/package.xml src/yolo_ros/package.xml
#COPY --chown=${USERNAME}:${USERNAME} ./ros2/yolo_msgs/package.xml src/yolo_msgs/package.xml
#COPY --chown=${USERNAME}:${USERNAME} ./ros2/requirements.txt src/requirements.txt


# Install ROS dependencies
RUN rosdep init && rosdep update --include-eol-distros
RUN apt update && rosdep install --from-paths src --ignore-src -r -y && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN if [ "$(lsb_release -rs | cut -d. -f1)" -ge 24 ]; then \
    pip3 install -r src/requirements.txt --break-system-packages --ignore-installed --no-cache-dir; \
    else \
    pip3 install -r src/requirements.txt --no-cache-dir; \
    fi

# Ensure config directory exists and assign user ownership
RUN mkdir -p /home/${USERNAME}/.config/Ultralytics && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}

# Copy the rest of the workspace files
#COPY --chown=${USERNAME}:${USERNAME} ./ros2 /${USERNAME}/ros2_ws

FROM deps AS builder

SHELL ["/bin/bash", "-c"]

# switch to non-root user for build
USER ${USERNAME}
WORKDIR /home/${USERNAME}/ros2_ws
ENV USER=${USERNAME}

# Build the workspace
RUN source /opt/ros/${ROS_DISTRO}/setup.bash && colcon build --symlink-install

# Source the ROS 2 setup file
RUN echo "source /home/${USERNAME}/ros2_ws/install/setup.bash" >> /home/${USERNAME}/.bashrc

# Set the entrypoint using the variable
COPY entrypoint.sh /home/${USERNAME}/entrypoint.sh
RUN sudo chmod +x /home/${USERNAME}/entrypoint.sh
ENTRYPOINT ["/bin/bash", "-c", "/home/${USER}/entrypoint.sh \"$@\"", "--"]
CMD ["bash"]