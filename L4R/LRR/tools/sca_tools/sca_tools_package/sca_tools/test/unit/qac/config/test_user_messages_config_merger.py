# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_user_messages_config_merger.py
# ----------------------------------------------------------------------------
"""Test for qac/config/user_messages_config_merger.py"""
import xml.etree.ElementTree as ET

from os import path

from unittest import TestCase, mock
from unittest.mock import patch
from swq.common.return_codes import RC_MESSAGE_ID_NOT_UNIQUE, \
    RC_FILE_PARSE_FAILED
from swq.qac.config import user_messages_config_merger
from swq.qac.config.user_messages_config_merger import UserMessagesConfigMerger

_FILE1_XML_CONTENT = '\
<user_messages>\
  <messages component="certcppcm">\
    <message severity="6" help="5003.html" id="5003" level="QA_WARNING">\
      <text>Declaration or definition of a reserved identifier.</text>\
    </message>\
  </messages>\
</user_messages>'

_FILE2_XML_CONTENT = '\
<user_messages>\
  <messages component="certcppcm">\
    <message severity="6" help="5004.html" id="5004" level="QA_WARNING">\
      <text>Some text.</text>\
    </message>\
  </messages>\
</user_messages>'

_NON_XML_FILE_CONTENT = 'foo-bar'


class TestUserMessagesConfigMerger(TestCase):
    """Test class for the qac.config.user_messages_config_merger"""
    def setUp(self):
        self.output_folder_path = 'project_dir'
        self.input_config_files = ['file1.xml', 'file2.xml']
        self.result_file = 'merged_user_messages.xml'
        self.merger = UserMessagesConfigMerger(self.output_folder_path,
                                               self.input_config_files)

        self.parsed_content = [
            ET.fromstring(_FILE1_XML_CONTENT),
            ET.fromstring(_FILE2_XML_CONTENT)
        ]

        self.mock_logger = patch("swq.qac.config.config_merger.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    def test_run(self):
        """Tests run()"""
        with patch('xml.etree.ElementTree.parse'),\
                patch('swq.qac.config.xml_config_merger.ET'):
            return_value = self.merger.run()
            self.assertEqual(
                path.join(self.output_folder_path, self.result_file),
                return_value)

    @patch("swq.qac.config.user_messages_config_merger.LOGGER")
    def test_merge_content(self, _):
        """Tests merge_content()"""
        with patch('xml.etree.ElementTree.parse'),\
                patch('swq.qac.config.xml_config_merger.ET'):

            expected_xpaths = [
                "messages[@component='certcppcm']",
                "messages[@component='certcppcm']message[@id='5003']",
                "messages[@component='certcppcm']message[@id='5004']"
            ]
            return_value = self.merger.merge_contents(self.parsed_content)
            self.assertEqual(
                all(return_value.findall(xpath) for xpath in expected_xpaths),
                True)

            with patch.object(user_messages_config_merger,
                              'log_and_exit') as mock_log_and_exit:

                self.parsed_content = [
                    ET.fromstring(_FILE1_XML_CONTENT),
                    ET.fromstring(_FILE1_XML_CONTENT)
                ]
                return_value = self.merger.merge_contents(self.parsed_content)
                mock_log_and_exit.assert_called_once_with(
                    RC_MESSAGE_ID_NOT_UNIQUE)

    @patch("swq.qac.config.xml_config_merger.LOGGER")
    def test_parse_content(self, _):
        """Tests _parse_content()"""
        with patch.object(UserMessagesConfigMerger, 'merge_contents'),\
                patch.object(UserMessagesConfigMerger, '_write_output_file'),\
                patch('xml.etree.ElementTree.parse') as mock_etree_parse,\
                patch('swq.qac.config.xml_config_merger.log_and_exit')\
                as mock_log_and_exit:
            parsed_xml = ET.fromstring(_FILE1_XML_CONTENT)
            mock_etree_parse.return_value = parsed_xml.find('user_messages')

            mocked_getroot = mock.Mock()
            attrs = {'getroot.return_value': parsed_xml}
            mocked_getroot.configure_mock(**attrs)
            mock_etree_parse.return_value = mocked_getroot

            return_value = self.merger._parse_content()
            self.assertEqual(return_value[0], parsed_xml)
            mock_etree_parse.reset_mock()
            mocked_getroot.reset_mock()

            mock_etree_parse.side_effect = ET.ParseError("boom!")
            return_value = self.merger._parse_content()
            mock_log_and_exit.assert_called_with(RC_FILE_PARSE_FAILED)
