# pylint: disable=C0103,E1120,W0613
import os
import json
import argparse
import unittest.mock
from collections import Counter
import jsonschema
import pytest

import lucxbox.tools.compiler_delta_check.compiler_delta_check as compiler_delta_check


@pytest.fixture
def warnings_json():
    file_path = os.path.join(os.path.dirname(__file__), 'warnings.json')
    with open(file_path, 'r') as warnings:
        warnings_json = json.loads(warnings.read())
    return warnings_json


@pytest.fixture
def clwarnings(warnings_json):
    return compiler_delta_check.CLWarnings(warnings_json)


@pytest.fixture
def mock_settings_env_vars():
    with unittest.mock.patch.dict(os.environ, {'LUCX_PULL_REQUEST': '1234', 'BUILD_NUMBER': '321'}):
        yield


@pytest.fixture
def argparse_required_args():
    return argparse.Namespace(build_number=321,
                              build_variant='TEST_ASIL_develop',
                              changed_files='CHANGED_FILES',
                              prid=1234,
                              warnings_baseline_file='warnings.json',
                              warnings_file='warnings.json',
                              )


@pytest.fixture
def argparse_args(monkeypatch):
    return argparse.Namespace(build_number=321,
                              build_variant='TEST_ASIL_develop',
                              changed_files='CHANGED_FILES',
                              debug=True,
                              ignore_type=['193-D'],
                              prid=1234,
                              threshold_file=None,
                              warnings_baseline_file='warnings.json',
                              warnings_file='warnings.json',
                              output_html='compiler_report.html',
                              output_json='compiler_report.json',
                              summary_json='compiler_summary.json',
                              target_branch='develop',
                              source_branch='@',
                              )


@pytest.mark.parametrize('string, expected', [('', ''),
                                              (r'L:\some\dir', r'some\dir'),
                                              (r'some\relative\dir', r'some\relative\dir')
                                              ])
def test_strip_drive_letter(string, expected):
    assert compiler_delta_check.strip_drive(string) == expected


def test_create_clwarning(warnings_json):
    for warning in warnings_json:
        assert compiler_delta_check.CLWarning(warning)


def test_create_clwarning_exception():
    with pytest.raises(TypeError):
        compiler_delta_check.CLWarning()


@pytest.mark.parametrize('key, value', [('row', 9999),
                                        ('teams', []),
                                        ('domain', 'unknown'),
                                        ('column', 9999)
                                        ])
def test_clwarning_equality(warnings_json, key, value):
    warning1 = warnings_json[0]
    warning2 = warnings_json[0].copy()
    warning2.update({key: value})
    assert compiler_delta_check.CLWarning(warning1) == compiler_delta_check.CLWarning(warning2)
    assert compiler_delta_check.CLWarning(warning1) != 0


@pytest.mark.parametrize('key, value', [('file_path', 'test_file.hpp'),
                                        ('components', ['test_component']),
                                        ('severity', 'test_severity'),
                                        ('type_name', 'test_type'),
                                        ('message', 'test_message')
                                        ])
def test_clwarning_unequality(warnings_json, key, value):
    warning1 = warnings_json[0]
    warning2 = warnings_json[0].copy()
    warning2.update({key: value})
    assert compiler_delta_check.CLWarning(warning1) != compiler_delta_check.CLWarning(warning2)


def test_create_clwarnings(warnings_json):
    assert isinstance(compiler_delta_check.CLWarnings(), Counter)
    assert isinstance(compiler_delta_check.CLWarnings(), compiler_delta_check.CLWarnings)
    assert compiler_delta_check.CLWarnings(warnings_json)


def test_clwarnings_filter_by_domain(clwarnings):
    assert isinstance(clwarnings.filter_by_domain(''), compiler_delta_check.CLWarnings)
    assert len(clwarnings.filter_by_domain('linker')) == 2
    assert len(clwarnings.filter_by_domain('compiler')) == 2


