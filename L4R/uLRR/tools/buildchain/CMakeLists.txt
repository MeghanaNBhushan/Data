cmake_minimum_required(VERSION 3.0.2)
project(ad_radar_sensor_app VERSION 0.0.1)

## Compile as C++11, supported in ROS Kinetic and newer
set(CMAKE_CXX_STANDARD 14)

# General packaging
set(CPACK_PACKAGE_VERSION ${PROJECT_VERSION})
set(CPACK_PACKAGE_NAME ${PROJECT_NAME})
set(CPACK_PACKAGE_RELEASE 1)
set(CPACK_PACKAGE_CONTACT "noreply@de.bosch.com")
set(CPACK_PACKAGE_VENDOR "Robert Bosch GmbH")
set(CPACK_PACKAGING_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX})
set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}-${CPACK_PACKAGE_RELEASE}.${CMAKE_SYSTEM_PROCESSOR}")

if(CMAKE_CROSSCOMPILING)
  # Do the RPM packaging for the target
  set(CPACK_GENERATOR "RPM")
  set(CPACK_RPM_PACKAGE_ARCHITECTURE "aarch64")
  set(CPACK_RPM_PACKAGE_AUTOREQPROV TRUE)
  set(CPACK_RPM_PACKAGE_PROVIDES "libstatepublisher.so()(64bit)") # For some reasons, the included library is not properly detected. I guess there is an error somewhere in this file.

  ## add_subdirectory(source_dir [binary_dir] [EXCLUDE_FROM_ALL] [SYSTEM])
  # source_dir - specifies the directory in which the source CMakeLists.txt and code files are located
  # binary_dir - specifies the directory in which to place the output files.
  add_subdirectory (../../software/ros/src ../../software/ros/build/aarm_arch64)
else()
  # Do the DEB packaging for the "host"
  set(CPACK_GENERATOR "DEB")

  ## add_subdirectory(source_dir [binary_dir] [EXCLUDE_FROM_ALL] [SYSTEM])
  # source_dir - specifies the directory in which the source CMakeLists.txt and code files are located
  # binary_dir - specifies the directory in which to place the output files.
  add_subdirectory (../../software/ros/src ../../software/ros/build/x86_64)
endif()
include(CPack)