""" Wrapper script for testing the robustness of another tool """

import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog, lucxutils


def parse_args(arguments):
    desc = "Wrapper script for testing the robustness of another tool. Just pass a build command" + \
        " and run it over night and you get a statistic of the robustness of the tool. Output will be saved" + \
        " if an error occures."
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter,
                                     usage="%(prog)s [options] -- [build command]")
    parser.add_argument("-n", dest="max_runs", help="Max numbers of runs.")
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    return parser.parse_args(arguments)


def build(build_argv, count):
    out, err, returncode = lucxutils.execute(build_argv)
    if returncode != 0:
        out_file = open("dauerlaufw_" + str(count) + ".out", "w")
        out_file.write(str(out))
        err_file = open("dauerlaufw_" + str(count) + ".err", "w")
        err_file.write(str(err))
        return 1
    return 0


def print_stats(min_run, max_run, avg_run):
    LOGGER.info("min:%s max:%s avg:%s", str(
        min_run), str(max_run), str(avg_run))
    LOGGER.info("Output of runs written to dauerlaufw_[1,2,..].[err|out]")


def loop(build_argv, max_runs=None):
    LOGGER.info("Start running command in loop until it fails ...")
    LOGGER.debug("cmd: %s", str(build_argv))
    LOGGER.info("Press Ctrl+C to stop and get summary.")
    count = 0
    avg_run = 0
    min_run = 0
    max_run = 0
    try:
        while True:
            count = count + 1
            run = 0
            while True:
                run = run + 1
                LOGGER.debug("Current run %s", str(run))
                if build(build_argv, count):
                    LOGGER.info("Failed in run %s", str(run))
                    LOGGER.info("Starting again ...")
                    avg_run = avg_run + run
                    if run > max_run:
                        max_run = run
                    if run < min_run or min_run == 0:
                        min_run = run
                    break
                if max_runs and run >= int(max_runs):
                    break
            if max_runs:
                avg_run = avg_run / count
                print_stats(min_run, max_run, avg_run)
                break
    except KeyboardInterrupt:
        avg_run = avg_run / count
        print_stats(min_run, max_run, avg_run)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    main_argv, build_argv = lucxargs.split_argv(argv)
    args = parse_args(main_argv)
    LOGGER.setLevel(args.log_level)

    if build_argv:
        loop(build_argv, args.max_runs)


if __name__ == "__main__":
    LOGGER = lucxlog.get_logger()
    sys.exit(main())
