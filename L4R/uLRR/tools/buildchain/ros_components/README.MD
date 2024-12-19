# ROS build script for PC Software
This script helps to copy AOS generated ros_msg files and build a ROS catkin project

## How to use it
This build script has two mandatory arguments:
 - Copy ros_msgs (-p)
 - Clean build (-c)
 - archive to create debian package (-a)

## How to build PC software
1. AOS x86-64 build
    a. Install conan recepy
    - ```./tools/buildchain/aos_components/build_script.sh -i -x <debug|release> -t x86-64```

    b.  Build AOS project
    - ```./tools/buildchain/aos_components/build_script.sh -b -x <debug|release> -t x86-64```

2. Copy ros_msgs and clean build ros workspace and create debian package (always depends on step1)
    - ```./tools/buildchain/ros_components/build_script.sh -c -p -a```


## Overview on build_script.sh
1. By passing -p argument aos x86 built ros_msgs are copied from ```software/aos/build_x86_64/build_x86_64_exe/yaaac_codegen/interfaces/cpp_ros_converter/ros_msgs/``` to ```software/ros/aos/ros_msgs```
2. All the ROS components which needs to be part of PC ROS software build should be kept inside ```software/ros/meas_gui_components.txt```
3. ROS catkin workspace - ```software/ros/```. For incremental build, don not pass -c argument

