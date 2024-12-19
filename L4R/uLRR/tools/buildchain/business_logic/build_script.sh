#!/bin/bash
set -e

#--------------------------------------------------------------------------------------------------------
# Global variables

# Define package details
package_name="ulrr-business-logic"
package_version="0.0.1"
maintainer="Imaging Radar - C3 Team <your.email@example.com>"
architecture=""
description="Imaging business logic package"

# Build script settings
rootfs_artifact="rootfs_tec0204_bullseye_final_arm64_latest.ext4.gz"
rootfs_repository_path="zugspitze-series-generic-local/releases/debian-base-image/latest/$rootfs_artifact"

# CMAKE fixed settings
CMAKE_TOOLCHAIN_FILE_VALUE=""
CMAKE_INSTALL_PREFIX_VALUE=""
CMAKE_MODULE_PATH_VALUE=""

ENABLE_UNIT_TESTS_VALUE="ON"
BL_ULRR_INDEPENDENT_BUILD_VALUE="ON"

# Initialize variables:
flag_clean=false
flag_build=false
flag_package=false
flag_run_unit_tests=false

rootfs_filename=""
rootfs_path=""

running_folder=$PWD
echo "Running folder: $running_folder"
if [[ "$running_folder" == "/__w/1/s" ]]; then
  echo "Running on cloud..."
  project_root_folder=$running_folder/
elif [[ -n $WORKSPACE_FOLDER ]]; then
  echo "Running on devcontainer"
  project_root_folder=$WORKSPACE_FOLDER/
else
  echo "Unknown environment"
  exit 1
fi

echo "Project root folder: $project_root_folder"

bl_folder=${project_root_folder}software/business_logic
echo "Business logic implementation folder: $bl_folder"

bl_build_folder=${project_root_folder}tools/buildchain/business_logic
echo "Business logic build tool folder: $bl_build_folder"

if [[ "$running_folder" != "$project_root_folder" ]]; then
  echo "Chaging folder to : $project_root_folder"
  cd $project_root_folder
fi

#--------------------------------------------------------------------------------------------------------
# Functions definitions
# Usage info
show_help() {
cat << EOF
Usage: ${0##*/} [-hcba] [-x BUILDTYPE] [-t TARGETTYPE]
Script to build AOS component with cmake

    -h          display this help and exit
    -c          clean
    -b          build business logic
    -a          archive
    
    -x BUILDTYPE          build type (debug/release)
    -t TARGETTYPE         architecture target (x86-64/armv8)
    -u XMLTESTREPORTPATH  run unit-test
    -o ROOTFSPATH         path to rootfs

EOF
}

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
# Parsing user inputs

OPTIND=1
# Resetting OPTIND

while getopts hcbax:t:u: opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        c)  
            echo "Clean"
            flag_clean=true
            ;;
        b)
            echo "Build of business logic"
            flag_build=true
            ;;
        a)
            echo "Archiving built business logic"
            flag_package=true
            ;;
        x)  build_type=$OPTARG
            echo "Specifying build type: $build_type"
            ;;
        t)  target_type=$OPTARG
            echo "Specifying target: $target_type"
            ;;
        o)  rootfs_path=$OPTARG
            echo "Specifying rootfs file"
            ;;
        u)  xml_test_report_path=$OPTARG
            echo "Execution of unit-test from built AOS packages was requested"
            flag_run_unit_tests=true
            ;;
        *)
            show_help >&2
            exit 1
            ;;
    esac
done
shift "$((OPTIND-1))"   # Discard the options and sentinel --

if [ "$target_type" == "x86-64" ]; then 
  CMAKE_MODULE_PATH_VALUE="$bl_build_folder/build_x86_64"
elif [ "$target_type" == "armv8" ]; then
  CMAKE_MODULE_PATH_VALUE="$bl_build_folder/build_armv8"
else
  echo "Unknown given target type: $target_type"
  exit 1
fi

if $flag_clean; then
  echo "Flag -flag_clean is set"

  rm -rf $CMAKE_MODULE_PATH_VALUE
  exit 0
fi

