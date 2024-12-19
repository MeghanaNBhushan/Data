# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 13:45:36 2021

@author: YAH3KOR
"""
import shutil
import argparse
import os
import distutils.dir_util

parser = argparse.ArgumentParser(description="Script to stash/Unstash jenkins artifacts")
parser.add_argument("-j", "--jobname",
                        help='Jobname for which the artifacts are generated', nargs='?', const='ATR/SW_Build/aras/PR-2044')
parser.add_argument("-bn", "--build",
                        help='Build Number', nargs='?', const='6')
args = parser.parse_args()
jobname = str(args.jobname)
build_no = str(args.build)
plant_path = os.path.join("//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI", jobname, build_no, "Plant_container")
sw_path = os.path.join("//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI", jobname, build_no, "SW_build")

distutils.dir_util.copy_tree(plant_path,os.path.abspath('../../ad_radar_apl/tools/AutoMatedTests/archive'))
distutils.dir_util.copy_tree(sw_path,os.path.abspath('../../ad_radar_apl/tools/AutoMatedTests/archive'))

from pathlib import Path
path1 = Path('../../ad_radar_apl/tools/AutoMatedTests/archive')
path2 = Path('../../ad_radar_apl/tools/AutoMatedTests/unarchive')

import logging
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
    
logger_console_handler = logging.StreamHandler()
logger_console_handler.setLevel(logging.DEBUG)
    
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_console_handler.setFormatter(log_format)

logger.addHandler(logger_console_handler)  

for file in path1.glob('**/*.zip'):# ** in a path means any number of sub-directories in the path to match regex
    try :
        logger.info("Found : " + file.name)
        logger.info("Path  : " + str(file))
        shutil.unpack_archive(file, '../../ad_radar_apl/tools/AutoMatedTests/unarchive')
    except FileNotFoundError :
        pass
        
Source_scom = os.path.realpath('../../ad_radar_apl/tools/AutoMatedTests/unarchive/scom_gen')
Destination_scom = os.path.realpath('../../generatedFiles/scom_gen')
		
shutil.copytree(Source_scom,Destination_scom)

for file in path2.glob('**/*.elf'):# ** in a path means any number of sub-directories in the path to match regex

    logger.info("Found : " + file.name)
    logger.info("Path  : " + str(file))
    shutil.copy(file, '../../generatedFiles')

for file in path2.glob('**/*_signed.hex'):# ** in a path means any number of sub-directories in the path to match regex

    logger.info("Found : " + file.name)
    logger.info("Path  : " + str(file))
    shutil.copy(file, '../../generatedFiles')

for file in path2.glob('**/rbBuild_Version.h'):# ** in a path means any number of sub-directories in the path to match regex

    logger.info("Found : " + file.name)
    logger.info("Path  : " + str(file))
    shutil.copy(file, '../../generatedFiles')

for file in path1.glob('**/rbBuild_Version_Cfg.h'):# ** in a path means any number of sub-directories in the path to match regex

    logger.info("Found : " + file.name)
    logger.info("Path  : " + str(file))
    shutil.copy(file, '../../generatedFiles')

