# ------------------------------------------------------------------------------
# Usage: To load and update the paths inside the FBLGeneric.vflash configuration
#        file for Short Range Radar (LRR) and Long Range Radar (LRR)
# Current build targets are: 
# ===============================================================================
#   C O P Y R I G H T
# -------------------------------------------------------------------------------
#   Copyright (c) 2018 by Robert Bosch GmbH. All rights reserved.
# 
#   This file is property of Robert Bosch GmbH. Any unauthorized copy, use or 
#   distribution is an offensive act against international law and may be 
#   prosecuted under federal law. Its content is company confidential.
# ===============================================================================
#  Author(s): Aski Sacheen (RBEI/ESD-ET3-XC))
#
# command --> script usage: 
#      python Cus_gen_release_zip.py -var <LRR> -ver <Version>        
# -------------------------------------------------------------------------------

import os
import argparse
import re
import shutil
from shutil import copytree, ignore_patterns
import sys

# function defination to create a customer folder
def create_cus_folder(path, variant):
    if variant == "LRR":
        shutil.copytree(path + "/int/executables/FR5CU_DENN1_CEN_N_XX_2_uC2", path + "/cus/executables/FR5CU_DENN1_CEN_N_XX_2_uC2",ignore=ignore_patterns('*.elf', '*.map', '*HSM.hex', '*uC2.hex'))
        shutil.copytree(path + "/int/executables/FR5CU_DNNN1_NNN_N_XX_2_uC1", path + "/cus/executables/FR5CU_DNNN1_NNN_N_XX_2_uC1",ignore=ignore_patterns('*.elf', '*.map', '*HSM.hex', '*uC1.hex'))

    shutil.copytree(path + "/int/measurement", path + "/cus/measurement", ignore=ignore_patterns('Canoe', '*.txt'))
    #shutil.copytree(path + "/int/releasenote", path + "/cus/releasenote")
    shutil.copytree(path + "/int/tools/DiaTester", path + "/cus/tools/DiaTester")
    shutil.copytree(path + "/int/tools/ROS4LGP", path + "/cus/tools/ROS4LGP", ignore=ignore_patterns('internal'))
    shutil.copytree(path + "/int/tools/VFlash", path + "/cus/tools/VFlash")
    #Create an empty release noote folder
    os.makedirs(path + "/cus/releasenote") 
    print(f"The cus folder is generated ...!!")

#Function defination to create customer .zip archive
def check_path_create_cus_folder(version, variant):
    #isilion share path
    path = "//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/LRR"
    release_folder_path = os.path.join(path,'LRR_LGU_PF_V' + version, variant )
    print(release_folder_path)
    isdir = os.path.isdir(release_folder_path)
    #Check if the release folder for particular variant & version is existing or not 
    if isdir != True :
        print(f"Please check the variant {variant} version LRR_LGU_PF_V{version} folder is existing....\nHence exiting from the python script.....")
        sys.exit(1)
    else:
        directory_contents = os.listdir(release_folder_path)    
        # Reading out the final delivery folder name
        r = re.compile(".*final")
        final_release_folder = list(filter(r.match, directory_contents)) # Read Note below
        print(final_release_folder)
        final_rel_folder_path = os.path.join(release_folder_path, final_release_folder[0])

        isExisting = os.path.exists(final_rel_folder_path + "/cus")
        if isExisting == True:
           print (f"Customer folder is already existing..!!\n Hence skipping customer folder creation for LRR_LGU_PF_V{version} ")
        else:
           print(f"Customer folder creation for variant: {variant} & version LRR_LGU_PF_V{version} is in progress .......")
           # function call to create a customer folder
           create_cus_folder(final_rel_folder_path, variant)  
           # Archive the customer foler with .zip extention           
           #shutil.make_archive(final_rel_folder_path + '/' + variant + '_LGU_PF_V' + version + '_cus','zip',final_rel_folder_path + '/cus' )
           print(f"The Archiving of Customer folder for variant: {variant} & Version LRR_LGU_PF_V{version}is Successful.......!!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to create Customer folder")
    parser.add_argument("-var", "--variant",
                        help='Variant name', nargs='?', default='LRR')
    parser.add_argument("-ver", "--version",
                        help='SW_Version', nargs='?', default='X.0.0')
    args = parser.parse_args()
    variant = str(args.variant)
    version = str(args.version)
    #Function call to create customer .zip archive
    check_path_create_cus_folder(version, variant)

