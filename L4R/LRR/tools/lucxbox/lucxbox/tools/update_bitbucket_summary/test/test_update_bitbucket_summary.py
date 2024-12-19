# pylint: disable=invalid-name
import argparse
import pytest
import stashy

from lucxbox.tools.update_bitbucket_summary.update_bitbucket_summary import UpdateBitbucketSummary


def get_default_comment_text():
    return '### Build №100 Report\n\n|**Variant**|**Tool**|**Result**|**Details**|**Components**' \
           '|**Comment**|\n|-|-|-|-|-|-|\n|MAIN|tool-x|OK|-|-|-|\n\n\n###### Reply to this comme' \
           'nt to make it permanent.'


def get_comment_activity(**_):
    yield {'action': 'COMMENTED', 'comment': {'text': get_default_comment_text(), 'id': 123, 'version': 1}}


@pytest.fixture
def argparse_args():
    return argparse.Namespace(bitbucket_project='test-project',
                              bitbucket_repo='test-repo',
                              bitbucket_url="https://bitbucket.test",
                              build_number=100,
                              build_variant='MAIN',
                              password='password',
                              tool='tool-x',
                              result='OK',
                              details='',
                              components=[],
                              comment='',
                              pr_id=1,
                              user='username')


@pytest.fixture
def updater_object(mocker, argparse_args, request):
    for key, value in request.param.items():
        argparse_args.__dict__[key] = value
    updater = UpdateBitbucketSummary(mocker.MagicMock(),
                                     argparse_args.bitbucket_project,
                                     argparse_args.bitbucket_repo,
                                     argparse_args.pr_id,
                                     argparse_args.build_variant,
                                     argparse_args.result,
                                     argparse_args.tool,
                                     argparse_args.details,
                                     argparse_args.components,
                                     argparse_args.comment,
                                     argparse_args.build_number,
                                     mocker.MagicMock())
    return updater


@pytest.mark.parametrize('updater_object, build_variant, expected_result',
                         [({},
                           None,
                           '||tool-x|OK|-|-|-|\n'),
                          ({},
                           'VAR1',
                           '|VAR1|tool-x|OK|-|-|-|\n'),
                          ({'comment': 'com1\ncom2'},
                           None,
                           '||tool-x|OK|-|-|com1|\n||||||com2|\n'),
                          ({'details': 'det1\ndet2\ndet3', 'result': 'res1\nres2'},
                           None,
                           '||tool-x|res1|det1|-|-|\n|||res2|det2|||\n||||det3|||\n'),
                          ({'details': 'det1\ndet2\ndet3', 'result': 'res1\nres2'},
                           'VAR_X',
                           '|VAR_X|tool-x|res1|det1|-|-|\n|||res2|det2|||\n||||det3|||\n'),
                          ({'components': ['A1', 'A2']},
                           None,
                           '||tool-x|OK|-|`A1` `A2`|-|\n'),
                          ],
                         ids=[
                             'without build variant',
                             'with build variant',
                             'without build variant, multiline comment',
                             'without build variant, details 3 lines, result 2 lines',
                             'with build variant, details 3 lines, result 2 lines',
                             'without build variant, with components',
                         ],
                         indirect=['updater_object'])
def test_get_table_rows(updater_object, expected_result, build_variant):
    # pylint: disable=protected-access
    if build_variant is None:
        assert updater_object._get_table_rows() == expected_result
    else:
        assert updater_object._get_table_rows(build_variant) == expected_result


@pytest.mark.parametrize('updater_object, expected_result',
                         [({}, get_default_comment_text()),
                          ],
                         ids=[
                             'new text from default fixture'
                         ],
                         indirect=['updater_object'])
def test_create_new_comment_text(updater_object, expected_result):
    ## pylint: disable=protected-access
    assert updater_object._get_new_comment_text() == expected_result


@pytest.mark.parametrize('updater_object, input_text, expected_result',
                         [({'tool': 'tool-y'},
                           get_default_comment_text(),
                           '### Build №100 Report\n\n|**Variant**|**Tool**|**Result**|**Details**|**Components**|'
                           '**Comment**|\n|-|-|-|-|-|-|\n|MAIN|tool-x|OK|-|-|-|\n||tool-y|OK|-|-|-|\n\n'
                           '\n###### Reply to this comment to make it permanent.'),
                          ({'build_variant': 'SECONDARY'},
                           get_default_comment_text(),
                           '### Build №100 Report\n\n|**Variant**|**Tool**|**Result**|**Details**|**Components**|'
                           '**Comment**|\n|-|-|-|-|-|-|\n|MAIN|tool-x|OK|-|-|-|\n|SECONDARY|tool-x|OK|-|-|-|\n\n'
                           '\n###### Reply to this comment to make it permanent.'),
                          ],
                         ids=[
                             'same variant different tool',
                             'different variant'
                         ],
                         indirect=['updater_object'])
def test_get_updated_text(updater_object, input_text, expected_result):
    # pylint: disable=protected-access
    assert updater_object._get_updated_comment_text(input_text) == expected_result


