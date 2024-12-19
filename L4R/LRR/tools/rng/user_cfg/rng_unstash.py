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
from pathlib import Path


import importlib
importlib.reload(distutils.dir_util)

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

shutil.copy(os.path.join(release_path, release_final_folder, 'int','build_info.json'), '../')
shutil.copy(os.path.join(release_path, release_final_folder, 'int','release_info.json'), '../')

shutil.rmtree(os.path.abspath('../rn_TestProject'))

distutils.dir_util.copy_tree(os.path.join(release_path, release_final_folder, 'int','releasenote'), os.path.abspath('../rn_TestProject'))

final_release_path = os.path.join(release_path, release_final_folder, 'int')

for f in os.scandir(os.path.join(release_path, release_final_folder, 'int')) :
    print(str(f.name))
    try :
        if f.is_dir():
            distutils.dir_util.copy_tree(f, os.path.join(os.path.abspath('../'), str(f.name)))
        if f.is_file():
            distutils.dir_util.file_copy(f, os.path.abspath('../'))
    except:
        continue


release_path = Path('//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/LRR/')
releases = [f.name for f in os.scandir(release_path) if ( f.is_dir() and (re.search(r'LRR.*V(\d*)\.(\d*)\.(\d*)', f.name) != None) )]

release_name = releasename

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
                 
             
shutil.copy(os.path.join(previous_release_path, release_final_folder, 'int', 'static_analysis','QAC_Warnings' ,'qacli-view.csv'), '../static_analysis/QAC_Warnings/qacli-view_prev.csv')
