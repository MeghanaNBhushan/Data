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
#  Author(s): Michael Hebestreit    CC/DA-ESI6 
#           
# ----------------------------------------------------------------------------

import os
import shutil
import re
import sys,os
import distutils.dir_util
import time
import subprocess


######## Color-Table #################

#    0 = Black       8 = Gray
#    1 = Blue        9 = Light Blue
#    2 = Green       A = Light Green
#    3 = Aqua        B = Light Aqua
#    4 = Red         C = Light Red
#    5 = Purple      D = Light Purple
#    6 = Yellow      E = Light Yellow
#    7 = White       F = Bright White


os.system('color 6')  


###### Subprogram ############

# No Subprograms #

###### Mainprogram ############

# count the arguments
arguments = len(sys.argv) - 1

print ("the script is called with %i arguments" % (arguments))

# read commandline arguments, first
fullCmdArguments = sys.argv

# - further arguments
argumentList = fullCmdArguments[1:]

#print ("List of arguments %s" %(argumentList))


if (arguments > 2) or (arguments < 1):
     print("The python arguments are too much!")

else:

#Folder_LRR_HW_Variant = input("Input of the Folder-Name of the LRR-ECU-Variant, which will be built by build-tool-chain\n")  
        
    Folder_LRR_HW_Variant_uC1 = argumentList[0]
    Folder_LRR_HW_Variant_uC2 = argumentList[1]
                     
    print('Build is started with LRR-ECU-Variant uC1: "%s"!!!\n' %(Folder_LRR_HW_Variant_uC1)) 
    print('Build is started with LRR-ECU-Variant uC2: "%s"!!!\n' %(Folder_LRR_HW_Variant_uC2))

    MainSource_unarchive = os.path.realpath('../../../../generatedFiles/unarchive')
    MainSource_archive = os.path.realpath('../../../../generatedFiles/archive')

    print('MainSource_archive ->',MainSource_archive)
    print('MainSource_unarchive ->',MainSource_unarchive)

    with open(MainSource_unarchive+'/SWBuild_Radar_'+Folder_LRR_HW_Variant_uC2+'/buildversion/rbBuild_Version.h', 'r') as f:
        datafile = f.readlines()
        list = None
        for line in datafile:
            if 'RBBUILD_VERSION_COMMITIDSHORT ' in line:
                pattern = re.search('\{([a-z0-9])*.*\}', line).group()
                commitid = pattern.replace(" ","").replace(",","").replace("'","").replace("}","").replace("{","")
                print(commitid)
            if 'RBBUILD_VERSION_TAG_DESCRIPTION ' in line:
                pattern = re.search('\{([a-z0-9])*.*\}', line).group()
                version_full = pattern.replace(" ","").replace(",","").replace("'","").replace("}","").replace("{","").replace("\\","")
                major = re.search(r'LRR.*V(\d*)\.(\d*)\.(\d*)', version_full).group(1)
                minor = re.search(r'LRR.*V(\d*)\.(\d*)\.(\d*)', version_full).group(2)
                patch = re.search(r'LRR.*V(\d*)\.(\d*)\.(\d*)', version_full).group(3)

    Version = 'LRR_LGU_PF_V'+str(major)+'.'+str(minor)+'.'+str(patch)

    print('commitid ->',commitid)
    print('Version ->',Version)

    MainDestination_LRR_internal = os.path.realpath('../../../../RelFolder')+'/'+Version+'/LRR/'+'rc0_'+commitid+'/int'

    MainDestination_LRR_int_final = os.path.realpath('../../../../RelFolder')+'/'+Version+'/LRR/'+'final_'+commitid+'/int'

    MainDestination_LRR_cus_final = os.path.realpath('../../../../RelFolder')+'/'+Version+'/LRR/'+'final_'+commitid+'/cus'

       
    print('\nPATH NAMES')
    print('MainDestination_LRR_internal ->',MainDestination_LRR_internal)

    print('MainDestination_LRR_int_final ->',MainDestination_LRR_int_final)

    print('MainDestination_LRR_cus_final ->',MainDestination_LRR_cus_final)

###############Release-Folder ##############################################################

    print('\nRELEASE FOLDER GENERATION - START COPY\n')
