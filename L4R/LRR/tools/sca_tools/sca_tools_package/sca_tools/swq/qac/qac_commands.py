# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: qac_commands.py
# ----------------------------------------------------------------------------
""" Defines QAC commands """
from multiprocessing import cpu_count
from subprocess import Popen
from os import path
from swq.common.command.command_decorator import command, \
        adapt_command_to_list_or_string_according_to_os
from swq.common.logger import LOGGER
from swq.qac import qac_utils
from swq.common.file.file_utils import write_sha256_to_metadata, \
    move_file_to_target_folder

# Format export in the following custom format
# %u   Context message depth
# %F - File name (absolute, including path)
# %l - Line number
# %c - Column number
# %G - Rule group
# %p - Producer component (e.g. qacpp-3.1)
# %N - Message number (zero padded to four digits)
# %r - Rule text
# %t - Message text
# %Y - Severity
# %S - Suppression type bitmask
# %j - Suppression justification

_FORMAT_SEQUENCE = [
    '%u', '%F', '%l', '%c', '%p:%N', '\\"%t\\"', '%Y', '%S', '\\"%j\\"',
    '\\"%G\\"', '\\"%r\\"'
]

_DIAG_XML_FORMAT_SEQUENCE = '%F%l%c%p%N%t%Y%S%j%G%r'


@command()
def create_qac_project(config, compiler_list, config_files_pair):
    """ Runs qacli command to create QAC project """
    command_string = '{} admin --qaf-project-config -P {} {} {}'.format(
        config.qacli, config.qac_project_path, compiler_list, ' '.join([
            '--{} {}'.format(param, config_file)
            for (param, config_file) in config_files_pair if config_file
        ]))
    return [command_string]


def _qacli_command(config, qacli_command):
    return [config.qacli, qacli_command]


def run_qacli_command(config, qacli_command):
    """Runs qacli command in qac_project_path"""
    command_decorator = command(cwd=config.qac_project_path)(_qacli_command)

    return command_decorator(config, qacli_command)


@command()
def set_license_server(config, sever_url: str):
    LOGGER.info("License server will be set to %s", sever_url)
    return [config.qacli, "admin", "--set-license-server", sever_url]


@command()
def list_license_server(config):
    return [config.qacli, "admin", "--list-license-servers"]


@command()
def check_license_server(config):
    return [config.qacli, "admin", "--check-license"]


@command()
def set_debug_level(config):
    return [config.qacli, "admin", "--debug-level", config.qac_logging_level]


def _analyze_file(config, filepath, output_log_file):
    return [
        config.qacli, "analyze", "-P", config.qac_project_path,
        "--output-progress", output_log_file, config.analyze_params, filepath
    ]


def analyze_file(config, filepath_or_command, output_log_file) -> (str, int):
    """Analyzes a specified file with QAC - if empty will analyze
    the whole project"""
    final_command = ""
    if filepath_or_command:
        final_command = filepath_or_command
    command_decorator = command(fail_fast=False,
                                cwd=config.project_root)(_analyze_file)

    return command_decorator(config, final_command, output_log_file)


@command()
def set_default_config(config):
    return [
        config.qacli, "admin", "--qaf-project", config.qac_project_path,
        "--set-default-config", "--config Initial"
    ]


@command()
def set_source_code_root(config):
    return [
        config.qacli, "admin", "--qaf-project", config.qac_project_path,
        "--set-source-code-root", config.project_root
    ]


@command()
def list_config_files(config):
    return [
        config.qacli, "admin", "--qaf-project", config.qac_project_path,
        "--list-config-files"
    ]


@command()
def export_report(config,
                  report_type: str,
                  parallel: bool = False,
                  ignore_dependencies: bool = False):
    """Exports a helix report using the report cmd line"""
    cmd_base = [config.qacli, "report"]
    args = []
    # This is used as a workaround for RCMA which can yield
    # the report cmd unusable if files are out-of-date/sync
    if ignore_dependencies:
        args.append('--ignore')
    if parallel:
        args.append('-j {}'.format(cpu_count()))
    args.extend([
        "-P", "\"{}\"".format(config.qac_project_path), "--type", report_type
    ])

    return [*cmd_base, *args]


@command()
def set_up_project(config, compiler_list, appendix: list):
    LOGGER.info("Creating QAC project in:  %s", config.qac_project_path)
    return [
        config.qacli, "admin", "--qaf-project-config", "-P",
        config.qac_project_path, compiler_list, *appendix
    ]


def _get_qacli_view_command(config, extra_args=[]):
    return [
        config.qacli,
        'view',
        '--qaf-project',
        '\"{}\"'.format(config.qac_project_path),
        *extra_args,
        *config.qacli_view_extra_args
    ]


