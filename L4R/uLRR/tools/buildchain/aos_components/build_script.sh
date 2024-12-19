#!/bin/bash

set -e

#--------------------------------------------------------------------------------------------------------
# Global variables

# Define package details
package_name="ulrr"
package_version="0.0.1"
maintainer="Imaging Radar - C3 Team <your.email@example.com>"
architecture=""
description="Imaging AOS runnables package"

# Build script settings
rootfs_artifact="rootfs_tec0204_bullseye_final_arm64_latest.ext4.gz"
rootfs_repository_path="zugspitze-series-generic-local/releases/debian-base-image/latest/$rootfs_artifact"
fpgagateway_folder="software/aos/business_logic/fpgagateway"

# CMAKE settings
CMAKE_BUILD_TYPE_VALUE=""
CMAKE_TOOLCHAIN_FILE_VALUE=""
CMAKE_INSTALL_PREFIX_VALUE=""
CMAKE_MODULE_PATH_VALUE=""

COMPILER_VERSION_VALUE=""
ENABLE_UNIT_TESTS_VALUE="ON"
CODE_GENERATOR_VALUE="yaaac2"
LOGGING_FRAMEWORK_VALUE="console"
MIDDLEWARE_TARGET_VALUE="carma_0_22"
MTA_VALUE="OFF"
DMC_VALUE="ON"
ROS_VALUE="ON"
ROS_CONVERTER_TOOL_VALUE="v2"
ROS_INITIALIZATION_VALUE="OFF"
TAPE_VALUE="ON"
RECALL="ON"

# Initialize variables:
flag_clean_conan_workspace=false
flag_install_build_env=false
flag_build_aos_pckg=false
flag_middleware_instance=false
flag_run_unit_tests=false
flag_archive_aos_pckg=false
flag_deploy_aos_runnable=false
flag_deploy_mmic_lib=false
flag_deploy_fpga_bit_file=false
flag_suppress_cmake_compiler_warnings=false

#--------------------------------------------------------------------------------------------------------
# Identifying the execution 
running_folder=$PWD
echo "Running script from: $running_folder"

if [[ "$running_folder" == "/__w/1/s" ]]; then
  echo "Running on cloud..."
  project_root_folder=$running_folder/
elif [[ -n $WORKSPACE_FOLDER ]]; then
  echo "Running on devcontainer"
  project_root_folder=$WORKSPACE_FOLDER/
elif git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "Running inside a project repository"
  git_remote_url=$(git config --get remote.origin.url)
  repo_name=$(basename -s .git "$git_remote_url" | sed 's/\.git$//')
  echo "Git repository name: $repo_name"

  project_root_folder=$(git rev-parse --show-toplevel)/
else
  echo "Unknown environment"
  exit 1
fi

echo "Project root folder: $project_root_folder"

if [[ "$running_folder" != "$project_root_folder" ]]; then
  echo "Chaging folder to : $project_root_folder"
  cd $project_root_folder
fi

conan_prj_path=$project_root_folder"software/aos"
aos_version="default"
target_type=""
build_type=""
middleware_instance=""
xml_test_report_path=""
debian_pckg_path=""
rootfs_path=""
rootfs_filename=""
a_core_sw_variant="${A_CORE_SW_VARIANT:-""}"
a_core_version_major="${A_CORE_VERSION_MAJOR:-""}"
a_core_version_minor="${A_CORE_VERSION_MINOR:-""}"
a_core_version_patch="${A_CORE_VERSION_PATCH:-""}"
a_core_commit_hash="${A_CORE_COMMIT_HASH:-""}"

