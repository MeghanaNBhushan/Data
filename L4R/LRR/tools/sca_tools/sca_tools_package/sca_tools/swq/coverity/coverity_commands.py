# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: coverity_commands.py
# ----------------------------------------------------------------------------
"""Defines coverity commands"""

import os

from os import path, environ
from swq.common.return_codes import log_and_exit, RC_MISSING_PARAMETER
from swq.coverity.coverity_version import CoverityVersion
from swq.common.command.command_decorator import command
from swq.common.logger import LOGGER


def get_os_command_exe(config, executable_name):
    """Gets path to executable by executable_name"""
    exe = path.normpath(
        path.join(
            config.coverity_bin_path,
            "{}{}".format(executable_name, config.platform_command_extension)))
    return exe


def _ensure_cov_env_parity(config):
    if config.webapi_coverity_user:
        if environ.get('COV_USER'):
            LOGGER.warning('Overriding COV_USER with %s',
                           config.get_parameter_name('COVERITY_USERNAME'))
        environ['COV_USER'] = config.webapi_coverity_user

    if config.webapi_coverity_passcode:
        if environ.get('COVERITY_PASSPHRASE'):
            LOGGER.warning('Overriding COVERITY_PASSPHRASE with %s',
                           config.get_parameter_name('COVERITY_PASSWORD'))
        environ['COVERITY_PASSPHRASE'] = config.webapi_coverity_passcode


def extend_coverity_command_with_connection_options(
    config, command_string):
    """Exntends coverity command with connection options"""
    if config.coverity_commit_url:
        command_string.extend(['--url', config.coverity_commit_url])
    if config.coverity_commit_host:
        command_string.extend(['--host', config.coverity_commit_host])
    if config.coverity_commit_dataport:
        command_string.extend(['--dataport', config.coverity_commit_dataport])

    if not (config.auth_key_filepath or
            (config.webapi_coverity_user and config.webapi_coverity_passcode)):
        LOGGER.error('Either %s with %s or %s should be defined',
                     config.get_parameter_name('COVERITY_USERNAME'),
                     config.get_parameter_name('COVERITY_PASSWORD'),
                     config.get_parameter_name('COVERITY_AUTH_KEY_FILEPATH'))
        log_and_exit(RC_MISSING_PARAMETER)

    if config.auth_key_filepath:
        command_string.extend(['--auth-key-file', config.auth_key_filepath])
    else:
        _ensure_cov_env_parity(config)


def _cov_commit_defects(config, output_path: str):
    command_string = [
        get_os_command_exe(config, 'cov-commit-defects'), '--stream',
        config.coverity_commit_stream, '--dir', config.coverity_project_path
    ]

    extend_coverity_command_with_connection_options(
        config, command_string)

    if output_path:
        command_string.extend(['--preview-report-v2', output_path])

    return command_string


def _cov_commit_defects_decorator(cwd, output_path):
    def _cov_commit_defects_wrapper(config):
        return _cov_commit_defects(config, output_path)

    return command(fail_fast=False, cwd=cwd)(_cov_commit_defects_wrapper)


def cov_commit_defects(config, output_path: str = ""):
    """cov-commit-defects command call, if output_path is supplied just
    a preview will be performed and NO data is commited to the server."""
    command_decorator = _cov_commit_defects_decorator(cwd=config.project_root,
                                                      output_path=output_path)

    return command_decorator(config)


def _get_version_of_json_format(config):
    (major, _) = CoverityVersion(config.cli_version_string).major_minor()
    return 8 if major >= 2021 else 6


def _coverity_export_errors(config):
    command_string = [
        get_os_command_exe(config, 'cov-format-errors'), '--dir',
        config.coverity_project_path
    ]

    if config.cov_export_blacklist:
        command_string.extend(['--exclude-files', config.cov_export_blacklist])

    if config.cov_export_whitelist:
        command_string.extend(['--include-files', config.cov_export_whitelist])

    return command_string


def _coverity_export_errors_json_decorator(cwd, coverity_json_filepath: str):
    def _coverity_export_errors_json_wrapper(config):
        command_string = \
            _coverity_export_errors(config)

        version = _get_version_of_json_format(config)
        command_string.extend(
            [f'--json-output-v{version}', coverity_json_filepath])

        return command_string

    return \
        command(fail_fast=False, cwd=cwd)(_coverity_export_errors_json_wrapper)


def coverity_export_errors_json(config, coverity_json_filepath: str):
    """Exports coverity errors in JSON format"""
    command_decorator = _coverity_export_errors_json_decorator(
        config.project_root, coverity_json_filepath)

    return command_decorator(config)


def _coverity_export_errors_html_decorator(cwd):
    def _coverity_export_errors_html_wrapper(config):
        command_string = \
            _coverity_export_errors(config)

        command_string.extend(
            ['--html-output', config.cov_errors_html_dirpath])

        return command_string

    return \
        command(fail_fast=False, cwd=cwd)(_coverity_export_errors_html_wrapper)


