#=======================================================================================================================
#  C O P Y R I G H T
#-----------------------------------------------------------------------------------------------------------------------
#  @copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  The reproduction, distribution and utilization of this file as well as the communication of its contents to others
#  without express authorization is prohibited. Offenders will be held liable for the payment of damages. All rights
#  reserved in the event of the grant of a patent, utility model or design.
#=======================================================================================================================
#  P R O J E C T   I N F O R M A T I O N
#-----------------------------------------------------------------------------------------------------------------------
#      Project name: PCIE Framework
#=======================================================================================================================
#  I N I T I A L   A U T H O R   I D E N T I T Y
#-----------------------------------------------------------------------------------------------------------------------
#        Ingo Diepholz (ITKG/EPM-RTA1.7)
#  Department: ITKG/EPM-RTA1.7
#=======================================================================================================================
#  R E V I S I O N  I N F O R M A T I O N
#-----------------------------------------------------------------------------------------------------------------------
# @author       Ingo Diepholz (ITKG/EPM-RTA1.7)
# @file         conan_install.cmake
# @brief        Script to add conan download target in nrcs repo for fpm integration
#=======================================================================================================================
cmake_minimum_required(VERSION 3.14)

include_guard()

## @brief         Download the Conan packages
## @param[in]     conanfilePath: Path (folder or file) to the conanfile.py
## @details       Usage: conan_install(conanfilePath)
function(conan_install)

    set(options        "")
    set(oneValueArgs   CONANFILE_PATH PROFILE)
    set(multiValueArgs "")
    cmake_parse_arguments(CONAN "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN} )

    execute_process(
        COMMAND conan install --build=missing --update ${CONAN_CONANFILE_PATH}
        WORKING_DIRECTORY   ${CMAKE_CURRENT_LIST_DIR}
        RESULT_VARIABLE     CONAN_INSTALL_RESULT
        OUTPUT_VARIABLE     CONAN_INSTALL_OUTPUT
        ERROR_VARIABLE      CONAN_INSTALL_ERROR
    )

    message(STATUS "CONAN_INSTALL_OUTPUT: [${CONAN_INSTALL_OUTPUT}]")
    if(NOT CONAN_INSTALL_RESULT MATCHES 0)
        message(STATUS "CONAN_INSTALL_RESULT: [${CONAN_INSTALL_RESULT}]")
        message(STATUS "CONAN_INSTALL_ERROR:  [${CONAN_INSTALL_ERROR}]")
        message(FATAL_ERROR "Download Conan packages from [${CONAN_CONANFILE_PATH}] failed!")
    else()
        message(STATUS "Download Conan packages from [${CONAN_CONANFILE_PATH}] successful.")
    endif()

endfunction()