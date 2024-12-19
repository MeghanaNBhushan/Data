  #!/usr/local/bin/ python3
import os
import shutil
import argparse
import time
import copy
import yaml
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.abspath(os.path.join(SCRIPT_DIR,  "..","..","..",".."))

def parse_arguments():
    # parses the commandline parameters
    # Getting the directory,variant and measurement files  from the argument

    parser = argparse.ArgumentParser(description="script to create directory")
    parser.add_argument("-d", "--directory", help="Path of target directory", required=True)
    parser.add_argument("-v", "--variant", help="Name of variant", required=True)
    parser.add_argument("-dc", "--directory_config", help='Path of the directory configuration file', required=True)
    args = parser.parse_args()
    return args

def create_directory(args):
    try:
        with open(os.path.join(SCRIPT_DIR,args.directory_config), 'r') as config_file:
            directory_structure_data = yaml.load(config_file, Loader=yaml.FullLoader)
    except:
        print(f"[E] given directory configuration file '{args.directory_conifg}' is not a valid yaml format")
        sys.exit(1)

    target_dir = os.path.abspath(os.path.join(args.directory, directory_structure_data['targetDir']))
    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir,ignore_errors=True)
    for folders in directory_structure_data['content']:
        src_raw = os.path.join(REPO_DIR, folders['source'])
        src = src_raw.replace("VARIANT", args.variant)
        dst_raw = os.path.join(target_dir, folders['dest'])
        dst = dst_raw.replace("VARIANT", args.variant)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        elif os.path.isfile(src):
            if not os.path.exists(os.path.dirname(dst)):
                os.makedirs(os.path.dirname(dst))
            shutil.copy2(src, dst)
        else:
            print(f"[E] given source path'{src}' does not exist")
            sys.exit(1)

def main():
    args = parse_arguments()
    create_directory(args)

if __name__ in "__main__":
    main()
