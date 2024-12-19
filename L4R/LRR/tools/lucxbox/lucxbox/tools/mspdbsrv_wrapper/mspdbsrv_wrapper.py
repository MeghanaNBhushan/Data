""" Wrapper script to fix MSBuild jenkins issues """

# Wrapper code from: http://blog.peter-b.co.uk/2017/02/stop-mspdbsrv-from-breaking-ci-build.html
#
# mspdbsrv is the service used by Visual Studio to collect debug
# data during compilation.  One instance is shared by all C++
# compiler instances and threads.  It poses a unique challenge in
# several ways:
#
# - If not running when the build job starts, the build job will
#   automatically spawn it as soon as it needs to emit debug symbols.
#   There"s no way to prevent this from happening.
#
# - The build job _doesn"t_ automatically clean it up when it finishes
#
# - By default, mspdbsrv inherits its parent process" file handles,
#   including (unfortunately) some log handles owned by Buildbot.  This
#   can prevent Buildbot from detecting that the compile job is finished
#
# - If a compile job starts and detects an instance of mspdbsrv already
#   running, by default it will reuse it.  So, if you have a compile
#   job A running, and start a second job B, job B will use job A"s
#   instance of mspdbsrv.  If you kill mspdbsrv when job A finishes,
#   job B will die horribly.  To make matters worse, the version of
#   mspdbsrv should match the version of Visual Studio being used.
#
# This class works around these problems:
#
# - It sets the _MSPDBSRV_ENDPOINT_ to a value that"s probably unique to
#   the build, to prevent other builds on the same machine from sharing
#   the same mspdbsrv endpoint
#
# - It launches mspdbsrv with _all_ file handles closed, so that it
#   can"t block the build from being detected as finished.
#
# - It explicitly kills mspdbsrv after the build job has finished.
#
# - It wraps all of this into a context manager, so mspdbsrv gets killed
#   even if a Python exception causes a non-local exit.

import argparse
import os
import subprocess
import sys
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog


class UniqueMspdbsrv:
    def __init__(self, msv_version):
        self.proc = None
        if msv_version == 14:
            self.__mspdbsrv_exe = "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\bin\\mspdbsrv.exe"
        elif msv_version == 10:
            self.__mspdbsrv_exe = "C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\Common7\\IDE\\mspdbsrv.exe"

    def __enter__(self):
        os.environ["_MSPDBSRV_ENDPOINT_"] = str(uuid.uuid4())
        args = [self.__mspdbsrv_exe, "-start", "-shutdowntime", "-1"]
        LOGGER.info(" ".join(args))
        try:
            self.proc = subprocess.Popen(args, cwd='\\', close_fds=True)
        except OSError as exception:
            LOGGER.error("Exception occured: %s", str(exception))
            sys.exit(1)
        return self

    def __exit__(self, type_in, value, traceback):
        if self.proc is not None:
            self.proc.terminate()
        return False


def parse_args(arguments):
    desc = "Wrapper for MSBuild based jenkins jobs. Details why this is needed can be found here:\n" + \
           "http://blog.peter-b.co.uk/2017/02/stop-mspdbsrv-from-breaking-ci-build.html"
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter,
                                     usage="%(prog)s [options] -- [build command]")
    parser.add_argument("-v", "--msv_version", type=str, help="MSVC version",
                        choices=['10', '14'], required=True)
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    return parser.parse_args(arguments)


def execute_command(f_cmd):
    try:
        sys.stdout.flush()
        subprocess.check_call(f_cmd, shell=True)
        sys.stdout.flush()
    except subprocess.CalledProcessError as exception:
        LOGGER.error("Exception occured: %s", str(exception))
        sys.exit(exception.returncode)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    main_argv, build_argv = lucxargs.split_argv(argv)
    args = parse_args(main_argv)
    LOGGER.setLevel(args.log_level)

    if build_argv:
        with UniqueMspdbsrv(int(args.msv_version)):
            execute_command(build_argv)


if __name__ == "__main__":
    LOGGER = lucxlog.get_logger()
    sys.exit(main())
