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
#      python UpdateVFlashPaths.py -var <LRR> -ver <Version> -cid <commitid>          
# -------------------------------------------------------------------------------


import re
import os
from pathlib import Path
import argparse

#Repository root path
root_path= os.path.abspath(__file__ + "/../../../../../")
print(root_path)

#Function defination to load and update VFlash config file 
def path_replacement(VFlashfile_path, variant, commit_id, version, version_to_search, commitid_to_search): 
    #Load the FBLGeneric.vflash file and replace the old path with new paths.        
    config_file_path = Path(VFlashfile_path + "/FBLGeneric.vflash")
    config_file = config_file_path.read_text()
    config_file = config_file.replace(version_to_search, version)
    config_file = config_file.replace(commitid_to_search, "final_" + commit_id )
    config_file_path.write_text(config_file)

#Function defination to call VFlash config file and update the path 
def read_vflash_config_file(root_path,variant, version, commit_id):
    if (variant == "LRR"):
        #Load and read the config file with open()
        VFlashfile_path = os.path.join(root_path,'RelFolder/' + version + '/' + variant + '/final_' + commit_id + '/int/tools/VFlash/VflashGeneric')
        config_file = open(VFlashfile_path + "/FBLGeneric.vflash", 'r')
        i=0
        for line in config_file:
            match = re.search(r'AbsolutePath', line) # found, match.group() == "AbsolutePath"
            #If "AbsolutePath" is found, search for version and commit_ids from the AbsolutePath
            if (match):
                version_to_search=re.search('(<)?(\w+_\w+(?:\.\w+)+)', line).group()
                commitid_to_search=re.search('([a-z]+_([\da-z0-9]+))', line).group()
                if ((commitid_to_search != "final_"+ commit_id) or (version_to_search !=version)):
                    i=i+1
                    #Function call to load and update VFlash config file 
                    path_replacement(VFlashfile_path, variant, commit_id, version, version_to_search , commitid_to_search)
                    print(f"INFO[{variant}]::Path {i} is UPDATED\n  info:The {version_to_search} is replaced by {version} \n  info:The {commitid_to_search} is replaced by {'final_' + commit_id}\n")                    

                else:
                    i=i+1
                    print (f"INFO[{variant}]:: Path {i}: Already UPTODATE !!!")
     
    else:
        print(f"Wrong input variant {variant} name\nPlease choose one variant from [LRR]")
if __name__ == "__main__":
    #Getting command line arguments into python script
    parser = argparse.ArgumentParser(description="Script to Update paths inside VFlash container config file ")
    parser.add_argument("-var", "--variant",
                        help='Variant for which the config file path is updated', nargs='?', default='LRR')
    parser.add_argument("-ver", "--version",
                        help='SW_Version to be updated', nargs='?', default='LRR_LGU_PF_V6.0.0')
    parser.add_argument("-cid", "--commit_id",
                        help='commit ID to be updated', nargs='?', default='0b5e391bb2')                                       
    args = parser.parse_args()
    variant = str(args.variant)
    version = str(args.version)
    commit_id = str(args.commit_id)
    #Function call to read VFlash config file
    read_vflash_config_file(root_path, variant, version, commit_id)
