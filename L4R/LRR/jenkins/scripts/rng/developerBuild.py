# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 08:02:02 2021

@author: YAH3KOR
"""
import json
import argparse
import re
from datetime import date
import os
import distutils.dir_util
import distutils.file_util
import shutil
import logging
import threading 
from time import sleep


parser = argparse.ArgumentParser(description="Script to trigger rng builds")
parser.add_argument("-exp", "--export",
                        help='Export', nargs='?', const='true')
parser.add_argument("-cnv", "--convert",
                        help='Convert', nargs='?', const='true')
parser.add_argument("-cmp", "--compile",
                        help='Compile', nargs='?', const='true')
parser.add_argument("-crt", "--create",
                        help='Create', nargs='?', const='true')
parser.add_argument("-pub", "--publish",
                        help='Publish', nargs='?', const='true')

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG,
                     datefmt="%H:%M:%S")



args = parser.parse_args()

import subprocess
import sys
      
buildCmd = 'cd ../../../ad_radar_apl/tools/rng\n '
if str(args.export) == 'true':
    buildCmd  += '01_rng_export.bat\n'
if str(args.convert) == 'true':
    buildCmd  += '02_rng_convert.bat\n'
if str(args.compile) == 'true':
    buildCmd  += '03_rng_compile.bat\n'
if str(args.create) == 'true':
    buildCmd  += '04_rng_create.bat\n'
if str(args.sign) == 'true':
    buildCmd  += '05_rng_sign.bat\n'
if str(args.publish) == 'true':
    buildCmd  += '06_rng_publish.bat\n'

try:
    setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
              stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
except:
    logging.error("Failed to open a cmd to run commands")
    sys.exit(-1)
    
try:
    buildOut, buildErr = setProcess.communicate(input=buildCmd)
    logging.info(buildOut)
    logging.info(buildErr)
except:
    logging.error(buildErr)
    logging.info("An rng stage failed ..........")
    sys.exit(-1)
