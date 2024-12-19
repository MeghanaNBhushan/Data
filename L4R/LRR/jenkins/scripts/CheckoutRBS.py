# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:19:13 2021

@author: YAH3KOR
"""

import subprocess
import sys

import logging
import argparse
import urllib3
import requests
import json
import getpass
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="Script to checkout the latest RBS")


parser.add_argument("-bn", "--buildNumber",
                        help='Build Number', nargs='?', const="6")
parser.add_argument("-hw", "--hardware",
                        help='Hardware', nargs='?', const="C0")

args = parser.parse_args()
logger_console_handler = logging.StreamHandler()
logger_console_handler.setLevel(logging.DEBUG)
        
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_console_handler.setFormatter(log_format)
    
        
logger = logging.getLogger("Checkout_RBS")
logger.setLevel(logging.DEBUG)
logger.addHandler(logger_console_handler)

build_url = 'https://rb-jmaas.de.bosch.com/CC-DA_ESI6/job/ATR/job/SW_Build/job/pf_rbs/' + args.buildNumber + '/'

headers = {"Content-Type": "application/json"}

USER = getpass.getuser()

PASS = os.environ["COVERITY_PASSWORD"]

commit_url = "https://sourcecode01.de.bosch.com/rest/api/1.0/projects/ARAS/repos/pf_rbs/commits?until=develop&limit=1"
commit_id = None
response = requests.get(commit_url, auth=(USER, PASS), headers=headers)
if response.status_code == requests.codes.ok:
    commit_id = json.loads(response.text)["values"][0]["id"]
    logger.info(f"SUCCESS - Obtained commit id {commit_id} to checkout")
else :    
    logger.error(response.text)
    sys.exit(-1)

if commit_id : 
    buildCmd = "cd ../../athena_mt/pf_rbs\n"
    buildCmd += 'git reset --hard\n'
    buildCmd += 'git clean -fdx\n'
    buildCmd += f'git checkout {commit_id}\n'
        
    try:
        setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    except:
        logger.error("Failed to open a cmd to run commands")
        sys.exit(1)
        
    try:
        buildOut, buildErr = setProcess.communicate(input=buildCmd)
        logger.info(buildOut)
        logger.error(buildErr)
    except:
        logger.error(buildErr)
        logger.info("Checking out rbs develop failed ..........")
        sys.exit(1)
    
    build_status = {
        "state": "INPROGRESS",
        "key": "RBS_SW_BUILD_"+args.hardware,
        "url": build_url
    }
    status_url = "https://sourcecode01.de.bosch.com/rest/build-status/1.0/commits/"+commit_id
    
    response = requests.post(status_url, auth=(USER, PASS), headers=headers, json=build_status)
    
    if response.status_code == 200 or response.status_code == 204 :
        logger.info(f"SUCCESS - Transmit status IN-PROGRESS to commit {commit_id}")
    else :    
        logger.error(response.text)
