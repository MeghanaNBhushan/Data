FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

ARG UID=1001
ARG GID=1001
ARG UNAME=AzDevOps

# configure system language
RUN     apt-get update && apt-get install -y locales && \
        locale-gen en_US.UTF-8 && \
        update-locale LANG=en_US.UTF-8 && \
        rm -rf /var/lib/apt/lists/*
ENV     LANG=en_US.UTF-8 \
        LANGUAGE=en_US:en \
        LC_ALL=en_US.UTF-8


# Install required apt packages from public repo
COPY    packages.txt packages.txt
RUN     apt-get update && apt-get install -y --no-install-recommends $(grep -v '^#' packages.txt) && \
        rm -rf /var/lib/apt/lists/* && \
        rm packages.txt


# Install Vitis
COPY    install-packages.sh .
RUN     chmod +x ./install-packages.sh
RUN     --mount=type=bind,source=.,target=/buildcontext ./install-packages.sh


# Install conan
RUN     pip install conan==1.56 && \
        mkdir -p /root/.conan/profiles


# Add BOSCH proxy certs into the docker container
COPY    certs/*  /usr/local/share/ca-certificates/
RUN     dpkg-reconfigure ca-certificates && \
        sed --in-place --regexp-extended --expression='s|!(.*)|\1|g' /etc/ca-certificates.conf && \
        update-ca-certificates --verbose --fresh


# Create and configure local User
RUN     groupadd -g $GID -o $UNAME && \
        adduser --disabled-password --uid $UID --gid $GID --force-badname $UNAME && \
        passwd -d $UNAME && \
        usermod -aG sudo $UNAME;


# Having free house ;-)
RUN     mkdir /etc/sudoers.d &>/dev/null && \
        echo "ALL ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/nopassword


