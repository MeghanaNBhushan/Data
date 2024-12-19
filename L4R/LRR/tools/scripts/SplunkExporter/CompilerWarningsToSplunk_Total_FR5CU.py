#//=============================================================================
#//  C O P Y R I G H T
#//-----------------------------------------------------------------------------
#/// @copyright (c) 2011 - 2018 by Robert Bosch GmbH. All rights reserved.
#//
#//  The reproduction, distribution and utilization of this file as
#//  well as the communication of its contents to others without express
#//  authorization is prohibited. Offenders will be held liable for the
#//  payment of damages. All rights reserved in the event of the grant
#//  of a patent, utility model or design.
#//=============================================================================
#//  P R O J E C T   I N F O R M A T I O N
#//-----------------------------------------------------------------------------
#//     Projectname: ATR
#//  Target systems: Windows
#//       Compilers: Python
#//=============================================================================
#//  I N I T I A L   A U T H O R   I D E N T I T Y
#//-----------------------------------------------------------------------------
#//  Name: Meghana N Bhushan
#//  Department: MS/ESD-ET3-XC
#//=============================================================================
#/// @brief This script merges UC1 and UC2 compiler warnings and uploads report to Artifactory
#/// @generatedcode no
#/// @copyright Robert Bosch GmbH
#/// @author Meghana N Bhushan (MS/ESD-ET3-XC)
#/// @swcomponent tools

#!/usr/bin/env python
# -*- coding: utf-8 -*- import os
import shutil
import re
import sys, os
import csv
import argparse
import pandas as pd

# Create argument parser
parser = argparse.ArgumentParser(description='merge uc1 and uc2 compiler warnings')
# Define arguments
parser.add_argument('--UC1', required=True, help='FR5CU_DNNN1_NNN_N_XX_2_uC1')
parser.add_argument('--UC2', required=True, help='FR5CU_DENN1_CEN_N_XX_2_uC2')
# Parse arguments
args = parser.parse_args()
UC1=args.UC1
UC2=args.UC2

#get current working directory
cwd = os.getcwd()
projectPath = os.path.join(cwd, '../../../../')

# opening the source csv files
uc1_file =os.path.join(projectPath, '//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI/Splunk/CompilerWar_'+UC1+'.csv')
uc2_file =os.path.join(projectPath, '//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI/Splunk/CompilerWar_'+UC2+'.csv')
#create destination file
dest_filename = os.path.join(projectPath, '//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI/Splunk/CompilerWar_Total_FR5CU.csv')

uc1_dataframe = pd.read_csv(uc1_file, header=0)
uc2_dataframe = pd.read_csv(uc2_file, header=0)
merged_dataframe=pd.concat([uc1_dataframe,uc2_dataframe]).drop_duplicates(subset=['File path', 'File name', 'Type'])
print("merged warning list")
print(merged_dataframe)
#export conactinated dataframe to csv
merged_dataframe.to_csv(dest_filename, index=False, encoding='utf-8')