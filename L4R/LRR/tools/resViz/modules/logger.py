# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  @copyright (c) 2021 by Robert Bosch GmbH. All rights reserved.
#
#  The reproduction, distribution and utilization of this file as
#  well as the communication of its contents to others without express
#  authorization is prohibited. Offenders will be held liable for the
#  payment of damages. All rights reserved in the event of the grant
#  of a patent, utility model or design.
# =============================================================================
#  P R O J E C T   I N F O R M A T I O N
# -----------------------------------------------------------------------------
#  Projectname            : resViz (Mapfile based memory resource analysis)
# =============================================================================
#  F I L E   I N F O R M A T I O N
# -----------------------------------------------------------------------------
#  @brief : Provides logging for resViz. It will write all console output to a
#           logfile in C:\TSDE_Localarea\Logfiles
# =============================================================================

# pylint: disable=bare-except

import os
import sys
import platform
from datetime import datetime


class Logger(object):
    """directs stdout to console and logfile"""

    def __init__(self):
        self.console = sys.stdout
        self.date = datetime.now()
        logdir = os.path.join(
            "c:\\TSDE_Localarea",
            "Logfiles",
            os.environ["COMPUTERNAME"],
            self.date.strftime("%Y-%m-%d"),
            "RESVIZ",
        )
        try:
            if not os.path.isdir(logdir):
                os.makedirs(logdir)
            logfilename = "{}_{}.log".format("RESVIZ", self.date.strftime("%Y-%m-%d_%H-%M-%S"))
            logfilepath = os.path.join(logdir, logfilename)
            self.logfile = open(logfilepath, "w")
            header = self._createheader()
            self.logfile.write(header)
        except:
            print("Warning: Logfile could not be generated in " + str(logdir))
            self.logfile = open(os.devnull, "w")

    def __del__(self):
        self.logfile.close()

    def _createheader(self):
        header = "[CS_LogFileInfo]\n"
        header += "Tool Name         = resViz\n"
        header += "Version           = " + self._readversionfile() + "\n"
        header += "Runstring         = " + " ".join(sys.argv) + "\n"
        try:
            header += "User              = " + os.environ["USERNAME"] + "\n"
        except:
            header += "User              = unkown\n"
        try:
            header += "Domain            = " + os.environ["USERDOMAIN"] + "\n"
        except:
            header += "Domain            = unkown\n"
        try:
            header += "Machine           = " + os.environ["COMPUTERNAME"] + "\n"
        except:
            header += "Machine           = unkown\n"
        try:
            header += "OperatingSystem   = " + platform.platform() + "\n"
        except:
            header += "OperatingSystem   = unkown\n"
        try:
            header += "Date              = " + self.date.strftime("%Y-%m-%d") + "\n"
        except:
            header += "Date              = unkown\n"
        try:
            header += "Time              = " + self.date.strftime("%H:%M:%S") + "\n"
        except:
            header += "Time              = unkown\n"
        try:
            header += "NumberProcessors  = " + str(os.cpu_count()) + "\n"
        except:
            header += "NumberProcessors  = unkown\n"
        try:
            header += "PythonVersion     = " + platform.python_version()
        except:
            header += "PythonVersion     = unkown"
        header += "\n\n[CS_LogFileData]\n\n"
        return header

    def _readversionfile(self):
        try:
            with open(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "VERSION")
            ) as versionfile:
                return versionfile.read()
        except:
            return "unkown"

    def write(self, message):
        """writes message to console and logfile"""
        self.console.write(message)
        self.logfile.write(message)

    def flush(self):
        """needed for Python 3 compability"""