#Copy executables
#LRR
    print('COPY EXECUTABLES LRR')
    Source = MainSource_unarchive+'/SWBuild_Radar_'+Folder_LRR_HW_Variant_uC1   
    Destination_int = MainDestination_LRR_internal+'/executables/'+Folder_LRR_HW_Variant_uC1
    Destination_int_final = MainDestination_LRR_int_final+'/executables/'+Folder_LRR_HW_Variant_uC1         

    print('Source ->',Source) 
    print('Destination_int ->',Destination_int) 
    print('Destination_int_final ->',Destination_int_final)

    if not os.path.exists(Destination_int):
        os.makedirs(Destination_int)

    if not os.path.exists(Destination_int_final):
        os.makedirs(Destination_int_final)

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".elf", ".hex", ".map")):
                shutil.copy(full_file_name, Destination_int)
                shutil.copy(full_file_name, Destination_int_final)
        
    print('COPY EXECUTABLES LRR uC1 SUCCESSFUL\n')

    Source = MainSource_unarchive+'/SWBuild_Radar_'+Folder_LRR_HW_Variant_uC2
    Destination_int = MainDestination_LRR_internal+'/executables/'+Folder_LRR_HW_Variant_uC2
    Destination_int_final = MainDestination_LRR_int_final+'/executables/'+Folder_LRR_HW_Variant_uC2

    print('Source ->',Source) 
    print('Destination_int ->',Destination_int) 
    print('Destination_int_final ->',Destination_int_final)

    if not os.path.exists(Destination_int):
        os.makedirs(Destination_int)

    if not os.path.exists(Destination_int_final):
        os.makedirs(Destination_int_final)

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".elf", ".hex", ".map")):
                shutil.copy(full_file_name, Destination_int)
                shutil.copy(full_file_name, Destination_int_final)

    print('COPY EXECUTABLES LRR uC2 SUCCESSFUL\n')

    Destination_int = MainDestination_LRR_internal+'/executables'
    f = open(Destination_int+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()

    Destination_int_final = MainDestination_LRR_internal+'/executables'
    f = open(Destination_int_final+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()

#Copy Plant Container delta
#LRR
    print('COPY Delta Plant Container LRR uC1')
    Source = MainSource_unarchive+'/plant_LRR_uC1_d/plant_uC1_delta'
    Destination_int = MainDestination_LRR_internal+'/init_dev'  
    Destination_int_final = MainDestination_LRR_int_final+'/init_dev' 

    print('Source ->',Source) 
    print('Destination_int ->',Destination_int) 
    print('Destination_int_final ->',Destination_int_final) 

    if not os.path.exists(Destination_int):
        os.makedirs(Destination_int)
    if not os.path.exists(Destination_int_final):
        os.makedirs(Destination_int_final)

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isdir(full_file_name):
              SelectSubFolderInLog = full_file_name

    SubFolderName = re.findall("\\\\([^\\\\]*)$",SelectSubFolderInLog) 
    Source = Source+'/'+SubFolderName[0]
    Destination_int = Destination_int+'/'+SubFolderName[0]
    Destination_int_final = Destination_int_final+'/'+SubFolderName[0]

    shutil.copytree(Source,Destination_int) 
    shutil.copytree(Source,Destination_int_final) 

    folders_in_given_folder = [name for name in os.listdir(Destination_int) if os.path.isdir(os.path.join(Destination_int, name))]
    folder_list = []
    for folder in folders_in_given_folder:
        path = os.path.join(Destination_int, folder)
        folder_list.append(os.path.basename(path))
    print(folder_list)

    for element in folder_list:
        search_regex = re.match('.*customizing.*', element)
        if search_regex:
            customizing = element         
    print('Customizing folder name -->', customizing)

    shutil.make_archive(MainDestination_LRR_internal+'/init_dev/UC1_DELTA/'+customizing,"zip", MainDestination_LRR_internal+'/init_dev/UC1_DELTA/'+customizing)
    if os.path.exists(MainDestination_LRR_internal+'/init_dev/UC1_DELTA/'+customizing):
        shutil.rmtree(MainDestination_LRR_internal+'/init_dev/UC1_DELTA/'+customizing)

    shutil.make_archive(MainDestination_LRR_int_final+'/init_dev/UC1_DELTA/'+customizing,"zip", MainDestination_LRR_int_final+'/init_dev/UC1_DELTA/'+customizing)
    if os.path.exists(MainDestination_LRR_int_final+'/init_dev/UC1_DELTA/'+customizing):
        shutil.rmtree(MainDestination_LRR_int_final+'/init_dev/UC1_DELTA/'+customizing)

    print('COPY DELTA PLANT CONTAINER LRR uC1 SUCCESSFUL\n')
    print('COPY Delta Plant Container LRR uC2')
        
    Source = MainSource_unarchive+'/plant_LRR_uC2_d/plant_uC2_delta'
    Destination_int = MainDestination_LRR_internal+'/init_dev'  
    Destination_int_final = MainDestination_LRR_int_final+'/init_dev' 
        
    print('Source ->',Source) 
    print('Destination_int ->',Destination_int) 
    print('Destination_int_final ->',Destination_int_final) 

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isdir(full_file_name):
              SelectSubFolderInLog = full_file_name

    SubFolderName = re.findall("\\\\([^\\\\]*)$",SelectSubFolderInLog) 
    Source = Source+'/'+SubFolderName[0]
    Destination_int = Destination_int+'/'+SubFolderName[0]
    Destination_int_final = Destination_int_final+'/'+SubFolderName[0]
         
    shutil.copytree(Source,Destination_int) 
    shutil.copytree(Source,Destination_int_final) 

    folders_in_given_folder = [name for name in os.listdir(Destination_int) if os.path.isdir(os.path.join(Destination_int, name))]
    folder_list = []
    for folder in folders_in_given_folder:
        path = os.path.join(Destination_int, folder)
        folder_list.append(os.path.basename(path))
    print(folder_list)

    for element in folder_list:
        search_regex = re.match('.*customizing.*', element)
        if search_regex:
            customizing = element         
    print('Customizing folder name -->', customizing)

    shutil.make_archive(MainDestination_LRR_internal+'/init_dev/UC2_DELTA/'+customizing,"zip", MainDestination_LRR_internal+'/init_dev/UC2_DELTA/'+customizing)
    if os.path.exists(MainDestination_LRR_internal+'/init_dev/UC2_DELTA/'+customizing):
        shutil.rmtree(MainDestination_LRR_internal+'/init_dev/UC2_DELTA/'+customizing)

    shutil.make_archive(MainDestination_LRR_int_final+'/init_dev/UC2_DELTA/'+customizing,"zip", MainDestination_LRR_int_final+'/init_dev/UC2_DELTA/'+customizing)
    if os.path.exists(MainDestination_LRR_int_final+'/init_dev/UC2_DELTA/'+customizing):
        shutil.rmtree(MainDestination_LRR_int_final+'/init_dev/UC2_DELTA/'+customizing)

    print('COPY DELTA PLANT CONTAINER LRR uC2 SUCCESSFUL\n') 

    Destination = MainDestination_LRR_internal+'/init_dev' 
    f = open(Destination+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()

#Copy Plant Container complete
#LRR
    print('COPY Complete Plant Container LRR uC1')
    Source = MainSource_unarchive+'/plant_LRR_uC1/plant_uC1'
    Destination_int = MainDestination_LRR_internal+'/plant_container'  
    Destination_int_final = MainDestination_LRR_int_final+'/plant_container' 

    print('Source ->',Source) 
    print('Destination_int ->',Destination_int) 
    print('Destination_int_final ->',Destination_int_final) 

    if not os.path.exists(Destination_int):
        os.makedirs(Destination_int)
    if not os.path.exists(Destination_int_final):
        os.makedirs(Destination_int_final)

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isdir(full_file_name):
              SelectSubFolderInLog = full_file_name

    SubFolderName = re.findall("\\\\([^\\\\]*)$",SelectSubFolderInLog) 
    Source = Source+'/'+SubFolderName[0]
    Destination_int = Destination_int+'/'+SubFolderName[0]
    Destination_int_final = Destination_int_final+'/'+SubFolderName[0]

    shutil.copytree(Source,Destination_int) 
    shutil.copytree(Source,Destination_int_final) 

    shutil.make_archive(MainDestination_LRR_internal+'/plant_container/UC1',"zip", MainDestination_LRR_internal+'/plant_container/UC1')
    if os.path.exists(MainDestination_LRR_internal+'/plant_container/UC1'):
        shutil.rmtree(MainDestination_LRR_internal+'/plant_container/UC1')

    shutil.make_archive(MainDestination_LRR_int_final+'/plant_container/UC1',"zip", MainDestination_LRR_int_final+'/plant_container/UC1')
    if os.path.exists(MainDestination_LRR_int_final+'/plant_container/UC1'):
        shutil.rmtree(MainDestination_LRR_int_final+'/plant_container/UC1')

    print('COPY COMPLETE PLANT CONTAINER LRR uC1 SUCCESSFUL\n')
    print('COPY Complete Plant Container LRR uC2')
    
    Source = MainSource_unarchive+'/plant_LRR_uC2/plant_uC2'
    Destination_int = MainDestination_LRR_internal+'/plant_container'  
    Destination_int_final = MainDestination_LRR_int_final+'/plant_container' 
    
    print('Source ->',Source) 
    print('Destination_int ->',Destination_int) 
    print('Destination_int_final ->',Destination_int_final) 

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isdir(full_file_name):
              SelectSubFolderInLog = full_file_name

    SubFolderName = re.findall("\\\\([^\\\\]*)$",SelectSubFolderInLog) 
    Source = Source+'/'+SubFolderName[0]
    Destination_int = Destination_int+'/'+SubFolderName[0]
    Destination_int_final = Destination_int_final+'/'+SubFolderName[0]
     
    shutil.copytree(Source,Destination_int) 
    shutil.copytree(Source,Destination_int_final) 

    shutil.make_archive(MainDestination_LRR_internal+'/plant_container/UC2',"zip", MainDestination_LRR_internal+'/plant_container/UC2')
    if os.path.exists(MainDestination_LRR_internal+'/plant_container/UC2'):
        shutil.rmtree(MainDestination_LRR_internal+'/plant_container/UC2')

    shutil.make_archive(MainDestination_LRR_int_final+'/plant_container/UC2',"zip", MainDestination_LRR_int_final+'/plant_container/UC2')
    if os.path.exists(MainDestination_LRR_int_final+'/plant_container/UC2'):
        shutil.rmtree(MainDestination_LRR_int_final+'/plant_container/UC2')

    print('COPY COMPLETE PLANT CONTAINER LRR uC2 SUCCESSFUL\n') 

    Destination = MainDestination_LRR_internal+'/plant_container' 
    f = open(Destination+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()

#Copy DiaTester
    print('COPY DiaTester')
    Source = MainSource_unarchive+'/DiaTester'
    Destination_LRR_int = MainDestination_LRR_internal+'/tools/DiaTester'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/tools/DiaTester' 
    
    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)

    shutil.copytree(Source,Destination_LRR_int)
    shutil.copytree(Source,Destination_LRR_int_final)

    print('COPY DIATESTER SUCCESSFUL\n')

#Copy VFlash
    print('COPY VFlash')
    Source_LRR = MainSource_unarchive+'/VFlash/FR5CU'
    Destination_LRR_int = MainDestination_LRR_internal+'/tools/VFlash'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/tools/VFlash' 

    print('Source_LRR ->',Source_LRR) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)

    shutil.copytree(Source_LRR,Destination_LRR_int)
    shutil.copytree(Source_LRR,Destination_LRR_int_final)
    os.system(f'python UpdateVFlashPaths.py -var LRR -ver {Version} -cid {commitid}')
    print('COPY VFLASH SUCCESSFUL\n')

#Copy supplements
    print('COPY Supplements')       
    Source = MainSource_unarchive+'/Supplements/supplements'
    Destination_LRR_int = MainDestination_LRR_internal+'/supplements'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/supplements'
    
    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)

    shutil.copytree(Source,Destination_LRR_int)
    shutil.copytree(Source,Destination_LRR_int_final)

    print('COPY SUPPLEMENTS SUCCESSFUL\n')

    f = open(Destination_LRR_int+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()

    f = open(Destination_LRR_int_final+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()


#Copy DemEvents
    print('COPY DemEvents')
    Source_LRR = MainSource_unarchive+'/DemEvents_fr5cu'
    Destination_LRR_int = MainDestination_LRR_internal+'/documentation/DemEvents'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/documentation/DemEvents'  

    
    print('Source_LRR ->',Source_LRR) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)

    shutil.copytree(Source_LRR,Destination_LRR_int)
    shutil.copytree(Source_LRR,Destination_LRR_int_final)

    print('COPY DEMEVENTS SUCCESSFUL\n')

    Destination_LRR_int = MainDestination_LRR_internal+'/documentation'
    f = open(Destination_LRR_int+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()

    Destination_LRR_int_final = MainDestination_LRR_internal+'/documentation'
    f = open(Destination_LRR_int_final+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()

#Copy dsp_FaultEventId
    print('COPY dsp_FaultEventId')
    Source_LRR = MainSource_unarchive+'/dsp_FaultEventId_fr5cu'
    Destination_LRR_int = MainDestination_LRR_internal+'/documentation/dsp_FaultEventId'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/documentation/dsp_FaultEventId'  
    
    print('Source_LRR ->',Source_LRR) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)

    shutil.copytree(Source_LRR,Destination_LRR_int)
    shutil.copytree(Source_LRR,Destination_LRR_int_final)

    print('COPY DSP_FAULTEVENTID SUCCESSFUL\n')

#Copy FR5CU_Specification_Document
    print('COPY FR5CU_Specification_Document')
    Source = MainSource_unarchive+'/FR5CU_Specification_Document'
    Destination_LRR_int = MainDestination_LRR_internal+'/documentation/'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/documentation/'  

    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)

    if not os.path.exists(Destination_LRR_int):
        os.makedirs(Destination_LRR_int)
    if not os.path.exists(Destination_LRR_int_final):
        os.makedirs(Destination_LRR_int_final)

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".pdf")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)

    print('COPY FR5CU_SPECIFICATION_DOCUMENTS SUCCESSFUL\n')

