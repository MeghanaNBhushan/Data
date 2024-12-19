#message (WARNING "This toolchain file is *not* ready for productive use!")
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_VERSION 1)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(WORK_DIR_PATH $ENV{WDIRPATH})
set(CMAKE_SYSROOT "${WORK_DIR_PATH}/software/os/debian/rootfs/build/rfs")
set(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})
set(CMAKE_LIBRARY_ARCHITECTURE aarch64-linux-gnu)
#set(BOOST_ROOT "${CMAKE_SYSROOT}/user")
# Optionally reduce compiler sanity check when cross-compiling.
#set(CMAKE_TRY_COMPILE_TARGET_TYPE         STATIC_LIBRARY)

# Library prefix and suffix
set(CMAKE_SHARED_LIBRARY_PREFIX "lib")
set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
set(CMAKE_STATIC_LIBRARY_PREFIX "lib")
set(CMAKE_STATIC_LIBRARY_SUFFIX ".a")

set(COMPILER_PATH   "/usr/bin")
set(COMPILER_PREFIX "aarch64-linux-gnu-")

# C tooling
set(CMAKE_C_COMPILER "${COMPILER_PATH}/${COMPILER_PREFIX}gcc"                     CACHE PATH "ARM64 C compiler")
set(CMAKE_C_FLAGS    "$ENV{CFLAGS} --sysroot=${CMAKE_FIND_ROOT_PATH}"             CACHE STRING "ARM64 C compiler flags")

# C++ tooling
set(CMAKE_CXX_COMPILER  "${COMPILER_PATH}/${COMPILER_PREFIX}g++"                  CACHE PATH "ARM64 C++ compiler")
set(CMAKE_CXX_FLAGS     "$ENV{CXXFLAGS} --sysroot=${CMAKE_FIND_ROOT_PATH}"        CACHE STRING "ARM64 C++ compiler flags")

# Common tooling
set(CMAKE_AR           "${COMPILER_PATH}/${COMPILER_PREFIX}ar"                    CACHE PATH "ARM64 ar")
set(CMAKE_RANLIB       "${COMPILER_PATH}/${COMPILER_PREFIX}ranlib"                CACHE PATH "ARM64 ranlib")
set(CMAKE_NM           "${COMPILER_PATH}/${COMPILER_PREFIX}nm"                    CACHE PATH "ARM64 nm")
set(CMAKE_OBJCOPY      "${COMPILER_PATH}/${COMPILER_PREFIX}objcopy"               CACHE PATH "ARM64 objcopy")
set(CMAKE_OBJDUMP      "${COMPILER_PATH}/${COMPILER_PREFIX}objdump"               CACHE PATH "ARM64 objdump")
set(CMAKE_LINKER       "${COMPILER_PATH}/${COMPILER_PREFIX}ld"                    CACHE PATH "ARM64 linker")
set(CMAKE_STRIP        "${COMPILER_PATH}/${COMPILER_PREFIX}strip"                 CACHE PATH "ARM64 strip")

# directives for e.g. find_file, find_package etc.
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# in some distros rpm-build uses the wrong strip version, uncomment this if
# rpm packaging fails with '/usr/bin/strip: Unable to recognise the format of the input file ...'
# prevent rpmbuild from stripping binaries
set(CPACK_RPM_SPEC_INSTALL_POST "/bin/true")