if [[ -n "$a_core_sw_variant" && -n "$a_core_version_major" && -n "$a_core_version_minor" && -n "$a_core_version_patch" && -n "$a_core_commit_hash" ]]; then
  echo -e "\033[0;32mA-Core Version:\033[0m
  \033[0;33mVariant:\033[0m $a_core_sw_variant
  \033[0;33mMajor:\033[0m $a_core_version_major
  \033[0;33mMinor:\033[0m $a_core_version_minor
  \033[0;33mPatch:\033[0m $a_core_version_patch
  \033[0;33mCommit:\033[0m $a_core_commit_hash"
fi

root_path=$PWD
echo $PWD

#--------------------------------------------------------------------------------------------------------
# Getting the current user based on running environment
user=""
if [[ -f "/.dockerenv" ]]; then
  echo "Running in a docker environment..."
  user=$UNAME
else
  echo "Running on host machine..."
  user=$USER
fi
echo "using user=$user"

#--------------------------------------------------------------------------------------------------------
# Functions definitions
# Usage info
show_help() {
cat << EOF
Usage: ${0##*/} [-hcibafmw] [-e MIDDLEWAREINSTANCE][-d DEBIANPCKGPATH] [-r ROOTFSPATH] [-u XMLTESTREPORTPATH] [-x BUILDTYPE] [-t TARGETTYPE] [-s AOSVERSION]
Script to build AOS component with cmake

    -h          display this help and exit
    -c          clean conan workspace
    -i          install conan recepy
    -b          build of AOS project
    -a          archive (generated debian package)
    -f          deploy fpga bit file into the rootfs
    -m          deploy mmic libraries into the rootfs
    -w          suppress the cmake compiler warnings
    
    -e MIDDLEWAREINSTANCE middleware instance (tec0204_linux/te0950_linux/te0950_neutrino/car_pc/testing)
    -d DEBIANPCKGPATH     deploy aos runnable into the rootfs 
    -r ROOTFSPATH         path to rootfs
    -u XMLTESTREPORTPATH  run unit-test
    -x BUILDTYPE          build type (debug/release)
    -t TARGETTYPE         architecture target (x86-64/armv8)
    -s AOSVERSION         AOS middleware version

EOF
}

# Function to find artefacts within Conan cache
find_artefact() {
  local artefact_name="$1"

  if [ "$target_type" == "armv8" ]; then
    target_arch="ARM aarch64"
  elif [ "$target_type" == "x86-64" ]; then
    target_arch="x86-64"
  else
    echo "Unknown target type: '$target_type'."
    exit 1
  fi

  local package_dir="/home/$user/.conan/data/"
  local artefacts=$(find "$package_dir" -name "$artefact_name" -type f)

  # Loop through the found artefacts and check the architecture
  for artefact_path in $artefacts; do
      # Use 'file' command to get architecture information
      local arch_info=$(file "$artefact_path")
      
      # Check if the architecture information contains the target architecture
      if [[ $arch_info == *"$target_arch"* ]]; then
          echo "'$artefact_name' found for architecture '$target_arch' in:"
          echo "$artefact_path"
          return 0  # Return success
      fi
  done

  # If no library was found for the specified architecture
  echo "'$artefact_name' for architecture '$target_arch' not found."
  return 1  # Return failure
}

#--------------------------------------------------------------------------------------------------------
# Parsing user inputs

OPTIND=1
# Resetting OPTIND

while getopts hcibrafmwe:d:r:u:x:t:s: opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        c)  
            echo "Clean of conan workspace was requested"
            flag_clean_conan_workspace=true
            ;;
        i)
            echo "Install of build env. was requested"
            flag_install_build_env=true
            ;;
        b)
            echo "Build of AOS package was requested"
            flag_build_aos_pckg=true
            ;;
        a)
            echo "Archiving of the built AOS package was requested"
            flag_archive_aos_pckg=true
            ;;
        f)
            echo "Deploy fpga bit file into the rootfs"
            flag_deploy_fpga_bit_file=true
            ;;
        m)
            echo "Deploy mmic libraries into the rootfs"
            flag_deploy_mmic_lib=true
            ;;
        w)
            echo "suppress the cmake compiler warnings"
            flag_suppress_cmake_compiler_warnings=true
            ;;
        e)  middleware_instance=$OPTARG
            echo "Middleware instance (tec0204_linux|te0950_linux|te0950_neutrino|car_pc|testing)"
            flag_middleware_instance=true
            ;;
        d)  debian_pckg_path=$OPTARG
            echo "Deploy aos runnable into the rootfs"
            flag_deploy_aos_runnable=true
            ;;
        r)  rootfs_path=$OPTARG
            echo "Specifying rootfs file"
            ;;
        u)  xml_test_report_path=$OPTARG
            echo "Execution of unit-test from built AOS packages was requested"
            flag_run_unit_tests=true
            ;;
        x)  build_type=$OPTARG
            echo "Specifying build type"
            ;;
        t)  target_type=$OPTARG
            echo "Specifying target"
            ;;
        s)  aos_version=$OPTARG
            echo "Specifying AOS version"
            ;;
        *)
            show_help >&2
            exit 1
            ;;
    esac
