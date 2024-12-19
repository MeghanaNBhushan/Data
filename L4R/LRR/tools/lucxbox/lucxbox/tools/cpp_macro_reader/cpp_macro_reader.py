""" Functions regarding reading sysconfig header files. """

import argparse
import os
import re
import shutil
import sys
import tempfile
from string import Template

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog, lucxutils, portal

LOGGER = lucxlog.get_logger()

TEMP_FILE_NAME = "cpp_macro_reader_temp"
MAIN = """
#include <iostream>
#include <string>
#define STR(x) std::cout << #x"=" << static_cast<unsigned>(x) << std::endl

$define

int main()
{
    $main
}
"""


def parse_args():
    desc = "This tool searches for macros and calculates the value with the given compiler. " + \
           "It will return a list of key value pairs. " + \
           "Currently only macros containing calculations like '+' and '-' are considered."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-f', '--file', required=True,
                        help="Path to sysconfig file")
    parser.add_argument('-c', '--compiler', required=True,
                        help="Path to compiler")
    parser.add_argument('-l', '--list', action="store_true",
                        help="List addresses")
    parser.add_argument('-o', '--output',
                        help="Write addresses to csv file")
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    return parser.parse_args()


def write_main(macros, file_name):
    main_string = ""
    define_string = ""
    for macro in macros:
        main_string = main_string + "STR(" + macro + "); "
        define_string = define_string + "#define " + \
            macro + " " + macros[macro] + "\n"

    template_string = Template(MAIN)
    main_content = template_string.substitute(
        header_file=file_name, main=main_string, define=define_string)

    with open(TEMP_FILE_NAME + ".c", "w") as temp_file:
        temp_file.write(main_content)


def get_main_output(compiler):
    out, err, returncode = lucxutils.execute([compiler, "-o", TEMP_FILE_NAME,
                                              "-static-libgcc", "-static-libstdc++", "-xc++", TEMP_FILE_NAME + ".c"])
    if returncode != 0:
        if out is not None:
            LOGGER.error("stdout:\n%s", out)
        if err is not None:
            LOGGER.error("stderr:\n%s", err)
        sys.exit(returncode)

    out, err, returncode = lucxutils.execute(
        [os.path.join(".", TEMP_FILE_NAME)])
    if returncode != 0:
        if out is not None:
            LOGGER.error("stdout:\n%s", out)
        if err is not None:
            LOGGER.error("stderr:\n%s", err)
        sys.exit(returncode)

    return out


def get_macros(file_name, compiler):
    """ Function to get a map of macros read from a cpp source file.
        Also tries to resolve dependencies, e.g.:
        #define ONE       0x1 // 1
        #define TWO       (ONE + ONE)
        will return: {'ONE': 0x1, 'TWO': 0x2}

        Please see unittest for expected behavior and covered functionality.
    """
    macros = {}

    with open(file_name, 'r') as sys_file:
        lines = sys_file.readlines()
        for line in lines:
            match = re.match(
                r"^\s*#define\s+(\w+)\s+([\w\s\)\(+-]+?)\s*(?:\/\/.*)?$", line)
            if match:
                macros[match.group(1)] = match.group(2)

    tmpdir = tempfile.mkdtemp()
    try:
        with portal.In(tmpdir):
            write_main(macros, file_name)

            out = get_main_output(compiler)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    for line in out.split("\n"):
        if line.strip():
            macro, value = line.split("=")
            macro, value = macro.strip(), int(value.strip())
            if value > (2**32 - 1):
                raise ValueError("Max. value exceeded for " + macro)
            if value < 0:
                raise ValueError("Negative value for " + macro)
            macros[macro] = '0x%08X' % value

    return macros


def main():
    args = parse_args()
    LOGGER.setLevel(args.log_level)

    macros = get_macros(os.path.abspath(args.file), args.compiler)
    max_len = max(len(macro) for macro in macros)
    if args.list:
        for macro in sorted(macros.keys()):
            print(macro.ljust(max_len + 2) + macros[macro])
    if args.output:
        with open(args.output, 'w') as out_file:
            out_file.write("name, value\n")
            for macro in sorted(macros.keys()):
                out_file.write(macro + ", " + macros[macro] + "\n")


if __name__ == "__main__":
    sys.exit(main())
