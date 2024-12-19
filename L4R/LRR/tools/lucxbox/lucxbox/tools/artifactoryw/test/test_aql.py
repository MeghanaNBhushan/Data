""" Testing the aql """

import pytest

from lucxbox.tools.artifactoryw.aql import items_in_repo_created_before, items_in_repo_downloaded_before


@pytest.mark.parametrize('retention_period, rt_repository, patterns, fields, expected_aql_query', [
    ('25d',
     'test_repository',
     {'include_path_pattern': 'path/to/artifact'},
     ('repo', 'name', 'path'),
     'items.find({"repo":{"$eq":"test_repository"},"created":{"$before":"25d"},"path":{"$match":"path/to/artifact"}'
     '}).include("repo","name","path","created")'
    ),
    ('25d',
     'test_repository',
     None,
     ('repo', 'name', 'path'),
     'items.find({"repo":{"$eq":"test_repository"},"created":{"$before":"25d"}'
     '}).include("repo","name","path","created")'),
    ('25d',
     'test_repository',
     {'include_path_pattern': 'path/to/artifact'},
     None,
     'items.find({"repo":{"$eq":"test_repository"},"created":{"$before":"25d"},"path":{"$match":"path/to/artifact"}})'
    ),
    ('25d',
     'test_repository',
     None,
     None,
     'items.find({"repo":{"$eq":"test_repository"},"created":{"$before":"25d"}})'
    ),
    ('25d',
     'test_repository',
     {'any_pattern': '*'},
     None,
     'items.find({"repo":{"$eq":"test_repository"},"created":{"$before":"25d"}})'
    ),
    ('25d',
     'test_repository',
     {'include_path_pattern': None},
     None,
     'items.find({"repo":{"$eq":"test_repository"},"created":{"$before":"25d"}})'
    ),
    ('25d',
     'test_repository',
     {'include_path_pattern': None},
     ('repo', 'name', 'path', 'path'),
     'items.find({"repo":{"$eq":"test_repository"},"created":{"$before":"25d"}'
     '}).include("repo","name","path","created")'
    )
])
def test_aql_of_created_before(retention_period, rt_repository, fields, patterns, expected_aql_query):
    actual_aql_query = items_in_repo_created_before(rt_repository, retention_period, patterns, fields)

    assert actual_aql_query.replace(' ', '') == expected_aql_query


@pytest.mark.parametrize('retention_period, rt_repository, patterns, fields, expected_aql_query', [
    ('2w',
     'test_repository',
     {'include_path_pattern': 'path/to/artifact'},
     ('repo', 'name', 'path'),
     'items.find({"repo":{"$eq":"test_repository"},"stat.downloaded":{"$before":"2w"},'
     '"path":{"$match":"path/to/artifact"}}).include("repo","name","path","stat.downloaded")'
    ),
    ('2w',
     'test_repository',
     None,
     ('repo', 'name', 'path'),
     'items.find({"repo":{"$eq":"test_repository"},"stat.downloaded":{"$before":"2w"}'
     '}).include("repo","name","path","stat.downloaded")'),
    ('2w',
     'test_repository',
     {'include_path_pattern': 'path/to/artifact'},
     None,
     'items.find({"repo":{"$eq":"test_repository"},"stat.downloaded":{"$before":"2w"},'
     '"path":{"$match":"path/to/artifact"}})'
    ),
    ('2w',
     'test_repository',
     None,
     None,
     'items.find({"repo":{"$eq":"test_repository"},"stat.downloaded":{"$before":"2w"}})'
    ),
    ('2w',
     'test_repository',
     {'any_pattern': None},
     None,
     'items.find({"repo":{"$eq":"test_repository"},"stat.downloaded":{"$before":"2w"}})'
    ),
    ('2w',
     'test_repository',
     {'include_path_pattern': None},
     None,
     'items.find({"repo":{"$eq":"test_repository"},"stat.downloaded":{"$before":"2w"}})'
    ),
    ('2w',
     'test_repository',
     {'include_path_pattern': None},
     ('repo', 'name', 'path', 'path', 'name'),
     'items.find({"repo":{"$eq":"test_repository"},"stat.downloaded":{"$before":"2w"}'
     '}).include("repo","name","path","stat.downloaded")'
    )
])
def test_aql_of_downloaded_before(retention_period, rt_repository, fields, patterns, expected_aql_query):
    actual_aql_query = items_in_repo_downloaded_before(rt_repository, retention_period, patterns, fields)

    assert actual_aql_query.replace(' ', '') == expected_aql_query
