# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	noxfile.py
# ----------------------------------------------------------------------------
"""Configuration file for nox routines"""

from pathlib import Path as pathlib_Path
from os import path as os_path
from sys import exit

import nox

_PYTHON_VERSIONS = ['3.9', '3.8', '3.7']
_SWQ_MODULE_NAME = 'swq'
_TEST_MODULE_NAME = 'test'
_LOCATIONS = [_SWQ_MODULE_NAME, _TEST_MODULE_NAME]
_NOXFILE = pathlib_Path(__file__)
_HERE = _NOXFILE.parent
_SCA_MINI_DEMO_FOLDER = os_path.join(_HERE, '..', 'sca_mini_demo')
_REPORTS_FOLDER = os_path.join(_HERE, 'reports', 'behave')
_FEATURES_LIST = [
    'create_config', 'full_analysis', 'delta_analysis',
    'compile_commands_full_analysis'
]

# Pylint-exe conversion table for return codes (can be a combination of it)
# Pylint code 	Message 	            Final return code (pylint-exit)
# 1 	        Fatal message issued 	    1
# 2 	        Error message issued 	    0
# 4 	        Warning message issued 	    0
# 8 	        Refactor message issued	    0
# 16 	        Convention message issued   0
# 32 	        Usage error 	            1
_PYLINT_VALID_RETURN_CODES = range(2, 32)


def _run_lint_session(session, location):
    pylintrc_path = f'{location}/.pylintrc'
    with open(f'{location}/pylint.log', "w") as pylint_out:
        session.run('pylint',
                    '--output-format=parseable',
                    '--reports=no',
                    f'--rcfile={pylintrc_path}',
                    '--jobs=0',
                    location,
                    stdout=pylint_out,
                    success_codes=_PYLINT_VALID_RETURN_CODES)


def _check_if_path_exists_or_exit_if_not(path):
    if os_path.exists(path):
        return

    print(f'Check whether {path} exists')
    exit(1)


def _get_behave_command(tool, version, feature):
    return [
        'python', '-m', 'coverage', 'run', '--branch', '-p',
        'test/integration/run_behave_tests.py', tool, '--project_root',
        _SCA_MINI_DEMO_FOLDER, '--features', feature, '--version', version,
        '--reports_dir', _REPORTS_FOLDER
    ]


@nox.session(python=_PYTHON_VERSIONS)
def install_dev_dependencies(session):
    session.install('-r', 'requirements-dev.txt')


@nox.session(python=_PYTHON_VERSIONS)
def lint(session):
    """Runs linting commands"""
    session.install("pylint")
    for location in _LOCATIONS:
        _run_lint_session(session, location)


@nox.session(python=_PYTHON_VERSIONS)
def style(session):
    """Runs style-check commands"""
    session.install('pycodestyle')
    session.run('pycodestyle', f'{_HERE}')


@nox.session(python=_PYTHON_VERSIONS)
def format_code(session):
    """Runs formatter command"""
    session.install('yapf')
    session.run('yapf', '-r', '-i', f'{_SWQ_MODULE_NAME}')
    session.run('yapf', '-r', '-i', f'{_TEST_MODULE_NAME}')
    session.run('yapf', '-r', '-i', f'{_NOXFILE}')


@nox.session(python=_PYTHON_VERSIONS)
def unit_tests(session):
    """Runs unit tests command"""
    install_dev_dependencies(session)
    session.run('python', '-m', 'unittest')


@nox.session(python=_PYTHON_VERSIONS)
def qac_behave_tests(session):
    """Runs qac integration tests"""
    _check_if_path_exists_or_exit_if_not(_SCA_MINI_DEMO_FOLDER)
    install_dev_dependencies(session)
    for feature in _FEATURES_LIST:
        session.run(*_get_behave_command('qac', '2021.1', feature))


@nox.session(python=_PYTHON_VERSIONS)
def coverity_behave_tests(session):
    """Runs coverity integration tests"""
    _check_if_path_exists_or_exit_if_not(_SCA_MINI_DEMO_FOLDER)
    install_dev_dependencies(session)
    for feature in _FEATURES_LIST:
        session.run(*_get_behave_command('coverity', '2020.06', feature))
