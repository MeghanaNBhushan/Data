""" Wrapper for using different folders for ccache and clcache in build """

import argparse
import hashlib
import os
import subprocess
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxargs, lucxlog, finder, portal

MAX_OBJECT_PATH_LENGTH = 255
LOGGER = lucxlog.get_logger()


def parse_args(arguments):
    desc = "### Description: ###\n" + \
        "This script is intended to wrap build commands to change the CLACHE_PATH and CCACHE_DIR variable.\n" + \
        "This is needed if the build produces different variants or runs in different jenkins\n" + \
        "workspaces since compiler cache tools have bad hit rates when using the same cache for different builds.\n" + \
        "Therefore we are calculating a hash from the build command string and the workspace\n" + \
        "to produce a unique cache identifier for certain build variation."
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter,
                                     usage="%(prog)s [options] -- [build command]")
    parser.add_argument("--path", "-p", help="If this parameter is set the tool " +
                        "will use this path as root dir instead of CLACHE_PATH and CCACHE_DIR. Optional parameter.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--clcache", help="Path to clcache exe.")
    group.add_argument("--ccache", help="Path to ccache exe.")
    parser.add_argument("--ccachelog", help="Enable log generation for ccache.", action="store_true")
    parser.add_argument("--ccachedepend", help="Enable depend mode for ccache (necessary for GHS compiler).", action="store_true")
    parser.add_argument("--clcache-object-timeout", "-cot", dest='object_timeout', type=int, required=False,
                        help="Sets the environment variable 'CLCACHE_OBJECT_CACHE_TIMEOUT_MS' to the given value. Increases stability." +
                        " Default value is 10000 (ms).")
    parser.add_argument("--size", "-M", help="Change default size (in GB).")
    parser.add_argument("--stats", "-s", action="store_true", help="Clear the statistics at the " +
                        "beginning of a run and print them at the end.")
    parser.add_argument("--compress", "-c", required=False,
                        action="store_true", help="Use ccache compression")
    parser.add_argument("--root", "-r", required=False,
                        help="Root of the repository.")
    parser.add_argument("--skip-object-path-length-check", required=False, action="store_true",
                        help="Skip the check for max path length of object files (max. " + str(MAX_OBJECT_PATH_LENGTH) + " character)." +
                        " The background is that ccache is a mingw based tool. Internally ccache escapes '\\' which reduces the" +
                        " possible file path. If you disable this check you will run into 'FileNotFoundError'.")
    parser.add_argument("--basedir", required=False,
                        help="clcache: Has effect only when direct mode is on. Set this to path to root " +
                        " directory of your project. (ccache: no effect)")
    parser.add_argument("--hardlink", required=False, action="store_true",
                        help="clcache: If this variable is set, cached object files won't be copied to their final location." +
                        " Instead, hard links pointing to the cached object files will be created. (ccache: no effect)")
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    return parser.parse_args(arguments)


def get_build_cmd_hash(parameter):
    hash_object = hashlib.md5(parameter.encode("utf-8"))
    return hash_object.hexdigest()[:7]


def set_compiler_cache_env(args, build_args, env):
    if args.basedir:
        unique_build_cmd_id = get_build_cmd_hash("".join(build_args))
    else:
        unique_build_cmd_id = get_build_cmd_hash("".join(build_args) + os.getcwd())

    if args.path:
        base_compiler_cache_dir = args.path
    else:
        try:
            base_compiler_cache_dir = os.environ[env]
        except KeyError:
            LOGGER.error("Environment variable '%s' not set.", env)
            sys.exit(1)

    new_compiler_cache_dir = os.path.join(
        base_compiler_cache_dir, unique_build_cmd_id)

    os.environ[env] = new_compiler_cache_dir

    LOGGER.info("%s= %s", env, os.environ[env])

    if not os.path.exists(new_compiler_cache_dir):
        os.makedirs(new_compiler_cache_dir)


