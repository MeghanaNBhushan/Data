#=======================================================================================================================
#  C O P Y R I G H T
#-----------------------------------------------------------------------------------------------------------------------
#  @copyright (c) 2011 - 2021 by Robert Bosch GmbH. All rights reserved.
#
#  The reproduction, distribution and utilization of this file as well as the communication of its contents to others
#  without express authorization is prohibited. Offenders will be held liable for the payment of damages. All rights
#  reserved in the event of the grant of a patent, utility model or design.
#=======================================================================================================================
#  P R O J E C T   I N F O R M A T I O N
#-----------------------------------------------------------------------------------------------------------------------
#      Projectname: PCIE Framework
#=======================================================================================================================
#  I N I T I A L   A U T H O R   I D E N T I T Y
#-----------------------------------------------------------------------------------------------------------------------
#             Name: Fengyu Chen
#       Department: ITKG/EPM-RTA1.6
#=======================================================================================================================
#  R E V I S I O N  I N F O R M A T I O N
#-----------------------------------------------------------------------------------------------------------------------
# @author       Fengyu Chen (ITKG/EPM-RTA1.6)
# @file         FindConan.cmake
# @brief        Find Conan toolchain
# @version      0.13.0
#=======================================================================================================================
cmake_minimum_required(VERSION 3.14 FATAL_ERROR)

include(FindPackageHandleStandardArgs)

set(_PACKAGE_NAME "Conan")
set(_PREFIX "")
set(PYTHON_REQUIRED_VERSION "3.8")

########################################################################################################################
### Find Python installation, path to installation folder should be set in user path
########################################################################################################################
find_package(Python3 ${PYTHON_REQUIRED_VERSION} COMPONENTS Interpreter)
if(Python3_FOUND)
    message(STATUS "Python found ${Python3_EXECUTABLE}")
    message(STATUS "Python interpreter: ${Python3_INTERPRETER_ID}")
    message(STATUS "Python version: ${Python3_VERSION}")
########################################################################################################################
### Find Conan in Python installation, if no Conan package is found, abort
########################################################################################################################
    execute_process(
        COMMAND ${Python3_EXECUTABLE} -m pip show conan
        OUTPUT_VARIABLE ${_PACKAGE_NAME}_OUTPUT
        RESULT_VARIABLE ${_PACKAGE_NAME}_RESULT
        ERROR_VARIABLE ${_PACKAGE_NAME}_ERROR
    )

else()
########################################################################################################################
### If no Python installation is found, no Conan will be found
########################################################################################################################
    message(WARNING "Python not found, no package management using Conan will be possible")
endif()

set(${_PACKAGE_NAME}_FOUND FALSE)

########################################################################################################################
### Parse output to get current version of Conan
########################################################################################################################
if(Python3_FOUND AND ${_PACKAGE_NAME}_RESULT MATCHES 0)
    string(
        REGEX MATCH "^.*Version: ([0-9]+)\.([0-9]+)"
        ${_PACKAGE_NAME}_VERSION_MATCH
        ${${_PACKAGE_NAME}_OUTPUT}
    )

    set(${_PACKAGE_NAME}_VERSION_MAJOR "${CMAKE_MATCH_1}")
    set(${_PACKAGE_NAME}_VERSION_MINOR "${CMAKE_MATCH_2}")
    set(${_PACKAGE_NAME}_VERSION
        "${${_PACKAGE_NAME}_VERSION_MAJOR}.${${_PACKAGE_NAME}_VERSION_MINOR}"
    )

########################################################################################################################
### If Conan version meets requirement, set variable Conan_FOUND to true
########################################################################################################################
    if(DEFINED ${_PACKAGE_NAME}_FIND_VERSION AND ${_PACKAGE_NAME}_VERSION VERSION_LESS ${_PACKAGE_NAME}_FIND_VERSION)
        set(${_PACKAGE_NAME}_FOUND FALSE)
        message(
            FATAL_ERROR
            "Found unsuitable ${_PACKAGE_NAME} version \"${${_PACKAGE_NAME}_VERSION}\" from ${_PACKAGE_NAME}"
        )
    else()
        set(${_PACKAGE_NAME}_FOUND TRUE CACHE BOOL "${_PACKAGE_NAME} found in toolchain!")
        message(STATUS "${_PACKAGE_NAME} ${${_PACKAGE_NAME}_VERSION} found in toolchains.")
    endif()

endif()
