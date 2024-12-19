#!/usr/bin/env python3
"""
Get JIRA Ticket data via REST api

# Author: Jochen Held (XC-DA/EDB7)
"""

import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def export_jira(fixVersion, cfgpath, outputpath):
    """
    Exports jira issues for a specific fixVersion and stores the exported json files
    in outputpath.

    Calls a powershell script
    TODO: This should be replaced by a python script in future

    Args:
        fixVersion: JIRA FixVersion
        cfgpath: path to project config file
        outputpath: Absolute path to storage location for json files

    Return:

    """

    logger.info("Powershell JIRA Export started")

    ps_export_path = Path(outputpath).joinpath("jira_export")
    ps_cfg_path = Path(cfgpath).joinpath("./jira_export_cfg.json")
    ps_script_path = Path(__file__).parent.absolute().joinpath("./jiraExport.ps1")

    # Define command line parameters for powershell script
    cmd = [
        "PowerShell",
        str(ps_script_path),
        "-CfgFilePath",
        str(ps_cfg_path),
        "-JQLFixVersion",
        fixVersion,
        "-OutputPath",
        str(ps_export_path),
    ]

    logger.debug("Powershell parameters used: " + "\n".join(cmd))

    ec = subprocess.call(cmd)
    logger.info("Powershell returned: {0:d}".format(ec))


def main():
    print("Used for testing")


if __name__ == "__main__":
    main()
