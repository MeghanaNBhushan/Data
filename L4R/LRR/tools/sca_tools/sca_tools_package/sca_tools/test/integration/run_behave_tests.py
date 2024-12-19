# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: run_behave_tests.py
# ----------------------------------------------------------------------------
""" Entrypoint script for behave tests """

from os import environ as os_environ, path as os_path

from behave.__main__ import main as behave_main

from sys import exit, path as sys_path
from pathlib import Path as pathlib_Path

_HERE = pathlib_Path(__file__).parent.parent
SWQ_MODULE_PATH = _HERE.parent

sys_path.insert(0, f'{SWQ_MODULE_PATH}')

from test.integration.utils.args_utils import setup_argument_parser    # noqa
from test.integration.utils.common_utils import LOGGER, \
    initialize_logger_if_verbose_enabled  # noqa
from test.integration.constants import FEATURES_QAC, \
    FEATURES_COVERITY, BEHAVE_FOLDER_NAME, OS_FOLDER  # noqa


def _get_options(args):
    options = []
    if args.version:
        options.append('--tags=@' + args.version)
        os_environ['VERSION'] = args.version

    if args.reports_dir:
        options.append('--junit')
        options.append('--junit-directory={}'.format(
            os_path.normpath(args.reports_dir)))
    return options


def _get_list_of_features_from_args(analyzer, parsed_args):
    features = parsed_args.features

    if 'all' in parsed_args.features:
        features.remove('all')
        features += globals()[f'FEATURES_{analyzer.upper()}'].keys()

    return list(set(features))


def _validate_features(features, feature_list):
    for feature in features:
        if feature not in feature_list:
            print(f'Feature with name {feature} is not found')
            exit(1)


def run_tests(list_of_features, analyzer, parsed_args):
    print(f'Start behave tests for {analyzer}')
    options = _get_options(parsed_args)
    features_from_args = _get_list_of_features_from_args(analyzer, parsed_args)
    _validate_features(features_from_args, list_of_features)
    feature_paths = sorted([
        f'{BEHAVE_FOLDER_NAME}/features/{analyzer}/{OS_FOLDER}' +
        f'/{list_of_features[feature]}'
        for feature in features_from_args
    ])

    return_code = 0

    for feature_path in feature_paths:
        behave_return_code = 0

        try:
            behave_args = [feature_path] + options
            behave_return_code = behave_main(behave_args)
        except Exception:
            return_code = behave_return_code

        if behave_return_code != 0:
            return_code = behave_return_code
            print('Feature {} failed with exitcode {}'.format(
                feature_path, behave_return_code))

    exit(return_code)


def run():
    arg_parser = setup_argument_parser()
    parsed_args = arg_parser.parse_args()

    initialize_logger_if_verbose_enabled(parsed_args)
    os_environ['BEHAVE_PROJECT_ROOT'] = parsed_args.project_root

    if parsed_args.test_type == 'qac':
        run_tests(FEATURES_QAC, 'qac', parsed_args)
    if parsed_args.test_type == 'coverity':
        run_tests(FEATURES_COVERITY, 'coverity', parsed_args)

    LOGGER.info(parsed_args)


if __name__ == '__main__':
    run()
