#!/usr/local/bin/ python3

import shutil
import os
import re
import subprocess
import sys
import glob
build_version_regex = '(LRR_LGU_PF_V\d*.\d*.\d*)'

def get_version(buildCmd , regex):
    try:
        setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    except:
        sys.exit(-1)
        
    try:
        buildOut, buildErr = setProcess.communicate(input=buildCmd)
        value = re.search(regex, buildOut).group(1)
        return value
    except:
        sys.exit(-1)


buildCmd = "cd ../../../\n"
buildCmd += 'git describe --tags\n'

release_name = get_version(buildCmd, build_version_regex)

Version = re.search('(V\d*.\d*.\d*)', release_name).group(1)


dir_name = os.path.dirname(os.path.abspath(__file__))


shutil.make_archive('FOSS_LRR_LGU_PF_'+Version, 'zip', dir_name+'/FOSS_LRR_LGU_PF_'+Version)
shutil.make_archive((glob.glob("*ROS4LGP*\\", recursive=True)[0]), 'zip', os.path.realpath(glob.glob("*ROS4LGP*\\", recursive=True)[0]))