# //=============================================================================
# //  C O P Y R I G H T
# //-----------------------------------------------------------------------------
# /// @copyright (c) 2011 - 2018 by Robert Bosch GmbH. All rights reserved.
# //
# //  The reproduction, distribution and utilization of this file as
# //  well as the communication of its contents to others without express
# //  authorization is prohibited. Offenders will be held liable for the
# //  payment of damages. All rights reserved in the event of the grant
# //  of a patent, utility model or design.
# //=============================================================================
# //  P R O J E C T   I N F O R M A T I O N
# //-----------------------------------------------------------------------------
# //     Projectname: ATR
# //  Target systems: Windows
# //       Compilers: Python
# //=============================================================================
# //  I N I T I A L   A U T H O R   I D E N T I T Y
# //-----------------------------------------------------------------------------
# //  Name: Martin Auchter
# //  Department: CC-DA/EAS2
# //=============================================================================
# /// @file  submodule_analysis.py
# /// @brief This script is for checking if the file is located within a submodule
# /// @generatedcode no
# /// @copyright Robert Bosch GmbH
# /// @Additional author Meghana N Bhushan(MS/ESD-ET3-XC)
# /// @swcomponent tools

#  Imports 
from __future__ import print_function
import os
import subprocess
import sys
import re
from collections import OrderedDict

# Return the submodule dictionary
def submodule_dict():
    # Path to the .gitmodule file
    gitmodule_file = '.gitmodules'
    # Submodule name regex
    submodule_name_regex = r'"([^"]+)"'
    # Submodule URL regex
    submodule_url_regex = r'([^/]*/[^/]*)?$'
    # Line counter
    line_counter = 0
    # Create the project/repo dictionary
    submodule_repo_dict = OrderedDict()

    # Read the gitmodule file line by line
    with open(gitmodule_file, 'r') as fgitmodules:
        # Read the gitmodules file. Every submodule has three lines in the git module file.
        lines = fgitmodules.read().splitlines()
        # Go through all the lines in the submodules file
        for line in lines:
            # Increment the line counter
            line_counter += 1
            # Find the submodule names
            if re.search(submodule_name_regex, line):
                match_name = re.search(submodule_name_regex, line)
                # Get the submodule name
                submodule_name = match_name.group(1)
                # Save the line number
                line_counter_saved = line_counter
            # Get the URL (two lines after the name)
            if line_counter == (line_counter_saved + 2):
                # Find the submodule URL
                if re.search(submodule_url_regex, line):
                    # Get the last part of the URL
                    match_url = re.search(submodule_url_regex, line)
                    # Remove the git ending
                    tmp = match_url.group(0).replace(".git", "")
                    # Replace the splash by a comma
                    project_repo = tmp.replace("/", ",")
                # Reset the counter
                line_counter_saved = 0

                # Add the submodule to the dictionary
                submodule_repo_dict.update({submodule_name:project_repo})
    
    # Return the submodule dictionary
    return submodule_repo_dict

# Check if the file is located within a submodule, if yes, return the submodule project and repo
def submodule_file_check(file_path, submodule_dictionary):
    # Go through the dict
    for submodule in submodule_dictionary:
        # Check if the file path contains the submodule
        if submodule in file_path:
            # Split up the project and repo
            tmp = submodule_dictionary[submodule]
            tmp_list = tmp.split(',')
            # Assign the values
            sub_project = tmp_list[0]
            sub_repo = tmp_list[1]
            # Remove the submodule project and repo from file_path (only needed for artifactory)
            submodule_path = submodule + '/'
            adapted_file_path = file_path.replace(submodule_path, '')
            # Return the values
            return sub_project, sub_repo, adapted_file_path
        else:
            pass

    # File not in a submodule --> file in main repo --> return nothing
    return '', '', ''