if [ "$build_type" != "debug" ] && [ "$build_type" != "release" ]; then
  echo "Unknown given build type: $build_type"
  exit 1
fi

#Update specific settings - x86-64
if [ "$target_type" == "x86-64" ]; then
  # Define package details
  architecture="amd64"
  
  # Update CMAKE settings
  if [ "$build_type" == "debug" ]; then
    CMAKE_TOOLCHAIN_FILE_VALUE="/home/$user/.conan/data/x86_64_linux_gcc8/0.12.0/aos/dev/package/8801d677d2372957a75ead7d94702a021050cadf/cmake/x86_64_linux_gcc8.cmake"
    COMPILER_VERSION_VALUE="8"
  else
    echo "Build for x86-64, release not available in AOS"
    exit 1
  fi
  CMAKE_INSTALL_PREFIX_VALUE="$bl_build_folder/build_x86_64/build_x86_64_exe/package"
fi

#Update specific settings - armv8
if [ "$target_type" == "armv8" ]; then
  # Define package details
  architecture="arm64"
  
  # Update CMAKE settings
  if [ "$build_type" == "debug" ]; then
    CMAKE_TOOLCHAIN_FILE_VALUE="/home/$user/.conan/data/armv8_linux_gcc8/0.12.0/aos/dev/package/0b9087fa2e697f5753918ed600436dc0f93f8994/cmake/armv8_linux_gcc8.cmake"
    COMPILER_VERSION_VALUE="8"
  else
    CMAKE_TOOLCHAIN_FILE_VALUE="/home/$user/.conan/data/armv8_linux_gcc8/0.12.0/aos/dev/package/0b9087fa2e697f5753918ed600436dc0f93f8994/cmake/armv8_linux_gcc8.cmake"
    COMPILER_VERSION_VALUE="8"
  fi
  CMAKE_INSTALL_PREFIX_VALUE="$bl_build_folder/build_armv8/build_armv8_exe/package"
fi

echo "CMAKE_TOOLCHAIN_FILE_VALUE=$CMAKE_TOOLCHAIN_FILE_VALUE"
echo "CMAKE_INSTALL_PREFIX_VALUE=$CMAKE_INSTALL_PREFIX_VALUE"
echo "CMAKE_MODULE_PATH_VALUE=$CMAKE_MODULE_PATH_VALUE"

if $flag_build; then
  echo "Flag -flag_build is set"

  mkdir -p $CMAKE_MODULE_PATH_VALUE
  cd $CMAKE_MODULE_PATH_VALUE
  
  if [ "$target_type" == "x86-64" ]; then
    conan install $bl_build_folder/conanfile.txt -pr:h=x86_64_linux_gcc8_debug  -pr:b=x86_64_linux_gcc8_debug_build
    mkdir -p $CMAKE_MODULE_PATH_VALUE/build_x86_64_exe && cd $CMAKE_MODULE_PATH_VALUE/build_x86_64_exe
  elif [ "$target_type" == "armv8" ]; then
    conan install $bl_build_folder/conanfile.txt -pr:h=armv8_linux_gcc8_debug  -pr:b=armv8_linux_gcc8_debug_build
    mkdir -p $CMAKE_MODULE_PATH_VALUE/build_armv8_exe && cd $CMAKE_MODULE_PATH_VALUE/build_armv8_exe
  fi
  ENABLE_CLANG_TIDY_CHECKS="${ENABLE_CLANG_TIDY_CHECKS:-ON}"
  echo "Running cmake..."
  cmake -G "Unix Makefiles" \
    -DCMAKE_BUILD_TYPE=$build_type \
    -Dtarget_type=$target_type \
    -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE_VALUE \
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
    -DBOSCH_ULRR_ENABLE_UNIT_TESTS=$ENABLE_UNIT_TESTS_VALUE \
    -DBL_ULRR_INDEPENDENT_BUILD=$BL_ULRR_INDEPENDENT_BUILD_VALUE \
    -DBL_ENABLE_CLANG_TIDY_CHECKS="$ENABLE_CLANG_TIDY_CHECKS" \
    -DCONAN_IN_LOCAL_CACHE="ON" \
    -Wno-dev \
    $bl_folder
  
  script -q -c "cmake --build . -- -j8" build.log

  if grep -q "make: \*\*\* \[.*\] Error [1-9]" build.log; then
      echo "CMake build failed, 'Error' found"
      exit 1
  else
      echo "CMake build succeeded"
  fi