#Copy UnitTests
    print('COPY UnitTests')
    Source = MainSource_unarchive+'/Cantata'
    Destination_LRR_int = MainDestination_LRR_internal+'/test_reports_gen/UnitTests'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/test_reports_gen/UnitTests' 

    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final) 

    if not os.path.exists(Destination_LRR_int):
        os.makedirs(Destination_LRR_int)

    if not os.path.exists(Destination_LRR_int_final):
        os.makedirs(Destination_LRR_int_final)

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((Folder_LRR_HW_Variant_uC2+".zip", Folder_LRR_HW_Variant_uC2+"_cantataMakeLog.txt")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)

    print('COPY UNITTESTS SUCCESSFUL\n')

    print('COPY UnitTests Coverage per Comp')
    Source = MainSource_unarchive+'/Coverage_per_Comp'

    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final) 

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((Folder_LRR_HW_Variant_uC2+".xlsx")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)

    print('COPY UNITTESTS COVERAGE PER COMP SUCCESSFUL\n')

    Destination_LRR_int = MainDestination_LRR_internal+'/test_reports_gen'
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/test_reports_gen'

    f = open(Destination_LRR_int+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()

    f = open(Destination_LRR_int_final+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()

#Copy calcres
    print('COPY Calcres')
    Source = MainSource_archive+'/Calcres'
    Destination_LRR_int = MainDestination_LRR_internal+'/static_analysis/CheckMem'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/static_analysis/CheckMem' 

    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final) 

    if not os.path.exists(Destination_LRR_int):
        os.makedirs(Destination_LRR_int)

    if not os.path.exists(Destination_LRR_int_final):
        os.makedirs(Destination_LRR_int_final)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((Folder_LRR_HW_Variant_uC2+".csv", Folder_LRR_HW_Variant_uC2+".xlsx")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((Folder_LRR_HW_Variant_uC1+".csv", Folder_LRR_HW_Variant_uC1+".xlsx")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)


    print('COPY CALCRES SUCCESSFUL\n')

    Destination_LRR_int = MainDestination_LRR_internal+'/static_analysis'
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/static_analysis'

    f = open(Destination_LRR_int+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()


    f = open(Destination_LRR_int_final+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()


#Copy scom_gen
    print('COPY scom_gen')
    Source_LRR_uC1 = MainSource_unarchive+'/scom_gen_'+Folder_LRR_HW_Variant_uC1+'/scom_gen/'+Folder_LRR_HW_Variant_uC1
    Source_LRR_uC2 = MainSource_unarchive+'/scom_gen_'+Folder_LRR_HW_Variant_uC2+'/scom_gen/'+Folder_LRR_HW_Variant_uC2

    Destination_LRR_uC1_int = MainDestination_LRR_internal+'/static_analysis/scom_gen/'+Folder_LRR_HW_Variant_uC1
    Destination_LRR_uC2_int = MainDestination_LRR_internal+'/static_analysis/scom_gen/'+Folder_LRR_HW_Variant_uC2
    Destination_LRR_uC1_int_final = MainDestination_LRR_int_final+'/static_analysis/scom_gen/'+Folder_LRR_HW_Variant_uC1
    Destination_LRR_uC2_int_final = MainDestination_LRR_int_final+'/static_analysis/scom_gen/'+Folder_LRR_HW_Variant_uC2
    
    print('Source_LRR_uC1 ->',Source_LRR_uC1) 
    print('Source_LRR_uC2 ->',Source_LRR_uC2) 
    print('Destination_LRR_uC1_int ->',Destination_LRR_uC1_int) 
    print('Destination_LRR_uC2_int ->',Destination_LRR_uC2_int) 
    print('Destination_LRR_uC1_int_final ->',Destination_LRR_uC1_int_final) 
    print('Destination_LRR_uC2_int_final ->',Destination_LRR_uC2_int_final) 

    if not os.path.exists(Destination_LRR_uC1_int):
        os.makedirs(Destination_LRR_uC1_int)
    if not os.path.exists(Destination_LRR_uC2_int):
        os.makedirs(Destination_LRR_uC2_int)
    if not os.path.exists(Destination_LRR_uC1_int_final):
        os.makedirs(Destination_LRR_uC1_int_final)
    if not os.path.exists(Destination_LRR_uC2_int_final):
        os.makedirs(Destination_LRR_uC2_int_final)


    source = os.listdir(Source_LRR_uC1)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR_uC1, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".hpp", ".cpp", ".h", ".xml")):
                shutil.copy(full_file_name, Destination_LRR_uC1_int)
                shutil.copy(full_file_name, Destination_LRR_uC1_int_final)

    source = os.listdir(Source_LRR_uC2)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR_uC2, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".hpp", ".cpp", ".h", ".xml", ".csv", ".png", ".md")):
                shutil.copy(full_file_name, Destination_LRR_uC2_int)
                shutil.copy(full_file_name, Destination_LRR_uC2_int_final)


    print('COPY SCOM_GEN SUCCESSFUL\n')

