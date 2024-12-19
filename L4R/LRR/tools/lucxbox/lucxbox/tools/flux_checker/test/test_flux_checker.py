""" Test for flux checker """
import platform
import sys
import unittest
from unittest import mock

import pytest

from lucxbox.tools.flux_checker import flux_checker


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.mock_logger = mock.patch("lucxbox.tools.flux_checker.flux_checker.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    @mock.patch("lucxbox.tools.flux_checker.flux_checker._find_fqm_executable")
    @mock.patch("lucxbox.tools.flux_checker.flux_checker.lucxutils.is_exe")
    @mock.patch("lucxbox.tools.flux_checker.flux_checker.lucxutils.execute")
    @mock.patch("lucxbox.tools.flux_checker.flux_checker.finder.get_files_with_ending")
    def test_main(self, mock_finder, mock_execute, mock_is_exe, mock_find_fqm_exe):
        mock_find_fqm_exe.return_value = "FQM/1.1-11/FQM.exe"
        mock_is_exe.return_value = True
        mock_execute.return_value = "Hello World", "", 0
        mock_finder.return_value = ["some.flux"]
        with mock.patch.object(sys, 'argv', ["flux_checker.py", "-d", "--fqm-version", "1.1-11", "check"]):
            returncode = flux_checker.main()
            self.assertEqual(0, returncode)

    @mock.patch("lucxbox.tools.flux_checker.flux_checker._find_fqm_executable")
    @mock.patch("lucxbox.tools.flux_checker.flux_checker.lucxutils.is_exe")
    @mock.patch("lucxbox.tools.flux_checker.flux_checker.lucxutils.execute")
    @mock.patch("lucxbox.tools.flux_checker.flux_checker.finder.get_files_with_ending")
    def test_main_error(self, mock_finder, mock_execute, mock_is_exe, mock_find_fqm_exe):
        mock_find_fqm_exe.return_value = "FQM/1.1-11/FQM.exe"
        mock_is_exe.return_value = True
        mock_execute.return_value = "", "Houston, we have a problem", 1
        mock_finder.return_value = ["some.flux"]
        with mock.patch.object(sys, 'argv', ["flux_checker.py", "-d", "--fqm-version", "1.1-11", "check"]):
            returncode = flux_checker.main()
            self.assertEqual(1, returncode)


@pytest.mark.skip(reason='Disabling test because of DACX-557')
@pytest.mark.usefixtures('suppress_logging', 'version_exists', 'mock_windows')
def test_download_from_artifactory(mocker, tmpdir):
    mocker.patch('lucxbox.tools.flux_checker.flux_checker.lucxutils')
    download = mocker.patch('lucxbox.tools.flux_checker.flux_checker.download_from_artifactory.lucxio').download
    directory = tmpdir.mkdir('download')
    version_path = directory.mkdir('version_path')

    flux_checker.download_from_artifactory('user', 'password', '1.1.0.19', directory, version_path)

    filename = 'Flux.QualityMetrics-windows-unsupported-1.1.0.19.zip'
    assert download.called_once()
    _, kwargs = download.call_args
    assert kwargs['filename'] == filename
    assert kwargs['url'].endswith('1.1.0.19/standalone_tools/windows/{}'.format(filename))


@pytest.mark.skipif(platform.system() == "Linux", reason="no linux version of flux on artifactory")
@pytest.mark.usefixtures('suppress_logging')
@pytest.mark.parametrize('version, expected_exists', [
    ('0.4.4', False),
    ('1.0.0.17', False),
    ('1.1.0.19', True),
    ('1.1.42', False),
])
def test_version_exists(session_with_versions_json, version, expected_exists):
    actual_exists = flux_checker.version_exists_in_artifactory(session_with_versions_json, version)

    assert actual_exists is expected_exists
