#!/usr/bin/env python3
"""
process resource consumption data

# Author: Jochen Held (XC-DA/EDB7)
"""

import os
import glob
from pathlib import Path
import csv
import pandas as pd

adoc_table_cfg = {
    "headerFormat": '[width="100%",cols="20%,20%,20%,20%,20%,20%,20%,20%,20%, options="header"]',
    "tableName": "Resource Concumption",
}

INPUT_FILE_SEARCH_STRING = "Calcres_Report_summary*"
OUTPUT_FILE_NAME = "resourceconsumption_adoc"


def generate_resource_consumption_adoc(input_dir, output_dir):

    os.chdir(input_dir)

    # To search for specific extension
    # extension = 'csv'
    # for counter, file in enumerateglob.glob('*.{}'.format(extension)):
    for counter, file in enumerate(glob.glob(INPUT_FILE_SEARCH_STRING)):
        with open(file) as csv_file:
            csv_data = list(csv.reader(csv_file, delimiter=","))

            # Remove all lines empty lines / invalid data
            csv_cleaned = []
            for element in csv_data:
                # Ignor empty rows
                if len(element) > 0:
                    csv_cleaned.append(element)
            csv_data = csv_cleaned

            with open(
                Path(output_dir).joinpath(
                    OUTPUT_FILE_NAME + "_" + str(counter + 1) + ".txt"
                ),
                "w+",
                newline="",
            ) as adoc_file:
                adoc_file.write(
                    "." + adoc_table_cfg["tableName"] + str(counter + 1) + os.linesep
                )
                adoc_file.write(adoc_table_cfg["headerFormat"] + os.linesep)
                adoc_file.write("|===" + os.linesep)
                for row in csv_data:
                    for item in row:
                        adoc_file.write("|" + str(item))
                    adoc_file.write(os.linesep)
                adoc_file.write("|===" + os.linesep)


def main():

    input_dir = "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/original"
    output_dir = "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/input/"

    generate_resource_consumption_adoc(input_dir, output_dir)


if __name__ == "__main__":
    main()