done
shift "$((OPTIND-1))"   # Discard the options and sentinel --

if { $flag_install_build_env || $flag_build_aos_pckg || $flag_run_unit_tests || $flag_archive_aos_pckg; } && [ "$target_type" != "x86-64" ] && [ "$target_type" != "armv8" ]; then
  echo "Unknown given target type: $target_type"
  exit 1
fi

if { $flag_install_build_env || $flag_build_aos_pckg; } && [ "$build_type" != "debug" ] && [ "$build_type" != "release" ]; then
  echo "Unknown given build type: $build_type"
  exit 1
fi

if [ $flag_archive_aos_pckg == false ] && [ $flag_deploy_aos_runnable == true ] && [ ! -f "$debian_pckg_path" ]; then
  echo "Given DEBIAN package doesn't exists... $debian_pckg_path"
  exit 1
fi

if [ $flag_suppress_cmake_compiler_warnings == true ]; then
  echo "Compiler warnings will be suppressed..."
  CMAKE_SUPPRESS_WARNINGS_VALUE="ON"
else
  CMAKE_SUPPRESS_WARNINGS_VALUE="OFF"
fi

if [ $flag_middleware_instance == true ]; then
  echo "Middleware instance set to: $middleware_instance"
  MIDDLEWARE_INSTANCE_VALUE=$middleware_instance
else
  MIDDLEWARE_INSTANCE_VALUE="tec0204_linux"
fi

if [ $flag_deploy_fpga_bit_file == true ] || [ $flag_deploy_mmic_lib == true ] || [ $flag_deploy_aos_runnable == true ] && [ -z "$rootfs_path" ]; then
  echo "Rootfs file path was not provided... The rootfs file will be downloaded through jfrog REST API"

  rootfs_filename=$(find * -type f -name 'rootfs_*ext4');
  if [ ! -z "$rootfs_filename" ]; then
    echo "$rootfs_filename was found."
    
    rootfs_path=$(readlink -f $rootfs_filename)
  else
    read -s -p "Provide JFrog token: " jfrog_token
    python3 devops/scripts/python/libraries/jfrog/jfrog-download-artifact.py https://artifactory.boschdevcloud.com/artifactory $jfrog_token  $rootfs_repository_path artifacts/ $rootfs_artifact
    if [ $? -eq 0 ]; then
        echo "$rootfs_artifact was download with success."
    else
        echo "Download of $rootfs_artifact failed."
        exit 1
    fi

    rootfs_archive=$(find * -type f -name 'rootfs_*ext4.gz');
    rootfs_archive_filename=$(basename "$rootfs_archive")
    rootfs_filename="${rootfs_archive_filename%.gz}"
    rootfs_archive_path=$(readlink -f $rootfs_archive)

    
    echo "Uncompress rootfs"
    echo "gunzip -k $rootfs_archive_path -c > artifacts/$rootfs_filename"
    if gunzip -k $rootfs_archive_path -c > artifacts/$rootfs_filename; then
      echo "Decompress successful"
    else
      echo "Decompress failed"
      exit 1
    fi

    rootfs_path=$(readlink -f artifacts/$rootfs_filename)
  fi

  echo "rootfs_path: $rootfs_path"
  echo "rootfs_filename: $rootfs_filename"
fi

# Update CMAKE settings based on the target type
IFS='_' read -ra file_name_array <<< "$middleware_instance"
os_type="${file_name_array[1]}"
source tools/buildchain/aos_components/settings/${os_type}_${target_type}.sh

if $flag_clean_conan_workspace; then
  echo "Flag -flag_clean_conan_workspace is set"

  # Clean Conan cache
  echo "Cleaning Conan cache..."
  cd $conan_prj_path
  conan remove "*" -f
  echo "Conan cache cleaned."

fi

