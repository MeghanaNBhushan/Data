#!/bin/bash
set -e

# Script Name: getcuser.sh
# Author: C3 Team
# Description: This script evalautes the current environment and returns the current user.

# Function getcuser
function getcuser() {
    echo "getcuser"

    user=""
    if [[ -f "/.dockerenv" ]]; then
        echo "Running in a docker environment..."
        user=$UNAME
    else
        echo "Running on host machine..."
        user=$USER
    fi
    echo "using user=$user"
}