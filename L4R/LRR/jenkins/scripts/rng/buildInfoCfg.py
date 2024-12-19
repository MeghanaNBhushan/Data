# -*- coding: utf-8 -*-
"""
Created on Mon May 31 12:49:24 2021

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


parser = argparse.ArgumentParser(description="Script to generate build version info")
parser.add_argument("-uC1", "--uC1",
                        help='Build variant for micro-controller 1', nargs='?', const='FR5CU_DNNN1_NNN_N_XX_2_uC1')
parser.add_argument("-uC2", "--uC2",
                        help='Build variant for micro-controller 2', nargs='?', const='FR5CU_DENN1_CEN_N_XX_2_uC2')

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG,
                     datefmt="%H:%M:%S")


args = parser.parse_args()

uC1 = str(args.uC1)
uC2 = str(args.uC2)


release_name = None
rng_cfg_data = None
commit_id = None
if_version = None
dsp_version = None
hsm_version = None
stil_version = None
fbl_version = None
boot_manager_version = None
customer_version = None
plant_container_no = None
plant_container_no_LRR = {}
release_name_variant = None

today = date.today()
baseline_link = ' https://inside-share-hosted-apps.bosch.com/DMS/GetDocumentService/Document.svc/GetDocumentURL?documentID=P12S147629-1956972250-182[Link]'
git_link = "https://sourcecode01.de.bosch.com/projects/ARAS/repos/aras/commits/"


build_version_regex = '(LRR_LGU_PF_V\d*\.\d*\.\d).*'
plant_container_no_regex = 'CONTAINER_NUMBER=([0-9]*).*'
build_commit_id_regex = 'git rev-parse HEAD\n([a-z0-9]*)'
if_version_regex = '.*(PJIF_.*_Radar)-?.*-?.*'   
rc_fw_version_regex = '(PJRC_[a-zA-Z0-9._]*)'
release_folder_base = "\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\Athena_Radar\\LRR"
build_commit_tag_regex = '(LRR_LGU_PF_V\d*.\d*.\d*_.*)'

if uC1 != 'None' and uC2 != 'None' :
    boot_manager_version_regex = 'BOOTMANAGER_INPUT.*uC._(V.*)_[a-zA-Z.]*'
    hsm_version_regex = r'HSM_INPUT.*\\(HSM.*)__PJIF.*Prem'
    stil_version_regex = r'STIL_Core_(.*)_SeedKey.*uC.*'
    fbl_version_regex = 'FBL_INPUT.*LRR.*(V.*).hex'
    release_folder_tail = 'LRR'
    args.variant = 'LRR'

import subprocess
import sys

def get_version(buildCmd , regex):
    try:
        setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    except:
        logging.error("Failed to open a cmd to run commands")
        sys.exit(-1)
        
    try:
        buildOut, buildErr = setProcess.communicate(input=buildCmd)
        value = re.search(regex, buildOut).group(1)
        logging.info(buildOut)
        logging.error(buildErr)
        return value
    except:
        logging.error(buildErr)
        logging.info("Getting version failed ..........")
        sys.exit(-1)

logging.info('Extracting submodule information')

buildCmd = "cd ../../../\n"
buildCmd += 'cd ip_if\n'
buildCmd += 'git describe --tags\n'

if_version = get_version(buildCmd, if_version_regex)

buildCmd = "cd ../../../\n"
buildCmd += 'cd rc_fw\n'
buildCmd += 'git describe --tags\n'

dsp_version = get_version(buildCmd, rc_fw_version_regex)

buildCmd = "cd ../../../\n"
buildCmd += 'git describe --tags\n'

release_name = get_version(buildCmd, build_version_regex)
commit_tag = get_version(buildCmd, build_commit_tag_regex)
buildCmd = "cd ../../../\n"
buildCmd += 'git rev-parse HEAD\n'

commit_id = get_version(buildCmd, build_commit_id_regex)

logging.info('Extracting information from plant container config')

with open('./../../../ad_radar_apl/tools/plant_container/config_Radar_all_Layouts.bat', 'r') as reader:
          # Read and print the entire file line by line
          for line in reader:
              if re.search(boot_manager_version_regex, line):
                  boot_manager_version = re.search(boot_manager_version_regex, line).group(1)
              if re.search(hsm_version_regex, line) :
                  hsm_version = re.search(hsm_version_regex, line).group(1)
              if re.search(stil_version_regex, line) :
                  stil_version = re.search(stil_version_regex, line).group(1)
              if re.search(fbl_version_regex, line) :
                  fbl_version = re.sub('p', '.', re.search(fbl_version_regex, line).group(1))

if str(args.variant) == 'LRR':
    with open('./../../../ad_radar_apl/tools/plant_container/__build_Container_Radar_'+uC2+'.bat', 'r') as reader:
              for line in reader:
                  if re.search(plant_container_no_regex, line):
                      plant_container_no_LRR['uC2'] = re.search(plant_container_no_regex, line).group(1)
    with open('./../../../ad_radar_apl/tools/plant_container/__build_Container_Radar_'+uC1+'.bat', 'r') as reader:
              for line in reader:
                  if re.search(plant_container_no_regex, line):
                      plant_container_no_LRR['uC1'] = re.search(plant_container_no_regex, line).group(1)
                     
    plant_container_no = "uc1:"+plant_container_no_LRR['uC1']+" / uc2: "+plant_container_no_LRR['uC2']+" "
    logging.info(f'release_name - {release_name}')
    release_name_variant = re.sub('LRR', 'LRR' ,release_name)

logging.info(f"Found commit_id - {commit_id}")
logging.info(f"Found if_version - {if_version}")
logging.info(f"Found dsp_version - {dsp_version}")
logging.info(f"Found release_name - {release_name}")
logging.info(f"Found boot_manager_version - {boot_manager_version}")
logging.info(f"Found hsm_version - {hsm_version}")
logging.info(f"Found stil_version - {stil_version}")
logging.info(f"Found fbl_version - {fbl_version}")
logging.info(f"Found plant_container_no - {plant_container_no}")
logging.info(f"Found release_name_variant - {release_name_variant}")


#Walk through all the releases to get the previous release             

from pathlib import Path
release_path = Path('//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/LRR/')

releases = [f.name for f in os.scandir(release_path) if ( f.is_dir() and (re.search(r'LRR.*V(\d*)\.(\d*)\.(\d*)', f.name) != None) )]

current_release = {}

current_release['major_version'] = int(re.search(r'LRR.*V(\d*)\.(\d*)\.(\d*)', release_name).group(1))
current_release['minor_version'] = int(re.search(r'LRR.*V(\d*)\.(\d*)\.(\d*)', release_name).group(2))
current_release['patch_version'] = int(re.search(r'LRR.*V(\d*)\.(\d*)\.(\d*)', release_name).group(3))

previous_release = {}

previous_release_name = None

previous_release['major_version'] = 0
previous_release['minor_version'] = 0
previous_release['patch_version'] = 0

for pre_release_candidate in releases : 

    temp = {}

    temp['major_version'] = int(re.search(r'LRR.*V(\d*)\.(\d*)\.(\d*)', pre_release_candidate).group(1))
    temp['minor_version'] = int(re.search(r'LRR.*V(\d*)\.(\d*)\.(\d*)', pre_release_candidate).group(2))
    temp['patch_version'] = int(re.search(r'LRR.*V(\d*)\.(\d*)\.(\d*)', pre_release_candidate).group(3))

    
    if temp['major_version'] < current_release['major_version']:

        if temp['major_version'] > previous_release['major_version']:
            
                previous_release['major_version'] = temp['major_version']
                previous_release['minor_version'] = temp['minor_version']
                previous_release['patch_version'] = temp['patch_version']
                previous_release_name = pre_release_candidate

        elif temp['major_version'] == previous_release['major_version']:

            if temp['minor_version'] > previous_release['minor_version']:
                previous_release['major_version'] = temp['major_version']
                previous_release['minor_version'] = temp['minor_version']
                previous_release['patch_version'] = temp['patch_version']
                previous_release_name = pre_release_candidate

            elif temp['minor_version'] == previous_release['minor_version']:

                if temp['patch_version'] > previous_release['patch_version']:
                    previous_release['major_version'] = temp['major_version']
                    previous_release['minor_version'] = temp['minor_version']
                    previous_release['patch_version'] = temp['patch_version']
                    previous_release_name = pre_release_candidate

    elif temp['major_version'] == current_release['major_version']:

        if temp['minor_version'] < current_release['minor_version']:

            if temp['major_version'] > previous_release['major_version']:
                previous_release['major_version'] = temp['major_version']
                previous_release['minor_version'] = temp['minor_version']
                previous_release['patch_version'] = temp['patch_version']
                previous_release_name = pre_release_candidate

            elif temp['major_version'] == previous_release['major_version']:

                if temp['minor_version'] > previous_release['minor_version']:
                    previous_release['major_version'] = temp['major_version']
                    previous_release['minor_version'] = temp['minor_version']
                    previous_release['patch_version'] = temp['patch_version']
                    previous_release_name = pre_release_candidate

                elif temp['minor_version'] == previous_release['minor_version']:

                    if temp['patch_version'] > previous_release['patch_version']:
                        previous_release['major_version'] = temp['major_version']
                        previous_release['minor_version'] = temp['minor_version']
                        previous_release['patch_version'] = temp['patch_version']
                        previous_release_name = pre_release_candidate


        elif temp['minor_version'] == current_release['minor_version']:

            if temp['patch_version'] < current_release['patch_version']:
            
                if temp['major_version'] > previous_release['major_version']:
                    previous_release['major_version'] = temp['major_version']
                    previous_release['minor_version'] = temp['minor_version']
                    previous_release['patch_version'] = temp['patch_version']
                    previous_release_name = pre_release_candidate
    
                elif temp['major_version'] == previous_release['major_version']:
    
                    if temp['minor_version'] > previous_release['minor_version']:
                        previous_release['major_version'] = temp['major_version']
                        previous_release['minor_version'] = temp['minor_version']
                        previous_release['patch_version'] = temp['patch_version']
                        previous_release_name = pre_release_candidate

                    elif temp['minor_version'] == previous_release['minor_version']:
    
                        if temp['patch_version'] > previous_release['patch_version']:
                            previous_release['major_version'] = temp['major_version']
                            previous_release['minor_version'] = temp['minor_version']
                            previous_release['patch_version'] = temp['patch_version']
                            previous_release_name = pre_release_candidate
                    
previous_release_path = os.path.join(str(release_path) , previous_release_name, str(args.variant))

release_final_folder = [f.name for f in os.scandir(previous_release_path) if ( (f.is_dir()) and re.search('final.*', str(f.name)))][0] 
                 
             
shutil.copy(os.path.join(previous_release_path, release_final_folder, 'int','build_info.json'), '../../../ad_radar_apl/tools/rng/')
shutil.copy(os.path.join(previous_release_path, release_final_folder, 'int','release_info.json'), '../../../ad_radar_apl/tools/rng/')
distutils.dir_util.copy_tree(os.path.join(previous_release_path, release_final_folder, 'int','releasenote'), os.path.abspath('../../../ad_radar_apl/tools/rng/rn_TestProject'))
            

logging.info('Writing Info into rng_cfg.json')

with open('./../../../ad_radar_apl/tools/rng/rn_TestProject/rng_cfg.json', 'r+') as f:
    rng_cfg_data = json.load(f)
    rng_cfg_data['release_name'] = release_name_variant

    rng_cfg_data['jira_fixversion'] = release_name
    f.seek(0)        # <--- should reset file position to the beginning.
    json.dump(rng_cfg_data, f, indent=4)
    f.truncate()     # remove remaining part
    
logging.info('Writing Info into build_info.json')

with open('./../../../ad_radar_apl/tools/rng/build_info.json', 'r+') as f:
    build_info_data = json.load(f)
    if build_info_data['general_info']['release_baseline']['value'] != re.sub('LRR', '' ,release_name) :
        build_info_data['general_info']['predecessor_baseline']['value'] = build_info_data['general_info']['release_baseline']['value']
        build_info_data['general_info']['predecessor_baseline']['link'] = build_info_data['general_info']['release_baseline']['link']

        build_info_data['general_info']['release_baseline']['value'] = release_name
        build_info_data['general_info']['release_baseline']['link'] = baseline_link
    
    build_info_data['build_info']['sw_build']['git_commit']['link'] = git_link + commit_id
    build_info_data['build_info']['sw_build']['git_commit']['value'] = commit_id
    build_info_data['build_info']['sw_build']['git_tag']['value'] = commit_tag 

    build_info_data['build_info']['reused_sw']['pjif']['value'] = if_version
    build_info_data['build_info']['reused_sw']['dsp']['value'] = dsp_version 
    build_info_data['build_info']['reused_sw']['bootmanager']['value'] = boot_manager_version 
    build_info_data['build_info']['reused_sw']['hsm']['value'] = hsm_version
    build_info_data['build_info']['reused_sw']['stil']['value'] = stil_version
    build_info_data['build_info']['reused_sw']['fbl']['value'] = fbl_version


    f.seek(0)        # <--- should reset file position to the beginning.
    json.dump(build_info_data, f, indent=4)
    f.truncate()     # remove remaining part

with open('./../../../ad_radar_apl/tools/rng/release_info.json', 'r+') as f:
    build_info_data = json.load(f)

    build_info_data['release_info']['sw_container_no']['value'] = plant_container_no

    f.seek(0)        # <--- should reset file position to the beginning.
    json.dump(build_info_data, f, indent=4)
    f.truncate()     # remove remaining part

CT_path = '//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI/ATR/Release/rng_stash/'+ str(args.variant) + '/' + release_name 


distutils.dir_util.copy_tree(os.path.abspath('../../../ad_radar_apl/tools/rng/rn_TestProject'), os.path.join(CT_path, 'rn_TestProject'))
shutil.copy('../../../ad_radar_apl/tools/rng/build_info.json', CT_path)
shutil.copy('../../../ad_radar_apl/tools/rng/release_info.json', CT_path)

shutil.copy('../../../ad_radar_apl/tools/rng/build_info.json', os.path.abspath('../../../ad_radar_apl/tools/rng/rn_TestProject'))
shutil.copy('../../../ad_radar_apl/tools/rng/release_info.json', os.path.abspath('../../../ad_radar_apl/tools/rng/rn_TestProject'))

