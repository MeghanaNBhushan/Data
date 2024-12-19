#!/bin/bash
set -e

# Script Name: deploy.sh
# Author: C3 Team
# Description: This script deploys the package, into the rootfs.

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTPATH

source auxiliar/print_colored_message.sh
source auxiliar/getbaseimagefile.sh
source config/settings.sh

# Function deploy
function deploy() {
    local base_image_file="$1"
    local fpga_bit_file="$2"
    local mmic_libraries="$3"
    local aos_runnables="$4"

    # Prints an overview, of the request
    print_colored_message "Installing on $base_image_file" "$GREEN"
    print_colored_message " - fpga bit file: $fpga_bit_file" "$GREEN"
    print_colored_message " - mmic libraries: $mmic_libraries" "$GREEN"
    print_colored_message " - aos runnables: $aos_runnables" "$GREEN"

    #----------------------------------------------------------------------------------------------------------------
    if [ "$base_image_file" == "-" ]; then
        print_colored_message "Rootfs file path was not provided... The rootfs file will be downloaded through jfrog REST API" "$YELLOW"
        
        getbaseimagefile
        echo $base_image_file
    fi

    #----------------------------------------------------------------------------------------------------------------
    if [ "$fpga_bit_file" == false ]; then
        print_colored_message "Install of FPGA bit file wasn't requested" "$BLUE"
    else
        print_colored_message "Build fpgautil binary" "$GREEN"
        pushd "tools/buildchain/fpgautil"
            mkdir -p build/ && cd build/
            cmake -DCMAKE_TOOLCHAIN_FILE=/opt/bosch/ulrr/toolchains-cmake/toolchainfile-linux-aarch64-a52.cmake -S ../
            cmake --build . '--' '-j8'
        popd

        print_colored_message "Extract fpga file" "$GREEN"
        unzip -o software/os/debian/hw/tec0204/radl4_tec0204.xsa -d "software/os/debian/hw/tec0204/"

        print_colored_message "Run qemu fusion" "$GREEN"
        # Installing fpgautil
        echo "python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $project_root_folder/tools/buildchain/fpgautil/build/fpgautil --destination-path /usr/bin/ --rootfs-filepath $base_image_file"
        python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $project_root_folder/tools/buildchain/fpgautil/build/fpgautil --destination-path /usr/bin/ --rootfs-filepath $base_image_file

        # Installing radl4_top.bit
        echo "python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $project_root_folder/software/business_logic/hrf_lal/uLRR_hrf_lal/bitfiles/rad0/radl4_top.bit --destination-path /opt/ulrr/scripts/ --rootfs-filepath $base_image_file"
        python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $project_root_folder/software/business_logic/hrf_lal/uLRR_hrf_lal/bitfiles/rad0/radl4_top.bit --destination-path /opt/ulrr/scripts/ --rootfs-filepath $base_image_file
    fi

    #----------------------------------------------------------------------------------------------------------------
    if [ "$mmic_libraries" == false ]; then
        print_colored_message "Install of MMIC libraries file wasn't requested" "$BLUE"
    else
        print_colored_message "Run qemu fusion" "$GREEN"

        echo "python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $project_root_folder/dist-packages/ --destination-path /usr/lib/python3.9/ --rootfs-filepath $base_image_file"
        python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $project_root_folder/dist-packages/ --destination-path /usr/lib/python3.9/ --rootfs-filepath $base_image_file

        echo "python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $project_root_folder/aarch64-linux-gnu/ --destination-path /usr/lib/ --rootfs-filepath $base_image_file"
        python3 devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact $project_root_folder/aarch64-linux-gnu/ --destination-path /usr/lib/ --rootfs-filepath $base_image_file
    fi

    #----------------------------------------------------------------------------------------------------------------
    if [ "$aos_runnables" == "-" ]; then
        print_colored_message "Install of AOS runnables wasn't requested" "$BLUE"
    else
        print_colored_message "Run qemu fusion" "$GREEN"

        echo "python3 devops/scripts/python/qemu/qemu_fusion.py install-deb --deb-package $aos_runnables --rootfs-filepath $base_image_file"
        python3 devops/scripts/python/qemu/qemu_fusion.py install-deb --deb-package $aos_runnables --rootfs-filepath $base_image_file
    fi    
}