#!/bin/bash
cd ../../../software/aos/build_armv8/

tar -cf build_armv8_exe.tar build_armv8_exe
 
echo Please provide the sensor name that corresponds to the configuration specified in '.ssh/config', which you wants to test. 

read -p "Please enter target name:" target_name
  
scp -r ../../../software/aos/build_armv8/build_armv8_exe.tar $target_name:

ssh $target_name 'tar -xf build_armv8_exe.tar; export ROS_IP=192.168.2.16 && export ROS_MASTER_URI=http://192.168.2.1:11311  && export PYTHONPATH=$PYTHONPATH:/usr/lib/python3.9/dist-packages/bsp_linux && export PYTHONPATH=$PYTHONPATH:/usr/lib/python3.9/dist-packages/device_library; mount -o remount,size=2G /dev/shm; cd build_armv8_exe; sh yaaac_codegen/deploy/carma_0_22/sensor/start_scripts/start_sensor.sh'





