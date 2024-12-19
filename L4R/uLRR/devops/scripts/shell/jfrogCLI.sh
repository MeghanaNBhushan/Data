#!/bin/bash

set -e

# Usage info
show_help() {
cat << EOF
Usage: ${0##*/} [-hd]
Script to interface with JFROG artifactory

    -h          display this help and exit
    -d          download artifact
    -r          repository path
    -o          output path

EOF
}

config_file="$HOME/.jfrog/jfrog-cli.conf"

# Initialize variables:
flag_configure_artifactory=false
flag_download_artifact=false

OPTIND=1
# Resetting OPTIND


while getopts hcdr:o: opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        d)  echo "Download artifact"
            flag_download_artifact=true
            ;;
        r)  repository_path=$OPTARG
            echo "Specifying repository path"
            ;;
        o)  outputh_path=$OPTARG
            echo "Specifying output path"
            ;;
        *)
            show_help >&2
            exit 1
            ;;
    esac
done
shift "$((OPTIND-1))"   # Discard the options and sentinel --

echo "Received input arguments"
echo "repository_path=$repository_path"
echo "outputh_path=$outputh_path"

# ---------------------------------------------------------------------------------
# Testing if is there any configuration set
# Run the command and capture the output
config_output=$(jfrog config s)

# Extract Server ID
server_id=$(echo "$config_output" | awk '/Server ID:/ {print $NF}')

# Check if Server ID is equal to "zugspitze-series-generic-local"
if [ "$server_id" == "zugspitze-series-generic-local" ]; then
  echo "Server ID is zugspitze-series-generic-local"
else
  echo "Server ID is not zugspitze-series-generic-local"

  echo "Do you want to add zugspitze-series-generic-local's configuration to JFrog CLI? (y/n)"
  read user_response
  
  if [[ "$user_response" == "y" ]]; then
    echo "Please provide the following information:"
    
    echo -n "Username: "
    read username
    
    echo -n "API Key: "
    read -s password
    
    echo -e "\nAdding configuration..."
  
    # Add the configuration using jfrog config command
    jfrog config add "zugspitze-series-generic-local" --url="https://artifactory.boschdevcloud.com/" --user="$username" --password="$password" --interactive="false"
    
    echo "Configuration added successfully."
  elif [[ "$user_response" == "n" ]]; then
    echo "No configuration added."
  else
    echo "Invalid response. Please enter 'y' or 'n'."
  fi

fi

# ---------------------------------------------------------------------------------
# Testing if JFrog Artifactory is working
# Run the jfrog rt ping command
ping_output=$(jfrog rt ping)

# Check if the ping was successful
if [[ "$ping_output" == *"OK"* ]]; then
  echo "Connection to Artifactory is OK"
else
  echo "Connection to Artifactory failed"
  exit 1
fi


if $flag_download_artifact; then
  echo "Flag -flag_download_artifact is set"

  jfrog rt dl $repository_path $outputh_path
fi
