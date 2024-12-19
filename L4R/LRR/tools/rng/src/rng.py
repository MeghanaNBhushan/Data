#!/usr/bin/env python3
"""
Release note generator (RnG) main file. Handles command line inputs and calls subfunctions for different stages

# Author: Jochen Held (XC-DA/EDB7)
"""


import argparse
import json
import os

import logging
from logging.config import dictConfig

from pathlib import Path

from exporter.jira_export.jira import export_jira
from converter.converter import convert_to_adoc_input
from compiler.compiler_adoc import compile_adoc
from creator.adoc_creator import create_adoc_pdfhtml
from signer.workon import sign_release_note
from signer.workon import get_release_note_approval_status

# Debugging switches
RUN_EXPORTER = True
RUN_CONVERTER = True
RUN_COMPILER = True


def setup_logging(
    default_path=Path(__file__).parent.absolute().joinpath("logging_cfg.json"),
    default_level=logging.INFO,
    env_key="LOG_CFG",
):
    """
    Loads logging configuration from config file

    """

    os.chdir(Path(__file__).parent.absolute())

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        print("WARNING: Logging Config not found")
        logging.basicConfig(level=default_level)


def parse_arguments():
    """
    Defines the scripts command line input argument and options
    """

    my_parser = argparse.ArgumentParser(
        prog="rng",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # The Line indent in the following line is intended to get formating of help correctly!!!
        description=""" 
Release Note Generator. 

The generator expects a config file of type rng_cgf.json.
The parameters in the rng_cfg.json can be overwritten by the optional
arguments, e.g. for testing purposes
""",
    )
    my_parser.add_argument(
        "stage",
        choices=["export", "convert", "compile", "create", "sign", "publish"],
        help="Selects the stage to be executed",
    )

    my_parser.add_argument(
        "-c",
        "--configfile",
        help="Path to json config file of format rng_cfg.json",
    )

    my_parser.add_argument(
        "-o",
        "--outputdir",
        help="Link to output directory. Overwrites values in configfile!!!",
    )

    my_parser.add_argument(
        "-f",
        "--fixversion",
        help="JIRA Fix Version to be used for Features/Problems. Overwrites values in configfile!!!",
    )

    my_parser.add_argument(
        "-r",
        "--release",
        help="Release name used for internal reference, storage locations. Overwrites values in configfile!!!",
    )

    # Execute parse_args()
    args = my_parser.parse_args()

    return args


def rng_export(cfg):
    """
    export data from tools

    Args:
        cfg: global config values

    """
    if RUN_EXPORTER:
        # Export jira issues for the given fix version
        export_jira(
            cfg["jira_fixversion"],
            Path(cfg["project_path"]).joinpath(cfg["cfg_dir"]),
            Path(cfg["project_path"]).joinpath(cfg["export_dir"]),
        )


def rng_convert(cfg):
    """
    convert data into adoc input formats

    Args:
        cfg: global config values

    """
    if RUN_CONVERTER:
        # TODO: fetch generated data.json file from build folder and put into
        convert_to_adoc_input(
            Path(cfg["project_path"]).joinpath(cfg["cfg_dir"]),
            Path(cfg["project_path"]).joinpath(cfg["export_dir"]),
            Path(cfg["project_path"]).joinpath(cfg["build_dir"]),
            Path(cfg["project_path"]).joinpath(cfg["adoc_input_dir"]),
        )


def rng_compile(cfg):
    """
    create release note markup language document bases on inputs

    Args:
        cfg: global config values

    """
    if RUN_COMPILER:
        # Generate the draft version of th adoc file
        compile_adoc(
            Path(cfg["project_path"]).joinpath(cfg["build_dir"]),
            Path(cfg["project_path"]).joinpath(cfg["adoc_input_dir"]),
            Path(cfg["project_path"]).joinpath(cfg["adoc_dir"]),
        )


def rng_create(cfg):
    """
    Generates the final version of the release note e.g in form of an pdf and html

    Args:
        cfg: global config values

    """

    create_adoc_pdfhtml(
        Path(cfg["project_path"]).joinpath(cfg["adoc_dir"]),
        Path(cfg["project_path"]).joinpath(cfg["output_dir"]),
        cfg["release_name"],
    )


def rng_sign(cfg):
    """
    Start signature process (e.g. via WorkOn)

    Args:
        cfg: global config values

    """

    workon_key = sign_release_note(
        Path(cfg["project_path"]).joinpath(cfg["cfg_dir"]),
        Path(cfg["project_path"]).joinpath(cfg["output_dir"]),
        Path(cfg["project_path"]).joinpath(cfg["build_dir"]),
    )
    logger.info("Workon successfully created - " + str(workon_key))

    approval_status = get_release_note_approval_status(workon_key)
    logger.info("WorkOnStatus - " + str(workon_key) + ": " + str(approval_status))


def rng_publish(cfg):
    """
    Publishes a signed release note Locations TBD

    Args:
        cfg: global config values
    """

    # TODO: Publishing needs to be defined
    logger.info("Publishing stage not available yet")


def load_cfg(args):
    """
    Read the global json configuration file and checks if any optional arguments
    have been passed and shall overwrite the values in the config file

    Args:
        args: arguments and options passed from command line

    Return:
        cfg: dict of configuration values
    """

    project_path = Path(args.configfile).absolute()

    logger.debug("Config file used: " + str(project_path))

    cfg = []
    with open(project_path, "r", newline="", encoding="utf-8-sig") as json_file:
        cfg = json.load(json_file)

    # Check if option arguments have been passed through command line and replace
    # values from json config file
    if args.fixversion is not None:
        cfg["jira_fixversion"] = args.fixversion
    if args.outputdir is not None:
        cfg["output_dir"] = Path(args.outputdir)
    if args.release is not None:
        cfg["release_name"] = args.release

    cfg["project_path"] = str(project_path.parents[0])

    logger.debug(
        "Used config: \n" + "\n".join("\t".join((key, cfg[key])) for key in cfg)
    )

    return cfg


def main():

    args = parse_arguments()
    cfg = load_cfg(args)

    logger.info("-------  Release Note Generation Started -------")
    logger.info("Stage: " + args.stage + " started")

    if args.stage == "export":
        rng_export(cfg)
    elif args.stage == "convert":
        rng_convert(cfg)
    elif args.stage == "compile":
        rng_compile(cfg)
    elif args.stage == "create":
        rng_create(cfg)
    elif args.stage == "sign":
        rng_sign(cfg)
    elif args.stage == "publish":
        rng_publish(cfg)

    logger.info("-------  Release Note Generation Finished -------")


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    main()
