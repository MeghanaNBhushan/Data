FROM artifactory.boschdevcloud.com/zugspitze-series-docker-local/ubuntu:20.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ARG DEBIAN_FRONTEND=noninteractive

ARG PETA_RUN_FILE=petalinux-v2021.2-final-installer.run

ARG UID=1001
ARG GID=1001
ARG UNAME=AzDevOps


# Obtains necessary packages and updates certificates
SHELL ["/bin/bash", "-c"]
RUN to_fetch='git cmake build-essential ca-certificates curl git-lfs build-essential net-tools xterm autoconf libtool texinfo zlib1g-dev gcc-multilib libncurses5-dev zlib1g ncurses-dev zlib1g:i386 make perl dkms gawk g++-multilib automake libtool autopoint libtinfo5 xterm unzip zip rsync cpio curl apt-transport-https iputils-ping xxd' && \
  dpkg --add-architecture i386 && \
  apt-get update && \
  apt-get install -y ${to_fetch} && \
  apt-get clean && \
#  apt-get autoremove -y && \
#  apt-get autoclean && \
  rm -rf /var/lib/apt/lists/* && \
  update-ca-certificates;

SHELL ["/bin/bash", "-c"]
RUN apt-get update && \
  apt-get install -qqy locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Set timezone inside Docker container
ENV TZ=America/New_York
SHELL ["/bin/bash", "-c"]
RUN echo $TZ > /etc/timezone && \
  apt-get update && apt-get install -qqy tzdata && \
  rm /etc/localtime && \
  dpkg-reconfigure -f noninteractive tzdata

ADD $PETA_RUN_FILE ./

SHELL ["/bin/bash", "-c"]
RUN chmod a+rx /${PETA_RUN_FILE} &&\
  mkdir -p /mnt/peta-transfer && \
  mkdir -p /etc/smbcredentials && \
  groupadd -g $GID -o $UNAME && \
  adduser --disabled-password --uid $UID --gid $GID --force-badname $UNAME && \
  passwd -d $UNAME && \
  usermod -aG sudo $UNAME;

USER $UNAME


SHELL ["/bin/bash", "-c"]
RUN  sudo mkdir -m 777 -p /petalinux && sudo mv /${PETA_RUN_FILE} /petalinux && sudo chown -hR $UNAME /petalinux && chmod 755 /petalinux && \
  sudo mkdir -m 755 -p /petalinux/2021.2 && sudo chown -hR $UNAME /petalinux/2021.2 && cd /petalinux && \
  yes | /petalinux/${PETA_RUN_FILE} --dir ./2021.2 --platform "arm aarch64" && rm -frv /petalinux/${PETA_RUN_FILE} && \
  yes no |sudo dpkg-reconfigure dash  ;

CMD ["/bin/bash"]