def coverity_export_errors_html(config):
    """Exports coverity errors in HTML format"""
    command_decorator = _coverity_export_errors_html_decorator(
        config.project_root)

    return command_decorator(config)


def _run_coverity_analyze(config):
    """Runs coverity analysis using command decorator"""
    command_string = [
        get_os_command_exe(config, 'cov-analyze'), '--dir',
        config.coverity_project_path, '--strip-path',
        path.normpath(config.project_root)
    ]
    if config.cov_analyze_option_list:
        command_string.extend(config.cov_analyze_option_list)

    return command_string


def _run_coverity_analyze_decorator(cwd):
    return command(fail_fast=False, cwd=cwd)(_run_coverity_analyze)


def run_coverity_analyze(config):
    """Runs coverity analysis using command decorator"""
    command_decorator = _run_coverity_analyze_decorator(config.project_root)

    return command_decorator(config)


@command(fail_fast=False)
def run_cov_run_desktop(config):
    """Runs cov_run_desktop using command decorator"""
    command_string = [
        get_os_command_exe(config, 'cov-run-desktop'),
        '--stream', config.coverity_commit_stream,
        '--dir', config.coverity_project_path,
        '--analyze-captured-source'
    ]

    extend_coverity_command_with_connection_options(
        config, command_string)

    if config.coverity_config_filepath:
        command_string.extend(['--config', config.coverity_config_filepath])

    if config.run_desktop_extra_options:
        command_string.extend(config.run_desktop_extra_options)

    return command_string


@command(fail_fast=False)
def get_coverity_analysis_version(config):
    """Gets coverity analysis version and build number"""
    return [
        get_os_command_exe(config, 'cov-analyze'),
        '--ident',
    ]


@command(fail_fast=False)
def list_coverity_translation_units(config):
    """Gets list of coverity translation units"""
    return [
        get_os_command_exe(config, 'cov-manage-emit'), '--dir',
        config.coverity_project_path, '--tus-per-psf=latest', 'list'
    ]


def _coverity_config_for_compiler_command(config, compiler: str):
    coverity_config = path.normpath(
        path.join(config.project_root, config.coverity_project_path, 'config',
                  'coverity_config.xml'))
    return [
        get_os_command_exe(config, 'cov-configure'), '--config',
        coverity_config, compiler
    ]


def _coverity_config_decorator(config, compiler: str):
    def _coverity_config_for_compiler_command_wrapper(config):
        return _coverity_config_for_compiler_command(config, compiler)

    return command(
        fail_fast=False,
        cwd=config.project_root)(_coverity_config_for_compiler_command_wrapper)


def create_coverity_config_for_compiler(config, compiler: str):
    """Creates coverity config for selected compiler"""
    command_decorator = _coverity_config_decorator(config, compiler)

    return command_decorator(config)


@command(fail_fast=False)
def coverity_filter_translation_unit(config, filter_line: str):
    """Runs coverity_helper filter for translation unit"""
    LOGGER.info('Removing %s', filter_line.strip())
    line_after_strip = filter_line.strip()

    return [
        get_os_command_exe(config, 'cov-manage-emit'), '--dir',
        config.coverity_project_path, '--tu-pattern',
        f'\"file(\'{line_after_strip}\')\" delete'
    ]


def _build_project_command(config, build_command):
    coverity_config = path.normpath(
        path.join(config.project_root, config.coverity_project_path, 'config',
                  'coverity_config.xml'))

    command_list = [
        get_os_command_exe(config, 'cov-build'), '--dir',
        config.coverity_project_path
    ]

    if config.cov_build_option_list:
        command_list.extend(config.cov_build_option_list)

    command_list.extend(['--config', coverity_config, build_command])

    return command_list


def _build_command_decorator(cwd, build_command):
    def _build_project_command_wrapper(config):
        return _build_project_command(config, build_command)

    return command(fail_fast=False, cwd=cwd)(_build_project_command_wrapper)


def run_coverity_build(config, build_command):
    """Runs coverity build using command decorator"""
    command_decorator = _build_command_decorator(cwd=config.project_root,
                                                 build_command=build_command)

    return command_decorator(config)


def _build_compile_commands_json(config):
    return [config.compile_commands_build_command]


def _compile_commands_decorator(config):
    return command(fail_fast=False,
                   cwd=config.project_root)(_build_compile_commands_json)


def run_generate_compile_commands(config):
    """Runs shell script to generate compile_commands.json"""
    command_decorator = _compile_commands_decorator(config)

    return command_decorator(config)


@command(fail_fast=False)
def git_rev_parse(config):
    """Gets git rev-parse command execution result"""
    return ['git', '-C', config.project_root, 'rev-parse', '--verify', 'HEAD']
