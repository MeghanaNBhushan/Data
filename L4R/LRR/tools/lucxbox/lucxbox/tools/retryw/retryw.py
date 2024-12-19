#!/usr/bin/python
""" Retry wrapper script """

import argparse
import logging
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog, lucxutils

LOGGER = lucxlog.get_logger()


def parse_args(arguments):
    desc = "Wrapper to retry a command if it fails due to a known instability."
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter,
                                     usage="%(prog)s [options] -- [build command]")
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    parser.add_argument('-n', '--num-retries', default=1)
    parser.add_argument('-s', '--string', dest="strings", action='append', required=True,
                        help="If this string is found in the output a retry will be triggered. Can be given multiple times.")
    return parser.parse_args(arguments)


def log(level, out, err):
    if out is not None:
        LOGGER.log(level, "stdout:\n%s", out)
    if err is not None:
        LOGGER.log(level, "stderr:\n%s", err)


def retry_loop(build_argv, num_retries, strings):
    counter = 0
    while counter < num_retries + 1:
        counter += 1
        out, err, returncode = lucxutils.execute(build_argv)
        if returncode != 0:
            hit = False
            for string in strings:
                if string in out or string in err:
                    if counter == num_retries + 1:
                        LOGGER.error(
                            "Found known issue in output in retry '%s', stopping retry wrapper.", str(num_retries))
                        log(logging.ERROR, out, err)
                        return returncode
                    else:
                        LOGGER.info(
                            "Found known issue in output, starting retry...")
                        log(logging.DEBUG, out, err)
                        hit = True
            if hit is False:
                LOGGER.error(
                    "Unkown error seen, stopping retry wrapper.")
                log(logging.ERROR, out, err)
                return returncode
        else:
            print(out)
            LOGGER.info("SUCCESS")
            return returncode


def main(argv=None):
    if argv is None:
        argv = sys.argv
    main_argv, build_argv = lucxargs.split_argv(argv)
    args = parse_args(main_argv)
    LOGGER.setLevel(args.log_level)

    LOGGER.info("Starting retryw with num_retries='%s' and strings='%s'",
                args.num_retries, args.strings)
    return retry_loop(build_argv, args.num_retries, args.strings)


if __name__ == "__main__":
    sys.exit(main())
