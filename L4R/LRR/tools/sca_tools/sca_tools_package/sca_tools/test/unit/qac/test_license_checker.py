# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_license_checker.py
# ----------------------------------------------------------------------------
""" Tests for qac/license_checker.py """

from unittest import TestCase, mock
from unittest.mock import patch
from swq.qac import license_checker


@mock.patch('swq.qac.license_checker.LOGGER', create=True)
class TestLicenseChecker(TestCase):
    """ TestQacUtils class """
    def setUp(self):
        self.config = mock.Mock(license_servers=None,
                                helix_config_project_xml_path=None,
                                verbose=False)

    @patch('swq.qac.license_checker.path.exists')
    def test_validate_license_settings(self, mock_path_exists, logger):
        """ Test validate_license_settings() """

        mock_path_exists.return_value = False
        self.config.license_servers = []
        self.config.helix_config_project_xml_path = 'config.xml'
        xml_file_content = ""

        with patch.object(license_checker, 'set_license_server') \
            as mock_set_license_server, \
                patch.object(license_checker, 'list_license_server') \
                as mock_list_license_server, \
                patch.object(license_checker, 'check_license_server') \
                as mock_check_license_server:

            license_checker.validate_license_settings(self.config)
            mock_set_license_server.assert_not_called()
            mock_list_license_server.assert_not_called()
            mock_check_license_server.assert_not_called()

            self.config.license_servers = [
                '5065@rb-lic-rlm-prqa2.de.bosch.com',
                '5065@rb-lic-rlm-prqa-gl.de.bosch.com',
                '5065@rb-lic-rlm-prqa-cc.de.bosch.com'
            ]
            license_checker.validate_license_settings(self.config)
            mock_set_license_server.assert_called()
            mock_set_license_server.reset_mock()

            mock_path_exists.return_value = True
            with patch('swq.common.filesystem.filesystem_utils.open',
                       new=mock.mock_open(
                           read_data=xml_file_content)) as mocked_open:
                license_checker.validate_license_settings(self.config)
                mocked_open.assert_called_with(
                    self.config.helix_config_project_xml_path,
                    mode='rt',
                    buffering=mock.ANY,
                    encoding='utf-8',
                    errors=mock.ANY,
                    newline=mock.ANY,
                    closefd=mock.ANY,
                    opener=mock.ANY)
                mock_set_license_server.assert_called()
                for call in mock_set_license_server.call_args_list:
                    args, _ = call
                    self.assertIn(args[1], self.config.license_servers)
                mock_set_license_server.reset_mock()

            xml_file_content = """<?xml version='1.0' encoding='UTF-8'?>
<settings version='2'>
 <license_servers>
  <server port="5065" host="rb-lic-rlm-prqa-cc.de.bosch.com"/>
  <server port="5065" host="rb-lic-rlm-prqa-gl.de.bosch.com"/>
  <server port="5065" host="rb-lic-rlm-prqa2.de.bosch.com"/>
 </license_servers>
</settings>"""
            self.config.verbose = True
            with patch('swq.common.filesystem.filesystem_utils.open',
                       new=mock.mock_open(
                           read_data=xml_file_content)) as mocked_open:
                mock_list_license_server.return_value = ['Command Output', 0]
                mock_check_license_server.return_value = ['Command Output', 0]
                license_checker.validate_license_settings(self.config)
                mock_set_license_server.assert_not_called()
                mock_list_license_server.assert_called()
                mock_check_license_server.assert_called()

        logger.info.assert_called()
