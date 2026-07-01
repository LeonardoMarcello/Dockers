<h1 align="center">
  Docker Images for ATI F/T Sensors
</h1>

The repository reimplement a portable dockerization of the [netft_rdt_drive](https://github.com/epfl-lasa/net-ft-ros) repository to ease its integration in a ROS2 framework.

## Prepare Environment

**1. Connect the Device**
  - Ati Sesor -> NetBox/Trasducer		(NetBox with same mark FT17788)  
  - NetBox/Ethernet -> NetGear/port	(Port 7 or more)  
  - NetGear/port -> PC/Ethernet		(Port 7 or more)  

**2. Connect the PC to the network**  
	- IPv4  
	- Address: 	172.16.0.0  
	- Gateway mask: 	255.255.0.0 (o 24 if using Franka Emika Panda)  

IP Devices List:  
	- Franka Desktop: 172.16.0.3	<- Franka Controller Interface (FCI)  
	- F/T indenter: 172.16.0.13	<- FT Sensor  

Set IP F/T tactip at 172.16.0.14  
Set IP F/T tactip nano at 172.16.0.20	 

## Run

**1. Clone the Repository**

```bash
git clone https://github.com/LeonardoMarcello/ati_ft_docker.git
```

**2. Configure the Device**

To manually configure the device parameters go to [**setup file**](https://github.com/LeonardoMarcello/ati_ft_docker/blob/c0906ef8c5ac9c97ed80aa2d764fab94e091821f/ros2/src/netft_rdt_driver/config/setup.yaml) located at ros2/src/netft_rdt_driver/config/setup.yaml

```bash
./ati-configure.sh
```

**3. Build the image again**

```bash
docker compose build
```
**3. Activate the Device**

```bash
docker compose up ati
```

# Net-FT ros2 (netft_rdt_driver)

ROS2 package for the ATI 6-axis force torque sensor. It extend the ROS1 [net-ft-ros](https://travis-ci.org/epfl-lasa/net-ft-ros) package

## Hardware setup

TODO: description of the ATI setup, with ATI box, how to connect to ethernet and ping the box.

Once you have connected the ATI box with an ethernet and power supply cable, check 
the network connection. From your PC try and ping the FT sensor.
```
$ ping 128.178.145.98
```
If you can ping the FT sensor then you are ready to use it. You can also put the ip into your web-brower 
and (if you could ping it) you should be able to see a webpage which shows the status of the FT. Normaly
the status should be: Healthy.


The force-torque information will be published on the topic: **/ft_sensor/netft_data**.
The message type is **geometry_msgs/WrenchStamped**.
```
ros2 topic echo /ft_sensor/netft_data


header: 
  seq: 9377
  stamp: 
    secs: 1454162697
    nsecs: 667636236
  frame_id: ''
wrench: 
  force: 
    x: -0.248077
    y: -1.12601
    z: -1.639932
  torque: 
    x: -0.106468
    y: -0.108128
    z: 0.22924
```

There are four arguments the node takes, see the  [**launch file**](https://github.com/epfl-lasa/net-ft-ros/blob/master/launch/ft_sensor.launch)  for more details.

* **ROS service**
```
 ros2 service call /ft_sensor/bias_cmd "cmd: 'bias'"
```
