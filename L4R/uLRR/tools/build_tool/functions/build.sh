#!/bin/bash
set -e

# Script Name: build.sh
# Author: C3 Team
# Description: This script builds software dependencies.

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTPATH

source auxiliar/print_colored_message.sh
source auxiliar/getcuser.sh
source config/settings.sh

# Function build
function build() {
    local project="$1"

    # Read the settings file
    settings_file="$SCRIPTPATH/tool_settings_$project"
    if [ -f "$settings_file" ]; then
        source $settings_file
    else
        print_colored_message "Error: settings file not found. Please run config command first." "$RED"
        exit 1
    fi

    if [ "$project" == "aos" ]; then
        # Checking undesired conditions
        checkrequest $target_type $build_type $middleware_instance
    fi

    # Prints an overview, of the request
    print_colored_message "Building $project for $target_type, $build_type" "$GREEN"

    source /opt/ros/noetic/setup.bash

    conan_recipe_path="conan_recipe_${project}"

    # Build the project, logging the output to a file
    export CONAN_LOG_RUN_TO_FILE=1

    # Pass the A-core version components as environment variables
    export A_CORE_SW_VARIANT=${a_core_sw_variant}
    export A_CORE_VERSION_MAJOR=${a_core_version_major}
    export A_CORE_VERSION_MINOR=${a_core_version_minor}
    export A_CORE_VERSION_PATCH=${a_core_version_patch}
    export A_CORE_COMMIT_HASH=${a_core_commit_hash}

    # Pass the environment variables to the Conan build process
    conan build $project_root_folder"${CONAN_SETTINGS[$conan_recipe_path]}" \
    -if=./build/${project}_${os_type}_${target_type}_${build_type} \
    -bf=./build/${project}_${os_type}_${target_type}_${build_type}
        
    if [ $? -eq 0 ]; then
        echo "CMake build succeeded"
    else
        echo "CMake build failed..."
        exit 1        
    fi
}