#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import logging
from pkgutil import iter_modules

DEFAULT_TEMPLATE_DIR = os.path.expanduser(os.path.join('~', '.git-template'))
REGISTERED_HOOKS = ['pre-commit', 'commit-msg']

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
log_format = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(log_format)

LOG.addHandler(console_handler)


def pre_commit_executable():
    if shutil.which('pre-commit'):
        # using executable in PATH
        return shutil.which('pre-commit')

    if os.name == 'nt':  # windows only
        python_path, _ = os.path.split(sys.executable)
        pre_commit_path = os.path.join(python_path, 'scripts', 'pre-commit.exe')
        if os.path.isfile(pre_commit_path):
            return pre_commit_path
    return None


def check_tool_installation(try_installation=True):
    if pre_commit_executable():
        LOG.info("Tool installation looks good")
        return

    script_folder_message = "the 'scripts/' folder of your python " \
                            "installation is available in your system PATH.\n"\
                            "A restart of your machine might be required for the changes in PATH to take effect"

    # checking if python module 'pre-commit'is installed

    installed_modules = [name for _, name, _ in iter_modules()]
    if 'pre_commit' in installed_modules:  # the module-name ahs an underscore instead of an minus
        LOG.info("Python module 'pre-commit' is already installed")
        LOG.error("Executable for 'pre-commit' not available in PATH")
        LOG.info("Please make sure that %s", script_folder_message)
        sys.exit(1)

    if try_installation:
        try:
            LOG.info("Trying to install 'pre-commit' using pip")
            install_pre_commit()
            LOG.info("Installation of 'pre-commit' was successful")
            # re-run the installation check but skip the installation next time
            check_tool_installation(False)
            return
        except subprocess.CalledProcessError:
            LOG.warning("Automatic installation failed!")

    LOG.info("Please make sure that:")
    LOG.info("  - %s", script_folder_message)
    LOG.info("  - the python version you are using has the module 'pre-commit' installed")
    LOG.info("     - use python3 of your project from TCC in PATH (this includes the 'pre-commit' module)")
    LOG.info("     - install 'pre-commit' (e.g 'python -m pip install pre-commit')")


def install_pre_commit():
    command = [sys.executable, '-m', 'pip', 'install', 'pre-commit']
    try:
        subprocess.run(command, check=True, capture_output=True)
    except subprocess.CalledProcessError as error:
        # print the output to the log
        if error.stderr:
            LOG.warning("Running '%s' failed with:\n%s", ''.join(command), error.stderr.decode('ascii'))
        raise error  # re-throw the error


def initialize_template_directory(path=DEFAULT_TEMPLATE_DIR):
    if os.path.isdir(path) and os.listdir(path):
        LOG.warning("The directory for setting up the template '%s' is already in use.", os.path.expanduser(path))
        user_input = input("Do you want to remove the folder and all the content? (y/n)")
        if user_input.lower() not in ['y', 'yes']:
            LOG.error("User aborted while initializing the template directory")
            sys.exit(1)

        shutil.rmtree(path)

    command = [pre_commit_executable(), 'init-templatedir', path]
    for hook in REGISTERED_HOOKS:
        command.extend(['-t', hook])
    try:
        subprocess.run(command, check=True, capture_output=True)
        LOG.info("Successfully initialized the git-template directory in '%s'", os.path.expanduser(path))
    except subprocess.CalledProcessError as error:
        # print the output to the log
        if error.stderr:
            LOG.warning("Running '%s' failed with:\n%s", ''.join(command), error.stderr.expanduser('ascii'))
            sys.exit(1)
        LOG.error("Failed while initializing the template directory")


def register_template_in_gitconfig(path=DEFAULT_TEMPLATE_DIR):
    command = ['git', 'config', '--global', 'init.templateDir', os.path.expanduser(path)]
    try:
        subprocess.run(command, check=True, capture_output=True)
        LOG.info("Successfully added template directory '%s' in the .gitconfig", os.path.expanduser(path))
    except subprocess.CalledProcessError as error:
        # print the output to the log
        if error.stderr:
            LOG.warning("Running '%s' failed with:\n%s", ''.join(command), error.stderr.expanduser('ascii'))
            sys.exit(1)
        LOG.error("Failed while setting up the template in the global .gitconfig")


def try_apply_for_current_repo():
    # remove existing .git/hooks
    hooks_dir = os.path.join('.git', 'hooks')
    if not os.path.isdir('.git'):
        LOG.info("No '.git' folder found in '%s'", os.getcwd())
        LOG.info("You have to enable the enable the hooks for your local repo manually "
                 "(or re-run this script when the console path is at your repository root)")
        return

    for hook in REGISTERED_HOOKS:
        hook_file_path = os.path.join(hooks_dir, hook)
        if os.path.isfile(hook_file_path):
            backup_filepath = hook_file_path + ".old"
            if os.path.isfile(backup_filepath):
                os.remove(backup_filepath)
            LOG.info("Renaming existing hook in '%s' from '%s' to '%s'", os.getcwd(), hook_file_path, backup_filepath)
            os.rename(hook_file_path, backup_filepath)

    command = ['git', 'init']
    try:
        subprocess.run(command, check=True, capture_output=True)
        LOG.info("Successfully initialized repository in '%s' with the new hooks", os.getcwd())
    except subprocess.CalledProcessError as error:
        # print the output to the log
        if error.stderr:
            LOG.warning("Running '%s' failed with:\n%s", ''.join(command), error.stderr.expanduser('ascii'))
            return
        LOG.warning("Problem while initialized repository in '%s' with the new hooks", os.getcwd())


def print_info_message():
    message = "\n\nInstallation of pre-commit was successful!\n\n"
    message += "To enable pre-commit for all local repositories you have to:\n"
    message += "  1. delete the following files in '.git/hooks' (if existing)\n"
    for hook in REGISTERED_HOOKS:
        message += "     - %s\n", hook
    message += "  2. run 'git init' to add the new pre-commit hooks\n"
    message += "\n!!! This steps need to be done on every local repository separately !!!"
    LOG.info(message)


if __name__ in "__main__":
    check_tool_installation()
    initialize_template_directory()
    register_template_in_gitconfig()
    try_apply_for_current_repo()
    print_info_message()
