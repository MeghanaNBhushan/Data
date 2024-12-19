# ----------------------------------------------------------------------------
# Usage: To build a Release-Folder of Short Range Radar (LRR)
# Current build targets are: 
# =============================================================================
#   C O P Y R I G H T
# -----------------------------------------------------------------------------
#   Copyright (c) 2018 by Robert Bosch GmbH. All rights reserved.
# 
#   This file is property of Robert Bosch GmbH. Any unauthorized copy, use or 
#   distribution is an offensive act against international law and may be 
#   prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Author(s): Nadja Zachert    XC/DA-EAS2
#           
# ----------------------------------------------------------------------------

import os
import shutil
import re
import sys,os
import distutils.dir_util

# read commandline arguments, first
fullCmdArguments = sys.argv

# - further arguments
argumentList = fullCmdArguments[1:]

publish = argumentList[0]

print('publish: "%s"!!!\n' %(publish))

if publish == 'true':

    RelFolder_dir = os.path.realpath('../../../../RelFolder/')
    release_path = os.path.join("//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/LRR/")

    print('Release folder directory: "%s"!!!\n' %(RelFolder_dir)) 
    print('Release directory destination: "%s"!!!\n' %(release_path)) 

    folders_in_given_folder = [name for name in os.listdir(RelFolder_dir) if os.path.isdir(os.path.join(RelFolder_dir, name))]
    folder_list = []
    for folder in folders_in_given_folder:
        path = os.path.join(RelFolder_dir, folder)
        folder_list.append(os.path.basename(path))
    print(folder_list)

    for element in folder_list:
        search_regex = re.match('.*LRR.*', element)
        if search_regex:
            Version = element         

    print('Version ->', Version)

    Source = RelFolder_dir + '/' + Version
    Destination = release_path + '/' + Version

    if os.path.exists(Destination):
        print('Release folder already exist. Please delete the release folder, if you want to overwrite it. Release folder path: "%s"!!!\n' %(Destination))
    
    if not os.path.exists(Destination):
        print('Start Release folder copy to shared drive')
        distutils.dir_util.copy_tree(Source,Destination)           
        print('Release folder copied to shared drive successfully')
        print('"%s"!!!\n' %(Destination))

else:
    print('No Release folder publish requested, Release folder not copied to shared drive')

