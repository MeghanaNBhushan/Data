message (WARNING "This toolchain file is *not* ready for productive use!")

set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_VERSION 1)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

# Library prefix and suffix
set(CMAKE_SHARED_LIBRARY_PREFIX "lib")
set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
set(CMAKE_STATIC_LIBRARY_PREFIX "lib")
set(CMAKE_STATIC_LIBRARY_SUFFIX ".a")

set(SDK_PATH        "/opt/petalinux/sdk-v2021.2/sysroots")
set(COMPILER_PATH   "${SDK_PATH}/x86_64-petalinux-linux/usr/bin/aarch64-xilinx-linux")
set(XILINX_PREFIX   "aarch64-xilinx-linux-")
set(CMAKE_SYSROOT   "${SDK_PATH}/cortexa72-cortexa53-xilinx-linux")
SET(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})

# C tooling
set(CMAKE_C_COMPILER "${COMPILER_PATH}/${XILINX_PREFIX}gcc"  CACHE PATH "Xilinx C compiler")
set(CMAKE_C_FLAGS    "$ENV{CFLAGS} --sysroot=${CMAKE_FIND_ROOT_PATH}"                                 CACHE STRING "Xilinx C compiler flags")

# C++ tooling
set(CMAKE_CXX_COMPILER  "${COMPILER_PATH}/${XILINX_PREFIX}g++"   CACHE   PATH    "Xilinx C++ compiler")
set(CMAKE_CXX_FLAGS     "$ENV{CXXFLAGS} --sysroot=${CMAKE_FIND_ROOT_PATH}"                                  CACHE   STRING  "Xilinx C++ compiler flags")

# Common tooling
set(CMAKE_AR           "${COMPILER_PATH}/${XILINX_PREFIX}ar"                    CACHE PATH "Xilinx ar")
set(CMAKE_RANLIB       "${COMPILER_PATH}/${XILINX_PREFIX}ranlib"                CACHE PATH "Xilinx ranlib")
set(CMAKE_NM           "${COMPILER_PATH}/${XILINX_PREFIX}nm"                    CACHE PATH "Xilinx nm")
set(CMAKE_OBJCOPY      "${COMPILER_PATH}/${XILINX_PREFIX}objcopy"               CACHE PATH "Xilinx objcopy")
set(CMAKE_OBJDUMP      "${COMPILER_PATH}/${XILINX_PREFIX}objdump"               CACHE PATH "Xilinx objdump")
set(CMAKE_LINKER       "${COMPILER_PATH}/${XILINX_PREFIX}ld"                    CACHE PATH "Xilinx linker")
set(CMAKE_STRIP        "${COMPILER_PATH}/${XILINX_PREFIX}strip"                 CACHE PATH "Xilinx strip")

# for libraries and headers in the target directories
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER) # search for programs in the build host directories
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)  # search for libraries in the target rootfs directories
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