#Copy CompilerWarnings
#complete log
    print('COPY compiler warnings')
    Source_LRR_uC1 = MainSource_unarchive+'/CompWarnings_'+Folder_LRR_HW_Variant_uC1
    Source_LRR_uC2 = MainSource_unarchive+'/CompWarnings_'+Folder_LRR_HW_Variant_uC2

    Destination_LRR_int = MainDestination_LRR_internal+'/static_analysis/Compiler_Warnings'
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/static_analysis/Compiler_Warnings'

    print('Source_LRR_uC1 ->',Source_LRR_uC1) 
    print('Source_LRR_uC2 ->',Source_LRR_uC2) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final) 

    if not os.path.exists(Destination_LRR_int):
        os.makedirs(Destination_LRR_int)
    if not os.path.exists(Destination_LRR_int_final):
        os.makedirs(Destination_LRR_int_final)

    source = os.listdir(Source_LRR_uC1)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR_uC1, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".txt", ".csv")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)

    source = os.listdir(Source_LRR_uC2)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR_uC2, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".txt", ".csv")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)


    print('COPY COMPILER WARNINGS SUCCESSFUL\n')

#per component
    print('COPY compiler warnings per component')
    Source = MainSource_archive+'/Quality_reports/Compiler_Warnings'
    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final) 

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((Folder_LRR_HW_Variant_uC1+".xlsx")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((Folder_LRR_HW_Variant_uC2+".xlsx")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)

    print('COPY COMPILER WARNINGS PER COMPONENT SUCCESSFUL\n')

#Copy FluxErrors
    print('COPY FluxErrorsDetails')
    Source = MainSource_unarchive+'/FluxErrorsDetails'
    Destination_LRR_int = MainDestination_LRR_internal+'/static_analysis/FluxErrors'
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/static_analysis/FluxErrors'

    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final) 

    if not os.path.exists(Destination_LRR_int):
        os.makedirs(Destination_LRR_int)
    if not os.path.exists(Destination_LRR_int_final):
        os.makedirs(Destination_LRR_int_final)

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".txt")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)


    print('COPY FLUXERRORSDETAILS SUCCESSFUL\n')

    print('COPY FluxErrorsReport')

    Source = MainSource_archive+'/Quality_reports/Flux_Errors'
    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final) 

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".csv")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)
                
    print('COPY FLUXERRORSREPORT SUCCESSFUL\n')
    
