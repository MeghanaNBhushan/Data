__copyright__ = """
@copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""
import os
import sys
import re
from collections import defaultdict

from tqdm import tqdm

import argparse

script_dir_path = os.path.dirname(os.path.abspath(__file__))

"""Import of Python Utils"""
python_utilities_path = os.path.abspath(os.path.join(script_dir_path, '../'))
sys.path.append(python_utilities_path)
from python_utilities import *

"""Import of auxiliar files"""
aux_path = os.path.abspath(os.path.join(script_dir_path, 'auxiliar/'))
sys.path.append(aux_path)
from file import *

# Console output switch
global g_verbose_mode
g_verbose_mode = True

if __name__ == "__main__":
    args = sys.argv[1:]
    ConsoleOutput(bcolors.OKBLUE, "build_log_parser", "Received arguments: ", g_verbose_mode, "debug_mode")
    ConsoleOutput(bcolors.OKBLUE, "build_log_parser", ' '.join(args), g_verbose_mode, "debug_mode")

    parser=argparse.ArgumentParser()
    parser.add_argument('--build_log', type=str, help='Path to the build log file.', required=True)
    parser.add_argument('--warnings_by_file', action='store_true', help='Shows the amount of warning per file.')
    parser.add_argument('--files_ranking', action='store_true', help='Shows the overall file\'s warnings ranking.')
    parser.add_argument('--warnings_ranking', action='store_true', help='Shows the overall warnings ranking.')
    parser.add_argument('--check_build_completed', action='store_true', help='Checks if build reached 100%.')

    args = parser.parse_args()

    if os.path.exists(args.build_log):
        file_path = args.build_log
    else:
        print("File provided with '--build_log' does not exist.")
        sys.exit(1)

    total_lines = sum(1 for line in open(file_path, 'r'))

    # Open the log file
    with open(file_path, 'r') as f:
        file_list = {}
        warning_list = {}
        build_completed = False

        # Loop through each line in the file
        for line in tqdm(f, total=total_lines, desc="Processing", unit="line"):
            # Use regular expressions to extract the data
            regex = r"(.+?):(\d+:\d+): (.+?) \[(.+?)\]"
            match = re.search(regex, line)
            if match:
                filename = match.group(1)
                position = match.group(2)
                message = match.group(3)
                flag = match.group(4)
                
                if filename not in file_list:
                    file_record = File(filename)
                    file_list[filename] = file_record
                
                file_list[filename].add_warning(message, position)

                if message not in warning_list:
                    warning_list[message] = Warning(message, position)
                elif message in warning_list and position not in warning_list[message].position:
                    warning_list[message].increase_counter(position)

            if re.search(r'\[100%\]', line):
                print(f'"{line}" contains 100%')
                build_completed = True

        if args.warnings_by_file:
            file_list_sorted = dict(sorted(file_list.items()))
            print("Warning by file: ")
            for file_name, file_info_dict in file_list_sorted.items():
                print(f"File: {file_name}: {file_info_dict.counter}")
                for warning_key, warning_data in file_info_dict.warnings.items():
                    print(f" - {warning_data.message}: {warning_data.counter}")
                print("------------------------------------------------------------------------------")
                print("")

        if args.files_ranking:
            warning_counts_by_file_sorted = dict(sorted(file_list.items(), key=lambda item: item[1].counter, reverse=True))
            print("File ranking: ")
            for file, file_data in warning_counts_by_file_sorted.items():
                print(f" - {file}: {file_data.counter}")
            print("------------------------------------------------------------------------------")
            print("")

        if args.warnings_ranking:
            warning_counts_by_warning_sorted = dict(sorted(warning_list.items(), key=lambda item: item[1].counter, reverse=True))
            print("Warning counts by warning: ")
            for warning_type, warning_data in warning_counts_by_warning_sorted.items():
                print(f" - {warning_type}: {warning_data.counter}")
            print("------------------------------------------------------------------------------")
            print("")

        if args.check_build_completed:
            if build_completed == True:
                sys.exit(0)
            else:
                sys.exit(1)