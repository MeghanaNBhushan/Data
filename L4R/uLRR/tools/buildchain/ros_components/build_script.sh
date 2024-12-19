#!/bin/bash

# Define package details
package_name="ulrr-ros"
package_version="0.0.1"
maintainer="Imaging Radar - C3 Team <your.email@example.com>"
architecture="amd64"
description="Imaging ROS package"

#user options
usage() {
  echo "Usage: $0 [-cpa]"
  echo "Options:"
  echo "  -c : Clean build (remove build and devel directories)"
  echo "  -p : Copy aos-ros_msgs"
  echo "  -a : archive ros into debian package"
  exit 1
}

#initialise variables
flag_clean_build=false
flag_copy_ros_msgs=false
flag_archive_ros_pckg=false

while getopts ":cpa" opt; do
  case $opt in
    c)
      flag_clean_build=true
      ;;
    p)
      flag_copy_ros_msgs=true
      ;;
    a)
      flag_archive_ros_pckg=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG"
      usage
      ;;
  esac
done


# Get the project and script paths
script_dir="$(dirname "$(readlink -f "$0")")"
project_root="$script_dir/../../.."
aos_ros_msgs_dir="$project_root/build/aos_linux_x86-64_debug/yaaac_codegen/interfaces/cpp_ros_converter/ros_msgs/"
ros_dir="$project_root/software/ros"

if [ "$flag_copy_ros_msgs" = true ]; then
  echo $flag_copy_ros_msgs is set
  mkdir -p "$ros_dir/aos_gen/ros_msgs"
  if ! cp -r "$aos_ros_msgs_dir" "$ros_dir/aos_gen/ros_msgs"; then
    echo "Error: Failed to copy aos ros_msgs to ros workspace."
    exit 1
  fi
else
  echo "not copied latest aos ros_msgs to ros workspace"
fi

echo "--------------------------------------------------------------------"
echo "---------------------ROS PC Software build--------------------------"
echo "--------------------------------------------------------------------"
# Specify the catkin build component list file
component_list_file="$ros_dir/meas_gui_components.txt"
# Check if the component list file exists
if [ ! -f "$component_list_file" ]; then
  echo "Error: $component_list_file not found."
  exit 1
fi

# Read component names
read -a components < "$component_list_file"
# Check if the component list is empty
if [ ${#components[@]} -eq 0 ]; then
  echo "Error: $component_list_file is empty."
  exit 1
fi

source /opt/ros/noetic/setup.bash
#Specify catkin workspace for ros pc sw
catkin_workspace="$ros_dir"
cd $catkin_workspace


# ROS PC Software build command
build_command=""
build_status=0
if [ "$flag_clean_build" = true ]; then
  catkin clean -y
  catkin config --install
  build_command+="catkin build ${components[@]}"
else
  build_command+="catkin build ${components[@]}"
fi

######  temporary python version adaptions start
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo update-alternatives --set python3 /usr/bin/python3.8
######  temporary python version adaptions end


# Execute the build command and capture return code
echo "Running build command: $build_command"
$build_command || build_status=$?

######  temporary python version adaptions start
sudo update-alternatives --set python3 /usr/bin/python3.9 
######  temporary python version adaptions end

# Check the build status
if [ "$build_status" -ne 0 ]; then
  echo "Error: Failed to execute the build command."
  exit 1
fi

if $flag_archive_ros_pckg; then
  echo "Flag -flag_archive_ros_pckg is set"

  cd $catkin_workspace

  echo "Archiving ROS PC Software "

  deb_package_name=$package_name-${package_version//./-}-ubuntu2004
  echo "Creating deb. packg with the following name: $deb_package_name"

  mkdir -p $deb_package_name/opt/ulrr/usr/ros
  
  cp -r install launch $deb_package_name/opt/ulrr/usr/ros/
  
  # Create control script
  mkdir -p $deb_package_name/DEBIAN

  cat > $deb_package_name/DEBIAN/control <<EOF
Package: ${package_name}-aos-runnable
Version: $package_version
Architecture: $architecture
Maintainer: $maintainer
Description: $description
EOF

  dpkg-deb --build --root-owner-group $deb_package_name

fi

