#!/bin/sh

# Script version, for traceability with VM image version
script_version=2.0.2

# List of packages to be installed
list_of_dependencies=(
    "ca-certificates" 
    "curl" 
    "apt-transport-https" 
    "lsb-release" 
    "gnupg"
    "wget"
    "software-properties-common")

list_of_packages=(
    "git-lfs" 
    "azure-cli" 
    "powershell"
    "docker-ce" 
    "docker-ce-cli" 
    "containerd.io" 
    "docker-compose-plugin"
    "zip")


# Docker image to be loaded (if Vitis is required)
image_name="vitis-v2021.2"

##### Install dependencies for preparation #####
sudo apt-get update
sudo apt-get install "${list_of_dependencies[@]}" -y


##### Preperation of required repos #####
curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null # Add Azrue official GPG key
echo "deb [arch=$(dpkg --print-architecture)] https://packages.microsoft.com/repos/azure-cli/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/azure-cli.list # Set up the azure repository

wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb"
sudo dpkg -i packages-microsoft-prod.deb

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg # Add Docker’s official GPG key
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null # Set up the docker repository

##### Install Packages #####
sudo apt-get update
sudo apt-get install "${list_of_packages[@]}" -y

##### Setup Vitis docker container #####
# Check if the flag is given
if [ "$1" == "--vitis_required" ]; then
  echo "Executing the portion of code"
  wget https://aka.ms/downloadazcopy-v10-linux
  tar -xzf downloadazcopy-v10-linux
  azcopy_linux_amd64_*/azcopy copy "https://swbuildst.file.core.windows.net/debian-build/Vitis/docker_container/vitis-v2021.tar?sv=2021-12-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-03-30T20:50:12Z&st=2023-03-30T11:50:12Z&spr=https&sig=v4ZpnSuOVyOdZuslPo%2B8KAxZeK1wzKUqWG5KFRxpJcs%3D" "vitis-v2021.tar"
  docker load -i vitis-v2021.tar
  # Check if the image is loaded
  if docker images | grep -q $image_name; then
    echo "The $image_name image is loaded."
  else
    echo "The $image_name image is not loaded."
    exit 1
  fi
else
  echo "Skipping the portion of code"
fi



##### add AzDevOps user #####

sudo adduser --disabled-password --uid 1001 --force-badname --gecos "" AzDevOps
sudo passwd -d AzDevOps 
sudo usermod -aG sudo AzDevOps
sudo usermod -aG docker AzDevOps

sudo echo $script_version > /home/AzDevOps/IMAGEVERSION
