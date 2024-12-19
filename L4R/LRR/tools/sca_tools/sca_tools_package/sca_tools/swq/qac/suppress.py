# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: suppress.py
# ----------------------------------------------------------------------------

from os import path, makedirs, walk
from json import load, dump
import subprocess

from swq.common.filesystem.filesystem_utils import open_t
from swq.common.logger import LOGGER
from swq.qac.qac_commands import qac_suppress


def suppress_file_in_static_list_s(modified_buildlog, files_in_list,
                                   output_filepath=None):
    files_in_list = [a_file.replace("\\", "/") for a_file in files_in_list]
    modified_buildlog_filtered = \
        output_filepath \
        if output_filepath else modified_buildlog + ".fil"
    modified_json = []
    with open_t(modified_buildlog) as file_input_list:
        data = load(file_input_list)
        LOGGER.info("Original JSON length: %s", len(data))
        for item in data:
            if all(f not in item['file'] for f in files_in_list):
                modified_json.append(item)
    LOGGER.info("Filtered JSON length: %s", len(modified_json))
    with open_t(modified_buildlog_filtered, mode="wt") as fout:
        dump(modified_json, fout, sort_keys=True, indent=4, ensure_ascii=False)
    return modified_buildlog_filtered


def suppress_file_in_static_list_s_build_log(modified_buildlog,
                                             file_list_path,
                                             output_filepath=None):
    with open_t(path.abspath(modified_buildlog)) as file:
        build_log_line_list = [
            path.normpath(line.rstrip('\n')) for line in file
        ]

    LOGGER.info("Original build log length: " + str(len(build_log_line_list)))
    for line_f in file_list_path:
        for line_b in build_log_line_list:
            if line_f in line_b:
                build_log_line_list.remove(line_b)
                break

    LOGGER.info("Filtered build log length: " + str(len(build_log_line_list)))
    modified_buildlog_filtered = \
        output_filepath \
        if output_filepath else modified_buildlog + ".fil"
    with open_t(modified_buildlog_filtered, mode='w') as fout:
        fout.writelines("%s\n" % line for line in build_log_line_list)
    return modified_buildlog_filtered


def suppress_c_header(config):
    header_files = _get_analysis_excluded_header_paths(config.project_root)
    LOGGER.debug('excluded header paths = %s', header_files)
    via_file = path.join(config.via_path, "suppress_h.via")
    _create_opt_file(header_files, via_file)
    # without modules we cant continue
    modules = config.qac_modules
    if modules:
        LOGGER.info("QAC_MODULES found")
        for module in modules:
            LOGGER.info("appyling suppress_h.via to module = %s", module)
            qac_suppress(config, module, via_file)
    return via_file, header_files


def suppress_file_in_static_list_a(config, files_in_list):
    if len(files_in_list) > 0:
        makedirs(config.via_path, exist_ok=True)
        via_file = path.join(config.via_path, "suppress_file_list.via")

        _create_opt_file(files_in_list, via_file)
        modules = config.qac_modules
        if modules:
            LOGGER.info("QAC_MODULES found")
            try:
                for module in modules:
                    LOGGER.info(
                        "appyling suppress_file_list.via to module = %s",
                        module)
                    qac_suppress(config, module, via_file)
            except subprocess.CalledProcessError as error:
                LOGGER.warning(
                    "Could not apply suppression to module %s with error %s",
                    module, error)

    return via_file


def _create_opt_file(header_files, via_file):
    with open_t(via_file, mode="w+") as opt_file:
        for header in header_files:
            opt_file.write("-q " + header + "\n")


def _get_all_header_files_in_directory(filepath):
    def is_c_or_cpp_header_file(filename):
        return filename.endswith('.h') or filename.endswith('.hpp')

    return [
        path.join(root, header_file) for root, _, files in walk(filepath)
        for header_file in files if is_c_or_cpp_header_file(header_file)
    ]


def _get_analysis_excluded_header_paths(filepath):
    LOGGER.info('_get_analysis_excluded_header_paths filepath = %s', filepath)
    all_header_files = _get_all_header_files_in_directory(filepath)
    directories_with_cpp_headers = {
        path.dirname(cpp_header_file)
        for cpp_header_file in all_header_files
        if cpp_header_file.endswith('.hpp')
    }
    all_c_header_files = [
        c_header_file for c_header_file in all_header_files
        if c_header_file.endswith('.h')
    ]
    directories_with_c_headers_only = {
        path.dirname(c_header_file)
        for c_header_file in all_c_header_files
        if not path.dirname(c_header_file) in directories_with_cpp_headers
    }
    mixed_c_in_cpp_filepaths = [
        c_header_file for c_header_file in all_c_header_files
        if path.dirname(c_header_file) in directories_with_cpp_headers
    ]

    return [*directories_with_c_headers_only, *mixed_c_in_cpp_filepaths]
