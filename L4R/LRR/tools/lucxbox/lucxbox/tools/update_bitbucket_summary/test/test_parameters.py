import argparse
import pytest

import lucxbox.tools.update_bitbucket_summary.update_bitbucket_summary as update_bitbucket_summary


@pytest.mark.parametrize('test_input,expected', [
    (1, 1),
    (7, 7),
    (0, None),
    (-1, None),
])
def test_type_check_positive_int(test_input, expected):
    assert update_bitbucket_summary.positive_int(test_input) is expected


@pytest.mark.parametrize('test_input,expected', [
    ('', None),
    ('test', 'test'),
])
def test_type_check_nonempty_str(test_input, expected):
    assert update_bitbucket_summary.nonempty_str(test_input) is expected


def test_init_args_from_summary(mocker):
    mocker.patch('lucxbox.tools.update_bitbucket_summary.update_bitbucket_summary.read_json_file',
                 lambda file_name: {
                     'pr_id': 123,
                     'build_number': 999,
                     "variant": 'MAIN',
                     "tool": 'check',
                     "result": 'OK',
                     "details": '',
                     "components": [],
                     "comment": ''
                 })
    args = argparse.Namespace()
    args.pr_id = None
    args.build_number = None
    args.build_variant = None
    args.tool = None
    args.result = None
    args.details = None
    args.components = None
    args.comment = None
    args = update_bitbucket_summary.init_args_from_summary_file('summary.json', args)
    for key in args.__dict__:
        assert args.__getattribute__(key) is not None
