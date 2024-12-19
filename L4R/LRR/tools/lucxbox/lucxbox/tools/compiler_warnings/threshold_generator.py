""" Terminal script for updating json config files with new errors in specific path. """

import argparse
import importlib
import json
import os
import re
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog

LOGGER = lucxlog.get_logger()


def parse_args():
    """
    Arguments parser for python.
    :return: arguments obj.
    """
    description = "Update json config files. Displaying difference between logs and configuration. Displaying errors" \
                  " in log files. Incoming parameters is path to directories. Script matches config files" \
                  " and logs based on their names. It means that config must be named thresholds_{cfg_name}.json" \
                  " and at the same time logs should have names {whatever}_{cfg_name}.log to successfully" \
                  " match each other."
    parser = argparse.ArgumentParser(description=description)
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    parser.add_argument('-l', '--log-directory', dest='logs_dir', required=True, help="Path to logs dir.")
    parser.add_argument('-c', '--config-directory', dest='config_dir', required=True, help="Path to config dir.")
    parser.add_argument('-a', '--action',
                        choices=['show', 'diff', 'gen'],
                        dest='action',
                        required=True,
                        help="Three types of actions available: show, diff, gen. Show - display all errors in log "
                             "files. Diff - displaying diff between log and conf. Gen - generate list if new warnings"
                             " and update conf files with new errors.")
    return parser.parse_args()


def check_directories(logs_directory, config_directory):
    """
    This function is checking 2 directories for matching json config
    files to log files depends on file names.
    :param logs_directory: Path to directory with log files.
    :param config_directory: Path to directory with threshold files.
    :return: dict with mapping of paths between logs and conf_json.
    """
    params_list = {}
    logs_array = os.listdir(logs_directory)
    config_array = os.listdir(config_directory)
    for config in config_array:
        search_string = config.replace('thresholds_', '.*').replace('json', 'log')
        for log in logs_array:
            if re.match(search_string, log):
                params_list[os.path.abspath(os.path.join(config_directory, config))] =\
                    os.path.abspath(os.path.join(logs_directory, log))
    if not params_list:
        LOGGER.critical("No matches were found. Please check directories given.")
        sys.exit(1)
    return params_list


def parsing_data(path_dict):
    """
    Using regexp to get all errors in log files and count them.
    :param path_dict: Dict with format {conf_path:log_path}
    :return: List with config file name and errors list from mapped logfile
    """
    error_list = []
    result_data = {}
    for conf, log in path_dict.items():
        errors = {}
        LOGGER.debug("Searching in file '%s' for compiler warnings", log)
        warnings = COMPILER.get_warnings_from_file(log, 1)
        for i in warnings:
            error_list.append(i.type_name)
        unique_errors = list(set(error_list))
        for err in unique_errors:
            errors[err] = str(error_list.count(err))
        if errors:
            result_data[conf] = {'errors_dict': errors}
    return result_data


def save_configuration_file(prepared_dict, config_file):
    """
    Updating config files with new errors on the given path.
    :param prepared_dict: Dict with prepared list of errors to save.
    :param config_file: Path and name of config file
    :return: Returns True if everything is okay.
    """
    array_to_json = []
    for item in prepared_dict:
        dict_to_file = {'warning_name': item, 'threshold': int(prepared_dict[item])}
        array_to_json.append(dict_to_file)
    json_file = open(config_file, "w")
    json_file.write(json.dumps(array_to_json, indent=4, sort_keys=True))
    json_file.close()
    LOGGER.info("Config file '%s' was updated.", config_file)
    return True


def generate_flag_files(data):
    """
    Generating cmake flags from generated threshold files.
    :param data: prepared data array.
    :return: Returns True if everything is okay.
    """
    for file_path in data:
        warnings_list = get_json_from_file(file_path)
        with open("Wno-List-for-" + str(os.path.basename(file_path)).replace(".json", ".txt"), "w") as flag_file:
            flag_file.write("set(l_FLAGS_WARNINGS_NO_ERROS\n")
            for warning in warnings_list:
                flag_file.write(" -Wno-error=" + str(warning['warning_name']).replace("#", "\\#") + "\n")
            flag_file.write(")")
            flag_file.close()
    return True


