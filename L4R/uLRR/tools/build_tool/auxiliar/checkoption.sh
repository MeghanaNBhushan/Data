#!/bin/bash
set -e

# Script Name: checkoption.sh
# Author: C3 Team
# Description: This script checks if given the option is valid.

# Function checkoption
function checkoption() {
    local option="$1"
    local list_of_allowed_options=("${@:2}")

    # Iterate through the list
    for item in "${list_of_allowed_options[@]}"; do
        if [ "$item" == "$option" ]; then
            return 0  # Option is found (success)
        fi
    done

    return 1  # Option is not found (failure)
}