fi

if $flag_package; then
  echo "Flag -flag_package is set"

  if [ "$target_type" == "x86-64" ]; then
    cd $CMAKE_MODULE_PATH_VALUE/build_x86_64_exe
  elif [ "$target_type" == "armv8" ]; then
    cd $CMAKE_MODULE_PATH_VALUE/build_armv8_exe
  fi

  echo $PWD

  echo "Archiving for $target_type"

  deb_package_name=$package_name-${package_version//./-}-ubuntu2004-$target_type-gcc$COMPILER_VERSION_VALUE-$build_type
  echo "Creating deb. packg with the following name: $deb_package_name"

  mkdir -p $deb_package_name/opt/ulrr/usr/lib
  
  if [ "$target_type" == "x86-64" ]; then
    cp -r lib/ $deb_package_name/opt/ulrr/usr/lib
  fi

  if [ "$target_type" == "armv8" ]; then
    cp -r lib/ $deb_package_name/opt/ulrr/usr/lib
  fi
  
  # Create control script
  mkdir -p $deb_package_name/DEBIAN

  cat > $deb_package_name/DEBIAN/control <<EOF
Package: ${package_name}-business-logic
Version: $package_version
Architecture: $architecture
Maintainer: $maintainer
Description: $description
EOF

  dpkg-deb --build --root-owner-group $deb_package_name

  zip -r $package_name.zip lib/

fi

if [ $flag_run_unit_tests == true ] && [ "$target_type" == "armv8" ] && [ -z "$rootfs_path" ]; then
  echo "Rootfs file path was not provided... The rootfs file will be downloaded through jfrog REST API"

  rootfs_filename=$(find * -type f -name 'rootfs_*ext4');
  if [ ! -z "$rootfs_filename" ]; then
    echo "$rootfs_filename was found."
    
    rootfs_path=$(readlink -f $rootfs_filename)

  else
    read -s -p "Provide JFrog token: " jfrog_token
    python3 devops/scripts/python/libraries/jfrog/jfrog-download-artifact.py https://artifactory.boschdevcloud.com/artifactory $jfrog_token $rootfs_repository_path artifacts/ $rootfs_artifact
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
      echo "Decompress Successful"
    else
      echo "Decompress failed"
      exit 1
    fi

    rootfs_path=$(readlink -f artifacts/$rootfs_filename)
  fi

  echo "rootfs_path: $rootfs_path"
  echo "rootfs_filename: $rootfs_filename"
fi



if $flag_run_unit_tests; then
  echo "Flag -flag_run_unit_tests is set"

  if [ "$target_type" == "x86-64" ]; then
    # cd $conan_prj_path/build_x86_64/build_x86_64_exe/bin

    if [ ! -d "$xml_test_report_path" ]; then
      mkdir "$xml_test_report_path"
      echo "Folder $xml_test_report_path created!"
    else
      echo "Folder $xml_test_report_path already exists!"
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
    echo "python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $CMAKE_MODULE_PATH_VALUE/build_armv8_exe/bin/ --destination-path /opt/ulrr/usr/bin/build_armv8_exe/bin/ --rootfs-filepath $rootfs_path"
    python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $CMAKE_MODULE_PATH_VALUE/build_armv8_exe/bin/ --destination-path /opt/ulrr/usr/bin/build_armv8_exe/bin/ --rootfs-filepath $rootfs_path

    echo "python3 devops/scripts/python/qemu/qemu_fusion.py run-unit-test --test-report-path $xml_test_report_path --rootfs-filepath $rootfs_path"
    python3 devops/scripts/python/qemu/qemu_fusion.py run-unit-test --test-report-path $xml_test_report_path --rootfs-filepath $rootfs_path
  fi
fi
