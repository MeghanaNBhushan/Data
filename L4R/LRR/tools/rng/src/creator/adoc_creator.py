#!/usr/bin/env python3
"""
Generate PDF / HTML with asciidoctor

# Author: Jochen Held (XC-DA/EDB7)
"""

import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

RELEASE_NOTES_DIR = "."
PS_ASCIIDOC_CMDLET = "asciidoc2htmlpdf.ps1"

# TODO: This configuration needs to go into global config file or needs to be read from a file here
ADOC_CFG_FILE = "asciidoc_cfg.json"
ADOC_GEN_FILE = "releasenote_gen.adoc"


def create_adoc_pdfhtml(adoc_dir, output_dir, release_name):
    """
    Generates an html and pdf based on the available configuration of the ascidoc.json

    Calls a powershell script
    TODO: This should be replaced by a python script in future

    Args:
        adoc_dir: storage location of adoc configuration file and adoc file
        output_dir: Absolute path to storage location for json files
        release_name: Name of the release used for naming of output folders

    Return:

    """

    logger.info("Powershell asciidoc HTML/PDF generation started")

    ps_script_path = Path(__file__).parent.absolute().joinpath(PS_ASCIIDOC_CMDLET)
    output_dir = Path(output_dir).absolute().joinpath(RELEASE_NOTES_DIR)
    adoc_cfg_file = Path(adoc_dir).absolute().joinpath(ADOC_CFG_FILE)
    adoc_gen_file = Path(adoc_dir).absolute().joinpath(ADOC_GEN_FILE)

    # Define command line parameters for powershell script
    cmd = [
        "PowerShell",
        str(ps_script_path),
        "-inputfile",
        str(adoc_gen_file),
        "-output_dir",
        str(output_dir),
        "-CfgFilePath",
        str(adoc_cfg_file),
        "-ReleaseVersion",
        release_name,
    ]

    logger.info("Powershell parameters used: " + "\n".join(cmd))

    ec = subprocess.call(cmd)
    logger.info("Powershell returned: {0:d}".format(ec))
