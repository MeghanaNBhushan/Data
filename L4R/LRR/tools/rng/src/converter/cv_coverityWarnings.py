#!/usr/bin/env python3
"""
process coverity warnings data

# Author: Jochen Held (XC-DA/EDB7)
"""

import os
import glob
from pathlib import Path
import csv
import pandas as pd

from pathlib import Path
import logging

logger = logging.getLogger(__name__)

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

INPUT_FILE_SEARCH_STRING = "json-output-export*"
OUTPUT_FILE_NAME = "coverityWarnings_adoc"

c_suffix = (".c", ".h")
cpp_suffix = (".cpp", ".hpp")
inl_suffix = ".inl"


def generate_coverity_warnings_adoc(input_dir, output_dir):

    os.chdir(input_dir)

    # To search for specific extension
    # extension = 'csv'
    # for counter, file in enumerateglob.glob('*.{}'.format(extension)):
    for counter, file in enumerate(
        glob.glob(
            str(Path(input_dir)) + "/**/json-output-export*",
            recursive=True,
        )
    ):
        with open(file) as csv_file:
            csv_data = list(csv.reader(csv_file, delimiter=","))

            # # Categorize elements and add collumns to csv for further pivot processing
            for element in csv_data[1:]:

                # Append column with programming language per file bases on file extension e.g. C, CPP
                if Path(element[0]).suffix in c_suffix:
                    element.append("C")
                elif Path(element[0]).suffix in cpp_suffix:
                    element.append("CPP")
                elif Path(element[0]).suffix in inl_suffix:
                    element.append("inl")
                else:
                    logger.warning(
                        "Warning: "
                        + element[0]
                        + " could not be mapped to category, added to category OTHER"
                    )
                    element.append("Other")

                # Append column with category based on categeroy array given
                categorie_found = False
                for categorie, value in categories.items():
                    if value in element[0]:
                        element.append(categorie)
                        categorie_found = True
                        break
                if categorie_found == False:
                    element.append("Other")
                    logger.warning(
                        "Warning: "
                        + element[0]
                        + " could not be mapped to category, added to category OTHER"
                    )
                # TODO: Add log entry

            # add "Language" to csv header
            csv_data[0].append("prog_language")
            # add "Category" to csv header
            csv_data[0].append("sw_part")

            # Create panda data frame from imported data and add header info
            df = pd.DataFrame.from_records(csv_data[1:], columns=csv_data[0])

            # Create Pivot table to calcluate accumulated sum of values
            pivot_export = pd.pivot_table(
                df,
                index=["sw_part", "prog_language"],
                columns="impact",
                values="checkerName",
                aggfunc="count",
                margins=True,
                fill_value=0,
            )

            logger.debug(pivot_export)

            # "Flatten" the pivot tabel headers to a single header
            adoc_table_header = list(pivot_export.index.names) + list(
                pivot_export.columns.values
            )

            # convert data to list object to make it easier to export adoc style table
            adoc_table = pivot_export.reset_index().values.tolist()

            # add the new header to the list
            adoc_table.insert(0, adoc_table_header)

            # h_start is the static part which is determined by the index choosen in the pivot table.
            # this index do not change if the pivot table isn't changed
            h_start = '[width="100%", cols="3a,1a'
            # the next columns depend on what is found in the dataset. e.g. if there no Medium warnings,
            # the column will not exist, i.e less columns to display
            h_index = str()
            for i in range(pivot_export.columns.values.size):
                h_index += ",1a"
            h_end = '", options="header"]'
            adoc_table_header_Format = h_start + h_index + h_end

            with open(
                Path(output_dir).joinpath(
                    OUTPUT_FILE_NAME + "_" + str(counter + 1) + ".txt"
                ),
                "w+",
                newline="",
            ) as adoc_file:
                adoc_file.write(adoc_table_header_Format + os.linesep)
                adoc_file.write("|===" + os.linesep)
                for row in adoc_table:
                    for item in row:
                        adoc_file.write("|" + str(item))
                    adoc_file.write(os.linesep)
                adoc_file.write("|===" + os.linesep)


def main():

    input_dir = (
        "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/build_data/Coverity"
    )
    output_dir = "C:/Users/hej3lr/git/releasenotegenerator/rn_TestProject/adoc_input/"

    generate_coverity_warnings_adoc(input_dir, output_dir)


if __name__ == "__main__":
    main()
