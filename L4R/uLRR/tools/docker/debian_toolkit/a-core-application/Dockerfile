FROM ubuntu:20.04

ARG CONANUSER
ARG CONANTOKEN

ENV DEBIAN_FRONTEND=noninteractive
ENV UID=1001
ENV GID=1001
ENV UNAME=AzDevOps
ENV CROSS=aarch64-linux-gnu
ENV INSTALL_MMIC_DIR=/opt/bosch/ulrr/cross-compilation/python
ENV TARGET_DIR=/data/usr

# configure system language
RUN     apt-get update && apt-get install -y locales && \
        locale-gen en_US.UTF-8 && \
        update-locale LANG=en_US.UTF-8 && \
        rm -rf /var/lib/apt/lists/*
ENV     LANG=en_US.UTF-8 \
        LANGUAGE=en_US:en \
        LC_ALL=en_US.UTF-8


# Install basics 
RUN     apt-get update && apt-get install -y ca-certificates curl gnupg wget sudo

# Install apt packages
COPY    apt_packages.txt apt_packages.txt
RUN     touch /etc/apt/apt.conf.d/99verify-peer.conf && \
        echo >> /etc/apt/apt.conf.d/99verify-peer.conf "Acquire { https::Verify-Peer false }" && \
        wget -qO - https://releases.jfrog.io/artifactory/jfrog-gpg-public/jfrog_public_gpg.key | sudo apt-key add - && \
        echo "deb https://releases.jfrog.io/artifactory/jfrog-debs xenial contrib" | sudo tee -a /etc/apt/sources.list && \
        echo "deb http://packages.ros.org/ros/ubuntu focal main" | tee /etc/apt/sources.list.d/ros-latest.list && \
        curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add - && \
        wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null && \
        echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ focal main' | sudo tee /etc/apt/sources.list.d/kitware.list >/dev/null && \
        apt-get update && apt-get install -y wget software-properties-common && \
        wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - && \
        add-apt-repository "deb http://apt.llvm.org/focal/ llvm-toolchain-focal main" && \
        apt-get install -q -y --no-install-recommends $(grep -v '^#' apt_packages.txt) && \
        rm -rf /var/lib/apt/lists/* && \
        rm apt_packages.txt && \
        apt-get clean

# Install SCA package, configure and update python alternatives
COPY    helix-qac-2023.2~tcc.deb helix-qac-2023.2~tcc.deb
# Configure SCA tools and update python alternatives
RUN     sudo dpkg -i helix-qac-2023.2~tcc.deb && \
        update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 10 && \
        update-alternatives --install /usr/bin/clangd clangd /usr/bin/clangd-12 100 && \
        ln -sf /usr/bin/clangd-12 /usr/bin/clangd

# Install pip provided packages 
COPY    pip_packages.txt pip_packages.txt
RUN     python3 -m pip install -i https://${CONANUSER}:${CONANTOKEN}@artifactory.boschdevcloud.com/artifactory/api/pypi/tcc-pypi-local/simple --no-cache-dir swq-sca-tools==1.11.1 && \
        python3 -m pip install $(grep -v '^#' pip_packages.txt) --upgrade numpy --upgrade scipy && \
        rm pip_packages.txt

ENV     PATH="/home/$UNAME/.local/bin:${PATH}"
ENV     PATH="$PATH:/opt/Perforce/Helix-QAC-2023.2/common/bin"

# Add BOSCH proxy certs into the docker container
COPY    certs/*  /usr/local/share/ca-certificates/
RUN     dpkg-reconfigure ca-certificates && \
        sed --in-place --regexp-extended --expression='s|!(.*)|\1|g' /etc/ca-certificates.conf && \
        update-ca-certificates --verbose --fresh

# Create and configure local User and 
RUN     groupadd -g $GID -o $UNAME && \
        adduser --disabled-password --uid $UID --gid $GID --force-badname $UNAME && \
        passwd -d $UNAME && \
        usermod -aG sudo $UNAME;

# No password for sudo commands
RUN     mkdir /etc/sudoers.d &>/dev/null && \
        echo "ALL ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/nopassword

# toolchain cmake config for cross-compilation
RUN     mkdir -p /opt/bosch/ulrr/toolchains-cmake
COPY    toolchains-cmake /opt/bosch/ulrr/toolchains-cmake

# Cross compilation of Python for MMIC driver in AARCH64
COPY    mmic_cross_compile.sh mmic_cross_compile.sh
RUN     mkdir -p /opt/bosch/ulrr/cross-compilation/source/config
COPY    Python3.9.5-glibc.tar.xz /opt/bosch/ulrr/cross-compilation/source
RUN     ./mmic_cross_compile.sh /opt/bosch/ulrr/cross-compilation/source

# Install aarch64-sysroot
COPY    ulrr-aarch64-sysroot-bullseye_0.0.0_amd64.deb /opt/bosch/ulrr/
RUN     apt install ./opt/bosch/ulrr/ulrr-aarch64-sysroot-bullseye_0.0.0_amd64.deb && \
        rm /opt/bosch/ulrr/ulrr-aarch64-sysroot-bullseye_0.0.0_amd64.deb

# Deploy the githook        
RUN     mkdir -p /githooks
COPY    githooks/pre-commit /githooks

# Login User
USER    $UNAME

# "Install" GDB pretty-printer
COPY    gdbinit ~/.gdbinit

# Configure Conan
RUN     conan remote add aos-conan-release-local https://artifactory.boschdevcloud.com/artifactory/api/conan/aos-conan-release-local && \
        conan remote add aos-conan-staging-local https://artifactory.boschdevcloud.com/artifactory/api/conan/aos-conan-staging-local && \
        conan remote add zugspitze-series-conan-local https://artifactory.boschdevcloud.com/artifactory/api/conan/zugspitze-series-conan-local && \
        conan user -p ${CONANTOKEN} -r aos-conan-release-local ${CONANUSER} && \
        conan user -p ${CONANTOKEN} -r aos-conan-staging-local ${CONANUSER} && \
        conan user -p ${CONANTOKEN} -r zugspitze-series-conan-local ${CONANUSER} && \
        conan config set general.parallel_download=8 && \
        conan config set general.revisions_enabled=1 && \
        conan config set general.default_profile=x86_64_linux_gcc8_debug
COPY    \
        conan_config/profiles/armv8_linux_gcc8_debug \
        conan_config/profiles/armv8_linux_gcc8_debug_build \
        conan_config/profiles/armv8_linux_gcc8_release \
        conan_config/profiles/armv8_linux_gcc8_release_build \
        conan_config/profiles/armv8_qnx71_qcc83_debug \
        conan_config/profiles/armv8_qnx71_qcc83_debug_build \
        conan_config/profiles/armv8_qnx71_qcc83_release \
        conan_config/profiles/armv8_qnx71_qcc83_release_build \
        conan_config/profiles/linux_dev \
        conan_config/profiles/x86_64_linux_gcc8_debug \
        conan_config/profiles/x86_64_linux_gcc8_debug_build \
        conan_config/profiles/x86_64_linux_gcc8_release \
        conan_config/profiles/x86_64_linux_gcc8_release_build \
        conan_config/profiles/x86_64_qnx71_qcc83_debug \
        conan_config/profiles/x86_64_qnx71_qcc83_debug_build \
        conan_config/profiles/x86_64_qnx71_qcc83_release \
        conan_config/profiles/x86_64_qnx71_qcc83_release_build \
        /home/AzDevOps/.conan/profiles/

# Install AOS Conan recipe
COPY    conanfile.py /home/AzDevOps/

# # build_x86_64
# RUN     cd /home/AzDevOps/ && \
#         rm -rf build_x86_64 && mkdir build_x86_64 && cd build_x86_64 && mkdir build_x86_64_exe && cd .. && \
#         conan install ./ -if=./build_x86_64 -pr:h=x86_64_linux_gcc8_debug  -pr:b=x86_64_linux_gcc8_debug_build && \
#         rm -rf build_x86_64
# # build_armv8
# RUN     cd /home/AzDevOps/ && \
#         rm -rf build_armv8 && mkdir build_armv8 && cd build_armv8 && mkdir build_armv8_exe && cd .. && \
#         conan install ./ -if=./build_armv8 -pr:h=armv8_linux_gcc8_debug  -pr:b=armv8_linux_gcc8_debug_build && \
#         rm -rf build_armv8

# Install V-GETK
COPY    config.ini install.sh /home/AzDevOps/
RUN     cd /home/AzDevOps/ && \
        ./install.sh && \
        rm config.ini install.sh

CMD     ["/bin/bash"]
