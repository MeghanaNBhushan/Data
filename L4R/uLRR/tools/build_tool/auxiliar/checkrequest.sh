#!/bin/bash
set -e

# Script Name: checkrequest.sh
# Author: C3 Team
# Description: This script checks if given the request combination is valid.

# Function checkrequest
function checkrequest() {
    local target_type="$1"
    local build_type="$2"
    local middleware_instance="$3"

    # Checking if x86-64 release was requested
    if [ "$target_type" == "x86-64" ] && [ "$build_type" == "release" ]; then
        print_colored_message "AOS doesn't provide x86-64 release build" "$RED"
        exit 1
    fi

    # Checking if x86-64 release was requested
    if [ "$target_type" == "armv8" ] && [ "$middleware_instance" == "car_pc" ]; then
        print_colored_message "CAR PC isn't compatible with target_type equal to armv8" "$RED"
        exit 1
    fi
}