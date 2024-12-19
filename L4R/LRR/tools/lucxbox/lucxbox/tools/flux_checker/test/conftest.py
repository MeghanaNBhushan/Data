import sys

import pytest


@pytest.fixture
def suppress_logging(mocker):
    mocker.patch('lucxbox.lib.lucxutils.LOGGER')
    mocker.patch('lucxbox.tools.flux_checker.flux_checker.LOGGER')


@pytest.fixture
def folders():
    return [
        '0.4.4',
        '0.4.5',
        '0.5.0.6',
        '1.0.0.17',
        '1.1.0.19',
        'jenkins',
    ]


@pytest.fixture
def folders_json(folders):
    return {'children': [{'uri': '/' + v} for v in folders]}


@pytest.fixture
def session_with_versions_json(mocker, folders_json):
    mock_versions_response = mocker.Mock()
    mock_versions_response.json.return_value = folders_json
    mock_session = mocker.Mock()
    mock_session.get.return_value = mock_versions_response
    return mock_session


@pytest.fixture
def mock_windows(monkeypatch):
    monkeypatch.setattr(sys, 'platform', 'win32')


@pytest.fixture
def version_exists(mocker):
    mocker.patch('lucxbox.tools.flux_checker.flux_checker.version_exists_in_artifactory', return_value=True)
