# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2020 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
# Filename: 	run_tests.py
# Author(s): 	Andre Silva (CC-AD/ESW4)
# ----------------------------------------------------------------------------
"""Entrypoint script to run test suites"""
import argparse
import sys
import unittest

import test.all_tests
import xmlrunner
import integration_test.all_tests


def __create_test_suites(args):
    test_suites = []

    test_suite_unit = test.all_tests.create_test_suite()
    test_suite_integration = integration_test.all_tests.create_test_suite()

    if 'unit' in args.test or 'all' in args.test:
        print('[RUN_TESTS] Adding unit tests...')
        test_suites.append(test_suite_unit)
    if 'int' in args.test or 'all' in args.test:
        print('[RUN_TESTS] Adding integration tests...')
        test_suites.append(test_suite_integration)

    return test_suites


def __create_runner(args):
    if args.generate_reports:
        test_runner = xmlrunner.XMLTestRunner(output=args.output_directory)
    else:
        test_runner = unittest.TextTestRunner()

    return test_runner


def __run_tests(runner, suites):
    result = []
    for suite in suites:
        result.append(runner.run(suite).wasSuccessful())
    return False in result


def run_tests(args):
    """Creates test suites and runs unit tests"""
    return_code = 0
    test_suites = __create_test_suites(args)

    if len(test_suites) > 0:
        print('[RUN_TESTS] Running tests...')
        test_runner = __create_runner(args)
        return_code = __run_tests(test_runner, test_suites)
        print('[RUN_TESTS] Done.')
    else:
        print('[RUN_TESTS] Nothing to run. Exiting...')
    return return_code


def create_argument_parser():
    """Creates CLI argument parser"""
    parser = argparse.ArgumentParser(
        description='Test runner for SCA Tools Package.'
                    ' Runs unit and integration tests by default.')

    parser.add_argument('-o',
                        '--output_directory',
                        default='test_results',
                        help='Directory to save test reports')

    parser.add_argument('-gr',
                        '--generate_reports',
                        action='store_true',
                        help='Generage XML reports')

    parser.add_argument('-t',
                        '--test',
                        nargs='+',
                        choices=['unit', 'int', 'all'],
                        default=['all'],
                        help='Run specified tests')

    return parser


argparser = create_argument_parser()
parsed_args = argparser.parse_args()
sys.exit(run_tests(parsed_args))
