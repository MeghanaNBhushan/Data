# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: swq.py
# ----------------------------------------------------------------------------
"""Main SWQ interfaces"""
import argparse
from pathlib import Path as pathlib_Path

from sys import argv, exit as sys_exit
from os import path
from datetime import datetime

from swq.version import VERSION
from swq.common.logger import LOGGER
from swq.common.command.command_decorator import ensure_utf8_stdout_call_once
from swq.common.return_codes import RC_INVALID_CMD_PARAMETERS
from swq.common.constants import LOGS_PREFIX, filter_sensitive_keys_from_dict
from swq.common.filesystem.filesystem_utils import create_dirs_if_necessary
from swq.common.params.params import SCAParameters
from swq.qac.config_qac import create_qac_config
from swq.qac.args_qac import parse_args_qac
from swq.qac.qac import qac_report, qac_qavupload, qac_gui, \
    qac_s101gen
from swq.qac.create import qac_create
from swq.qac.qac_analyze import qac_analyze
from swq.qac.fix_cl_json import fix_cl_json_entrypoint
from swq.qac.filter_qaview import filter_qaview_entrypoint
from swq.qac.export_analysis import qac_export_analysis
from swq.qac.exporters.state_exporter import qac_state, \
    qac_export_state
from swq.qac.qac_commands import create_baseline
from swq.find_includes.args_find_includes import parse_args_find_includes
from swq.find_includes.find_includes import find_includes_entrypoint
from swq.find_includes.config_find_includes import create_find_includes_config
from swq.coverity.args_coverity import parse_args_coverity
from swq.coverity.coverity import coverity_create, coverity_run_desktop, \
    coverity_show_build_log_metrics, coverity_analyze, \
    coverity_export, coverity_preview_report, coverity_upload, \
    coverity_webapi_export
from swq.coverity.export_analysis import coverity_export_analysis
from swq.coverity.filter_preview_report import coverity_filter_report
from swq.coverity.config_coverity import create_coverity_config
from swq.map_teams.args_map_teams import parse_args_map_teams
from swq.map_teams.map_teams import map_teams
from swq.map_teams.config_map_teams import create_map_teams_config
from swq.unify_reports.args_unify_reports import parse_args_unify_reports
from swq.unify_reports.unify_reports import unify_reports
from swq.unify_reports.config_unify_reports import create_unify_reports_config
from swq.compiler_warnings.args_compiler_warnings \
    import parse_args_compiler_warnings
from swq.compiler_warnings.compiler_warnings import compiler_warnings
from swq.compiler_warnings.config_compiler_warnings \
    import create_compiler_warnings_config

_MODULE_NAME = 'SCA_TOOLS'
PYTHON_MINIMUM_VERSION = (3, 7)


def init_logger_for_helper_command(config, command):
    """ Initialize logger for helper command """
    log_filepath = create_dirs_if_necessary(
        path.join(
            config.helper_logs_path, '{}_{}_{}.log'.format(
                LOGS_PREFIX,
                command,
                datetime.today().strftime('%Y%m%d_%H%M%S.%f')[:-3])))
    LOGGER.initialize_file_once(log_filepath)
    LOGGER.info("sca_tools_version: {}".format(VERSION))
    LOGGER.info("swq filepath: {}".format(
        pathlib_Path(__file__).absolute()))
    LOGGER.info("helper_command: {}".format(command))
    LOGGER.info('Logging into file %s', log_filepath)
    LOGGER.info("commandline_config: {}".format(config.commandline_config))
    LOGGER.info("env_config: {}".format(
        filter_sensitive_keys_from_dict(config.env_config)))
    LOGGER.info("general_config: {}".format(
        filter_sensitive_keys_from_dict(config.general_config)))
    LOGGER.info("target_config: {}".format(
        filter_sensitive_keys_from_dict(config.target_config)))
    LOGGER.debug("merged_config: {}".format(
        filter_sensitive_keys_from_dict(config.merged_config)))


