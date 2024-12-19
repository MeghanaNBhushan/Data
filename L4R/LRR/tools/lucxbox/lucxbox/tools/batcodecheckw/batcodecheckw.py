#!/usr/bin/python
"""Wrapper Script for running BatCodeCheck"""
import argparse
import os
import sys
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from pathlib import Path

from lucxbox.lib import lucxlog, lucxargs

LOGGER = lucxlog.get_logger()


class BatCodeCheck:
    file_path = os.path.dirname(__file__)

    def __init__(self, tool_path):
        self.reports = {}
        self.src_id = 0
        self.src_paths = {}
        self.tool_path = tool_path

    def valid_source_exists(self):
        return bool(self.src_paths)

    def add_source(self, source_path):
        if Path(source_path).exists():
            self.src_paths[self.src_id] = source_path
            self.src_id += 1
        else:
            LOGGER.warning("Following source does not exist: %s", source_path)

    def add_list_file(self, list_path):
        if Path(list_path).exists():
            with open(list_path, 'r') as list_file:
                lines = (k.rstrip() for k in list_file if k.strip())
                for path in lines:
                    self.add_source(path)
        else:
            LOGGER.warning("Following list file does not exist: %s", list_path)

    def analyze(self, output_dir):
        # Create output directory
        out_file = Path(output_dir)
        if out_file.suffix:
            out_file = Path.joinpath(out_file.parent, out_file.stem)
        out_file.mkdir(parents=True, exist_ok=True)

        for src_path in self.src_paths.values():
            # Determine output file name
            src_stem = Path(src_path).stem
            out_path = Path.joinpath(out_file, "{}.html".format(src_stem))
            # Avoid overwriting files. If it can't be helped, issue a warning
            if Path(out_path).exists():
                for index in range(100):
                    out_path = Path.joinpath(out_file, "{}_{}.html".format(src_stem, index))
                    if not Path(out_path).exists():
                        break
                    if index == 99:
                        LOGGER.warning("Following file was overwritten: %s", out_path)
            # Execute BatCodeCheck
            command = "{} {} /H:{}".format(self.tool_path, src_path, out_path)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            out, err = process.communicate()
            returncode = process.returncode

            if returncode == 1:
                LOGGER.warning("BatCodeCheck was run with command %s", command)
                LOGGER.warning("BatCodeCheck returned code %s", returncode)
                LOGGER.warning("BatCodeCheck returned error %s", err)
                LOGGER.warning("BatCodeCheck returned output %s", out)
            else:
                LOGGER.info("Analyzed file: %s", src_path)


def check_installation(install_path, tcc_local_config, tcc_server_config, tcc_var):
    if all(element is None for element in [install_path, tcc_local_config, tcc_server_config, tcc_var]):
        return "BatCodeCheck.exe"
    if install_path:
        LOGGER.debug("Using local installation")
        if not Path(install_path).is_file():
            LOGGER.error("Executable cannot be found")
            sys.exit("Executable cannot be found")
        return install_path
    else:
        if not tcc_var:
            tcc_var = 'TCC_BATCODECHECK'
        LOGGER.debug("Using TCC installation")
        if tcc_server_config:
            LOGGER.debug("Using TCC server config")
            config = "-c {}".format(tcc_server_config)
        else:
            LOGGER.debug("Using local TCC config")
            if not Path(tcc_local_config).exists():
                LOGGER.error("Local TCC config cannot be found.")
                sys.exit("Local TCC config not found.")
            config = "-l {}".format(tcc_local_config)
        path = "{} {} {}  -- %{}%/BatCodeCheck.exe".format(sys.executable,
                                                           os.path.join(os.path.dirname(__file__), '..', 'tccw', 'tccw.py'),
                                                           config,
                                                           tcc_var)
        return path


def parse_args(arguments):
    parser = argparse.ArgumentParser(prog='batcodecheckw.py', description='Wrapper script for runnning BatCodeCheck')
    parser = lucxargs.add_version(parser)
    parser = lucxargs.add_log_level(parser)
    parser.add_argument('-o', '--output', type=str, metavar='DIR',
                        required=True, dest='output_dir', help='directory for reports')

    src_group = parser.add_mutually_exclusive_group(required=True)
    src_group.add_argument('-s', '--sources', type=str, nargs='+',
                           metavar='FILE', dest='sources',
                           help='source file(s) for analysis')
    src_group.add_argument('-l', '--list', type=str,
                           metavar='FILE', dest='list_files', nargs='+',
                           help='text file(s) with one file path for analysis per line')

    tool_group = parser.add_mutually_exclusive_group(required=False)
    tool_group.add_argument('-tc', '--tcc-server-config', type=str,
                            help="Pass here name of TCC Server config -> e.g. TCC_NRCS2_Windows_DevLatest")
    tool_group.add_argument('-tl', '--tcc-local-config', type=str,
                            help="Pass here name of local TCC config")
    tool_group.add_argument('-i', '--install-path', type=str,
                            help='Pass here the path to the BatCodeCheck executable')
    tool_group.add_argument('-tv', '--tcc-var', type=str,
                            help="Pass here the TCC variable for BatCodeCheck, e.g. 'TCC_BATCODECHECK'")
    return parser.parse_args(arguments)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parse_args(argv[1:])
    LOGGER.setLevel(args.log_level)
    tool_path = check_installation(args.install_path, args.tcc_local_config, args.tcc_server_config, args.tcc_var)
    LOGGER.debug("Tool path is %s", tool_path)
    bcc_obj = BatCodeCheck(tool_path)
    if args.sources:
        for path in args.sources:
            bcc_obj.add_source(path)
    if args.list_files:
        for path in args.list_files:
            bcc_obj.add_list_file(path)
    if bcc_obj.valid_source_exists():
        bcc_obj.analyze(args.output_dir)
    else:
        LOGGER.warning("There are no existing source files. Batch file linting with BatCodeCheck is skipped.")


if __name__ == '__main__':
    main()