def _export_project_summary(config):
    export_args = '-m XML -o'

    if qac_utils.has_summary_export(config):
        export_args = '-t SUMMARY -m XML -o'

    return _get_qacli_view_command(
        config, extra_args=[
            export_args, '\"{}\"'.format(config.project_reports_path)])


def export_project_summary(config):
    """Exports a XML summary of the project current findings"""

    command_decorator = command(
        fail_fast=False,
        use_logger=False,
        silent=True,
        cwd=config.project_root)(_export_project_summary)

    return command_decorator(config)


def _export_formatted_project_analysis(config):
    return _get_qacli_view_command(
        config, extra_args=[
            '--suppressed-messages --rules --medium STDOUT --format',
            ','.join(_FORMAT_SEQUENCE)])


def export_formatted_project_analysis(config):
    """Exports a formatted project analysis in a csv compliant format"""
    command_decorator = command(
        fail_fast=False,
        use_logger=False,
        silent=True,
        cwd=config.project_root)(_export_formatted_project_analysis)

    return command_decorator(config)


@command(fail_fast=False)
def qac_suppress(config, module, filepath):
    """Suppresses a specific filepath"""
    final_filepath = config.get_absolute_path_or_relative_to_project_root(
        filepath)
    return [
        config.qacli, "pprops --qaf-project",
        "\"" + config.qac_project_path + "\"", "-c", module, "-O",
        final_filepath, "--set-options"
    ]


def _get_common_qac_sync_command(config):
    command_base = [
        config.qacli, 'sync', '--qaf-project',
        '\"{}\"'.format(config.qac_project_path)
    ]
    if not config.disable_optimization and config.optimization:
        command_base.append(config.optimization)
    return command_base


@command(fail_fast=False)
def sync_project_build_log(config):
    """Populates QAC project with BUILD_LOG synchronization type"""
    command_list = _get_common_qac_sync_command(config)
    command_list.extend(['--type', 'BUILD_LOG', config.actual_build_log])

    return command_list


@command(fail_fast=False)
def sync_project_json(config):
    """Populates QAC project with JSON synchronization type"""
    command_list = _get_common_qac_sync_command(config)
    command_list.extend(['--type', 'JSON', config.actual_sync_json])

    return command_list


@command(fail_fast=False)
def apply_sync_settings(config, sync_option, option):
    return [
        config.qacli, "pprops", "-P", config.qac_project_path,
        "--sync-setting", sync_option, "--set", option
    ]


@command(fail_fast=False, silent=True)
def delete_file_to_optimize_project(config, optimization_workaround_path):
    """Workaround to optimize QAC project with MONITOR synchronization type"""
    return [
        config.qacli, "admin --qaf-project", config.qac_project_path,
        "--optimize --remove-files", optimization_workaround_path
    ]


def _remove_files_from_project(config):
    return [
        config.qacli, "admin", "--qaf-project",
        "\"{}\"".format(config.qac_project_path), "-D",
        config.helper_remove_file_list
    ]


def remove_files_from_project(config):
    """Removes files listed in helper_remove_file_list from qac project"""
    command_decorator = command(cwd=config.project_root, fail_fast=False)(
        _remove_files_from_project)
    return command_decorator(config)


def sync_project_monitor(config):
    """Populates QAC project with MONITOR synchronization type"""
    def _get_sync_project_monitor_command(config):
        return [
            config.qacli, "admin", "--qaf-project",
            f'"{config.qac_project_path}"',
            "-b", f'"{config.sync_build_command}"'
        ]

    command_decorator = command(cwd=config.project_root, fail_fast=False)(
        _get_sync_project_monitor_command)

    return command_decorator(config)


@command(fail_fast=False)
def s101_gen(config):
    return [
        config.qacli, "upload", "--qaf-project", config.qac_project_path,
        "--s101-upload", "--upload-location",
        path.join(config.qac_project_path, "s101")
    ]


@command()
def list_components(config):
    return [
        config.qacli, "pprops", "--qaf-project",
        "\"" + config.qac_project_path + "\"", "--list-components"
    ]


@command(fail_fast=False, use_logger=False)
def vscode_output(config):
    file_to_analyze_arg = ''
    if config.analyze_file:
        file_to_analyze_arg = config.analyze_file

    return _get_qacli_view_command(
        config, extra_args=[
            "--format \"%F:%l:%c: %p-%N-%r %t\"", "-m", "STDOUT",
            file_to_analyze_arg])


@command()
def setup_baseline(config, baseline_path: str):
    return [
        config.qacli, "baseline", "-P",
        "\"{}\"".format(config.qac_project_path), "--baseline-type", "LOCAL",
        "--set-baseline", "--local-source", "\"{}\"".format(baseline_path)
    ]


