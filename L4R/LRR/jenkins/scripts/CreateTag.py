# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:19:13 2021

@author: YAH3KOR
"""

import subprocess
import sys

import logging

import argparse

parser = argparse.ArgumentParser(description="Script to create tags")
parser.add_argument("-bn", "--build",
                        help='Build Number', nargs='?', const='5')

args = parser.parse_args()
build_no = str(args.build)


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG,
                     datefmt="%H:%M:%S")

release_path = "//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/LRR/"

import re

build_version_regex = '(LRR_LGU_PF_V\d*.\d*.\d*)'

def get_version(buildCmd , regex):
    try:
        setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    except:
        logging.error("Failed to open a cmd to run commands")
        sys.exit(1)
        
    try:
        buildOut, buildErr = setProcess.communicate(input=buildCmd)
        value = re.search(regex, buildOut).group(1)
        logging.info(buildOut)
        logging.error(buildErr)
        return value
    except:
        logging.error(buildErr)
        logging.info("Getting version failed ..........")
        sys.exit(1)

buildCmd = "cd ../../\n"
buildCmd += 'git describe --tags\n'

release_name = get_version(buildCmd, build_version_regex)

buildCmd = f"git tag {release_name}_pre#{build_no}\n"
buildCmd += 'git push --tags\n'

try:
    setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
              stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
except:
    logging.error("Failed to open a cmd to run commands")
    sys.exit(1)
    
try:
    buildOut, buildErr = setProcess.communicate(input=buildCmd)
    logging.info(buildOut)
    logging.error(buildErr)
except:
    logging.error(buildErr)
    logging.info("Creating git tag failed ..........")
    sys.exit(1)
