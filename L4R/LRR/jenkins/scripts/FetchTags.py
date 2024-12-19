# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:19:13 2021

@author: YAH3KOR
"""

import subprocess
import sys

import logging


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG,
                     datefmt="%H:%M:%S")


#next release is assumed to be next incremental major version
buildCmd = "git fetch --tags\n"

try:
    setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
              stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
except:
    logging.error("Failed to open a cmd to run commands")
    sys.exit(-1)
    
try:
    buildOut, buildErr = setProcess.communicate(input=buildCmd)
    logging.info(buildOut)
    logging.error(buildErr)
except:
    logging.error(buildErr)
    logging.info("Fetching git tags failed ..........")
    sys.exit(-1)
