#!/bin/bash
set -e

# Identifying the execution 
running_folder=$PWD
echo "Running script from: $running_folder"

if [[ "$running_folder" == "/__w/1/s" ]]; then
  echo "Running on cloud..."
  project_root_folder=$running_folder/
elif [[ -n $WORKSPACE_FOLDER ]]; then
  echo "Running on devcontainer"
  project_root_folder=$WORKSPACE_FOLDER/
elif git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "Running inside a project repository"
  git_remote_url=$(git config --get remote.origin.url)
  repo_name=$(basename -s .git "$git_remote_url" | sed 's/\.git$//')
  echo "Git repository name: $repo_name"

  project_root_folder=$(git rev-parse --show-toplevel)/
else
  echo "Unknown environment"
  exit 1
fi

echo "Project root folder: $project_root_folder"

if [[ "$running_folder" != "$project_root_folder" ]]; then
  echo "Chaging folder to : $project_root_folder"
  cd $project_root_folder
fi

export IR2_BUILD_TOOL_PATH=$project_root_folder"tools/build_tool"
echo "IR2_BUILD_TOOL_PATH: $IR2_BUILD_TOOL_PATH"
export PATH="$IR2_BUILD_TOOL_PATH:$PATH"
echo "PATH: $PATH"

echo "export IR2_BUILD_TOOL_PATH=$IR2_BUILD_TOOL_PATH" >> /home/$(whoami)/.bashrc
echo "export PATH=\"\$IR2_BUILD_TOOL_PATH:\$PATH\"" >> /home/$(whoami)/.bashrc