def _create_top_level_arguments_parser(parameters, entrypoints):
    parser = argparse.ArgumentParser(
        description='Helper for the configuration and analysis of \
            QAC and Coverity. Version = {}'.format(VERSION))

    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        default=False,
                        help='Enable debug mode')
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='v{version}'.format(version=VERSION))

    helper_sub = parser.add_subparsers(title='SCA Sub-Commands')
    parse_args_coverity(helper_sub, parameters.coverity, entrypoints)
    parse_args_find_includes(helper_sub, parameters.find_includes, entrypoints)
    parse_args_map_teams(helper_sub, parameters.map_teams, entrypoints)
    parse_args_qac(helper_sub, parameters.qac, entrypoints)
    parse_args_unify_reports(helper_sub, parameters.unify_reports, entrypoints)
    parse_args_compiler_warnings(helper_sub, parameters.compiler_warnings,
                                 entrypoints)

    return parser


def _parse_arguments(parameters, entrypoints, args=None):
    """Parses arguments from commandline"""

    parser = _create_top_level_arguments_parser(parameters, entrypoints)
    if args:
        parsed_args = parser.parse_args(args)
    else:
        parsed_args = parser.parse_args()

    try:
        parsed_args.entrypoint
    except AttributeError:
        parser.print_help()
        sys_exit(RC_INVALID_CMD_PARAMETERS)

    if not hasattr(parsed_args, 'func'):
        parsed_args.parser.print_help()
        sys_exit(RC_INVALID_CMD_PARAMETERS)

    return parsed_args


def run():
    """ Main entry function of SCA helper """
    ensure_utf8_stdout_call_once()
    LOGGER.initialize_once(_MODULE_NAME)
    entrypoints = {
        'compiler_warnings': compiler_warnings,
        'coverity_create': coverity_create,
        'coverity_check_buildlog': coverity_show_build_log_metrics,
        'coverity_analyze': coverity_analyze,
        'coverity_run_desktop': coverity_run_desktop,
        'coverity_export': coverity_export,
        'coverity_export_analysis': coverity_export_analysis,
        'coverity_preview_report': coverity_preview_report,
        'coverity_upload': coverity_upload,
        'coverity_webapi_export': coverity_webapi_export,
        'coverity_filter_report': coverity_filter_report,
        'find_includes': find_includes_entrypoint,
        'map_teams': map_teams,
        'unify_reports': unify_reports,
        'qac_create': qac_create,
        'qac_create_baseline': create_baseline,
        'qac_analyze': qac_analyze,
        'qac_report': qac_report,
        'qac_qavupload': qac_qavupload,
        'qac_gui': qac_gui,
        'qac_s101gen': qac_s101gen,
        'qac_state': qac_state,
        'qac_export_state': qac_export_state,
        'qac_fix_cl_json': fix_cl_json_entrypoint,
        'qac_filter_qaview': filter_qaview_entrypoint,
        'qac_export_analysis': qac_export_analysis
    }

    parameters = SCAParameters()
    parsed_args = _parse_arguments(parameters, entrypoints)

    if parsed_args.debug:
        LOGGER.set_verbose()

    if parsed_args.entrypoint == "compiler_warnings":
        config = create_compiler_warnings_config(parameters.compiler_warnings,
                                                 vars(parsed_args))
    elif parsed_args.entrypoint == "coverity":
        parameters.coverity.set_subcommand(parsed_args.subcommand)
        config = create_coverity_config(parameters.coverity, vars(parsed_args))
    elif parsed_args.entrypoint == "find_includes":
        config = create_find_includes_config(parameters.find_includes,
                                             vars(parsed_args))
    elif parsed_args.entrypoint == "map_teams":
        config = create_map_teams_config(parameters.map_teams,
                                         vars(parsed_args))
    elif parsed_args.entrypoint == "qac":
        parameters.qac.set_subcommand(parsed_args.subcommand)
        config = create_qac_config(parameters.qac, vars(parsed_args))
    elif parsed_args.entrypoint == "unify_reports":
        config = create_unify_reports_config(parameters.unify_reports,
                                             vars(parsed_args))

    entry_index = argv.index(parsed_args.entrypoint)
    slice_length = 1 if argv[entry_index + 1].startswith('-') else 2
    helper_command = '_'.join(argv[entry_index:entry_index + slice_length])
    init_logger_for_helper_command(config, helper_command)

    parsed_args.func(config)

    LOGGER.info("- done -")


if __name__ == "__main__":
    run()
