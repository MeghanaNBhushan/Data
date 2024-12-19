architecture="arm64"

CMAKE_TOOLCHAIN_FILE_VALUE="/home/$user/.conan/data/armv8_qnx71_qcc83/0.6.0/aos/dev/package/0b9087fa2e697f5753918ed600436dc0f93f8994/cmake/armv8_qnx71_qcc83.cmake"
COMPILER_VERSION_VALUE="8"

CMAKE_INSTALL_PREFIX_VALUE="$conan_prj_path/build_armv8/build_armv8_exe/package"
CMAKE_MODULE_PATH_VALUE="$conan_prj_path/build_armv8"

if [ "$build_type" == "debug" ]; then
    CMAKE_BUILD_TYPE_VALUE="Debug"
    conan_host_profile="armv8_qnx71_qcc83_debug"
    conan_build_profile="armv8_qnx71_qcc83_debug_build"
else
    CMAKE_BUILD_TYPE_VALUE="Release"
fi