def test_create_comment_new_text(mocker, argparse_args):
    updater = UpdateBitbucketSummary(mocker.MagicMock(),
                                     argparse_args.bitbucket_project,
                                     argparse_args.bitbucket_repo,
                                     argparse_args.pr_id,
                                     argparse_args.build_variant,
                                     argparse_args.result,
                                     argparse_args.tool,
                                     argparse_args.details,
                                     argparse_args.components,
                                     argparse_args.comment,
                                     argparse_args.build_number,
                                     )
    pr_mock = mocker.MagicMock()
    updater.pr = pr_mock

    assert updater.update() is None
    pr_mock.comment.assert_called_once_with(commentText=get_default_comment_text())


def test_update_comment_new_text(mocker, argparse_args):
    expected_result = '### Build №101 Report\n\n|**Variant**|**Tool**|**Result**|**Details**|**Components**' \
                      '|**Comment**|\n|-|-|-|-|-|-|\n|MAIN|tool-x|OK|-|-|-|\n\n\n###### Reply to this comme' \
                      'nt to make it permanent.'
    updater = UpdateBitbucketSummary(mocker.MagicMock(),
                                     argparse_args.bitbucket_project,
                                     argparse_args.bitbucket_repo,
                                     argparse_args.pr_id,
                                     argparse_args.build_variant,
                                     argparse_args.result,
                                     argparse_args.tool,
                                     argparse_args.details,
                                     argparse_args.components,
                                     argparse_args.comment,
                                     argparse_args.build_number + 1,
                                     )

    pr_mock = mocker.MagicMock()
    pr_mock.activities = get_comment_activity
    updater.pr = pr_mock

    assert updater.update() is None
    pr_mock.delete_comment.assert_called_once_with(123, 1)
    pr_mock.comment.assert_called_once_with(commentText=expected_result)


def test_update_comment_error_on_delete(mocker, argparse_args):
    expected_result = '### Build №101 Report\n\n|**Variant**|**Tool**|**Result**|**Details**|**Components**' \
                      '|**Comment**|\n|-|-|-|-|-|-|\n|MAIN|tool-x|OK|-|-|-|\n\n\n###### Reply to this comme' \
                      'nt to make it permanent.'
    logger_mock = mocker.MagicMock()
    updater = UpdateBitbucketSummary(mocker.MagicMock(),
                                     argparse_args.bitbucket_project,
                                     argparse_args.bitbucket_repo,
                                     argparse_args.pr_id,
                                     argparse_args.build_variant,
                                     argparse_args.result,
                                     argparse_args.tool,
                                     argparse_args.details,
                                     argparse_args.components,
                                     argparse_args.comment,
                                     argparse_args.build_number + 1,
                                     logger_mock)

    exception = stashy.errors.GenericException(mocker.MagicMock())
    pr_mock = mocker.MagicMock()
    pr_mock.activities = get_comment_activity
    pr_mock.delete_comment = mocker.MagicMock()
    pr_mock.delete_comment.side_effect = exception

    updater.pr = pr_mock
    assert updater.update() is None
    logger_mock.warning.assert_called_once_with('Could not delete old comment: %s', exception)
    pr_mock.comment.assert_called_once_with(commentText=expected_result)


def test_update_comment_combined_text(mocker, argparse_args):
    expected_result = '### Build №100 Report\n\n|**Variant**|**Tool**|**Result**|**Details**|**Components**' \
                      '|**Comment**|\n|-|-|-|-|-|-|\n|MAIN|tool-x|OK|-|-|-|\n||NEW_TOOL|FAIL|-|`A1` `A2`|-|' \
                      '\n\n\n###### Reply to this comment to make it permanent.'
    updater = UpdateBitbucketSummary(mocker.MagicMock(),
                                     argparse_args.bitbucket_project,
                                     argparse_args.bitbucket_repo,
                                     argparse_args.pr_id,
                                     argparse_args.build_variant,
                                     'FAIL',
                                     'NEW_TOOL',
                                     argparse_args.details,
                                     ['A1', 'A2'],
                                     argparse_args.comment,
                                     argparse_args.build_number,
                                     )

    pr_mock = mocker.MagicMock()
    pr_mock.activities = get_comment_activity
    updater.pr = pr_mock

    assert updater.update() is None
    pr_mock.delete_comment.assert_called_once_with(123, 1)
    pr_mock.comment.assert_called_once_with(commentText=expected_result)


def test_update_comment_combined_text_error_on_delete(mocker, argparse_args):
    logger_mock = mocker.MagicMock()
    updater = UpdateBitbucketSummary(mocker.MagicMock(),
                                     argparse_args.bitbucket_project,
                                     argparse_args.bitbucket_repo,
                                     argparse_args.pr_id,
                                     argparse_args.build_variant,
                                     'FAIL',
                                     'NEW_TOOL',
                                     argparse_args.details,
                                     ['A1', 'A2'],
                                     argparse_args.comment,
                                     argparse_args.build_number,
                                     logger_mock)

    exception = stashy.errors.GenericException(mocker.MagicMock())
    pr_mock = mocker.MagicMock()
    pr_mock.activities = get_comment_activity
    pr_mock.delete_comment = mocker.MagicMock()
    pr_mock.delete_comment.side_effect = exception
    updater.pr = pr_mock

    with pytest.raises(stashy.errors.GenericException):
        updater.update()
    pr_mock.comment.assert_not_called()
    logger_mock.error.assert_called_once_with('Could not delete old comment: %s', exception)