if $flag_install_build_env; then
  echo "Flag -flag_install_build_env is set"

  cd $conan_prj_path

  conan_options=""
  if [ $aos_version != "default" ]; then
      conan_options+="-o AOS_VERSION=$aos_version "
  fi
  conan_options+="-o MIDDLEWARE_INSTANCE=$middleware_instance "

  # Install Conan dependencies to build folder
  echo "Installing Conan dependencies to build folder..."
  if [ "$target_type" == "x86-64" ]; then
    rm -rf build_x86_64 && mkdir build_x86_64 && cd build_x86_64 && mkdir build_x86_64_exe && cd ..
    conan install ./ -if=./build_x86_64 -pr:h=${conan_host_profile} -pr:b=${conan_build_profile} --update $conan_options 
  fi

  if [ "$target_type" == "armv8" ]; then
    rm -rf build_armv8 && mkdir build_armv8 && cd build_armv8 && mkdir build_armv8_exe && cd ..
    conan install ./ -if=./build_armv8 -pr:h=${conan_host_profile} -pr:b=${conan_build_profile} --update $conan_options
  fi

  echo "Conan dependencies installed."
fi

if $flag_build_aos_pckg; then
  echo "Flag -flag_build_aos_pckg is set"


  source /opt/ros/noetic/setup.bash

  if [ "$target_type" == "x86-64" ]; then
    cd $conan_prj_path/build_x86_64
    source activate.sh
    cd build_x86_64_exe

    PYTHON_EXECUTABLE="/usr/bin/python3.9"
    if [ -L /usr/include/python3.9 ]; then
      sudo rm /usr/include/python3.9
    fi 
  fi

  if [ "$target_type" == "armv8" ]; then
    cd $conan_prj_path/build_armv8
    source activate.sh
    cd build_armv8_exe
    
    #mmic settings intended for only armv8 target
    PYTHON_INCLUDE_DIR="/opt/bosch/ulrr/cross-compilation/python/include"
    PYTHON_LIBRARY="/opt/bosch/ulrr/cross-compilation/python/lib/libpython3.9.so"
    PYTHON_EXECUTABLE="/usr/bin/python3.9"
    #aligning python headers for mmic
    if [ -L /usr/include/python3.9/include ]; then
      echo "Link already exists"
    else
      sudo ln -s /opt/bosch/ulrr/cross-compilation/python/include/ /usr/include/python3.9
    fi
  fi

  ENABLE_CLANG_TIDY_CHECKS=""
  if [ $os_type == "linux" ]; then
    os_type="Linux"
    ENABLE_CLANG_TIDY_CHECKS="${ENABLE_CLANG_TIDY_CHECKS:-ON}"
  fi
  if [ $os_type == "neutrino" ]; then
    os_type="Neutrino"
    ENABLE_CLANG_TIDY_CHECKS="${ENABLE_CLANG_TIDY_CHECKS:-OFF}"
  fi

  # echo "Running ros_gateway_generator..."
  # ros_gateway_generator -g ../../gateway_configuration/RosStatePublisher.out_ros_gateway.yaml -o ../../generated_artifacts -I ../../ros_messages/src/ros_gateway && sed -i '1s/^/#include <ros\/duration.h> /' ../../generated_artifacts/interfaces/include/ros_example/custom_type/BoschHeader.hpp
  echo "CMAKE_PREFIX_PATH=$CMAKE_PREFIX_PATH"
  echo "CMAKE_TOOLCHAIN_FILE_VALUE=$CMAKE_TOOLCHAIN_FILE_VALUE"
  echo "CMAKE_INSTALL_PREFIX_VALUE=$CMAKE_INSTALL_PREFIX_VALUE"
  echo "CMAKE_MODULE_PATH_VALUE=$CMAKE_MODULE_PATH_VALUE"

  echo "Running cmake..."
  cmake -G "Unix Makefiles" \
    -DMIDDLEWARE_INSTANCE=$MIDDLEWARE_INSTANCE_VALUE \
    -DMIDDLEWARE_OS_TYPE=$os_type \
    -Dtarget_type=$target_type \
    -DCMAKE_SUPPRESS_WARNINGS=$CMAKE_SUPPRESS_WARNINGS_VALUE \
    -DBUILD_AOS="ON" \
    -DYAAA_VIS_STRICT_MODE="OFF" \
    -DCMAKE_BUILD_TYPE=$CMAKE_BUILD_TYPE_VALUE \
    -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE_VALUE \
    -DCONAN_IN_LOCAL_CACHE="ON" \
    -DCONAN_COMPILER="gcc" \
    -DCONAN_COMPILER_VERSION=$COMPILER_VERSION_VALUE \
    -DCONAN_CXX_FLAGS="-m64" \
    -DCONAN_SHARED_LINKER_FLAGS="-m64" \
    -DCONAN_C_FLAGS="-m64" \
    -DCONAN_LIBCXX="libstdc++11" \
    -DCMAKE_INSTALL_PREFIX=$CMAKE_INSTALL_PREFIX_VALUE \
    -DCMAKE_INSTALL_BINDIR="bin" \
    -DCMAKE_INSTALL_SBINDIR="bin" \
    -DCMAKE_INSTALL_LIBEXECDIR="bin" \
    -DCMAKE_INSTALL_LIBDIR="lib" \
    -DCMAKE_INSTALL_INCLUDEDIR="include" \
    -DCMAKE_INSTALL_OLDINCLUDEDIR="include" \
    -DCMAKE_INSTALL_DATAROOTDIR="share" \
    -DCMAKE_MODULE_PATH=$CMAKE_MODULE_PATH_VALUE \
    -DCMAKE_EXPORT_NO_PACKAGE_REGISTRY="ON" \
    -DCONAN_EXPORTED="1" \
    -DBOSCH_ULRR_ENABLE_UNIT_TESTS=$ENABLE_UNIT_TESTS_VALUE \
    -DCODE_GENERATOR=$CODE_GENERATOR_VALUE \
    -DLOGGING_FRAMEWORK=${LOGGING_FRAMEWORK_VALUE} \
    -DMIDDLEWARE_TARGET=$MIDDLEWARE_TARGET_VALUE \
    -DMTA=$MTA_VALUE \
    -DDMC=$DMC_VALUE \
    -DROS=$ROS_VALUE \
    -DROS_CONVERTER_TOOL=$ROS_CONVERTER_TOOL_VALUE \
    -DROS_INITIALIZATION=$ROS_INITIALIZATION_VALUE \
    -DTAPE=$TAPE_VALUE \
    -DPYTHON_INCLUDE_DIR=$PYTHON_INCLUDE_DIR \
    -DPYTHON_LIBRARY=$PYTHON_LIBRARY \
    -DPYTHON_EXECUTABLE:FILEPATH=$PYTHON_EXECUTABLE \
    -DRECALL="$RECALL" \
    -DBL_ENABLE_CLANG_TIDY_CHECKS="$ENABLE_CLANG_TIDY_CHECKS" \
    -DA_CORE_SW_VARIANT:STRING=$a_core_sw_variant \
    -DA_CORE_VERSION_MAJOR:STRING=$a_core_version_major \
    -DA_CORE_VERSION_MINOR:STRING=$a_core_version_minor \
    -DA_CORE_VERSION_PATCH:STRING=$a_core_version_patch \
    -DA_CORE_COMMIT_HASH:STRING=$a_core_commit_hash \
    -Wno-dev ../..
  
  script -q -c "cmake --build . -- -j8" build.log

  if grep -q "make: \*\*\* \[.*\] Error [1-9]" build.log; then
      echo "CMake build failed, 'Error' found"
      exit 1
  else
      echo "CMake build succeeded"
  fi
  
  cd ..
  source deactivate.sh

