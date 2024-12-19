#!/bin/bash

set -e

# Usage info
show_help() {
cat << EOF
Usage: ${0##*/}
Script to build AOS 18 mirror

EOF
}

OPTIND=1
# Resetting OPTIND

WORK_DIR=$(pwd)/temp_dir/ # The current working directory


while getopts hcibrafd:o:u:x:t:p: opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        *)
            show_help >&2
            exit 1
            ;;
    esac
done

shift "$((OPTIND-1))"   # Discard the options and sentinel --


# Unzip aos-18-installation.zip
unzip aos-18-installation.zip 

# Launch docker env.
cd aos-18-installation

sed -i 's/docker run -it --rm --net host \\/docker run -t -d --rm --net host --name aos_con \\/' "docker-environment.sh"
sudo chmod +x docker-environment.sh
export BOSCH_USER=$(whoami)
./docker-environment.sh

docker exec -t aos_con bash -c "git clone -b release_0.18 ssh://git@sourcecode01.de.bosch.com:7999/aos/aos_base.git"

# setup conan config
docker exec -t aos_con bash -c "\
  cd aos_base; \
  _tools/scripts/conan_config_dev.sh"

# adapt the target to "armv8-a" in cmake_templates
docker exec -t aos_con bash -c "\
  cd aos_base/ext/cross_compiler_toolchain/compiler_utils/cmake_templates/; \
  sed -i 's/string(APPEND CMAKE_CXX_FLAGS \"-march={{ arch }}-a \")/string(APPEND CMAKE_CXX_FLAGS \"-march=armv8-a \")/' \"gcc_options.cmake.j2\" "

# build cross_compiler_toolchain/x86_64_linux_gcc8
docker exec -t aos_con bash -c "\
  cd aos_base; \
  ./build_product -prb ubuntu2004_x86_64_gcc8_debug -pr ubuntu2004_x86_64_gcc8_debug -p ext/cross_compiler_toolchain/x86_64_linux_gcc8"

# build cross_compiler_toolchain/compiler_utils
docker exec -t aos_con bash -c "\
  cd aos_base; \
  ./build_product -prb ubuntu2004_x86_64_gcc8_debug -pr ubuntu2004_x86_64_gcc8_debug -p ext/cross_compiler_toolchain/compiler_utils"

# build cross_compiler_toolchain/armv83_linux_gcc8 locally (attribute -fb: force build)
docker exec -t aos_con bash -c "\
  cd aos_base; \
  ./build_product -prb ubuntu2004_x86_64_gcc8_debug -pr ubuntu1804_armv83_gcc8_debug -p ext/cross_compiler_toolchain/armv83_linux_gcc8 -fb"

# Build AOS (for cross-compilation)
docker exec -t aos_con bash -c "\
  cd aos_base; \
  ./build_product -prb ubuntu2004_x86_64_gcc8_debug -pr ubuntu2004_x86_64_gcc8_debug -p aos_products/dev_tools/; \
  ./build_product -prb ubuntu2004_x86_64_gcc8_debug -pr ubuntu2004_x86_64_gcc8_debug -p aos_products/build_tools"

# exclude "recompute_mock_algo" from aos_products/runtime_development/conanfile.py
docker exec -t aos_con bash -c "\
  cd aos_base/aos_products/runtime_development/; \
  sed -i '/recompute_mock_algo/d' conanfile.py"

# build runtime_development
docker exec -t aos_con bash -c "\
  cd aos_base; \
  ./build_product -prb ubuntu2004_x86_64_gcc8_debug -pr ubuntu1804_armv83_gcc8_debug -p aos_products/runtime_development -fb; \
  ./build_product -prb ubuntu2004_x86_64_gcc8_debug -pr ubuntu1804_armv83_gcc8_debug -p aos_products/runtime_production"




docker stop aos_con

# rm -rf WORK_DIR
# Remove temp_dir folder
