#!/usr/bin/python
""" coverityw scripts """

import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog
from lucxbox.tools.coverityw.parameters import Parameters
from lucxbox.tools.coverityw.process import run_command
from lucxbox.tools.coverityw.tcc_processor import TccProcessor

LOGGER = lucxlog.get_logger()


class Coverity:
    """Coverity configuration simple wrapper"""

    def __init__(self, coverity_configuration, compiler_configuration):
        self.coverity_configuration = coverity_configuration
        self.compiler_configuration = compiler_configuration

    def configure(self):
        LOGGER.info('Coverity configure')

        for configuration in self.compiler_configuration.configs:
            LOGGER.info('Running configuration: %s', configuration)

            command = os.path.join(
                self.coverity_configuration.dir, 'cov-configure')
            command += ' ' + \
                configuration.replace(
                    '{COMPILER}', self.compiler_configuration.path)
            run_command(command)

    def build(self):
        LOGGER.info('Coverity build')

        command = os.path.join(self.coverity_configuration.dir, 'cov-build')
        command += ' --dir "{}"'.format(self.coverity_configuration.output_dir)
        command += ' ' + self.compiler_configuration.build_args
        command += ' ' + self.compiler_configuration.build_command.replace(
            '{COMPILER}', self.compiler_configuration.path)
        run_command(command)

    def filter(self):

        if self.coverity_configuration.filter:
            LOGGER.info('Filtering files')

            if LOGGER.isEnabledFor('DEBUG'):
                LOGGER.info('Files used before applying filters')
                self.emit('list')

            for filter_item in self.coverity_configuration.filter:
                LOGGER.info('Applying filter: %s', filter_item)
                emit_args = '--tu-pattern'
                emit_args += ' "file(\'{pattern}\')"'.format(pattern=filter_item)
                emit_args += ' delete'
                self.emit(emit_args)

            if LOGGER.isEnabledFor('DEBUG'):
                LOGGER.info('Files used after applying filters')
                self.emit('list')

    def emit(self, args):
        LOGGER.info('Coverity build')

        command = os.path.join(
            self.coverity_configuration.dir, 'cov-manage-emit')
        command += ' --dir "{}"'.format(self.coverity_configuration.output_dir)
        command += ' ' + args
        run_command(command, exit_on_error=False)

    def analyze(self):
        LOGGER.info('Coverity analyze')

        command = os.path.join(self.coverity_configuration.dir, 'cov-analyze')
        command += ' --dir "{}"'.format(self.coverity_configuration.output_dir)
        command += ' ' + self.coverity_configuration.analyze_options
        run_command(command)

    def commit(self, user_name, user_password):
        LOGGER.info('Coverity commit defects')

        command = os.path.join(
            self.coverity_configuration.dir, 'cov-commit-defects')
        command += ' --dir "{}"'.format(self.coverity_configuration.output_dir)
        command += ' --host "{}"'.format(self.coverity_configuration.host)
        command += ' --port "{}"'.format(self.coverity_configuration.port)
        command += ' --stream "{}"'.format(self.coverity_configuration.stream)
        command += ' --user "{}"'.format(user_name)
        command += ' --password "{}"'.format(user_password)
        run_command(command, remove_password=user_password)


def parse_args():
    desc = 'Coverity configuration wrapper.'
    parser = argparse.ArgumentParser(description=desc)
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    step_choices = ['all', 'configure', 'build', 'filter', 'analyze', 'commit']
    parser.add_argument('-s', '--step', choices=step_choices,
                        default='all', type=str, help='Coverity step to run')
    parser.add_argument('-c', '--config-file', required=True,
                        type=str, help='Coverity configuration file')
    parser.add_argument('-o', '--output-dir', required=True, type=str,
                        help='Temporary directory for outputing coverity files')
    parser.add_argument('-b', '--build-cmd', required=True,
                        type=str, help='Build command used to build the project')
    parser.add_argument('-u', '--user', default=None, type=str,
                        help='User id that can publish to coverity server')
    parser.add_argument('-p', '--password', default=None, type=str,
                        help='User password that can publish to coverity server')
    return parser.parse_args()


def main():
    args = parse_args()
    LOGGER.setLevel(args.log_level)

    parameters = Parameters(args.config_file, args.output_dir,
                            args.build_cmd, args.user, args.password)

    # tcc integration
    if parameters.tcc_configuration.use_tcc:
        tcc_processor = TccProcessor(parameters.tcc_configuration)
        # get coverity path on windows/linux
        coverity_dir = tcc_processor.check_tool_dir('coverity')
        parameters.coverity_configuration.dir = os.path.join(
            coverity_dir, 'bin')
        # mount compiler path on windows/linux
        compiler_dir = tcc_processor.check_tool_dir(
            tcc_processor.tcc_configuration.compiler_tool_name)
        parameters.compiler_configuration.path = os.path.join(
            compiler_dir, parameters.tcc_configuration.compiler_relative_path)

    coverity = Coverity(parameters.coverity_configuration,
                        parameters.compiler_configuration)

    if args.step == 'all' or args.step == 'configure':
        coverity.configure()
    if args.step == 'all' or args.step == 'build':
        coverity.build()
    if args.step == 'all' or args.step == 'filter':
        coverity.filter()
    if args.step == 'all' or args.step == 'analyze':
        coverity.analyze()
    if args.step == 'all' or args.step == 'all':
        coverity.commit(parameters.user_name, parameters.user_password)


if __name__ == '__main__':
    main()
