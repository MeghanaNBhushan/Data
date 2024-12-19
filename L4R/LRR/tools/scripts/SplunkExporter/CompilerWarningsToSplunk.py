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
#//  Name: Archana Halehalli Lokesh
#//  Department: RBEI/ESD-PP2
#//=============================================================================
#/// @brief This script uploads Compiler_warning report to Artifactory
#/// @generatedcode no
#/// @copyright Robert Bosch GmbH
#/// @additional author Meghana N Bhushan (MS/ESD-ET3-XC)
#/// @swcomponent tools

#---------
# Imports
#---------
from __future__ import print_function
import os
import sys
import csv
import argparse
import shutil
import pandas as pd
from lib import submodule_analysis
cwd = os.getcwd()
os.chdir('../../../../')

# Create argument parser
parser = argparse.ArgumentParser(description='Upload compiler warning to Artifactory')

# Define arguments
parser.add_argument('--HW_Variant', required=True, help='FR5CU_DNNN1_NNN_N_XX_2_uC1/FR5CU_DENN1_CEN_N_XX_2_uC2')

# Parse arguments
args = parser.parse_args()


# csv report to be uploaded
HW_Variant=args.HW_Variant
detailed_report = 'generatedFiles\Radar_'+HW_Variant+'\log\CompilerWar_'+HW_Variant+'.csv'

#-----------------------------------------------------
# trim file path in csv file (detailed_report)
#-----------------------------------------------------
def trim_file_path_csv(detailed_report):
    # Read csv file
    read_csv = csv.reader(open(detailed_report))
    # Convert to list
    lines = list(read_csv)
    for row in lines:
        if "repo" in row[0]:
            # Remove until "repo\" eg as in D:\LRR\repo\rc_fw\dsp\SW\src\dsp\xuc\_datadef\uC2\dsp_hssl_datadef_dsp_dataStatus.h
            row[0] = row[0].split("repo\\")[1]
    # Write back to csv
    writer = csv.writer(open(detailed_report, 'w'))
    writer.writerows(lines)

#-----------------------------------------------------
# Update csv file with submodule information
#-----------------------------------------------------
def submodule_csv_update(report_file):
    # Line counter
    line_counter = 0
    # Get the submodule dictionary
    submodules_dict = submodule_analysis.submodule_dict()
    # Create new file
    detailed_report_new = report_file.replace('.csv', '_new.csv')
    # Open the file
    fdetailed_report = open(detailed_report_new, "w+")

    # Read in the report
    with open(report_file, 'r') as freport:
        # Read the lines
        report_lines = freport.read().splitlines()
        # Go through the lines
        for report_line in report_lines:
            # Increment the counter
            line_counter += 1
            # Add the new columns required for the submodules
            if line_counter == 1:
                # Append the new columns
                fdetailed_report.write(report_line + ',Subproject,Subrepo\n')
            # Modify the rest of the lines
            else:
                if report_line != '':
                    # Temp line
                    modified_line = ''
                    # Split up the line
                    csv_line_content = report_line.split(',')
                    csv_line_length = range(len(csv_line_content))
                    # Perform check if file is located in a submodule
                    sub_repo, sub_project, modified_file_path = submodule_analysis.submodule_file_check(csv_line_content[0].replace('\\','/'), submodules_dict)
                    # Change the file path
                    #if modified_file_path != '':
                        #csv_line_content[0] = modified_file_path.replace('/','\\')
                    # Assemble the list again
                    for n in csv_line_length:
                        modified_line += csv_line_content[n] + ','
                    # Add the submodule repo and project
                    modified_line += sub_repo + ',' + sub_project
                    # Add the modified line to the report
                    fdetailed_report.write(modified_line + '\n')
    
    # Close the file
    fdetailed_report.close()
    # Delete old file and rename new file
    rename_delete_file(report_file, detailed_report_new)

#-----------------------------------------------------
# Update file names
#-----------------------------------------------------
def rename_delete_file(delete_file, rename_file):
    # Delete the old file
    if os.path.isfile(delete_file) == True:
        # Remove csv file
        os.remove(delete_file)
    else:
        print('File does not exist.')
    
    # Rename new file
    os.rename(rename_file, delete_file)

def copy_to_sharedrive(report_file):
    if os.path.isfile(report_file) == True:
        # copy report to sharedrive
        shutil.copy(report_file, "//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI/Splunk/.")
    else:
        print('File does not exist.')

def remove_duplicates(report_file):
    if os.path.isfile(report_file) == True:
        # remove duplicates baed on file path, file name and warning id
        dataframe = pd.read_csv(report_file, header=0)
        final_dataframe=dataframe.drop_duplicates(subset=['File path', 'File name', 'Row', 'Type'])
        final_dataframe.to_csv(report_file, index=False, encoding='utf-8')
    else:
        print('File does not exist.')
#---------------
# Main function
#---------------
def main():
    """ Main function """
    # Clean up the file paths
    trim_file_path_csv(detailed_report)
    # Update the csv file with the submodule information
    submodule_csv_update(detailed_report)
    # remove duplicated warningss
    remove_duplicates(detailed_report)
    # copy the csv file to share drive
    copy_to_sharedrive(detailed_report)

if __name__ == "__main__":
    main()