#Copy sw_build_protocol and buildversion
    print('COPY sw_build_protocoll and buildversion')
    Source_LRR_uC1 = MainSource_unarchive+'/SWBuild_Radar_'+Folder_LRR_HW_Variant_uC1
    Source_LRR_uC2 = MainSource_unarchive+'/SWBuild_Radar_'+Folder_LRR_HW_Variant_uC2

    Destination_LRR_uC1_int = MainDestination_LRR_internal+'/static_analysis/SW_build_protocol/'+Folder_LRR_HW_Variant_uC1
    Destination_LRR_uC2_int = MainDestination_LRR_internal+'/static_analysis/SW_build_protocol/'+Folder_LRR_HW_Variant_uC2
    Destination_LRR_uC1_int_final = MainDestination_LRR_int_final+'/static_analysis/SW_build_protocol/'+Folder_LRR_HW_Variant_uC1
    Destination_LRR_uC2_int_final = MainDestination_LRR_int_final+'/static_analysis/SW_build_protocol/'+Folder_LRR_HW_Variant_uC2

    print('Source_LRR_uC1 ->',Source_LRR_uC1) 
    print('Source_LRR_uC2 ->',Source_LRR_uC2) 
    print('Destination_LRR_uC1_int ->',Destination_LRR_uC1_int) 
    print('Destination_LRR_uC2_int ->',Destination_LRR_uC2_int) 
    print('Destination_LRR_uC1_int_final ->',Destination_LRR_uC1_int_final) 
    print('Destination_LRR_uC2_int_final ->',Destination_LRR_uC2_int_final) 

    if not os.path.exists(Destination_LRR_uC1_int):
        os.makedirs(Destination_LRR_uC1_int)
    if not os.path.exists(Destination_LRR_uC2_int):
        os.makedirs(Destination_LRR_uC2_int)
    if not os.path.exists(Destination_LRR_uC1_int_final):
        os.makedirs(Destination_LRR_uC1_int_final)
    if not os.path.exists(Destination_LRR_uC2_int_final):
        os.makedirs(Destination_LRR_uC2_int_final)

    source = os.listdir(Source_LRR_uC1)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR_uC1, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".txt", ".json")):
                shutil.copy(full_file_name, Destination_LRR_uC1_int)
                shutil.copy(full_file_name, Destination_LRR_uC1_int_final)

    Source_buildversion = Source_LRR_uC1+'/buildversion'
    Destination_buildversion_int = Destination_LRR_uC1_int+'/buildversion'
    Destination_buildversion_int_final = Destination_LRR_uC1_int_final+'/buildversion'
    Source_log = Source_LRR_uC1+'/log'
    Destination_log_int = Destination_LRR_uC1_int+'/log'
    Destination_log_int_final = Destination_LRR_uC1_int_final+'/log'

    shutil.copytree(Source_buildversion,Destination_buildversion_int)
    shutil.copytree(Source_buildversion,Destination_buildversion_int_final)
    shutil.copytree(Source_log,Destination_log_int)
    shutil.copytree(Source_log,Destination_log_int_final)

    print('COPY LRR uC1 SW_BUILD_PROTOCOL AND BUILDVERSIONINFO SUCCESSFUL\n')

    source = os.listdir(Source_LRR_uC2)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR_uC2, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".txt", ".json")):
                shutil.copy(full_file_name, Destination_LRR_uC2_int)
                shutil.copy(full_file_name, Destination_LRR_uC2_int_final)

    Source_buildversion = Source_LRR_uC2+'/buildversion'
    Destination_buildversion_int = Destination_LRR_uC2_int+'/buildversion'
    Destination_buildversion_int_final = Destination_LRR_uC2_int_final+'/buildversion'
    Source_log = Source_LRR_uC2+'/log'
    Destination_log_int = Destination_LRR_uC2_int+'/log'
    Destination_log_int_final = Destination_LRR_uC2_int_final+'/log'

    shutil.copytree(Source_buildversion,Destination_buildversion_int)
    shutil.copytree(Source_buildversion,Destination_buildversion_int_final)
    shutil.copytree(Source_log,Destination_log_int)
    shutil.copytree(Source_log,Destination_log_int_final)

    print('COPY LRR uC2 SW_BUILD_PROTOCOL AND BUILDVERSION SUCCESSFUL\n')


