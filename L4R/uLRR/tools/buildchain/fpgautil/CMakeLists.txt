cmake_minimum_required(VERSION 3.25)

project(FPGA)

add_library(${PROJECT_NAME})

target_sources(FPGA PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src/fpgautil.c)

add_executable(fpgautil src/fpgautil.c)
