#!/bin/bash
set -e

# Script Name: unit-test.sh
# Author: C3 Team
# Description: This script triggers the execution of the unit-test.

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTPATH

source auxiliar/print_colored_message.sh
source config/settings.sh

# Function build
function unit-test() {
    local project="$1"
    local base_image_file="$2"

    # Read the settings file
    settings_file="$SCRIPTPATH/tool_settings_$project"
    if [ -f "$settings_file" ]; then
        source $settings_file
    else
        print_colored_message "Error: settings file not found. Please run config command first." "$RED"
        exit 1
    fi

    # Prints an overview, of the request
    print_colored_message "Triggering unit-test on $project for $target_type, $build_type" "$GREEN"



    # Run unit-test based on target_type
    if [ "$target_type" == "x86-64" ]; then

        conan_recipe_path="conan_recipe_${project}"
        conan build $project_root_folder"${CONAN_SETTINGS[$conan_recipe_path]}" -if=./build/${project}_${os_type}_${target_type}_${build_type} -bf=./build/${project}_${os_type}_${target_type}_${build_type} --test

    elif [ "$target_type" == "armv8" ]; then
        mkdir test_reports

        echo "python3 devops/scripts/python/qemu/qemu_fusion.py run-unit-test --test-report-path $(realpath "test_reports") --rootfs-filepath $base_image_file"
        python3 devops/scripts/python/qemu/qemu_fusion.py run-unit-test --test-report-path $(realpath "test_reports") --rootfs-filepath $base_image_file
        
    else
        print_colored_message "Error - Not expected target_type: $target_type" "$RED"
        exit 1
    fi
}