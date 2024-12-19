#!/usr/bin/env python3
"""
convert input data to adoc format text file snippets

# Author:  Jochen Held (XC-DA/EDB7)
"""

from pathlib import Path
import json
import logging
from .cv_compilerWarnings import generate_compiler_warnings_adoc
from .cv_coverityWarnings import generate_coverity_warnings_adoc
from .cv_qacWarnings import generate_qac_warnings_adoc
from .cv_jiraTickets import generate_jira_tickets_adoc
from .cv_resourceConsumption import generate_resource_consumption_adoc
from .cv_problemStatistics import generate_problem_stats_adoc

logger = logging.getLogger(__name__)

CFG_FILE_NAME = "build_dir_cfg.json"


def convert_to_adoc_input(cfg_dir, export_dir, build_dir, adoc_input_dir):

    # load the config file with path information to input data such as coverity, compiler, qac outputs
    build_dir_cfg = []
    try:
        with open(
            Path(cfg_dir).joinpath(CFG_FILE_NAME),
            "r",
            newline="",
            encoding="utf-8-sig",
        ) as json_file:
            build_dir_cfg = json.load(json_file)
    except EnvironmentError:
        logger.error("Importing " + CFG_FILE_NAME + "failed")
        sys.exit(10)

    # Handle data which was exported from other tools
    generate_jira_tickets_adoc(export_dir, adoc_input_dir)

    generate_problem_stats_adoc(export_dir, adoc_input_dir)

    # Handle data which is part of release/build folder

    data_dir = (
        Path(build_dir).absolute().joinpath(build_dir_cfg["compiler_warnings_dir"])
    )
    generate_compiler_warnings_adoc(data_dir, adoc_input_dir)

    data_dir = (
        Path(build_dir).absolute().joinpath(build_dir_cfg["coverity_warnings_dir"])
    )
    generate_coverity_warnings_adoc(data_dir, adoc_input_dir)

    data_dir = Path(build_dir).absolute().joinpath(build_dir_cfg["qac_warnings_dir"])
    generate_qac_warnings_adoc(data_dir, adoc_input_dir)

    data_dir = Path(build_dir).absolute().joinpath(build_dir_cfg["resource_data_dir"])
    generate_resource_consumption_adoc(data_dir, adoc_input_dir)
