project (crosscompilation_example)
cmake_minimum_required (VERSION 3.16)
set(VERSION "0.0.1")

# Build shared objects and adapt the RPath of runtimes during the install phase
set(BUILD_SHARED_LIBS TRUE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

# Compile the lib
add_library(
    sayhello

    hello.cpp
)

# ... and the executable
add_executable(
    yahwa # Yet another Hello World App

    main.cpp
) 
target_link_libraries(
    yahwa
    
    PRIVATE
    sayhello
)

# Install statement to export the targets to the RPM package
install(
    TARGETS
    sayhello
    yahwa

    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# General packaging
set(CPACK_PACKAGE_VERSION ${VERSION})
set(CPACK_GENERATOR "RPM")
set(CPACK_PACKAGE_NAME ${PROJECT_NAME})
set(CPACK_PACKAGE_RELEASE 1)
set(CPACK_PACKAGE_CONTACT "noreply@bosch.com")
set(CPACK_PACKAGE_VENDOR "Robert Bosch GmbH")
set(CPACK_PACKAGING_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX})
set(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}-${CPACK_PACKAGE_RELEASE}.${CMAKE_SYSTEM_PROCESSOR}")
# Do the RPM packaging
set(CPACK_RPM_PACKAGE_ARCHITECTURE "aarch64")
set(CPACK_RPM_PACKAGE_AUTOREQPROV TRUE)
set(CPACK_RPM_PACKAGE_PROVIDES "libsayhello.so()(64bit)") # For some reasons, the included library is not properly detected. I guess there is an error somewhere in this file.
include(CPack)