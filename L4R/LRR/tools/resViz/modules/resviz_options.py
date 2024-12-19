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
#  @brief : command line parser for resViz application
# =============================================================================

import os
import sys
import argparse


class ResVizOptions:
    """command line parser for resViz application"""

    _demangle_plugin = "demangle_ghs.so"

    def __init__(self):
        self._parser = argparse.ArgumentParser(
            description="Create Resource Resource (RAM,ROM) consumption report (xlsx format)",
            fromfile_prefix_chars="@",
            prog=os.path.splitext(os.path.basename(sys.argv[0]))[0],
        )
        self._parser.add_argument(
            "--projectconfig",
            action="store",
            type=str,
            default="",
            required=True,
            help="project configuration file - configure project budget, domain budget and symbol mapping",
        )
        self._parser.add_argument(
            "--memconfig",
            action="store",
            type=str,
            default="",
            required=True,
            help="project physical memory size configuration file",
        )
        self._parser.add_argument(
            "--mapfile",
            action="store",
            type=str,
            default=[],
            nargs="+",
            required=True,
            help="list of mapfiles",
        )
        self._parser.add_argument(
            "--ldfile",
            action="store",
            type=str,
            default=[],
            nargs="+",
            help="list of linker scripts - either one used for all map files or one for each of the map files in respective order",
        )
        self._parser.add_argument(
            "--compilerpath",
            action="store",
            type=str,
            required=False,
            default=os.path.join(
                os.path.dirname(sys.argv[0]),
                "Demangler",
                "lib",
                "win" if sys.platform.startswith("win") else "linux",
            ),
            help="directory containing demangler plugin",
        )
        self._parser.add_argument(
            "--budgetviolationreport",
            action="store",
            type=str,
            default="",
            help="budget violation report file - enable creation of budget violation report and write to given file",
        )
        self._parser.add_argument(
            "--logfile",
            action="store",
            type=str,
            default=None,
            help="logfile - enable logging write to given log",
        )
        self._parser.add_argument(
            "--output",
            action="store",
            type=str,
            default=".",
            help="output directory to create xlsx file - filename defaults to the basename of first mapfile, or output file the given name has .xlsx file extension",
        )
        self._parser.add_argument(
            "--debug",
            action="store_true",
            default=False,
            help="enable debugging mode",
        )
        self._options = vars(self._parser.parse_args())
        self._outputfile = ""

    @classmethod
    def _check_input_file(cls, filetype, filename):
        """Checks if input file exists and can be accessed"""
        result = True
        if not os.path.isfile(filename):
            print("Fatal Error: {0} file '{1}' does not exist".format(filetype, filename))
            result = False
        elif not os.access(filename, os.R_OK):
            print("Fatal Error: {0} file '{1}' is not readable".format(filetype, filename))
            result = False
        return result

    def _calc_output_file(self):
        """Generates output file path"""
        output_arg = self._options["output"]
        fext = os.path.splitext(output_arg)[1]
        if fext:
            if fext == ".xlsx":
                self._outputfile = output_arg
            else:
                print(
                    "Fatal Error: unexpected file extension '{0}' in output option '{1}'".format(
                        fext, output_arg
                    )
                )
        else:
            basename = os.path.basename(self._options["mapfile"][0])
            basename = os.path.splitext(basename)[0]
            if basename:
                self._outputfile = os.path.join(output_arg, "ram_rom_report_" + basename + ".xlsx")
            else:
                print("Fatal Error: malformed mapfile name {0}".format(self._options["mapfile"][0]))
        return self._outputfile != ""

    def validate(self):
        """Checks if given options are valid"""
        result = True
        if not self._check_input_file("project config", self._options["projectconfig"]):
            result = False
        if not self._check_input_file("memory config", self._options["memconfig"]):
            result = False
        for mapfile in self._options["mapfile"]:
            if not self._check_input_file("map", mapfile):
                result = False
        for ldfile in self._options["ldfile"]:
            if ldfile == "":
                continue
            if not self._check_input_file("linker", ldfile):
                result = False
        num_ldfile = len(self._options["ldfile"])
        if num_ldfile > 1:
            if num_ldfile < len(self._options["mapfile"]):
                print(
                    "Fatal Error: when configuring more than one ldfile for each of the map files one ldfile has to be given"
                )
                result = False
            elif num_ldfile > len(self._options["mapfile"]):
                print(
                    "Warning there are more ldfiles given than mapfiles - ignoring addtional ldfiles ..."
                )
        if not self._calc_output_file():
            result = False
        if self._options["compilerpath"]:
            plugin = os.path.join(self._options["compilerpath"], self._demangle_plugin)
            if not self._check_input_file("demanglerplugin", plugin):
                print(
                    "Fatal Error: demangler plugin {0} not found in compilerpath {1}".format(
                        self._demangle_plugin, self._options["compilerpath"]
                    )
                )
                result = False
        return result

    def p_debug_mode(self):
        """returns debug mode"""
        return self._options["debug"]

    def get_mapfile_data(self, count):
        """returns mapfile and linker script"""
        mapfile = None
        ldfile = None
        if self._p_mapfile_available(count):
            mapfile = self._options["mapfile"][count]
            if self._options["ldfile"]:
                ldfile = self._options["ldfile"][0]
                if len(self._options["ldfile"]) > 1:
                    ldfile = self._options["ldfile"][count]
                if ldfile == "":
                    ldfile = None
        return mapfile, ldfile

    def get_mapfile(self):
        """mapfile getter"""
        return self._options["mapfile"]

    def get_ldfile(self):
        """linker script getter"""
        return self._options["ldfile"]

    def get_project_config(self):
        """project config getter"""
        return self._options["projectconfig"]

    def get_memory_config(self):
        """memory config getter"""
        return self._options["memconfig"]

    def get_budgetviolationreport(self):
        """budget violation report getter"""
        return self._options["budgetviolationreport"]

    def get_logfile(self):
        """logfile getter"""
        return self._options["logfile"]

    def get_output_file(self):
        """output file getter"""
        return self._outputfile

    def _p_mapfile_available(self, n_read_mapfiles):
        """checks if mapfile is available"""
        return len(self._options["mapfile"]) > n_read_mapfiles

    def get_number_of_mapfiles(self):
        """returns number of mapfiles"""
        return len(self._options["mapfile"])

    def get_compiler_path(self):
        """returns demangler plugin dir"""
        return self._options["compilerpath"]

    def dump(self):
        """writes options to console"""
        for option in self._options:
            print("{0} --> {1}".format(option, self._options[option]))
        print("{0} --> {1}".format("outputfile", self._outputfile))


def get_resviz_options():
    """validates and returns all options"""
    options = ResVizOptions()
    if options.validate():
        return options
    if options.p_debug_mode():
        options.dump()
    return None


def testmain():
    """main function for testing command line parser"""
    options = get_resviz_options()
    if options is not None:
        options.dump()
    for num in range(3):
        map_file, ld_file = options.get_mapfile_data(num)
        print("{0} mapfile: {1}  ldfile: {2}".format(num, map_file, ld_file))


if __name__ == "__main__":
    testmain()
