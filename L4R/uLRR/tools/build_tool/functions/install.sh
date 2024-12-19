#!/bin/bash
set -e

# Script Name: install.sh
# Author: C3 Team
# Description: This script installs dependencies.

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTPATH

source auxiliar/print_colored_message.sh
source config/settings.sh


# Function install
function install() {
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
    print_colored_message "Installing $project for $target_type, $build_type" "$GREEN"
    if [ "$project" == "aos" ]; then
        print_colored_message " - middleware instance: $middleware_instance" "$GREEN"
        print_colored_message " - os type: $os_type" "$GREEN"
    fi
    print_colored_message " - aos version: $aos_version" "$GREEN"
    print_colored_message " - suppress warnings: $suppress_warnings" "$GREEN"
    print_colored_message " - skip tests: $skip_unit_tests" "$GREEN"
    print_colored_message " - A-core SW variant: $a_core_sw_variant" "$GREEN"
    print_colored_message " - A-core version major: $a_core_version_major" "$GREEN"
    print_colored_message " - A-core version minor: $a_core_version_minor" "$GREEN"
    print_colored_message " - A-core version patch: $a_core_version_patch" "$GREEN"
    print_colored_message " - A-core commit hash: $a_core_commit_hash" "$GREEN"

    # Creates the install folder
    cd $project_root_folder
    rm -rf build/${project}_${os_type}_${target_type}_${build_type} && mkdir -p build/${project}_${os_type}_${target_type}_${build_type}

    conan_options=""
    if [ $project = "aos" ]; then
        conan_options+="-o MIDDLEWARE_INSTANCE=$middleware_instance "
        if [ $aos_version != "default" ]; then
            conan_options+="-o AOS_VERSION=$aos_version "
        fi
        conan_options+="-o A_CORE_SW_VARIANT=$a_core_sw_variant "
        conan_options+="-o A_CORE_VERSION_MAJOR=$a_core_version_major "
        conan_options+="-o A_CORE_VERSION_MINOR=$a_core_version_minor "
        conan_options+="-o A_CORE_VERSION_PATCH=$a_core_version_patch "
        conan_options+="-o A_CORE_COMMIT_HASH=$a_core_commit_hash "
    fi

    conan_recipe_path="conan_recipe_${project}"
    host_profile="profile_${os_type}_${target_type}_${build_type}"
    build_profile="${host_profile}_build"

    conan install $project_root_folder"${CONAN_SETTINGS[$conan_recipe_path]}" -if=./build/${project}_${os_type}_${target_type}_${build_type} -pr:h="${CONAN_SETTINGS[$host_profile]}" -pr:b="${CONAN_SETTINGS[$build_profile]}" --update $conan_options
}