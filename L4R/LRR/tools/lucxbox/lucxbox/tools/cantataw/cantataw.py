""" Cantata wrapper """

import argparse
import json
import os
import subprocess
import sys

import jsonschema
from jsonschema.exceptions import SchemaError, ValidationError

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog, portal

LOGGER = lucxlog.get_logger()


def parse_args(arguments):
    desc = 'This script is a simple wrapper around the functionality of Cantata.'
    parser = argparse.ArgumentParser(description=desc)
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    parser.add_argument('config', help='Configuration file for Cantata project.')
    parser.add_argument('step', choices=['all', 'build', 'test', 'report'], help='Cantata step to perform.')
    return parser.parse_args(arguments)


def validate(configuration, schema):
    with open(schema) as schema_file:
        try:
            jsonschema.validate(configuration, json.load(schema_file))
        except ValidationError:
            LOGGER.error('Could not validate "%s" against schema "%s".', configuration, schema)
            sys.exit(1)
        except SchemaError:
            LOGGER.error('Could not validate "%s" against schema "%s". Invalid schema.', configuration, schema)
            sys.exit(1)


def environment_from_script(configuration, cwd):
    LOGGER.info('*** Cantata: set environment ***')
    LOGGER.debug('command=%s', configuration)
    LOGGER.debug('cwd=%s', cwd)

    separator = '&' if os.name == 'nt' else ';'
    environment_command = 'set' if os.name == 'nt' else 'env'

    script = _abs_path_command_arguments(configuration, cwd)[0]
    args = [script, '>', os.devnull, '2>&1', separator, environment_command]
    if os.name != 'nt':
        args.insert(0, '.')  # POSIX compliant version of bash's source builtin
    process = subprocess.Popen(args=' '.join(args), stdout=subprocess.PIPE, shell=True)
    stdout = process.communicate()[0]
    return dict([str(s) for s in line.decode('ascii').split('=', 1)] for line in stdout.splitlines())


def build(configuration_build, cwd, env):
    LOGGER.info('*** Cantata: build ***')
    LOGGER.debug('command=%s', configuration_build)
    LOGGER.debug('cwd=%s', cwd)
    LOGGER.debug('env=%s', env)

    command, arguments = _abs_path_command_arguments(configuration_build, cwd)
    _wrap_check_call(args=[command] + arguments, cwd=cwd, env=env)


def test(configuration_test, cwd, env):
    LOGGER.info('*** Cantata: test ***')
    LOGGER.debug('command=%s', configuration_test)
    LOGGER.debug('cwd=%s', cwd)
    LOGGER.debug('env=%s', env)

    command, arguments = _abs_path_command_arguments(configuration_test, cwd)
    _wrap_check_call(args=[command] + arguments, cwd=cwd, env=env)


def _wrap_check_call(args, cwd, env):
    try:
        subprocess.check_call(args=args, cwd=cwd, env=env, shell=True)
    except subprocess.CalledProcessError as exception:
        LOGGER.error('Could not call "%s"', args)
        sys.exit(exception.returncode)


def report(configuration_report, cwd, env):
    LOGGER.info('*** Cantata: report ***')
    LOGGER.debug('configuration=%s', configuration_report)
    LOGGER.debug('cwd=%s', cwd)
    LOGGER.debug('env=%s', env)
    args = ['cppgetcov',
            '--covFile:{}'.format(configuration_report['cov_file']),
            '--output:{}'.format(configuration_report['output']),
            '--type:{};'.format(';'.join(configuration_report['report_types']))]
    try:
        subprocess.check_call(args=args, cwd=cwd, env=env, shell=True)
    except subprocess.CalledProcessError as exception:
        LOGGER.error('Coverage errors encountered: "%s"', configuration_report['cov_file'])
        sys.exit(exception.returncode)


def _abs_path_command_arguments(command, cwd):
    command_arguments = command.split(' ')
    return os.path.join(cwd, command_arguments[0]), command_arguments[1:]


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = parse_args(argv[1:])
    LOGGER.setLevel(args.log_level)

    with open(args.config) as config_file:
        configuration = json.load(config_file)

    validate(configuration, os.path.join(os.path.dirname(__file__), 'schema/v0.1.json'))

    config_file_path = os.path.abspath(os.path.dirname(args.config))
    with portal.In(config_file_path):
        env = environment_from_script(configuration['env_script'], '.')

        if args.step == 'build' or args.step == 'all':
            build(configuration['build'], '.', env)
        if args.step == 'test' or args.step == 'all':
            test(configuration['test'], '.', env)
        if args.step == 'report' or args.step == 'all':
            report(configuration['report'], '.', env)


if __name__ == '__main__':
    main()
