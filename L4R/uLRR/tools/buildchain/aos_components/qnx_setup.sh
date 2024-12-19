#!/bin/bash

set -e
#--------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------
# ENV var 
export QNX_SOFTWARE_CENTER_VERSION="qnx-setup-2.0-202209011607-linux.run"
export QNX_SETUP_BIN="https://artifactory.boschdevcloud.com/artifactory/aosp-generic-external-remote/"

export QNX_LICENSE_KEY=79KJ-JNCV-6NP6-SC9L-50JH

if [ "$1" = "cloud" ]; then
    export FLEXLMRC_SERVER=6287@rb-lic-qnxlm-xc-cloud.bosch.tech
else
    export FLEXLMRC_SERVER=6287@10.58.140.79
fi
#--------------------------------------------------------------------------------------------------------
sudo apt-get update
sudo apt-get install -y expect

#--------------------------------------------------------------------------------------------------------
# Download Software Center from Artifactory
echo "INFO: Downloading QNX Software Center from Artifactory..."
mkdir -p $HOME/tmp
curl "https://swbuildir2st.file.core.windows.net/qnx-build/qnx_setup/qnx-setup-2.0-202209011607-linux.run?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-12-01T21:49:04Z&st=2024-05-23T12:49:04Z&spr=https&sig=zjVg1zOCbrwSLx4F8TuZ8SvXtIO3%2B7DqiuoymqDS5wI%3D" -o $HOME/tmp/${QNX_SOFTWARE_CENTER_VERSION}
chmod a+x $HOME/tmp/${QNX_SOFTWARE_CENTER_VERSION}

#--------------------------------------------------------------------------------------------------------
# Install QNX Software Center
/usr/bin/expect << EOE
spawn $HOME/tmp/${QNX_SOFTWARE_CENTER_VERSION} --quiet --nox11 --nochown
expect "press q to scroll to the bottom of this agreement"
send -- "q\n"
expect "Please type y to accept, n otherwise:"
send -- "y\n"
send -- "\n"
expect
EOE

# Add QNX license
echo "${BOLD}${BLUE}INFO: Add QNX license${NORMAL}"
$HOME/qnx/qnxsoftwarecenter/qnxsoftwarecenter_clt -addLicenseKey ${QNX_LICENSE_KEY}

# Create .flexlmrc
echo "QNXLM_LICENSE_FILE=${FLEXLMRC_SERVER}"  > $HOME/.flexlmrc