def test_clwarnings_filter_by_types(clwarnings):
    result = clwarnings.filter_by_types(['193-D', '270'])
    assert isinstance(result, compiler_delta_check.CLWarnings)
    assert len(result) == 2


def test_clwarnings_filter_by_component(clwarnings):
    assert isinstance(clwarnings.filter_by_component('IP_IF'), compiler_delta_check.CLWarnings)
    assert len(clwarnings.filter_by_component('IP_IF')) == 1


def test_clwarnings_get_warnings_per_component(clwarnings):
    result = clwarnings.get_warnings_per_component()
    assert isinstance(result, Counter)
    assert dict(result) == {'IP_IF': 2572, 'FSICOM': 30}


def test_clwarnings_filter_with_changed_files(clwarnings):
    result = clwarnings.filter_with_changed_files(
        ['ip_if\\rba\\CUBAS\\BswLib\\rba_BswSrv\\api\\rba_BswSrv.h',
         'C:\\JT\\ws\\commonrepo@1\\repo\\ip_if\\uC_fwBg\\core\\rbHwCfgCheck\\src\\rbHwCfgCheck_Init.c'])
    assert isinstance(result, compiler_delta_check.CLWarnings)
    assert len(result) == 2


def test_clwarnings_apply_renames(warnings_json):
    orig_warnings = compiler_delta_check.CLWarnings(warnings_json)
    clwarnings = compiler_delta_check.CLWarnings(warnings_json)
    filenames = [warning.file_path for warning in clwarnings.keys()]
    renames = [(filename, str(idx)) for idx, filename in enumerate(filenames)]
    result = clwarnings.apply_renames(renames)
    for warning, orig_warning, rename in zip(result.keys(), orig_warnings.keys(), renames):
        assert warning.file_path == rename[1] and orig_warning.file_path == rename[0]


def test_clwarnings_subtraction(clwarnings, warnings_json):
    warnings_a = clwarnings
    warnings_json[0]['quantity'] -= 10
    warnings_json[3]['quantity'] -= 1
    warnings_b = compiler_delta_check.CLWarnings(warnings_json)
    assert sum((warnings_a - warnings_a).values()) == 0
    assert sum((warnings_b - warnings_a).values()) == 0
    assert sum((warnings_b - warnings_b).values()) == 0
    assert sum((warnings_a - warnings_b).values()) == 11


def test_compilerWarningsDeltaCheck_build_number_not_provided(argparse_args, mock_settings_env_vars, monkeypatch):
    monkeypatch.delenv('BUILD_NUMBER')
    argparse_args.prid = None
    argparse_args.build_number = None
    with pytest.raises(ValueError):
        compiler_delta_check.CompilerWarningsDeltaCheck(argparse_args)


def test_compilerWarningsDeltaCheck_lucx_pull_request_not_provided(argparse_args, mock_settings_env_vars, monkeypatch):
    monkeypatch.delenv('LUCX_PULL_REQUEST')
    argparse_args.prid = None
    argparse_args.build_number = None
    with pytest.raises(ValueError):
        compiler_delta_check.CompilerWarningsDeltaCheck(argparse_args)


def test_get_warnings(warnings_json):
    file_name = os.path.join(os.path.dirname(__file__), 'warnings.json')
    warnings = compiler_delta_check.get_warnings(file_name)
    assert warnings == warnings_json


def test_get_warnings_non_existing_file():
    with pytest.raises(IOError):
        compiler_delta_check.get_warnings('non-existent-file.json')


def test_parse_args(monkeypatch, argparse_required_args):
    """ Check argument parser with required arguments
    """
    args: list = list()
    for key, value in argparse_required_args.__dict__.items():
        args.append(f'--{key.replace("_", "-")}={value}')
    monkeypatch.setattr('sys.argv', ['pytest'] + args)
    parsed_args = compiler_delta_check.parse_args()
    for arg in argparse_required_args.__dict__.keys():
        assert parsed_args.__getattribute__(arg) == argparse_required_args.__getattribute__(arg)