fi

if $flag_run_unit_tests; then
  echo "Flag -flag_run_unit_tests is set"

  if [ "$target_type" == "x86-64" ]; then
    cd $conan_prj_path/build_x86_64/
    source activate.sh
    source activate_run.sh
    cd build_x86_64_exe/bin

    if [ ! -d "$xml_test_report_path" ]; then
      mkdir "$xml_test_report_path"
      echo "Folder $xml_test_report_path created!"
    else
      echo "Folder $xml_test_report_path already exists."
    fi

    # Find and execute the unit test executables
    find . \
      -type f \
      \( -name "*_test*" -a -executable \) \
      -not -name "*esme*" \
      -exec {} --gtest_output="xml:$xml_test_report_path" \;

    echo "Test results written to: $xml_test_report_path"
  fi

  if [ "$target_type" == "armv8" ]; then
    echo "python3 devops/scripts/python/qemu/qemu_fusion.py run-unit-test --test-report-path $xml_test_report_path --rootfs-filepath $rootfs_path"
    python3 devops/scripts/python/qemu/qemu_fusion.py run-unit-test --test-report-path $xml_test_report_path --rootfs-filepath $rootfs_path
  fi
fi

if $flag_archive_aos_pckg; then
  echo "Flag -flag_archive_aos_pckg is set"

  cd $conan_prj_path

  conan_info_file=""
  if [ "$target_type" == "x86-64" ]; then
    build_folder="build_x86_64/build_x86_64_exe"
    conan_info_file="build_x86_64/conaninfo.txt"
  fi

  if [ "$target_type" == "armv8" ]; then
    build_folder="build_armv8/build_armv8_exe"
    conan_info_file="build_armv8/conaninfo.txt"
  fi

  build_type=$(awk -F= '/^    build_type/ {gsub(/[[:space:]]/, "", $2); print $2; exit}' "${conan_info_file}")
  middleware_instance=$(awk -F= '/^    MIDDLEWARE_INSTANCE/ {gsub(/[[:space:]]/, "", $2); print $2; exit}' "${conan_info_file}")

  echo "Archiving for $target_type, $build_type, $middleware_instance"

  deb_package_name=$package_name-${package_version//./-}-ubuntu2004-$target_type-gcc$COMPILER_VERSION_VALUE-${build_type,}
  echo "Creating deb. packg with the following name: $deb_package_name"
  
  ######################################################################################################################################
  ## Grabbing AOS application

  pkg_base_folder="$deb_package_name/opt/ulrr/usr/$build_folder"
  if [ "$target_type" == "armv8" ]; then
      folder_names=("bin" \
                    "lib" \
                    "lib_static" \
                    "yaaac_codegen/deploy/carma_0_22/${middleware_instance}/esme" \
                    "yaaac_codegen/deploy/carma_0_22/${middleware_instance}/manifests" \
                    "yaaac_codegen/deploy/carma_0_22/${middleware_instance}/start_scripts" \
                    "yaaac_codegen/deploy/carma_0_22/${middleware_instance}/stop_scripts" \
                    "sw_versions" )
  fi 

  if [ "$target_type" == "x86-64" ]; then
      folder_names=("bin" \
                    "lib" \
                    "lib_static" \
                    "yaaac_codegen/deploy/carma_0_22/car_pc/esme" \
                    "yaaac_codegen/deploy/carma_0_22/car_pc/manifests" \
                    "yaaac_codegen/deploy/carma_0_22/car_pc/start_scripts" \
                    "yaaac_codegen/deploy/carma_0_22/car_pc/stop_scripts" )
  fi 

  # Iterate through folder_names and create the same 
  for folder_name in "${folder_names[@]}"; do
      folder_path="$pkg_base_folder/$folder_name"
      
      # Create the folder if it doesn't exist
      mkdir -p "$folder_path"

      # Copy the artifacts
      cp -r $build_folder/$folder_name/* $folder_path
  done

  mkdir -p "$pkg_base_folder/scripts"
  if [ "$target_type" == "armv8" ]; then
      cp -r ../ros/scripts/* $pkg_base_folder/scripts
  fi 

  ######################################################################################################################################
  ## Grabbing AOS libraries

  shared_library_names=("libros1cpp_runtime.so" "libaos_xmlrpcpp.so")

  # Iterate through library_names and copy the same
  for library_name in "${shared_library_names[@]}"; do
      artefact_path=""
      find_artefact $library_name
      library_path=$artefact_path

      if [ -n "$library_path" ]; then
        folder_path="$pkg_base_folder/AOS/lib/"

        # Create the folder if it doesn't exist
        mkdir -p "$folder_path"

        cp $library_path $folder_path
      else
        echo "Missing shared library: $library_path"
        exit 1
      fi
  done

  ######################################################################################################################################
  ## Grabbing AOS tools

  aos_tools_names=("esme")

  for tool_name in "${aos_tools_names[@]}"; do
      artefact_path=""
      find_artefact $tool_name
      tool_path=$artefact_path

      if [ -n "$tool_path" ]; then
        folder_path="$pkg_base_folder/AOS/tools/"

        # Create the folder if it doesn't exist
        mkdir -p "$folder_path"

        cp $tool_path $folder_path
      else
        echo "Missing tool: $tool_path"
        exit 1
      fi
  done

  cat > $pkg_base_folder/AOS/update_paths.sh << EOF
#!/bin/bash
aos_libs_path="/opt/ulrr/usr/${build_folder}/AOS/lib"
aos_tools_path="/opt/ulrr/usr/${build_folder}/AOS/tools"

if [ -z "\$LD_LIBRARY_PATH" ]; then
    export LD_LIBRARY_PATH="\$aos_libs_path"
else
    export LD_LIBRARY_PATH="\$aos_libs_path:\$LD_LIBRARY_PATH"
fi

if [ -z "\$PATH" ]; then
    export PATH="\$aos_tools_path"
else
    export PATH="\$aos_tools_path:\$PATH"
fi

echo "LD_LIBRARY_PATH updated. New value: \$LD_LIBRARY_PATH"
echo "PATH updated. New value: \$PATH"
EOF
  sudo chmod +x $pkg_base_folder/AOS/update_paths.sh

  cat > $pkg_base_folder/scripts/ir2_start_with_esme_example.sh << EOF
#!/bin/bash

export ROS_IP=192.168.2.16
export ROS_MASTER_URI=http://192.168.2.1:11311

export PYTHONPATH=\$PYTHONPATH:/usr/lib/python3.9/dist-packages/bsp_linux
export PYTHONPATH=\$PYTHONPATH:/usr/lib/python3.9/dist-packages/device_library

mount -o remount,size=2G /dev/shm

echo "Update LD_LIBRARY_PATH and PATH, to find AOS artefacts"
. /opt/ulrr/usr/$build_folder/AOS/update_paths.sh

# Execute the specified script
echo "Executing esme from 'root folder'"
cd /opt/ulrr/usr/$build_folder
esme yaaac_codegen/deploy/carma_0_22/$middleware_instance/esme/esme_manifest_sensor.json -1

EOF
  sudo chmod +x $pkg_base_folder/scripts/ir2_start_with_esme_example.sh

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

if $flag_deploy_fpga_bit_file; then
  echo "Flag -flag_deploy_fpga_bit_file is set"

  echo "Build fpgautil binary"
  cd $root_path/tools/buildchain/fpgautil/
  mkdir -p build/ && cd build/
  cmake -DCMAKE_TOOLCHAIN_FILE=/opt/bosch/ulrr/toolchains-cmake/toolchainfile-linux-aarch64-a52.cmake -S ../
  cmake --build . '--' '-j8'
  cd $root_path

  echo "Extract fpga file"
  unzip -o $root_path/software/os/debian/hw/tec0204/radl4_tec0204.xsa -d "$root_path/software/os/debian/hw/tec0204/"

  echo "Run qemu fusion"
  # Installing fpgautil
  echo "python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $root_path/tools/buildchain/fpgautil/build/fpgautil --destination-path /usr/bin/ --rootfs-filepath $rootfs_path"
  python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $root_path/tools/buildchain/fpgautil/build/fpgautil --destination-path /usr/bin/ --rootfs-filepath $rootfs_path

  # Installing radl4_top.bit
  echo "python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $root_path/software/business_logic/hrf_lal/uLRR_hrf_lal/bitfiles/rad0/radl4_top.bit --destination-path /opt/ulrr/scripts/ --rootfs-filepath $rootfs_path"
  python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $root_path/software/business_logic/hrf_lal/uLRR_hrf_lal/bitfiles/rad0/radl4_top.bit --destination-path /opt/ulrr/scripts/ --rootfs-filepath $rootfs_path
fi

if $flag_deploy_mmic_lib; then
  echo "Flag -flag_deploy_mmic_lib is set"
  cd $root_path

  echo "Run qemu fusion"
  echo "python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $root_path/dist-packages/ --destination-path /usr/lib/python3.9/ --rootfs-filepath $rootfs_path"
  python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $root_path/dist-packages/ --destination-path /usr/lib/python3.9/ --rootfs-filepath $rootfs_path

  echo "python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $root_path/aarch64-linux-gnu/ --destination-path /usr/lib/ --rootfs-filepath $rootfs_path"
  python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $root_path/aarch64-linux-gnu/ --destination-path /usr/lib/ --rootfs-filepath $rootfs_path
fi

if $flag_deploy_aos_runnable; then
  echo "Flag -flag_deploy_aos_runnable is set"
  
  cd $root_path
  echo "Run qemu fusion"
  echo "python3 devops/scripts/python/qemu/qemu_fusion.py install-deb --deb-package $debian_pckg_path --rootfs-filepath $rootfs_path"
  python3 devops/scripts/python/qemu/qemu_fusion.py install-deb --deb-package $debian_pckg_path --rootfs-filepath $rootfs_path
  
fi
