#!/bin/bash
set -e

# Script Name: package.sh
# Author: C3 Team
# Description: This script generate the conan package, for deploy.

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTPATH

source auxiliar/print_colored_message.sh
source auxiliar/gendebpckg.sh
source config/settings.sh

# Function package
function package() {
    local project="$1"
    local package_type="$2"

    # Read the settings file
    settings_file="$SCRIPTPATH/tool_settings_$project"
    if [ -f "$settings_file" ]; then
        source $settings_file
    else
        print_colored_message "Error: settings file not found. Please run config command first." "$RED"
        exit 1
    fi

    if [ $package_type = "conan" ]; then
        echo "DEBUG: print env varaible SPECIAL_VERSON = $SPECIAL_VERSON"
        conan_recipe_path="conan_recipe_${project}"
        host_profile="profile_${os_type}_${target_type}_${build_type}"
        build_profile="${host_profile}_build"
        
        conan export-pkg $project_root_folder"${CONAN_SETTINGS[$conan_recipe_path]}" ir2/platform -bf=./build/${project}_${os_type}_${target_type}_${build_type} --json build/${project}_${os_type}_${target_type}_${build_type}/conanpackageinfo.json -f

    fi

    if [ $package_type = "deb" ]; then
        # Generate the deb package
        gendebpckg $project $os_type $target_type $build_type $middleware_instance
    fi
}
