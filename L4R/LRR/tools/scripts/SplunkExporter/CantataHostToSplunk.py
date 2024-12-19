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
import openpyxl
import argparse
import shutil
import pandas as pd
from lib import submodule_analysis
cwd = os.getcwd()
os.chdir('../../../../')

# Create argument parser
parser = argparse.ArgumentParser(description='Upload compiler warning to Artifactory')

# Define arguments
parser.add_argument('--HW_Variant', required=True, help='FR5CU_DENN1_CEN_N_XX_2_uC2')

# Parse arguments
args = parser.parse_args()


# csv report to be uploaded
HW_Variant=args.HW_Variant
initial_report = 'generatedFiles/SWQualityReports/Cantata'+'/'+'Host_Radar_'+ HW_Variant+'/'+'Cantata.xlsx'
detailed_report = 'generatedFiles/SWQualityReports/Cantata'+'/'+'Cantata_Host_'+ HW_Variant + '.csv'

#-----------------------------------------------------
# Convert input xlsx to csv (detailed_report)
#-----------------------------------------------------
def xlsx_to_csv(initial_report):
    read_file = pd.read_excel (initial_report)
    read_file.to_csv (detailed_report, index = None, header=True)


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
        shutil.copy(report_file, "//abtvdfs1.de.bosch.com/ismdfs/ida/abt/SW_Build/Radar/SystemC/Athena_Radar/CI/Splunk/Cantata/.")
    else:
        print('File does not exist.')

#---------------
# Main function
#---------------
def main():
    """ Main function """
    #convert xlsx to csv
    xlsx_to_csv(initial_report)
    # Update the csv file with the submodule information
    submodule_csv_update(detailed_report)
    # copy the csv file to share drive
    copy_to_sharedrive(detailed_report)

if __name__ == "__main__":
    main()