def generate_configuration(logs_dict):
    """
    Checking logs array and config file for new errors and send generated data for saving in file.
    :param logs_dict: Dictionary with data
    :return: Print or True from save_configuration_file function.
    """
    for i in logs_dict:
        configuration_dict = {}
        logs_errors_dict = logs_dict[i]['errors_dict']
        for config in get_json_from_file(i):
            configuration_dict[config['warning_name']] = config['threshold']
        for warning_conf in configuration_dict:
            if warning_conf in logs_errors_dict.keys():
                logs_errors_dict.pop(warning_conf)
        if not logs_errors_dict:
            LOGGER.info("There are no new warnings in the log file for: '%s' Configuration file was not changed.", i)
        else:
            for warning_conf in configuration_dict:
                logs_errors_dict[warning_conf] = configuration_dict[warning_conf]
            save_configuration_file(logs_errors_dict, i)


def get_json_from_file(file_path):
    """
    Getting data from json file.
    :param file_path: Config file path.
    :return: data from file
    """
    configuration = []
    with open(file_path) as file_data:
        try:
            configuration = json.load(file_data)
        except ValueError:
            return configuration
        else:
            return configuration


def print_current_log_state(logs_dict):
    """
    Printing all errors inside given log files
    :param logs_dict: Dictionary with errors
    :return: Readable print of errors.
    """
    LOGGER.debug("ALL WARNINGS IN LOG FILES")
    for i in logs_dict:
        logs_errors_dict = logs_dict[i]['errors_dict']
        LOGGER.debug("JSON config file path: '%s'", i)
        if not logs_errors_dict:
            LOGGER.info("There are no warnings in the log file")
        else:
            for err_name in logs_errors_dict:
                LOGGER.debug(err_name + " :" + logs_errors_dict[err_name])


def print_difference(logs_dict):
    """
    Printing only unique(new) errors from log files.
    :param logs_dict: Dictionary with errors
    :return: Readable print of new (unique errors) in the files.
    """
    LOGGER.debug("DIFFERENCE CONFIGURATION AND LOGS")
    for i in logs_dict:
        configuration_dict = {}
        logs_errors_dict = logs_dict[i]['errors_dict']
        for config in get_json_from_file(i):
            configuration_dict[config['warning_name']] = config['threshold']
        for warning_conf in configuration_dict:
            if warning_conf in logs_errors_dict.keys():
                logs_errors_dict.pop(warning_conf)
        LOGGER.debug("JSON config file path: '%s'", i)
        if not logs_errors_dict:
            LOGGER.info("There are no new warnings in the log file")
        else:
            for err_name in logs_errors_dict:
                LOGGER.debug(err_name + " :" + logs_errors_dict[err_name])


if __name__ == "__main__":
    ARGS = parse_args()
    LOGGER.setLevel(ARGS.log_level)

    if not os.path.exists(ARGS.logs_dir):
        LOGGER.critical("Path '%s' does not exist", ARGS.logs_dir)
        sys.exit(1)
    elif not os.path.exists(ARGS.config_dir):
        LOGGER.critical("Path '%s' does not exist.", ARGS.config_dir)
        sys.exit(1)

    COMPILER_LIB = importlib.import_module("compiler_clang")
    COMPILER = COMPILER_LIB.Compiler()

    LOGGER.debug("Cross checking directories: logs '%s'<=> configs '%s'", ARGS.logs_dir, ARGS.config_dir)
    PATH_LIST = check_directories(ARGS.logs_dir, ARGS.config_dir)
    PREPARED_DATA = parsing_data(PATH_LIST)

    if ARGS.action == 'diff':
        print_difference(PREPARED_DATA)
        sys.exit(0)
    elif ARGS.action == 'show':
        print_current_log_state(PREPARED_DATA)
        sys.exit(0)
    elif ARGS.action == 'gen':
        generate_configuration(PREPARED_DATA)
        generate_flag_files(PREPARED_DATA)
        sys.exit(0)
