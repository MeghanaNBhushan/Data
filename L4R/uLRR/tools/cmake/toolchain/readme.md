# toolchainfile-petalinux-aarch-a52.cmake
Using ```petalinux-build -c myapp && petalinux-build -x package``` to compile an app is a time consuming task that might last hours. In addition, tool integration (e.g. Visual Studio Code) is poor for PetaLinux and by far better for CMake. Therefore, it makes sense to build apps and libraries using a CMake build system. 

## Precondition - the build environment
### Docker
@todo: Create a docker container that includes all mandatory tools.

## PetaLinux SDK
In order to crosscompile with CMake, the rootfs of the target is mandatory in addition to the cross compiler. Both artifacts can be created using the PetaLinux tool chain. They are called "PetaLinux SDK" in the documentation. Within the working folder of your PetaLinux project, run the following commands:
```
# Create the SDK
petalinux-build --sdk
# Install it in /opt/petalinux/sdk-v2021.2/. The directory has to exist and has to be writeable for installation
petalinux-package --sysroot --dir /opt/petalinux/sdk-v2021.2/
```

## Example
You can try the example on the evaluation board:
On the PC, run
```
mkdir -p example/build
cd example/build
cmake .. -DCMAKE_TOOLCHAIN_FILE=../../toolchainfile-petalinux-aarch64-a52.cmake -G Ninja
ninja package
scp crosscompilation_example-0.0.1-1.aarch64.rpm root@192.168.0.2:
```

Install the rpm file on the target (ensure that both dnf and rpm are available on the target):
```
rpm -i myproject.rpm
```

## Building a ros node using cross compilation (DRAFT)
A ROS node can be built using the petalinux SDK. It generates a cross compiler and a rootfs.
In contrast to the description in the [ROS documentation](http://wiki.ros.org/ROS/CrossCompiling), cross compilation using catkin_build is tricky. The root cause seems to be the use of "old" CMake style in the generated CMake system. That results in linking x86 and aarch64 libraries if no measures are implemented.
Please find an instruction for cross compilation, below:

* Install a PetaLinux SDK that includes all mandatory libraries
* Copy the toolchain to ```${SDK}/sysroots/cortexa72-cortexa53-xilinx-linux/opt/ros/noetic/share/ros/rostoolchain.cmake```
* Create a build directory: ```mkdir -p <your catking WS>/build && cd <your catking WS>/build```
* Build the binary:
~~~
source ${SDK}/environment-setup-cortexa72-cortexa53-xilinx-linux 

source ${SDK}/sysroots/cortexa72-cortexa53-xilinx-linux/opt/ros/noetic/setup.sh 

cmake -DPYTHON_EXECUTABLE='/usr/bin/python3' -DCMAKE_TOOLCHAIN_FILE=${SDK}/sysroots/cortexa72-cortexa53-xilinx-linux/opt/ros/noetic/share/ros/rostoolchain.cmake ../src/

make -j
~~~

This approach has been tested in the scope of ATR-15449/ATR-15450.