@command()
def _create_baseline(config):
    LOGGER.info("Baseline will be created in %s",
                config.target_baseline_folder)

    return [
        config.qacli, "baseline", "-P",
        "\"{}\"".format(config.qac_project_path), "--baseline-type", "LOCAL",
        "--generate-baseline"
    ]


def create_baseline(config):
    """Creates baseline"""
    _create_baseline(config)
    move_file_to_target_folder(config.local_baseline_cache_filepath,
                               config.target_baseline_filepath)
    write_sha256_to_metadata(config.target_baseline_filepath)


@command(fail_fast=False)
def apply_sync_filter(config, sync_filter: str):
    return [
        config.qacli, "pprops", "--qaf-project",
        "\"{}\"".format(config.qac_project_path), "--sync-setting",
        "FILE_FILTER", "--set", sync_filter
    ]


@command(fail_fast=False)
def apply_path_blacklist(config, module: str, analysis_filters_file: str,
                         toolchain: str):
    return [
        config.qacli, "pprops", "--qaf-project",
        "\"" + config.qac_project_path + "\"", "-c", module, "-O",
        analysis_filters_file, "--set-options", "--toolchain", toolchain
    ]


def _build_project_command(config):
    return [config.sync_build_command]


def _build_command_decorator(build_shell, cwd):
    return command(fail_fast=False, build_shell=build_shell,
                   cwd=cwd)(_build_project_command)


def build_project_with_shell(config) -> (str, int):
    """"Builds project with build shell active"""
    command_decorator = _build_command_decorator(build_shell=True,
                                                 cwd=config.project_root)
    return command_decorator(config)


def build_project_without_shell(config) -> (str, int):
    """"Builds project without build shell"""
    command_decorator = _build_command_decorator(build_shell=False,
                                                 cwd=config.project_root)
    return command_decorator(config)


def launch_gui(config):
    """Launchs the QAC UI according to configured version
    for the specified project"""
    launch_gui_command = " ".join(
        [config.qagui, "--qaf-project", config.qac_project_path])
    launch_gui_string_or_list = \
        adapt_command_to_list_or_string_according_to_os(launch_gui_command)
    LOGGER.info("Launching gui with command \"%s\"", launch_gui_string_or_list)
    Popen(launch_gui_string_or_list)


@command(fail_fast=False)
def upload_qaf_project(config):
    return [
        config.qacli, "upload", "--qaf-project", config.qac_project_path,
        "--qav-upload", "--upload-project", config.qav_project_name,
        "--snapshot-name", config.qav_project_snapshot, "--upload-source",
        config.qav_upload_source, "--url", config.qav_server_url, "--username",
        config.qav_username, "--password", config.qav_password
    ]


@command(fail_fast=False)
def git_rev_parse(config):
    return ['git', '-C', config.project_root, 'rev-parse', '--verify', 'HEAD']


@command(fail_fast=False)
def cli_version(config):
    return [config.qacli, "--version"]


@command(fail_fast=False)
def cli_config_folder(config):
    return [config.qacli, "admin --get-user-data-location"]


@command()
def set_namerule_config(config):
    return [
        config.qacli, "pprops", "--qaf-project", config.qac_project_path, "-c",
        "namecheck-2.0.0", "-T", "C++", "-o", "nrf", "--set",
        config.ncf_file.get_result_filepath()
    ]


def setup_c_as_cpp_extensions(config):
    """Adds C-related file extensions to C++ analysis"""
    @command()
    def _remove_file_extension_from_language(config, extension, language='C'):
        return [
            config.qacli, 'admin', '--qaf-project', config.qac_project_path,
            '--target-language', language, '--remove-source-extension',
            extension
        ]

    @command()
    def _add_file_extension_to_language(config, extension, language='C++'):
        return [
            config.qacli, 'admin', '--qaf-project', config.qac_project_path,
            '--target-language', language, '--add-source-extension', extension
        ]

    _remove_file_extension_from_language(config, '.c', 'C')
    _remove_file_extension_from_language(config, '.C', 'C')
    _add_file_extension_to_language(config, '.c', 'C++')
    _add_file_extension_to_language(config, '.C', 'C++')


@command()
def export_diagnostics(config):
    """ Exports diagnostics for each analyzed file """
    return _get_qacli_view_command(
        config, extra_args=[
            '--suppressed-messages',
            '-m XML -o', '\"{}\"'.format(config.project_diagnostics_path),
            '--xml-format "{}" --format ""'.format(_DIAG_XML_FORMAT_SEQUENCE)])


@command()
def set_maximum_cpu(config):
    """Sets maximum number of CPUs for parallel workers"""
    return [config.qacli, 'admin', '--set-cpus', config.max_parallel_workers]
