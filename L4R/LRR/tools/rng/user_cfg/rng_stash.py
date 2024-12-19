# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 12:41:31 2021

@author: YAH3KOR
"""
# -*- coding: utf-8 -*-
import argparse
import os
import distutils.dir_util
import shutil
import re

import imp
imp.reload(distutils.dir_util)

parser = argparse.ArgumentParser(description="Script to stash/Unstash jenkins artifacts for release note generator")
parser.add_argument("-rn", "--releasename",
                        help='Jobname for which the artifacts are generated', nargs='?', const='LRR_LGU_PF_V9.0.0')
parser.add_argument("-v", "--variant",
                        help='Variant for which the artifacts are generated', nargs='?', const='LRR')

args = parser.parse_args()
releasename = str(args.releasename)
variant = str(args.variant)

release_path = os.path.join("//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/LRR/" + releasename + '/' + variant + '/')


release_final_folder = [f.name for f in os.scandir(release_path) if ( (f.is_dir()) and re.search('final.*', str(f.name)))][0] 


CT_path = '//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI/ATR/Release/rng_stash/'+ variant + '/' + releasename 
shutil.copy( '../build_info.json' , os.path.join(release_path, release_final_folder, 'int') )
shutil.copy( '../release_info.json' , os.path.join(release_path, release_final_folder, 'int') )

shutil.copy( '../build_info.json' , CT_path )
shutil.copy( '../release_info.json' , CT_path )

CT_path = '//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI/ATR/Release/rng_stash/'+ variant + '/' + releasename  
distutils.dir_util.copy_tree(os.path.abspath('../rn_TestProject'), os.path.join(CT_path, 'rn_TestProject'))

distutils.dir_util.copy_tree(os.path.abspath('../rn_TestProject'), os.path.join(release_path, release_final_folder, 'int','releasenote'))
