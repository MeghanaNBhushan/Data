#!/bin/bash
set -e

# Script Name: getbaseimagefile.sh
# Author: C3 Team
# Description: This script download a base image file through jfrog REST API, from artifactory.

cd $IR2_BUILD_TOOL_PATH
source auxiliar/print_colored_message.sh
source config/settings.sh

# Function getbaseimagefile
function getbaseimagefile() {
    read -s -p "Provide JFrog token: " jfrog_token

    python3 devops/scripts/python/jfrog-download-artifact.py https://artifactory.boschdevcloud.com/artifactory $jfrog_token "${CONAN_SETTINGS[rootfs_repository_path]}${CONAN_SETTINGS[rootfs_artifact]}" artifacts/ "${CONAN_SETTINGS[rootfs_artifact]}"
    if [ $? -eq 0 ]; then
        echo "$rootfs_artifact was download with success."
    else
        echo "Download of $rootfs_artifact failed."
        exit 1
    fi

    rootfs_archive=$(find * -type f -name 'rootfs_*ext4.gz');
    rootfs_archive_filename=$(basename "$rootfs_archive")
    rootfs_filename="${rootfs_archive_filename%.gz}"
    rootfs_archive_path=$(readlink -f $rootfs_archive)

    
    echo "Uncompress rootfs"
    echo "gunzip -k $rootfs_archive_path -c > artifacts/$rootfs_filename"
    if gunzip -k $rootfs_archive_path -c > artifacts/$rootfs_filename; then
      echo "Decompress successful"
    else
      echo "Decompress failed"
      exit 1
    fi

    base_image_file=$(readlink -f artifacts/$rootfs_filename)
}