#Copy sw_build_config
    print('COPY sw_build_config')
    Source = MainSource_archive+'/SW_build_config'
    Destination_LRR_int = MainDestination_LRR_internal+'/static_analysis/SW_build_config'
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/static_analysis/SW_build_config'

    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int)
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)

    if not os.path.exists(Destination_LRR_int):
        os.makedirs(Destination_LRR_int)
    if not os.path.exists(Destination_LRR_int_final):
        os.makedirs(Destination_LRR_int_final)

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".txt", ".bat", ".flux", "_C0.cmake", "_settings.cmake", "Premium_LayoutLinker.cmake", Folder_LRR_HW_Variant_uC1+".cmake", Folder_LRR_HW_Variant_uC2+".cmake", "config_uC2.cmake")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)

    Source_jenkins = Source+'/jenkins'
    Destination_LRR_jenkins_int = Destination_LRR_int+'/jenkins'
    Destination_LRR_jenkins_int_final = Destination_LRR_int_final+'/jenkins'
    shutil.copytree(Source_jenkins,Destination_LRR_jenkins_int)
    shutil.copytree(Source_jenkins,Destination_LRR_jenkins_int_final)

    print('COPY SW_BUILD_CONFIG SUCCESSFUL\n')

#Copy rbPdm generated files

    print('COPY sw_build_config')
    Source = MainSource_unarchive+'/rbPdmGen_'+Folder_LRR_HW_Variant_uC2
    Destination_LRR_int = MainDestination_LRR_internal+'/static_analysis/SW_build_config/rbPdmGen'
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/static_analysis/SW_build_config/rbPdmGen'

    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int)
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)

    if not os.path.exists(Destination_LRR_int):
        os.makedirs(Destination_LRR_int)
    if not os.path.exists(Destination_LRR_int_final):
        os.makedirs(Destination_LRR_int_final)

    source = os.listdir(Source)

    for file_name in source:
        full_file_name = os.path.join(Source, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".c", ".h", ".cpp", ".hpp", ".xml", ".arxml")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)


#Copy SW Integration Test Results
    print('COPY SW Integration and SW Test Results')
    Source_LRR = MainSource_unarchive+'/SoftIntTest_fr5cu_C0'
    Destination_LRR_int = MainDestination_LRR_internal+'/test_reports_gen/SoftIntTest_C0'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/test_reports_gen/SoftIntTest_C0'  
    
    print('Source_LRR ->',Source_LRR) 
    print('Destination_LRR_int ->',Destination_LRR_int)
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)
    
    shutil.copytree(Source_LRR,Destination_LRR_int)
    shutil.copytree(Source_LRR,Destination_LRR_int_final)

    Source_LRR = MainSource_unarchive+'/SoftIntTest_fr5cu_unstable_C0'
    Destination_LRR_int = MainDestination_LRR_internal+'/test_reports_gen/SoftIntTest_unstable_C0'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/test_reports_gen/SoftIntTest_unstable_C0'  
    
    print('Source_LRR ->',Source_LRR) 
    print('Destination_LRR_int ->',Destination_LRR_int)
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)
    
    shutil.copytree(Source_LRR,Destination_LRR_int)
    shutil.copytree(Source_LRR,Destination_LRR_int_final)

    Source_LRR = MainSource_unarchive+'/SoftIntTest_fr5cu_C1'
    Destination_LRR_int = MainDestination_LRR_internal+'/test_reports_gen/SoftIntTest_C1'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/test_reports_gen/SoftIntTest_C1'  

    print('Source_LRR ->',Source_LRR) 
    print('Destination_LRR_int ->',Destination_LRR_int)
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)
    
    shutil.copytree(Source_LRR,Destination_LRR_int)
    shutil.copytree(Source_LRR,Destination_LRR_int_final)

    Source_LRR = MainSource_unarchive+'/SoftIntTest_fr5cu_unstable_C1'
    Destination_LRR_int = MainDestination_LRR_internal+'/test_reports_gen/SoftIntTest_unstable_C1'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/test_reports_gen/SoftIntTest_unstable_C1'  

    print('Source_LRR ->',Source_LRR) 
    print('Destination_LRR_int ->',Destination_LRR_int)
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)
    
    shutil.copytree(Source_LRR,Destination_LRR_int)
    shutil.copytree(Source_LRR,Destination_LRR_int_final)

    print('COPY SW INTEGRATION AND SW TEST RESULTS SUCCESSFUL\n')

