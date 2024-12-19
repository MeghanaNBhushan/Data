""" Script for test and release of lucxbox """

import argparse
import os
import platform
import shutil
import sys

import PyInstaller.__main__
import pytest
from setuptools.sandbox import run_setup

import lucxbox
from lucxbox.lib import lucxargs, lucxlog, finder, lucxutils, lucxpkgutil

PYTHON = sys.executable
PYLINT = [PYTHON, "-m", "pylint"]
COVERAGE = [PYTHON, "-m", "coverage"]
PYCODESTYLE = "pycodestyle"
PEP8 = "pep8"


def print_logo():
    logo = """   __        _____      ___
  / /  __ __/ ___/_ __ / _ )___ __ __
 / /__/ // / /__ \\ \\ // _  / _ \\\\ \\ /
/____/\\_,_/\\___//_\\_\\/____/\\___/_\\_\\
"""
    print(logo)


def parse_args():
    desc = "Script for test and release of lucxbox."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-a', '--all', action='store_true',
                        help="Run pylint and unittests.")
    parser.add_argument('-b', '--build', action='store_true',
                        help="Build executables using PyInstaller.")
    parser.add_argument('-l', '--lint', action='store_true', help="Run pylint.")
    parser.add_argument('-t', '--test', action='store_true',
                        help="Run unittests and generate a coverage report.")
    parser.add_argument('-r', '--readme', action='store_true',
                        help="Checks README files.")
    parser.add_argument('-c', '--clean', action='store_true',
                        help="Delete ./reports folder and all *.pyc files.")
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    return parser.parse_args()


def build():
    LOGGER.info("Building source distribution and wheel")
    run_setup("setup.py", ["clean", "sdist", "bdist_wheel"])

    LOGGER.info("Building executables using PyInstaller")
    specpath = "specs"
    if not os.path.exists(specpath):
        os.mkdir(specpath)
    for tool in lucxpkgutil.toolnames():
        if tool == 'template_script':
            continue
        LOGGER.info("Building executable for %s", tool)
        tool_script_path = os.path.join(lucxbox.tools.__path__[0], tool, tool + ".py")
        PyInstaller.__main__.run([
            "--onefile",
            "--specpath",
            specpath,
            tool_script_path,
        ])


def check_readme(tool):
    LOGGER.info("Checking README file for %s.", tool)

    cmd = [PYTHON, "-m", '.'.join([lucxbox.tools.__name__, tool, tool]), "-h"]
    out, err, returncode = lucxutils.execute(cmd)

    if returncode != 0:
        if err is not None:
            LOGGER.error(err)
        LOGGER.error("Checking README file failed for %s.", tool)
        sys.exit(returncode)

    folder = os.path.join(lucxbox.tools.__path__[0], tool)
    try:
        with open(os.path.join(folder, "README.md"), "r") as readme_file:
            content = readme_file.read()
            lines = out.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if line not in content:
                    LOGGER.error("Line '%s' not in README.md", line)
                    sys.exit(1)
                else:
                    LOGGER.debug("%s in README.md", line)
    except IOError:
        LOGGER.error("README.md not found")
        sys.exit(1)


def write_test_folder(file_name, content):
    with open(os.path.join(ROOT, "reports", file_name), "w") as out_file:
        out_file.write(content)


def coverage(folder):
    LOGGER.info("Check coverage for %s", folder)
    cmd = COVERAGE + ["report", "--include", folder + "/*"]
    out, err, returncode = lucxutils.execute(cmd)

    if returncode == 2:
        LOGGER.error("Code coverage too low for: %s\n%s", folder, out)
        sys.exit(returncode)
    elif returncode != 0:
        if out is not None:
            LOGGER.error("stdout:\n%s", out)
        if err is not None:
            LOGGER.error("stderr:\n%s", err)
        sys.exit(returncode)


def lint():
    shutil.rmtree("reports", ignore_errors=True)
    os.mkdir("reports")

    LOGGER.info("Running pylint (style check)")
    name = "pylint"
    matches = finder.get_files_with_ending(
        endings=[".py"], excludes=["/venv/", ".git"])

    cmd = PYLINT + ["--rcfile", ".pylintrc"]
    cmd.extend(matches)
    out, err, returncode = lucxutils.execute(cmd)

    if returncode != 0:
        if err is not None:
            LOGGER.error(err)
        LOGGER.error("%s findings:\n %s", name, out)
        LOGGER.error("%s failed. See reports/%s.txt", name, name)
        sys.exit(returncode)
    else:
        write_test_folder(name + "_report.txt", out)


def test(check_coverage=False):
    returncode = pytest.main(["--cov={}".format(lucxbox.__path__[0]), "--cov-report=html", "-m", "not system"])
    if returncode != 0:
        sys.exit(returncode)
    if check_coverage:
        lib_path = lucxbox.lib.__path__[0]
        tools_path = lucxbox.tools.__path__[0]
        coverage(lib_path)
        for tool in lucxpkgutil.toolnames():
            if "yaml_executor" in tool and platform.system() != "Windows":       # Windows only
                continue
            if "py_format_check" in tool:
                continue
            coverage(os.path.join(tools_path, tool))


def readme():
    LOGGER.info("Checking README files")
    for tool in lucxpkgutil.toolnames():
        check_readme(tool)


def clean():
    LOGGER.info("Cleaning up")
    shutil.rmtree("./build", ignore_errors=True)
    shutil.rmtree("./dist", ignore_errors=True)
    shutil.rmtree("./specs", ignore_errors=True)
    shutil.rmtree("./reports", ignore_errors=True)
    matches = finder.get_files_with_ending(endings=[".pyc"])
    for file_name in matches:
        os.remove(file_name)


def main():
    args = parse_args()
    print_logo()
    LOGGER.setLevel(args.log_level)
    if args.lint or args.all:
        lint()
    if args.test or args.all:
        test(check_coverage=True)
    if args.build:
        build()
    if args.readme:
        readme()
    if args.clean:
        clean()
    LOGGER.info("SUCCESS")


if __name__ == "__main__":
    LOGGER = lucxlog.get_logger()
    ROOT = os.path.dirname(os.path.realpath(__file__))
    sys.exit(main())
