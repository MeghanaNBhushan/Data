architecture="amd64"

CMAKE_TOOLCHAIN_FILE_VALUE="/home/$user/.conan/data/x86_64_linux_gcc8/0.12.0/aos/dev/package/8801d677d2372957a75ead7d94702a021050cadf/cmake/x86_64_linux_gcc8.cmake"
COMPILER_VERSION_VALUE="8"

CMAKE_INSTALL_PREFIX_VALUE="$conan_prj_path/build_x86_64/build_x86_64_exe/package"
CMAKE_MODULE_PATH_VALUE="$conan_prj_path/build_x86_64"

if [ "$build_type" == "debug" ]; then
  CMAKE_BUILD_TYPE_VALUE="Debug"
  conan_host_profile="x86_64_linux_gcc8_debug"
  conan_build_profile="x86_64_linux_gcc8_debug_build"
else
  CMAKE_BUILD_TYPE_VALUE="Release"
fi