#Copy QAC Warnings
    print('COPY QAC Warnings')
    Source_LRR_uC1 = MainSource_archive+'/Quality_reports/QAC_reports/'+Folder_LRR_HW_Variant_uC1
    Source_LRR_uC2 = MainSource_archive+'/Quality_reports/QAC_reports/'+Folder_LRR_HW_Variant_uC2
    Source_LRR_total = MainSource_archive+'/Quality_reports/QAC_reports/Total_FR5CU'
    Destination_LRR_int_uC1 = MainDestination_LRR_internal+'/static_analysis/QAC_Warnings/'+Folder_LRR_HW_Variant_uC1
    Destination_LRR_int_uC2 = MainDestination_LRR_internal+'/static_analysis/QAC_Warnings/'+Folder_LRR_HW_Variant_uC2
    Destination_LRR_int_total = MainDestination_LRR_internal+'/static_analysis/QAC_Warnings'
    Destination_LRR_int_final_uC1 = MainDestination_LRR_int_final+'/static_analysis/QAC_Warnings/'+Folder_LRR_HW_Variant_uC1
    Destination_LRR_int_final_uC2 = MainDestination_LRR_int_final+'/static_analysis/QAC_Warnings/'+Folder_LRR_HW_Variant_uC2
    Destination_LRR_int_final_total = MainDestination_LRR_int_final+'/static_analysis/QAC_Warnings'

    print('Source LRR uC1 ->',Source_LRR_uC1)
    print('Source LRR uC2 ->',Source_LRR_uC2) 
    print('Source LRR total ->',Source_LRR_total) 
    print('Destination_LRR_int_uC1 ->',Destination_LRR_int_uC1)
    print('Destination_LRR_int_uC2 ->',Destination_LRR_int_uC2)
    print('Destination_LRR_int_total ->',Destination_LRR_int_total)
    print('Destination_LRR_int_final_uC1 ->',Destination_LRR_int_final_uC1)
    print('Destination_LRR_int_final_uC2 ->',Destination_LRR_int_final_uC2)
    print('Destination_LRR_int_final_total ->',Destination_LRR_int_final_total)

    if not os.path.exists(Destination_LRR_int_uC1):
        os.makedirs(Destination_LRR_int_uC1)
    if not os.path.exists(Destination_LRR_int_uC2):
        os.makedirs(Destination_LRR_int_uC2)
    if not os.path.exists(Destination_LRR_int_final_uC1):
        os.makedirs(Destination_LRR_int_final_uC1)
    if not os.path.exists(Destination_LRR_int_final_uC2):
        os.makedirs(Destination_LRR_int_final_uC2)

    source = os.listdir(Source_LRR_uC1)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR_uC1, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".csv")):
                shutil.copy(full_file_name, Destination_LRR_int_uC1)
                shutil.copy(full_file_name, Destination_LRR_int_final_uC1)

    source = os.listdir(Source_LRR_uC2)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR_uC2, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".csv")):
                shutil.copy(full_file_name, Destination_LRR_int_uC2)
                shutil.copy(full_file_name, Destination_LRR_int_final_uC2)

    source = os.listdir(Source_LRR_total)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR_total, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".csv")):
                shutil.copy(full_file_name, Destination_LRR_int_total)
                shutil.copy(full_file_name, Destination_LRR_int_final_total)


    print('COPY QAC WARNINGS SUCCESSFUL\n')

#Copy Coverity Warnings
    print('COPY Coverity Warnings')
    Source_LRR_uC1 = MainSource_archive+'/Quality_reports/Coverity/uC1/cov-format-errors'
    Source_LRR_uC2 = MainSource_archive+'/Quality_reports/Coverity/uC2/cov-format-errors'
    Destination_LRR_uC1_int = MainDestination_LRR_internal+'/static_analysis/Coverity/uC1'
    Destination_LRR_uC2_int = MainDestination_LRR_internal+'/static_analysis/Coverity/uC2'
    Destination_LRR_uC1_int_final = MainDestination_LRR_int_final+'/static_analysis/Coverity/uC1'
    Destination_LRR_uC2_int_final = MainDestination_LRR_int_final+'/static_analysis/Coverity/uC2'

    print('Source_LRR_uC1 ->',Source_LRR_uC1) 
    print('Source_LRR_uC2 ->',Source_LRR_uC2) 
    print('Destination_LRR_uC1_int ->',Destination_LRR_uC1_int) 
    print('Destination_LRR_uC2_int ->',Destination_LRR_uC2_int) 
    print('Destination_LRR_uC1_int_final ->',Destination_LRR_uC1_int_final) 
    print('Destination_LRR_uC2_int_final ->',Destination_LRR_uC2_int_final) 

    if not os.path.exists(Destination_LRR_uC1_int):
        os.makedirs(Destination_LRR_uC1_int)
    if not os.path.exists(Destination_LRR_uC2_int):
        os.makedirs(Destination_LRR_uC2_int)
    if not os.path.exists(Destination_LRR_uC1_int_final):
        os.makedirs(Destination_LRR_uC1_int_final)
    if not os.path.exists(Destination_LRR_uC2_int_final):
        os.makedirs(Destination_LRR_uC2_int_final)

    source = os.listdir(Source_LRR_uC1)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR_uC1, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".csv", ".json")):
                shutil.copy(full_file_name, Destination_LRR_uC1_int)
                shutil.copy(full_file_name, Destination_LRR_uC1_int_final)

    source = os.listdir(Source_LRR_uC2)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR_uC2, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith((".csv", ".json")):
                shutil.copy(full_file_name, Destination_LRR_uC2_int)
                shutil.copy(full_file_name, Destination_LRR_uC2_int_final)

    print('COPY COVERITY WARNINGS SUCCESSFUL\n')

#Copy Lines of Code
    print('COPY Lines of code')
    Source = MainSource_unarchive+'/Linesofcode'
    Destination_LRR_int = MainDestination_LRR_internal+'/static_analysis/Linesofcode'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/static_analysis/Linesofcode'  
    
    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final) 

    shutil.copytree(Source,Destination_LRR_int)
    shutil.copytree(Source,Destination_LRR_int_final)

    print('COPY LINESOFCODE SUCCESSFUL\n')

#Copy Doxygen
    print('COPY Doxygen')
    Source = MainSource_unarchive+'/Doxygen'
    Destination_LRR_int = MainDestination_LRR_internal+'/documentation/Doxygen'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/documentation/Doxygen'  
    
    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int) 
    print('Destination_LRR_int_final ->',Destination_LRR_int_final) 

    shutil.copytree(Source,Destination_LRR_int)
    shutil.copytree(Source,Destination_LRR_int_final)

    print('COPY DOXYGEN SUCCESSFUL\n')

#Copy merged Hexfile for LRR
    print('COPY merged Hexfile for LRR')
    Source_LRR = MainSource_unarchive+'/Merged_Hex'
    Destination_LRR_int = MainDestination_LRR_internal+'/tools/VFlash/VflashGeneric'
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/tools/VFlash/VflashGeneric'

    print('Source_LRR ->',Source_LRR) 
    print('Destination_LRR_int ->',Destination_LRR_int)
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)

    source = os.listdir(Source_LRR)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith(("Virtual.hex")):
                shutil.copy(full_file_name, Destination_LRR_int)
                shutil.copy(full_file_name, Destination_LRR_int_final)

    print('COPY MERGED HEX FOR LRR SUCCESSFUL\n')

