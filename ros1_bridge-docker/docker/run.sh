#!/bin/bash

# ------------------------------------------------------------
#	DEFINE PARAMS
# ------------------------------------------------------------
# Select docker image
DOCKER_IMAGE=rosbridge
# Select user
DOCKER_USER=rosbridge


# ------------------------------------------------------------
#	RUN CONTAINER
# ------------------------------------------------------------
# uncomment to grant permission to access server X to all user
# disable access control
xhost +

#run container
docker run \
	-it \
	--rm \
	--name ${DOCKER_USER} \
	--privileged --network=host --ipc=host \
	-v /tmp/.X11-unix:/tmp/.X11-unix:rw --env DISPLAY=$DISPLAY \
	-v /home/$USER/.config/terminator:/home/${DOCKER_USER}/.config/terminator --env NO_AT_BRIDGE=1 \
	-v ~/.bash_history:/home/${DOCKER_USER}/.bash_history \
	${DOCKER_IMAGE} 
	
# uncomment to remove permissions to acces server X to all users
# enable access control
xhost -
