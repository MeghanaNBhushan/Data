#!/bin/bash
set -e

# Script Name: find_artefact.sh
# Author: C3 Team
# Description: This script looks searck for a given artefact within Conan cache

cd $IR2_BUILD_TOOL_PATH
source auxiliar/getcuser.sh

# Function find_artefact
function find_artefact() {
  local artefact_name="$1"

  if [ "$target_type" == "armv8" ]; then
    target_arch="ARM aarch64"
  elif [ "$target_type" == "x86-64" ]; then
    target_arch="x86-64"
  else
    echo "Unknown target type: '$target_type'."
    exit 1
  fi

  user=""
  getcuser

  local package_dir="/home/$user/.conan/data/"
  local artefacts=$(find "$package_dir" -name "$artefact_name" -type f)

  # Loop through the found artefacts and check the architecture
  for artefact_path in $artefacts; do
      # Use 'file' command to get architecture information
      local arch_info=$(file "$artefact_path")
      
      # Check if the architecture information contains the target architecture
      if [[ $arch_info == *"$target_arch"* ]]; then
          echo "'$artefact_name' found for architecture '$target_arch' in:"
          echo "$artefact_path"
          return 0  # Return success
      fi
  done

  # If no library was found for the specified architecture
  echo "'$artefact_name' for architecture '$target_arch' not found."
  return 1  # Return failure
}