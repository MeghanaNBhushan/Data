#!/bin/bash
set -e

# Script Name: config.sh
# Author: C3 Team
# Description: This script initializes/customizes the build tool.

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTPATH

source auxiliar/print_colored_message.sh
source config/settings.sh

# Function config
function config() {
    local project="$1"
    local target_type="$2"
    local build_type="$3"
    if [ "$project" == "aos" ]; then
        local middleware_instance="$4"
        local aos_version="$7"
        local a_core_sw_variant="$8"
        local a_core_version_major="$9"
        local a_core_version_minor="${10}"
        local a_core_version_patch="${11}"
        local a_core_commit_hash="${12}"
    fi
    local suppress_warnings="$5"
    local skip_unit_tests="$6"

    # Write the settings to the settings file
    settings_file="$SCRIPTPATH/tool_settings_$project"

    # If target type is given
    if [ "$target_type" != "-" ]; then
        # updates the value of target_type in a settings file with the value of the $target_type
        awk -F'=' -v val="$target_type" '/target_type/ {$2=val}1' OFS='=' $settings_file > temp && mv temp $settings_file
    fi

    # If build type is given
    if [ "$build_type" != "-" ]; then
        # updates the value of build_type in a settings file with the value of the $build_type
        awk -F'=' -v val="$build_type" '/build_type/ {$2=val}1' OFS='=' $settings_file > temp && mv temp $settings_file
    fi

    # If suppress warnings is given
    if [ "$suppress_warnings" != "-" ]; then
        # updates the value of suppress_warnings in a settings file with the value of the $suppress_warnings
        awk -F'=' -v val="$suppress_warnings" '/suppress_warnings/ {$2=val}1' OFS='=' $settings_file > temp && mv temp $settings_file
    fi

    # If skip unit tests is given
    if [ "$skip_unit_tests" != "-" ]; then
        # updates the value of skip_unit_tests in a settings file with the value of the $skip_unit_tests
        awk -F'=' -v val="$skip_unit_tests" '/skip_unit_tests/ {$2=val}1' OFS='=' $settings_file > temp && mv temp $settings_file
    fi

    # If middleware instance is given
    if [ "$middleware_instance" != "-" ]; then
        # updates the value of middleware_instance in a settings file with the value of the $middleware_instance
        if [ "$middleware_instance" != "car_pc" ] && [ "$middleware_instance" != "testing" ]; then
            IFS='_' read -ra file_name_array <<< "$middleware_instance"
            os_type="${file_name_array[1]}"
        else
            os_type="linux"
        fi
        awk -F'=' -v val="$os_type" '/os_type/ {$2=val}1' OFS='=' $settings_file > temp && mv temp $settings_file
        awk -F'=' -v val="$middleware_instance" '/middleware_instance/ {$2=val}1' OFS='=' $settings_file > temp && mv temp $settings_file
    fi

    # If aos version is given
    if [ "$aos_version" != "-" ] && [ "$project" == "aos" ]; then
        # updates the value of aos_version in a settings file with the value of the $aos_version
        awk -F'=' -v val="$aos_version" '/aos_version/ {$2=val}1' OFS='=' $settings_file > temp && mv temp $settings_file
    fi

    # If A-core version arguments are given
    declare -A acore_versions=(
        ["a_core_sw_variant"]=$a_core_sw_variant
        ["a_core_version_major"]=$a_core_version_major
        ["a_core_version_minor"]=$a_core_version_minor
        ["a_core_version_patch"]=$a_core_version_patch
        ["a_core_commit_hash"]=$a_core_commit_hash
    )
    for key in "${!acore_versions[@]}"; do
        if [ "${acore_versions[$key]}" != "-" ]; then
            awk -F'=' -v key="$key" -v val="${acore_versions[$key]}" '
                BEGIN {updated=0}
                $1 == key {$2=val; updated=1}
                {print}
                END {if (updated == 0) print key"="val}
            ' OFS='=' $settings_file > temp && mv temp $settings_file
        else
            awk '!/^'$key'=/' $settings_file > temp && mv temp $settings_file
        fi
    done
}
