#=============================================================================
#  C O P Y R I G H T
#-----------------------------------------------------------------------------
# @copyright (c) 2021 - 2022 by Robert Bosch GmbH. All rights reserved.
#
#  The reproduction, distribution and utilization of this file as
#  well as the communication of its contents to others without express
#  authorization is prohibited. Offenders will be held liable for the
#  payment of damages. All rights reserved in the event of the grant
#  of a patent, utility model or design.
#=============================================================================
#  P R O J E C T   I N F O R M A T I O N
#-----------------------------------------------------------------------------
#     Projectname: L4 Radar
#=============================================================================
#  I N I T I A L   A U T H O R   I D E N T I T Y
#-----------------------------------------------------------------------------
#        Name: ZNA8FE
#  Department: XC-AD/PJ-AS12
#=============================================================================
# @file  ATF_clean_ws.py
#=============================================================================

import os
import shutil

root_dir = os.path.realpath('../../')
print('root_dir ->',root_dir)

# Remove generated smokeTests folder in generatedFiles directory
if os.path.exists(root_dir+'/generatedFiles/smokeTests/'):
    shutil.rmtree(root_dir+'/generatedFiles/smokeTests/')

atf_dir = root_dir+'/ad_radar_apl/tools/AutoMatedTests/'
file_list = os.listdir(atf_dir)

print('atf_dir ->',atf_dir)
print('file_list ->',file_list)

# Remove generated txt and log files in AutoMatedTests directory
for item in file_list:
    if item.endswith(".txt"):
        os.remove(os.path.join(atf_dir, item))
    elif item.endswith(".log"):
        os.remove(os.path.join(atf_dir, item))