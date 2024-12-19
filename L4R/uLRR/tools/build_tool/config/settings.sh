#!/bin/bash
set -e

# Script Name: settings.sh
# Author: C3 Team
# Description: This redefines the environment for ir2-build-tool.

declare -A CONAN_SETTINGS=(
    ["profile_linux_x86-64_debug"]="x86_64_linux_gcc8_debug"
    ["profile_linux_x86-64_debug_build"]="x86_64_linux_gcc8_debug_build"
    ["profile_linux_armv8_debug"]="armv8_linux_gcc8_debug"
    ["profile_linux_armv8_debug_build"]="armv8_linux_gcc8_debug_build"
    ["profile_linux_armv8_release"]="armv8_linux_gcc8_release"
    ["profile_linux_armv8_release_build"]="armv8_linux_gcc8_release_build"
    ["profile_neutrino_armv8_debug"]="armv8_qnx71_qcc83_debug"
    ["profile_neutrino_armv8_debug_build"]="armv8_qnx71_qcc83_debug_build"
    ["conan_recipe_aos"]="software/aos"
    ["conan_recipe_bl"]="software/business_logic"
    ["rootfs_artifact"]="rootfs_tec0204_bullseye_final_arm64_latest.ext4.gz"
    ["rootfs_repository_path"]="zugspitze-series-generic-local/releases/debian-base-image/latest/"
)

declare -A DEB_PCKG_SETTINGS=(
    ["build_folders_to_pckg"]="bin \
                               lib \
                               lib_static \
                               yaaac_codegen/deploy/carma_0_22/car_pc/esme \
                               yaaac_codegen/deploy/carma_0_22/car_pc/manifests \
                               yaaac_codegen/deploy/carma_0_22/car_pc/start_scripts \
                               yaaac_codegen/deploy/carma_0_22/car_pc/stop_scripts \
                               yaaac_codegen/deploy/carma_0_22/${middleware_instance}/esme \
                               yaaac_codegen/deploy/carma_0_22/${middleware_instance}/manifests \
                               yaaac_codegen/deploy/carma_0_22/${middleware_instance}/start_scripts \
                               yaaac_codegen/deploy/carma_0_22/${middleware_instance}/stop_scripts \
                               sw_versions"
    ["scripts_to_pckg"]="${IR2_BUILD_TOOL_PATH}/../../software/ros/scripts"
    ["aos_shared_library"]="libros1cpp_runtime.so \
                            libaos_xmlrpcpp.so"
    ["aos_tools"]="esme"
    ["diag_configs"]="DoIP_config.json \
                      board-ir2.json5"
)

# List of allowed tool options
allowed_projects=("bl" "aos")
allowed_target_types=("armv8" "x86-64")
allowed_build_types=("debug" "release")
allowed_middleware_instances=("tec0204_linux" "te0950_linux" "te0950_neutrino" "car_pc" "testing")
allowed_package_types=("conan" "deb")
allowed_booleans=("true" "false")
