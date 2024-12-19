#!/bin/bash
set -e

# Script Name: print_colored_message.sh
# Author: C3 Team
# Description: This prints on standard output a message in a given color.

# Define text formatting variables
BOLD='\033[1m'
UNDERLINE='\033[4m'
BLINK='\033[5m'

# Define color variables
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
RESET='\033[0m'  # Reset color to default

# Function print_colored_message
function print_colored_message() {
    local message="$1"
    local color_code="$2"
    local formatting="$3"

    echo -e "${formatting}${color_code}${message}${RESET}"    
}