FROM artifactory.boschdevcloud.com/zugspitze-series-docker-local/petalinux-v2021.2:latest
USER root
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies and ROS
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(grep "UBUNTU_CODENAME" /etc/os-release | cut -d= -f2) main" > /etc/apt/sources.list.d/ros-latest.list' && \
    curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add - && \
    apt-get update && \
    apt-get install -y bc rpm ninja-build gnupg ros-noetic-desktop

# Setup environment
USER AzDevOps

RUN mkdir -p /home/AzDevOps/petalinux/sdk-v2021.2

ADD zcu-102 /home/AzDevOps/petalinux/zcu-102

# Install SDK
RUN sudo chown -R AzDevOps:AzDevOps /home/AzDevOps/petalinux/ && \
    cd /home/AzDevOps/petalinux/zcu-102 && \
    source /petalinux/2021.2/settings.sh && \
    petalinux-package --sysroot --sdk /home/AzDevOps/petalinux/zcu-102/images/linux/sdk.sh --dir /home/AzDevOps/petalinux/sdk-v2021.2/ && \
    rm -r /home/AzDevOps/petalinux/zcu-102

CMD ["/bin/bash"]
