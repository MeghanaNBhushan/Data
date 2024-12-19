#!/usr/bin/python

import argparse
import sys
import time
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog
from lucxbox.tools.tccw import tcc_config, tcc_wrapper

LOGGER = lucxlog.get_logger()


def parse_args(arguments):
    desc = "TCC wrapper script for a 'docker-like' tcc usage."
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter,
                                     usage="%(prog)s [options] -- [build command]")
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--config-file',
                       help="TCC wrapper configuration file")
    group.add_argument('-c', '--tcc-config', help="TCC xml configuration")
    group.add_argument('-cf', '--tcc-config-from-file',
                       help="Read TCC xml configuration from first line of specified file")
    group.add_argument('-l', '--local-config',
                       help="TCC xml configuration (local)")
    parser.add_argument('-s', '--no-install', action='store_true',
                        help="Skips the availability check (and installation) of tools in " +
                        "the TCC configuration (overwrites the config file)")
    parser.add_argument('--no-cache', action='store_true',
                        help="Skips using tcc cache.")
    parser.add_argument('--tries', '-t', default=1, type=int,
                        help='Number of retries for invoking TCC since TCC is not thread safe')
    parser.add_argument('--extend-path', '-e', nargs='+', help='Extends the PATH with given paths based on TCC_ environment variables.\n' +
                        'Example: Environment variable TCC_PYTHON3 -> --extend-path PYTHON3\n' +
                        'Example2: Environment variable TCC_GIT -> --extend-path GIT/bin.\n' +
                        'PATH will be extended on the front to assure that those entries are taken first!')
    parser.add_argument('--env-export', '-x', help='Exports all tcc variables into a seperate given file for further processing\n' +
                        'This will exit the script afterwards. It will extend the given file with ".env" when not given.\n' +
                        'It will also create a "sh.env" version of the file in the same directory')
    return parser.parse_args(arguments)


# pylint: disable=W0703
def get_env(config, no_install, no_cache, tries):
    while(tries > 0):
        try:
            return tcc_wrapper.run_tcc(config, no_install, no_cache)
        except tcc_wrapper.TccError as exception:
            tries = tries - 1
            LOGGER.error(
                "Getting TCC env failed. Have '%s' tries left. ('%s')", tries, exception)
            time.sleep(5)
        except IOError as exception:
            LOGGER.error("Getting TCC env failed. ('%s')", exception)
    LOGGER.error("Getting TCC env failed and no tries are left. Exiting")
    LOGGER.error(
        "Common problem is a missing home drive. Please check this first.")
    sys.exit(1)


def extend_env_path(env, extend_path):
    current_path = os.environ.get('PATH')
    for path_extend in extend_path:
        path_extend = os.path.normpath(path_extend)
        LOGGER.debug("Path extend request is %s", path_extend)
        env_var = 'TCC_' + path_extend.split(os.sep)[0]
        LOGGER.debug("Env var is %s", env_var)
        env_content = env.get(env_var)
        if len(path_extend.split(os.sep)) > 1:
            env_content += os.sep + os.sep.join(path_extend.split(os.sep)[1:])
        if env_var not in env:
            LOGGER.warning("Cannot add %s to path. Not existing", env_var)
            continue
        current_path = env_content + os.pathsep + current_path
        env.update({'PATH': current_path})
        LOGGER.debug("Updated env PATH with %s", env_content)
    return env


def main(argv=None):
    if argv is None:
        argv = sys.argv
    main_argv, build_argv = lucxargs.split_argv(argv)
    args = parse_args(main_argv)
    LOGGER.setLevel(args.log_level)
    tcc_wrapper.LOGGER.setLevel(args.log_level)
    tcc_config.LOGGER.setLevel(args.log_level)

    config = tcc_config.TccConfig()
    if args.config_file:
        config.set_by_file(args.config_file)
    elif args.tcc_config:
        config.set_by_value(args.tcc_config)
    elif args.tcc_config_from_file:
        try:
            with open(args.tcc_config_from_file, "r") as version_file:
                tcc_version = version_file.readline().strip()
            LOGGER.info("Using TCC configuration '%s'", tcc_version)
            config.set_by_value(tcc_version)
        except IOError:
            LOGGER.error("Failed reading file '%s'", args.tcc_config_from_file)
            sys.exit(1)
    else:
        config.set_local_file(args.local_config)

    execution_environment = get_env(config, args.no_install, args.no_cache, args.tries)
    if args.env_export:
        if not args.env_export.endswith('.env'):
            args.env_export = args.env_export + '.env'

        with open(args.env_export, 'w') as batch_env:
            for env_var, value in execution_environment.items():
                batch_env.write("{}={}\n".format(env_var, os.path.normpath(value)))

        sh_env = args.env_export.split('.env')[0] + '.sh.env'
        with open(sh_env, 'w') as sh_env_file:
            for env_var, value in execution_environment.items():
                unix_path = "/" + os.path.normpath(value)
                unix_path = unix_path.replace(':', '')
                unix_path = unix_path.replace('\\', '/')
                sh_env_file.write('{}="{}"\n'.format(env_var, unix_path))

        return
    if args.extend_path:
        execution_environment = extend_env_path(execution_environment, args.extend_path)
    tcc_wrapper.execute(build_argv, execution_environment)


if __name__ == "__main__":
    main()