#Copy Canoe
    print('COPY Canoe')
    Source = MainSource_unarchive+'/Canoe/canoe'
    Destination_LRR_int = MainDestination_LRR_internal+'/measurement/Canoe'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/measurement/Canoe'  
    
    print('Source ->',Source) 
    print('Destination_LRR_int ->',Destination_LRR_int)
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)

    shutil.copytree(Source,Destination_LRR_int)
    shutil.copytree(Source,Destination_LRR_int_final)

    print('COPY CANOE SUCCESSFUL\n')

    Destination_LRR_int = MainDestination_LRR_internal+'/measurement'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/measurement'  

    f = open(Destination_LRR_int+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()

    f = open(Destination_LRR_int_final+'/automatically_generated_do_not_change_anything_here.txt', 'w+')
    f.close()

#Copy canape folder
    print('COPY Canape')
    Source_LRR = MainSource_unarchive+'/MT_Update_FR5CU/Canape'
    Destination_LRR_int = MainDestination_LRR_internal+'/measurement/Canape'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/measurement/Canape'  
    
    print('Source_LRR ->',Source_LRR) 
    print('Destination_LRR_int ->',Destination_LRR_int)
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)
    
    shutil.copytree(Source_LRR,Destination_LRR_int)
    shutil.copytree(Source_LRR,Destination_LRR_int_final)

    print('COPY CANAPE SUCCESSFUL\n')

#Copy database folder
    print('COPY Database')
    Source_LRR = MainSource_unarchive+'/MT_Update_FR5CU/database'
    Destination_LRR_int = MainDestination_LRR_internal+'/measurement/database'  
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/measurement/database'  
    
    print('Source_LRR ->',Source_LRR) 
    print('Destination_LRR_int ->',Destination_LRR_int)
    print('Destination_LRR_int_final ->',Destination_LRR_int_final)
    
    shutil.copytree(Source_LRR,Destination_LRR_int)
    shutil.copytree(Source_LRR,Destination_LRR_int_final)

    print('COPY DATABASE SUCCESSFUL\n')

###############Final Release Folder ##############################################################

# Create folders
    print('Create empty folders for manual input in final release folder')
    Destination_LRR_oss = MainDestination_LRR_int_final+'/oss'
    Destination_LRR_test_reports = MainDestination_LRR_int_final+'/test_reports_manual'
    Destination_LRR_supplier_docu = MainDestination_LRR_int_final+'/supplier_docu'

    if not os.path.exists(Destination_LRR_oss):
        os.makedirs(Destination_LRR_oss)
    if not os.path.exists(Destination_LRR_test_reports):
        os.makedirs(Destination_LRR_test_reports)
    if not os.path.exists(Destination_LRR_supplier_docu):
        os.makedirs(Destination_LRR_supplier_docu)


    f = open(Destination_LRR_oss+'/put_manual_input_here.txt', 'w+')
    f.close()

    f = open(Destination_LRR_test_reports+'/put_manual_input_here.txt', 'w+')
    f.close()

    f = open(Destination_LRR_supplier_docu+'/put_manual_input_here.txt', 'w+')
    f.close()

    print('CREATE EMPTY FOLDERS SUCCESSFUL\n')

#Copy base release note folders
    print('COPY Base Releasenote folder')
    Source_LRR = MainSource_unarchive+'/rng_FR5CU/rn_TestProject'
    Destination_LRR_int_final = MainDestination_LRR_int_final+'/releasenote'  
    
    print('Source_LRR ->',Source_LRR)
    print('Destination_LRR_int_final ->',Destination_LRR_int_final) 

    shutil.copytree(Source_LRR,Destination_LRR_int_final)

    os.remove(Destination_LRR_int_final+'/build_info.json')
    os.remove(Destination_LRR_int_final+'/release_info.json')

    source = os.listdir(Source_LRR)

    for file_name in source:
        full_file_name = os.path.join(Source_LRR, file_name)
        if os.path.isfile(full_file_name):
              if full_file_name.endswith(("_info.json")):
                shutil.copy(full_file_name, MainDestination_LRR_int_final)


    #LRR Release Note
    shutil.copy(os.path.join(MainDestination_LRR_int_final,'build_info.json'), '../../rng')
    shutil.copy(os.path.join(MainDestination_LRR_int_final,'release_info.json'), '../../rng')

    import importlib
    importlib.reload(distutils.dir_util)

    distutils.dir_util.copy_tree(os.path.join(MainDestination_LRR_int_final,'releasenote'), os.path.abspath('../../rng/rn_TestProject'))

    print('\n\nGenerate release note environment locally\n\n')
    for f in os.scandir(MainDestination_LRR_int_final) :
        print(str(f.name)+'-> rng/rn_TestProject')
        try :
            if f.is_dir():
                distutils.dir_util.copy_tree(f, os.path.join(os.path.abspath('../../rng'), str(f.name)))
            if f.is_file():
                distutils.dir_util.file_copy(f, os.path.abspath('../../rng'))
        except:
            continue
            
    buildCmd = 'cd ../../rng\n '
    buildCmd  += '01_rng_export.bat\n'
    buildCmd  += '02_rng_convert.bat\n'
    buildCmd  += '03_rng_compile.bat\n'
    buildCmd  += '04_rng_create.bat\n'
    
    try:
        setProcess = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE,
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    except:
        print("Failed to open a cmd to run commands")
        sys.exit(2)
        
    try:
        buildOut, buildErr = setProcess.communicate(input=buildCmd)
        print(buildOut)
        print(buildErr)
        if re.search('WinError', buildOut) or re.search('WinError', buildErr):
            raise Exception
    except:
        print(buildErr)
        print("An rng stage failed ..........")
        sys.exit(3)
    time.sleep(10)
    distutils.dir_util.copy_tree(os.path.abspath('../../rng/rn_TestProject'), os.path.join( MainDestination_LRR_int_final,'releasenote'))
    shutil.rmtree(os.path.join( MainDestination_LRR_int_final,'releasenote', 'build_data'))

    print('COPY BASE RELEASENOTE FOLDER SUCCESSFUL\n')

####### The end of program ##################