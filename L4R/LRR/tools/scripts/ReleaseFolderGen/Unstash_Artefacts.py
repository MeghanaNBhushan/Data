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
                        help='Jobname for which the artifacts are generated', nargs='?', const='ATR/Release/Release_Build')
parser.add_argument("-bn", "--build",
                        help='Build Number', nargs='?', const='103')
args = parser.parse_args()
jobname = str(args.jobname)
build_no = str(args.build)

artefact_path = os.path.join("//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI", jobname, build_no)

Destination_archive = os.path.abspath('../../../../generatedFiles/archive')
Destination_unarchive = os.path.abspath('../../../../generatedFiles/unarchive')

if not os.path.exists(Destination_archive):
            os.makedirs(Destination_archive)

if not os.path.exists(Destination_unarchive):
            os.makedirs(Destination_unarchive)

distutils.dir_util.copy_tree(artefact_path,Destination_archive)

from pathlib import Path
path_archive = Path('../../../../generatedFiles/archive')
path_unarchive = Path('../../../../generatedFiles/unarchive')

import logging
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
    
logger_console_handler = logging.StreamHandler()
logger_console_handler.setLevel(logging.DEBUG)
    
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_console_handler.setFormatter(log_format)

logger.addHandler(logger_console_handler)  

for file in path_archive.glob('**/*.zip'):# ** in a path means any number of sub-directories in the path to match regex

    logger.info("Found : " + file.name)
    logger.info("Path  : " + str(file))
    filename = Path(str(file)).stem
    shutil.unpack_archive(file,Destination_unarchive+'/'+filename)