@pytest.mark.parametrize('path, result', [('.', True),
                                          ('/', False),
                                          ])
def test_is_git_repo(path, result):
    assert compiler_delta_check.is_git_repo(path) is result


### Track renaming of the files
@unittest.mock.patch('lucxbox.tools.compiler_delta_check.compiler_delta_check.is_git_repo', lambda: False)
def test_git_renames_not_in_repo():
    """ Should return empty list if not in git repo
    """
    assert len(compiler_delta_check.get_git_renames('develop', '@')) == 0


class MockGitDiffCommand:
    """ Mock object for get_git_rename tests
    """
    stdout = None
    stderr = None
    returncode = None

    @staticmethod
    def return_renames(*args, **kwargs):
        mock_result = MockGitDiffCommand()
        mock_result.stdout = b''' rename somedir/file.txt => dir1/dir2/dir3/file1 (100%)
 create mode 100644 dir1/rootfile.csv
 create mode 100644 new_file.txt
 rename testdir/{file.txt.old => file.txt} (100%)
 rename testdir1/somefile.txt => testdir1-renamed/somefile-renamed.txt (100%)'''
        mock_result.stderr = b''
        mock_result.returncode = 0
        return mock_result

    @staticmethod
    def return_no_renames(*args, **kwargs):
        mock_result = MockGitDiffCommand()
        mock_result.stdout = b''
        mock_result.returncode = 0
        return mock_result

    @staticmethod
    def return_bad_errorcode(*args, **kwargs):
        mock_result = MockGitDiffCommand()
        mock_result.stderr = b'Git error message'
        mock_result.returncode = 128
        return mock_result


@unittest.mock.patch('lucxbox.tools.compiler_delta_check.compiler_delta_check.is_git_repo', lambda: True)
@unittest.mock.patch('subprocess.run', MockGitDiffCommand.return_renames)
def test_get_git_renames():
    renames = compiler_delta_check.get_git_renames('develop', '@')
    assert isinstance(renames, list)
    assert renames == [('somedir/file.txt', 'dir1/dir2/dir3/file1'),
                       ('testdir/file.txt.old', 'testdir/file.txt'),
                       ('testdir1/somefile.txt', 'testdir1-renamed/somefile-renamed.txt')]


@unittest.mock.patch('lucxbox.tools.compiler_delta_check.compiler_delta_check.is_git_repo', lambda: True)
@unittest.mock.patch('subprocess.run', MockGitDiffCommand.return_no_renames)
def test_get_git_renames_empty():
    renames = compiler_delta_check.get_git_renames('develop', '@')
    assert isinstance(renames, list)
    assert len(renames) == 0


@unittest.mock.patch('lucxbox.tools.compiler_delta_check.compiler_delta_check.is_git_repo', lambda: True)
@unittest.mock.patch('subprocess.run', MockGitDiffCommand.return_bad_errorcode)
def test_get_git_renames_error():
    renames = compiler_delta_check.get_git_renames('develop', '@')
    assert isinstance(renames, list)
    assert len(renames) == 0


@pytest.fixture
def sample_json_schema():
    return '''{
      "$schema": "http://json-schema.org/draft-04/schema#",
      "title": "Test schema",
      "type": "object",
      "properties": {
        "test": {
          "type": "integer"
        }
      },
      "required": [
        "test"
      ]
    }'''


def test_validate_json_success(sample_json_schema):
    json_data = json.loads('{"test" : 1}')
    mock_open = unittest.mock.mock_open(read_data=sample_json_schema)
    with unittest.mock.patch('builtins.open', mock_open):
        assert compiler_delta_check.validate_json('schema.json', json_data) is None


def test_validate_json_failure(sample_json_schema):
    json_data = json.loads('{"test" : "wrong"}')
    mock_open = unittest.mock.mock_open(read_data=sample_json_schema)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        with unittest.mock.patch('builtins.open', mock_open):
            compiler_delta_check.validate_json('schema.json', json_data)
