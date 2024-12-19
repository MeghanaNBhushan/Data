# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:19:13 2021

@author: YAH3KOR
"""
import subprocess
import sys
import logging
import urllib3
import requests
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import argparse
import os
import getpass

parser = argparse.ArgumentParser(description="Script to checkout the latest RBS")
parser.add_argument("-bn", "--buildNumber",
                        help='Build Number', nargs='?', const="6")
parser.add_argument("-s", "--status",
                        help='Status', nargs='?', const="FAILED")
parser.add_argument("-hw", "--hardware",
                        help='Hardware', nargs='?', const="C0")

args = parser.parse_args()

logger_console_handler = logging.StreamHandler()
logger_console_handler.setLevel(logging.DEBUG)
        
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_console_handler.setFormatter(log_format)

logger = logging.getLogger("Test_RBS")
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
    sys.exit(1)
   
status_url = "https://sourcecode01.de.bosch.com/rest/build-status/1.0/commits/"+commit_id

build_status = {
    "state": args.status,
    "key": "RBS_SW_BUILD_"+args.hardware,
    "url": build_url
}

response = requests.post(status_url, auth=(USER, PASS), headers=headers, json=build_status)

if response.status_code == 200 or response.status_code == 204 :
    logger.info(f"SUCCESS - Transmit status {args.status} to commit {commit_id}")
else :    
    logger.error(response.text)
    sys.exit(1)


if args.status == 'SUCCESSFUL':

    branch_url = "https://sourcecode01.de.bosch.com/rest/api/1.0/projects/ARAS/repos/aras/branches"
    branch_name = f"ATR-14015-checkout-latest-rbs-{commit_id}"
    branch_info = {
        "name": branch_name,
        "startPoint": "AD_Radar_PF"
        }
    
    response = requests.post(branch_url, auth=(USER, PASS), headers=headers, json=branch_info)
    
    if response.status_code == 200 :
        logger.info(f"SUCCESS -  Created branch {branch_name}")
    elif  response.status_code == 409 :
        logger.info(f"Branch {branch_name} already exists")    
    else :    
        logger.error(response.text)
        sys.exit(1)

    buildCmd = 'git reset --hard\n'
    buildCmd += 'git clean -fdx\n'
    buildCmd += 'git pull\n'
    buildCmd += f'git checkout {branch_name}\n'
    buildCmd += "cd ../../athena_mt/\n"
    buildCmd += 'git reset --hard\n'
    buildCmd += 'git clean -fdx\n'
    buildCmd += 'git submodule update --force\n'
    buildCmd += 'git pull\n'
    buildCmd += 'git checkout AD_Radar_PF\n'
    buildCmd += 'cd pf_rbs\n'
    buildCmd += 'git reset --hard\n'
    buildCmd += 'git clean -fdx\n'
    buildCmd += f'git checkout {commit_id}\n'
    buildCmd += 'cd ..\n'
    buildCmd += 'git add pf_rbs\n'
    buildCmd += f'git commit -m "ATR-14015 Checkout latest rbs {commit_id}"\n'
    buildCmd += 'git push\n'
    buildCmd += 'cd ..\n'

    mt_commit_url = "https://sourcecode01.de.bosch.com/rest/api/1.0/projects/ARAS/repos/athena_mt/commits?until=AD_Radar_PF&limit=1"
    mt_commit_id = None
    response = requests.get(mt_commit_url, auth=(USER, PASS), headers=headers)

    if response.status_code == requests.codes.ok:
        mt_commit_id = json.loads(response.text)["values"][0]["id"]
        logger.info(f"SUCCESS - Obtained MT commit id {commit_id} to checkout")
    else :    
        logger.error(response.text)
        sys.exit(1)

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
        logger.info("Checking out MT commit_id failed ..........")
        sys.exit(1)

    
    buildCmd += 'git add athena_mt\n'
    buildCmd += f'git commit -m "ATR-14015 Checkout latest rbs {commit_id} using MT commit {mt_commit_id}"\n'
    buildCmd += 'git push\n'

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
        logger.info("Checking out MT commit_id failed ..........")
        sys.exit(1)

    pr_url = "https://sourcecode01.de.bosch.com/rest/api/1.0/projects/ARAS/repos/aras/pull-requests"
    pr_info = {
        "title": branch_name,
        "description": f"Reference build : {build_url}",
        "state": "OPEN",
        "open": True,
        "closed": False,
        "fromRef": {
            "id": f"refs/heads/{branch_name}",
            "repository": {
                "slug": "aras",
                "name": None,
                "project": {
                    "key": "ARAS"
                }
            }
        },
        "toRef": {
            "id": "refs/heads/AD_Radar_PF",
            "repository": {
                "slug": "aras",
                "name": None,
                "project": {
                    "key": "ARAS"
                }
            }
        },
        "locked": False
    }

    response = requests.post(pr_url, auth=(USER, PASS), headers=headers, json=pr_info)

    if response.status_code == 200 or response.status_code == 201 or response.status_code == 409  :
        logger.info(f"SUCCESS - Create PR from branch {branch_name}")
    else :    
        logger.error(response.text)
        sys.exit(1)



