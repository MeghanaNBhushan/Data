# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 13:45:36 2021

@author: YAH3KOR
"""
import shutil
import argparse
import os
import distutils.dir_util

parser = argparse.ArgumentParser(description="Script to stash jenkins artifacts")
parser.add_argument("-rbj", "--releaseBuildJobname",
                        help='Jobname for which the artifacts are generated', nargs='?', const='ATR/Release/Release_build_new')
parser.add_argument("-rbbn", "--releaseBuildNo",
                        help='Build Number', nargs='?', const='8')
parser.add_argument("-rtj", "--releaseTestJobname",
                        help='Jobname for which the artifacts are generated', nargs='?', const='ATR/Release_restructured/Release_test')
parser.add_argument("-rtbn", "--releaseTestNo",
                        help='Build Number', nargs='?', const='7')
args = parser.parse_args()
release_build_jobname = str(args.releaseBuildJobname)
release_build_no = str(args.releaseBuildNo)
release_test_jobname = str(args.releaseTestJobname)
release_test_no = str(args.releaseTestNo)
release_build_path = os.path.join("//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI", release_build_jobname, release_build_no)
release_test_path = os.path.join("//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI", release_test_jobname, release_test_no)

distutils.dir_util.copy_tree(release_test_path, release_build_path)
