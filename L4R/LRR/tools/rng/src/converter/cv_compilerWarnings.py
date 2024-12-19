#!/usr/bin/env python3
"""
process compiler warnings data

# Author: Jochen Held (XC-DA/EDB7)
"""

import os
import glob
from pathlib import Path
import csv
import pandas as pd
import sys

# ********** ATTENTION **********
# categerories with multiple subpathes have to given in the order of path depths to ensure correct (unique counting)
# Example: ip_if/rba/CUBAS/, ip_if, ip_if/mom/daddy, ip_if/rba/CUBAS/ComServices
# Correct order: ip_if/rba/CUBAS/ComServices, ip_if/rba/CUBAS/, ip_if/mom/daddy, ip_if
categories = {
    "L4 Radar": "ad_radar_apl",
    "L4 Radar generated": "generatedFiles",
    "Other": "ip_dc",
    "CUBAS": "ip_if/rba/CUBAS/",
    "PJ-IF": "ip_if",
    "DSP": "rc_fw",
}

adoc_table_cfg = {
    "headerFormat": '[width="100%",cols="50%,25%,25%", options="header"]',
    "tableName": "Compiler Warnings",
    "ColumnTitles": "| sw_part | Deprecated | Warning",
}

csv_header = ["Category", "Type", "File", "Description"]

INPUT_FILE_SEARCH_STRING = "CompilerWarnings*"
OUTPUT_FILE_NAME = "CompilerWarnings_adoc"


def generate_compiler_warnings_adoc(input_dir, output_dir):

    try:
        os.chdir(input_dir)
    
        csv_joined = []
    
        # To search for specific extension
        # extension = 'csv'
        # for counter, file in enumerateglob.glob('*.{}'.format(extension)):
        for counter, file in enumerate(glob.glob(INPUT_FILE_SEARCH_STRING)):
            with open(file) as csv_file:
                csv_data = list(csv.reader(csv_file, delimiter=","))
    
                # Special Handling Start
                # Special Handling for Compiler Warnings
                # Remove all lines empty lines / invalid data
                csv_cleaned = []
                for element in csv_data:
                    # Valid data contains File name and warning in sepreate entries => >=2
                    if len(element) >= 2:
                        # in case length is greater than 2 additional unwanted data is in list
                        if len(element) >= 3:
                            # del element[2 - len(element)]
                            del element[2 : len(element)]
                        csv_cleaned.append(element)
                csv_data = csv_cleaned
                # Special Handling End
    
                csv_joined += csv_data
    
        # Categorize elements and add collumns to csv for further pivot processing
        for element in csv_joined:
            for categorie, value in categories.items():
                if value in element[0]:
                    if "deprecated" in element[1]:
                        element.insert(0, "Deprecated")
                    else:
                        element.insert(0, "Warning")
                    element.insert(0, categorie)
                    break
    
        # Create panda data frame from imported data and add header info
        df = pd.DataFrame.from_records(csv_joined, columns=csv_header)
    
        # Create Pivot table to calcluate accumulated sum of values
        pivot_export = pd.pivot_table(
            df,
            index=["Category"],
            columns="Type",
            values="File",
            aggfunc="count",
            fill_value=0,
        )
    
        # convert data to list object to make it easier to export adoc style table
        pivot_list = pivot_export.reset_index().values.tolist()
    
        with open(
            Path(output_dir).joinpath(OUTPUT_FILE_NAME + ".txt"),
            "w+",
            newline="",
            # encoding="utf-8-sig",
        ) as adoc_file:
            # adoc_file.write("." + adoc_table_cfg["tableName"] + os.linesep)
            adoc_file.write(adoc_table_cfg["headerFormat"] + os.linesep)
            adoc_file.write("|===" + os.linesep)
            adoc_file.write(adoc_table_cfg["ColumnTitles"] + os.linesep)
            for row in pivot_list:
                for item in row:
                    adoc_file.write("|" + str(item))
                adoc_file.write(os.linesep)
            adoc_file.write("|===" + os.linesep)
    except Exception as e :
        print(e)
        sys.exit(10)
        


def main():

    input_dir = "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/build_data"
    output_dir = "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/adoc_input/"

    generate_compiler_warnings_adoc(input_dir, output_dir)


if __name__ == "__main__":
    main()
