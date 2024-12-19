#!/usr/bin/env python3
"""
This script compiles the adoc file from different sources using


Author:  Jochen Held (XC-DA/EDB7)
"""

from pathlib import Path
import sys
import json
import re
from jinja2 import Template, Environment, FileSystemLoader

import logging

logger = logging.getLogger(__name__)

# TODO: This configuration needs to go into global config file or needs to be read from a file here
# Global Config values
ADOC_BASE_FILE = "releasenote_base.adoc"
ADOC_GEN_FILE = "releasenote_gen.adoc"
BUILD_INFO_FILE = "build_info.json"
RELEASE_INFO_FILE = "release_info.json"

# Function to read JSON file
def read_json_file(json_file_path):
    """
    Read a json file

    Args:
        json_file_path: full path to json file

    Return:
        json_data: dict of json data
    """
    json_data = None

    try:
        with open(json_file_path, "r", newline="", encoding="utf-8-sig") as json_file:
            json_data = json.load(json_file)
    except EnvironmentError:
        logger.error("Importing " + Path(json_file_path).name + "failed")
        sys.exit(10)
    return json_data


def data2list(d, list, start):
    # check if the value field is in the validation options
    if "validation" in d.keys() and (d["validation"] != ""):
        if d["value"] not in d["validation"].split("|"):
            logger.error(
                "*** "
                + d["value"]
                + " *** is not a valid value for "
                + start
                + " -> "
                + d["validation"]
            )

    # create a list of values from the project data
    for k, v in d.items():
        if isinstance(v, dict):
            data2list(v, list, start + "." + k)
        else:
            if k == "value":
                list.append(start + "." + k)


# Main script function
def compile_adoc(build_dir, adoc_input_dir, adoc_dir):
    """
    generates the adoc document based on release input data

    Args:
        build_dir: path to release/build folder
        adoc_input_dir: path to the input data
        adoc_dir: storage of adoc base document which is updated by this function
    Return:
        -
    """

    logger.info("Generation of asciDoc draft started")
    # run the jinja template engine
    # read project data from a json files (build_info and release_info)
    # convert json to directory for the jinja template
    build_info_data = read_json_file(Path(build_dir).joinpath(BUILD_INFO_FILE))
    release_info_data = read_json_file(Path(build_dir).joinpath(RELEASE_INFO_FILE))
    projectData = {**build_info_data, **release_info_data}

    # open project template and render with project data
    with open(
        Path(adoc_dir).joinpath(ADOC_BASE_FILE),
        "r",
        newline="",
        encoding="utf-8-sig",
        errors="replace",
    ) as projectTemplateFile:
        # read file content
        projectTemplate = projectTemplateFile.read()

        # check if all project data is in the template
        listOfProjectData = []
        listOfUnusedData = []
        data2list(projectData, listOfProjectData, "data")
        for entry in listOfProjectData:
            if entry not in projectTemplate:
                listOfUnusedData.append(entry)

        # list all unused data from the project data json
        if listOfUnusedData:
            i = 1
            for entry in reversed(listOfUnusedData):
                logger.error(
                    str(i)
                    + ". {{ "
                    + entry
                    + " }} DOES NOT EXISTS IN TEMPLATE ("
                    + str(Path(adoc_dir).joinpath(ADOC_BASE_FILE))
                    + ")"
                )
                i = i + 1

        # check if all data from the template are defined in the project data
        listOfTemplateData = []
        # listOfWrongTemplateData = []
        listOfTemplateData = re.findall(r"\bdata\..+\w", projectTemplate)
        for entry in listOfTemplateData:
            if entry not in listOfProjectData:
                logger.warning(
                    entry
                    + " IS WRONG IN THE TEMPLATE OR DOES NOT EXIST IN THE PROJECT DATA ("
                    + BUILD_INFO_FILE
                    + " or "
                    + RELEASE_INFO_FILE
                    + ")"
                )
                pass

        template = Environment(
            loader=FileSystemLoader(str(Path(adoc_input_dir)))
        ).from_string(projectTemplate)

        projectTemplateRendered = template.render(data=projectData)

    # write the generated .adoc file
    with open(
        Path(adoc_dir).joinpath(ADOC_GEN_FILE),
        "w",
        newline="",
        encoding="utf-8-sig",
        errors="replace",
    ) as projectGeneratedFile:
        projectGeneratedFile.write(projectTemplateRendered)
        logger.info("Jinja Template updated")
