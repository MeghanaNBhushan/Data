#!/bin/bash

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for
# details.
set -euo pipefail

# Tell apt-get we're never going to be able to give manual
# feedback:
export DEBIAN_FRONTEND=noninteractive

# dpkg --add-architecture i386

# Update the package listing, so we know what package exist:
apt-get update

# Install security updates:
# apt-get -y upgrade

# Update certificates
# update-ca-certificates

# Install Vitis tool prerequisites
apt-get -y install --no-install-recommends g++ \
                                            git \
                                            graphviz \
                                            libc6-dev-i386 \
                                            libtinfo5 \
                                            libncursesw5 \
                                            make \
                                            net-tools \
                                            unzip \
                                            x11-utils \
                                            xvfb

# # Install the "payload" of this container: e.g. qemum, debootstrap, git
apt-get -y install --no-install-recommends aptitude \
                                            bc \
                                            binfmt-support \
                                            bison \
                                            ca-certificates \
                                            cpio \
                                            curl \
                                            debootstrap \
                                            flex \
                                            git \
                                            git-lfs \
                                            gnupg \
                                            kmod \
                                            libssl-dev \
                                            libyaml-0-2 \
                                            locales \
                                            locales-all \
                                            nano \
                                            net-tools \
                                            openssl \
                                            qemu-user-static \
                                            quilt \
                                            rpm \
                                            sudo \
                                            symlinks \
                                            u-boot-tools \
                                            vim

# Delete cached files we don't need anymore (note that if you're
# using official Docker images for Debian or Ubuntu, this happens
# automatically, you don't need to do it yourself):
apt-get clean
# Delete index files we don't need anymore:
rm -rf /var/lib/apt/lists/*

# Install Vitis
cd buildcontext/Xilinx_Unified_2021.2_1021_0703
./xsetup -b Add -a XilinxEULA,3rdPartyEULA -c ../xilinx_install_config.txt
