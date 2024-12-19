FROM    artifactory.boschdevcloud.com/zugspitze-series-docker-local/a-core-application:3.4.2

ARG     UNAME

# Set root user
USER    root

# Create local user
RUN     adduser --disabled-password --force-badname $UNAME && \
        passwd -d $UNAME && \
        usermod -aG sudo $UNAME;

# Set up 'conangroup' for shared '/home/AzDevOps/.conan/' access between 'AzDevOps' and local user.
RUN     sudo groupadd conangroup && \
        sudo usermod -aG conangroup AzDevOps && \
        sudo usermod -aG conangroup $UNAME && \
        sudo chown -R :conangroup /home/AzDevOps/.conan/ && \
        sudo chmod -R 775 /home/AzDevOps/.conan/ && \
        ln -s /home/AzDevOps/.conan/ /home/$UNAME/.conan

# Set user
USER    $UNAME

CMD     ["/bin/bash"]