def setup_ccache(build_args, args):
    set_compiler_cache_env(args, build_args, "CCACHE_DIR")
    LOGGER.info("Performing cache cleanup")
    subprocess.check_call([args.ccache, "-c"])
    if args.size:
        subprocess.check_call([args.ccache, "-M", args.size])
    if args.stats:
        subprocess.check_call([args.ccache, "-z"])
    try:
        if args.ccachelog:
            subprocess.check_call([args.ccache, "-o", "log_file=" + os.environ["CCACHE_DIR"] + "/ccache.log"])
            LOGGER.info("log_file=%s/ccache.log", os.environ["CCACHE_DIR"])
        if args.ccachedepend:
            subprocess.check_call([args.ccache, "-o", "depend_mode=true"])
            LOGGER.info("Setting 'CCACHE_DEPEND=1' environment variable.")
    except subprocess.CalledProcessError as ccacheexception:
        if args.ccachelog:
            LOGGER.error("ERROR while running: %s -o log_file=%s/ccache.log", args.ccache, os.environ["CCACHE_DIR"])
        if args.ccachedepend:
            LOGGER.error("ERROR while running: %s -o depend_mode=true", args.ccache)
        LOGGER.error("\toutput = %s, error code = %s\n", ccacheexception.output, ccacheexception.returncode)

def setup_clcache(build_args, args):
    set_compiler_cache_env(args, build_args, "CLCACHE_DIR")
    if args.object_timeout:
        LOGGER.info("Setting '%s' to be '%s ms'",
                    "CLCACHE_OBJECT_CACHE_TIMEOUT_MS", str(args.object_timeout))
        os.environ["CLCACHE_OBJECT_CACHE_TIMEOUT_MS"] = str(
            args.object_timeout)
    LOGGER.info("Performing cache cleanup")
    subprocess.check_call([args.clcache, "-c"])
    if args.size:
        subprocess.check_call(
            [args.clcache, "-M", str(int(args.size) * 1024 * 1024 * 1024)])
    if args.stats:
        subprocess.check_call([args.clcache, "-z"])
    if args.hardlink:
        LOGGER.info("Setting '%s' to be '%s'",
                    "CLCACHE_HARDLINK", "true")
        os.environ["CLCACHE_HARDLINK"] = "1"
    if args.basedir:
        LOGGER.info("Setting '%s' to '%s'", "CLCACHE_BASEDIR", str(args.basedir))
        os.environ["CLCACHE_BASEDIR"] = args.basedir


def object_path_length_check(root=None):
    if not root:
        try:
            root = finder.get_git_root()
            LOGGER.debug("Git repo root: %s", root)
        except ValueError as exception:
            LOGGER.error(exception)
            LOGGER.error(
                "Can not determine repo root and '--root' was not given.")
            sys.exit(1)

    with portal.In(root):
        matches = finder.get_files_with_ending(endings=[".o", ".obj"])

        for match in matches:
            escaped_path = os.path.abspath(match)
            if len(escaped_path) > MAX_OBJECT_PATH_LENGTH:
                LOGGER.error("Object file path longer than '%d': '%s'",
                             MAX_OBJECT_PATH_LENGTH, escaped_path)
                LOGGER.error(
                    "This check can be disabled by '--skip-object-path-length-check'.")
                sys.exit(1)
            if len(escaped_path) > (MAX_OBJECT_PATH_LENGTH - 10):
                LOGGER.warning("Object file path near max length of '%d': '%s'",
                               MAX_OBJECT_PATH_LENGTH, escaped_path)
                LOGGER.warning(
                    "This check can be disabled by '--skip-object-path-length-check'.")


def build(args, build_args):
    if args.ccache:
        setup_ccache(build_args, args)

    if args.clcache:
        setup_clcache(build_args, args)

    if args.compress:
        LOGGER.debug(
            "Setting 'CCACHE_COMPRESS=1' environment variable. Compression used.")
        os.environ['CCACHE_COMPRESS'] = '1'

    try:
        subprocess.check_call(build_args, shell=True)
    except subprocess.CalledProcessError as exception:
        LOGGER.error("Exception occured: %s", str(exception))
        sys.exit(exception.returncode)

    if args.stats:
        LOGGER.info("compiler cache statistics:")
        if args.ccache:
            subprocess.check_call([args.ccache, "-s"])
        if args.clcache:
            subprocess.check_call([args.clcache, "-s"])


def main(argv=None):
    if argv is None:
        argv = sys.argv
    main_args, build_args = lucxargs.split_argv(argv)
    args = parse_args(main_args)
    LOGGER.setLevel(args.log_level)

    if args.size or args.stats:
        if not (args.clcache or args.ccache):
            LOGGER.error(
                "Parameter 'size' and 'stats' require either 'clcache' or 'ccache'.")
            sys.exit(1)

    if build_args is not None:
        LOGGER.debug("Build command might be given.")
        build(args, build_args)
    else:
        LOGGER.debug("No build command seen.")

    if not args.skip_object_path_length_check:
        object_path_length_check(args.root)


if __name__ == "__main__":
    main()
