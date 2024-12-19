# CMakeLists - 1 RPM package "generator"
This CMakeLists enables the packaging of the all available applications into a single rpm package.

## Precondition - the build environment
### Packages setup
All packages has their own CMakeLists files and can be built in independent way.

## PetaLinux SDK
SDK is installed and sourced (requirement automatically fullfilled, if application's Docker env. is used)

## Usage example
Considering application's Docker env. is in use
```
cp [ad-radar-sensor root]/tools/cmake/toolchain/toolchainfile-petalinux-aarch64-a52.cmake [sdk installation folder]/sysroots/cortexa72-cortexa53-xilinx-linux/opt/ros/noetic/share/ros
source [sdk installation folder]/environment-setup-cortexa72-cortexa53-xilinx-linux
source [sdk installation folder]/sysroots/cortexa72-cortexa53-xilinx-linux/opt/ros/noetic/setup.sh
mkdir -p [ad-radar-sensor root]/tools/buildchain/outputbuild
cd [ad-radar-sensor root]/tools/buildchain/outputbuild
cmake -DPYTHON_EXECUTABLE='/usr/bin/python3' -DCMAKE_TOOLCHAIN_FILE=[sdk installation folder]/sysroots/cortexa72-cortexa53-xilinx-linux/opt/ros/noetic/share/ros/toolchainfile-petalinux-aarch64-a52.cmake [ad-radar-sensor root]/tools/buildchain/ -G Ninja
ninja package
```

Install the rpm file on the target (ensure that both dnf and rpm are available on the target):
```
rpm -i ad_radar_sensor_app--1.aarch64.rpm
```

Checking the installed files
rpm -ql ad_radar_sensor_app

Checking rpm package info
rpm -qi ad_radar_sensor_app