#!/usr/local/bin/ python3

"""
Script to create releases from a source repository in another release repository.
- Multiple releases with different content can be created
    - content can be a list folders and a list files for each release
- structure changes possible 
    - folders or submodules inside of sub-folders in the source repository can be moved up in the folder hierarchy in
      the release
"""

import os
import sys
import subprocess
import shutil
import configparser
import argparse
import git
import re
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import logging

LOG = None

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
START_DIR = os.getcwd()
SBX_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..",".."))

class Config(object):
    file_extensions = []
    folders = []


def parse_args():
    """Reads the input parameters"""
    parser = argparse.ArgumentParser(description='Script to create a package for an FOSS scan',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-c", "--config-path", help="Path and name of config file",
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "foss.cfg"))
    parser.add_argument("-s", "--source", help='Path to the source where the FOSS relevant files are copied from',
                        default=SBX_ROOT)
    parser.add_argument("-d", "--destination",
                        help='Path to the destination where the FOSS relevant files are copied to', required=True)

    args = parser.parse_args()
    args.config_path = os.path.abspath(args.config_path)
    args.source = os.path.abspath(args.source)
    print(args.source)
    args.destination = os.path.abspath(args.destination)
    return args	


def get_version(buildCmd , regex):
    try:
        setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    except:
        sys.exit(-1)
        
    try:
        buildOut, buildErr = setProcess.communicate(input=buildCmd)
        value = re.search(regex, buildOut).group(1)
        return value
    except:
        sys.exit(-1)

def __get_config_list(config_value):
    config_list = []
    if config_value:
        config_list = list()
        for element in config_value.split(","):
            config_list.append(element.strip())
    # we sort the list so everything is processed alphabetically
    config_list.sort()
    return config_list


def read_configfile(config_path):
    required_config_options = ["folders", "file_extensions"]
    section_name = "FOSS"
    
    if not os.path.isfile(config_path):
        logging.error(f"configfile file '{config_path}' was not found")
        sys.exit(1)
        
    configfile = configparser.ConfigParser()
    configfile.read(config_path)
    
    if not configfile.has_section(section_name):
        logging.error(f"configfile file '{config_path}' does not contain a [{section_name}] section")
        sys.exit(1)

    for option in required_config_options:
        if not configfile.has_option(section_name, option):
            logging.error(f"Missing required option '{option}' in [{section_name}] section of config file")
            sys.exit(1)

    config = Config()
    for key, value in configfile[section_name].items():
        setattr(config, key, __get_config_list(value))
    return config


def copy_files(source, dest, file_extensions):
    if not os.path.isdir(source):
        logging.error(f"Source directory '{source}' does not exist")
        sys.exit(1)
    logging.info(f"Copying files from  '{source}' to '{dest}'")

    copied_files = []
    for root, _, filenames in os.walk(source):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in file_extensions:
                source_file = os.path.join(root, filename)
                relative_path = os.path.relpath(source_file, source)
                dest_file = os.path.join(dest, relative_path)
                copied_files.append(relative_path)
                directory, _ = os.path.split(dest_file)
                try:
                    os.makedirs(directory, exist_ok=True)
                    shutil.copy(source_file, dest_file)
                except Exception as ex:
                    logging.error(f"Failed to copy '{source_file}' to '{dest_file}' with exception:\n {str(ex)} ")
                    sys.exit(1)

    logging.info(f"Copied {len(copied_files)} files from '{source}'", 1)


def create_git_info_file(repo_path, dest):
    logging.info("Creating file containing information about the current git revision of source")
    git_repo = git.Repo(repo_path)
    commit = git_repo.head.commit
    if not commit:
        logging.error("Current revision to use could not be found. -> skipping", 1)
        sys.exit(1)
    logging.info("Current revision is '{}'.".format(commit), 1)

    filename = f"{commit}.info"
    file_content = f"Commit: {commit}\n"

    # get tag on the current commit matching the pattern
    pattern = r"PJIF_\d{4}\.\d+\.\d+(?:-.*)?$"
    tag = next((tag.name for tag in git_repo.tags if (re.compile(pattern).match(tag.name.strip())
                                                      and tag.commit == commit)), None)
    if tag:
        logging.info(f"Found tag '{tag}' for current revision.", 1)
        filename = f"{tag}.info"
        file_content += f"Tag: {tag}\n"
    with open(os.path.join(dest, filename), 'w') as info_file:
        info_file.write(file_content)


def main():
    """Main function to call when this script is called directly and not imported"""
    args = parse_args()

    build_version_regex = '(ROS_LGU_PF_V\d*.\d*.\d*)'

    buildCmd = "cd ../../../athena_mt/tools/ROS4LGP/\n"
    buildCmd += 'git describe --tags\n'

    release_name = get_version(buildCmd, build_version_regex)

    Version = re.search('(V\d*.\d*.\d*)', release_name).group(1)	

    destination=args.destination+'_ROS4LGP_LGU_PF_'+Version+'/FOSS_ROS4LGP_LGU_PF_'+Version

    config = read_configfile(args.config_path)
    for folder in config.folders:
        src = os.path.join(args.source, folder)
        dest = os.path.join(destination, folder)
        copy_files(src, dest, config.file_extensions)

    create_git_info_file(args.source, destination)


if __name__ in "__main__":
    main()