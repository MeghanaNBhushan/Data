#!/usr/bin/python
"""Script for running CppCheck on Windows and Linux"""
import argparse
import os
import sys
import configparser
import io

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxutils, lucxlog, lucxargs
from lucxbox.tools.cppcheckw.htmlreport import convert_to_html

LOGGER = lucxlog.get_logger()


class CppCheck:
    """Wrapper for CppCheck"""

    script_dir = os.path.dirname(__file__)

    def __init__(self, args):
        self.args = args
        self.path = self.check_installation()
        self.config = self.read_config()

    def check_installation(self):
        """Checks if CppCheck is installed"""
        args = [self.args.install_path, self.args.tcc_server_config, self.args.tcc_local_config, self.args.tcc_var]
        if all(element is None for element in args):
            return "cppcheck.exe"
        if self.args.install_path:
            LOGGER.debug("Using local installation for CppCheck")
            if not os.path.exists(self.args.install_path):
                LOGGER.error("CppCheck executable cannot be found.")
                sys.exit("Cppcheck is not installed.")
            return self.args.install_path
        else:
            if not self.args.tcc_var:
                self.args.tcc_var = 'TCC_CPPCHECK'
            LOGGER.debug("Using TCC installation for CppCheck")
            if self.args.tcc_server_config:
                LOGGER.debug("Using TCC server config")
                config = "-c {}".format(self.args.tcc_server_config)
            else:
                LOGGER.debug("Using local TCC config")
                if not os.path.exists(self.args.tcc_local_config):
                    LOGGER.error("Local TCC config cannot be found.")
                    sys.exit("Local TCC config not found.")
                config = "-l {}".format(self.args.tcc_local_config)
            path = "python {} {}  -- %{}%/cppcheck.exe".format(os.path.join(self.script_dir, '..', 'tccw', 'tccw.py'),
                                                               config,
                                                               self.args.tcc_var)
            return path

    def analyze(self):
        """Runs the cppcheck.exe and stores outcomes in the requested format"""
        self.check_sources()
        full_command = self.cppcheck_command()
        LOGGER.debug('Running Cppcheck with command: %s', full_command)
        print("\nRunning Cppcheck with command: {}".format(full_command))
        out, err, return_code = lucxutils.execute(full_command)
        print("\nCppcheck finished with return code {}".format(return_code))
        print("\nSkript returned on stdout:\n{}".format(out))
        LOGGER.debug('Output: %s', out)
        if return_code == 0:
            if self.args.format == "html":
                report_dir = self.args.output_file
                if "." in report_dir:
                    report_dir, _, _ = report_dir.partition(".")
                convert_to_html(err, report_dir)
            else:
                with io.open(self.args.output_file, 'w') as out_file:
                    out_file.write(err)
        else:
            LOGGER.error('Command returned error: %s', err)
            sys.exit(return_code)

    def check_sources(self):
        """Checks that sources are supplied and all sources exist"""
        existing_files_flag = False
        if self.args.sources is not None:
            # Check if paths in args.sources exist
            for path in self.args.sources:
                if not os.path.exists(path):
                    LOGGER.warning("Following source does not exist: %s", path)
                else:
                    existing_files_flag = True
        if self.args.list_files:
            for list_path in self.args.list_files:
                # Check if paths of list files exist
                if not os.path.exists(list_path):
                    LOGGER.warning("List file does not exist: %s", list_path)
                else:
                    # Check if paths in list_files exist
                    with io.open(list_path, 'r') as list_file:
                        lines = (k for k in list_file if k.strip())
                        for path in lines:
                            if not os.path.exists(path.rstrip()):
                                LOGGER.warning("Following source in list file does not exist: %s", path)
                            else:
                                existing_files_flag = True
        # Check if at least one source file exist
        if not existing_files_flag:
            LOGGER.warning("There are no existing source files. Linting with CppCheck is skipped.")
            sys.exit(0)

    def read_config(self):
        """Parses config file and return values for requested format as dictionary"""
        if not os.path.exists(self.args.config_file):
            LOGGER.error("Can't find config file: %s", self.args.config_file)
            sys.exit(1)
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(self.args.config_file)
        return config

    def cppcheck_command(self):
        """Builds the command for running the cppcheck.exe"""
        command = [self.path]
        if self.args.sources:
            for path in self.args.sources:
                command.append("\"{}\"".format(path))
        if self.args.list_files:
            for list_path in self.args.list_files:
                command.append("--file-list=\"{}\"".format(list_path))
        if self.args.format in ['xml', 'html']:
            command.append('--xml')
        for (key, value) in self.config.items(self.args.format):
            if value:
                for arg in filter(None, value.splitlines()):
                    command.append("{}={}".format(key, arg))
            else:
                command.append(key)
        return " ".join(command)


def parse_args():
    """Parses arguments and stores them as attributes"""
    parser = argparse.ArgumentParser(prog='cppcheckw.py', description='Script for running Cppcheck')
    parser = lucxargs.add_version(parser)
    parser.add_argument('-s', '--sources', type=str, nargs='+',
                        metavar='FILE|DIR', dest='sources',
                        help='source file(s) or directories for analyze')
    parser.add_argument('-l', '--lists', type=str,
                        metavar='FILE', dest='list_files', nargs='+',
                        help='text file(s) with one file path for analysis per line')
    parser.add_argument('-o', '--output', type=str, metavar='FILE',
                        required=True, dest='output_file', help='file for report')
    parser.add_argument('-c', '--config', type=str, metavar='FILE',
                        dest='config_file', default=os.path.join(os.path.dirname(__file__), "standard_config.ini"),
                        help='file with parameters for Cppcheck')
    parser.add_argument('-f', '--format', type=str, metavar='txt|xml|html',
                        choices=['txt', 'xml', 'html'], default='xml', dest='format',
                        help='report output format')

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-tc', '--tcc-server-config', type=str,
                       help="Pass here name of TCC Server config -> e.g. TCC_NRCS2_Windows_DevLatest")
    group.add_argument('-tl', '--tcc-local-config', type=str,
                       help="Pass here name of local TCC config")
    group.add_argument('-i', '--install-path', type=str,
                       help='Path to the directory that contains the CppCheck executable')

    parser.add_argument('-tv', '--tcc-var', type=str,
                        help="Pass here the TCC variable for CppCheck, e.g. 'TCC_CPPCHECK'")

    return parser.parse_args()


def main():
    args = parse_args()
    cc_obj = CppCheck(args)
    cc_obj.analyze()


if __name__ == '__main__':
    main()
