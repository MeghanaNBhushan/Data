cmake_minimum_required (VERSION 3.14)

project (uLRR_unit_tests)

# GoogleTest requires at least C++14
set(CMAKE_CXX_STANDARD 14)

# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

enable_testing()

add_executable(${CMAKE_PROJECT_NAME}
	tools/googletest/ulrr/ulrr_gtest_entry.cpp
)

add_subdirectory(tools/googletest/)

target_include_directories(${CMAKE_PROJECT_NAME}
	PUBLIC
)	  

target_link_libraries(${CMAKE_PROJECT_NAME} 
	gtest_main
)
