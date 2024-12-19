# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	output_producer.py
# ----------------------------------------------------------------------------
"""Defines output producer for the scripts"""
from os import path
from swq.common.logger import LOGGER
from swq.common.filesystem.filesystem_utils import open_t


def create_output_producer(config):
    """Creates an output producer, depending on the \
    parsed command line arguments.

    If to_stdout is True, the created function will print \
    the output to stdout.
    Otherwise, it will append the filter report output file \
    file with aggregated summary.

    :return: A function which takes a dict, and writes them \
    to the defined output.
    """
    def output_producer_to_stdout(data):
        LOGGER.info('=' * 25 + ' Warnings Summary ' + '=' * 25)
        for key, value in sorted(data.items()):
            LOGGER.info('{}: {}'.format(key, value))

    def output_producer_to_file(data):
        output_file_path = path.join(config.project_root,
                                     config.filter_report_output_file)
        with open_t(output_file_path, mode='w') as output_file:
            output_file.writelines([
                '{}: {}\n'.format(key, value)
                for key, value in sorted(data.items(), reverse=True)
            ])

        LOGGER.info('Aggregated summary have been written to file %s',
                    output_file_path)

    if config.filter_report_output_file:
        return output_producer_to_file

    return output_producer_to_stdout
