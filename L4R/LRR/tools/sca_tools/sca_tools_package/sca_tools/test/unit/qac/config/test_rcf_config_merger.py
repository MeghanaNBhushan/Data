# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_rcf_config_merger.py
# ----------------------------------------------------------------------------
"""Test for qac/config/rcf_config_merger.py"""
import xml.etree.ElementTree as ET

from unittest import TestCase
from unittest.mock import patch
from swq.common.return_codes import RC_RCF_RULE_GROUP_NOT_UNIQUE
from swq.qac.config.rcf_config_merger import RcfConfigMerger

_FILE1_RCF_CONTENT = '\
<rcf name="rule_1" version="1.0">\
  <rulegroup name="RULE 1">\
    <rule help="" active="yes" id="RULE ID 1">\
      <text> Some Text.</text>\
      <enforcement>\
        <message mapped="yes" component="sca" id="1" />\
        <message mapped="no" component="sca" id="2" />\
      </enforcement>\
    </rule>\
</rulegroup>\
</rcf>'

_FILE2_RCF_CONTENT = '\
<rcf name="rule_2" version="1.0">\
  <rulegroup name="RULE 2">\
    <rule help="" active="yes" id="RULE ID 1">\
      <text> Some Text.</text>\
      <enforcement>\
        <message mapped="yes" component="sca_tools" id="1" />\
      </enforcement>\
    </rule>\
</rulegroup>\
</rcf>'


class TestRcfConfigMerger(TestCase):
    """Test class for the qac.config.rcf_config_merger"""
    def setUp(self):
        self.output_folder_path = 'project_dir'
        self.input_config_files = ['rcf_file1.rcf', 'rcf_file2.rcf']
        self.result_file = 'merged_coding_rules.rcf'
        self.merger = RcfConfigMerger(self.output_folder_path,
                                      self.input_config_files)

        self.parsed_content = [
            ET.fromstring(_FILE1_RCF_CONTENT),
            ET.fromstring(_FILE2_RCF_CONTENT)
        ]

        self.mock_logger = patch("swq.qac.config.config_merger.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    @patch("swq.qac.config.rcf_config_merger.LOGGER")
    def test_merge_content(self, _):
        """Tests merge_content()"""
        with patch('xml.etree.ElementTree.parse'),\
                patch('swq.qac.config.xml_config_merger.ET'):

            rule_group_name_xpath = [
                "rulegroup[@name='RULE 1']", "rulegroup[@name='RULE 2']"
            ]
            return_value = self.merger.merge_contents(self.parsed_content)
            self.assertEqual(
                all(
                    return_value.findall(xpath)
                    for xpath in rule_group_name_xpath), True)
            self.assertFalse(
                return_value.findall('.//message[@mapped=\'no\']'))

    @patch("swq.qac.config.rcf_config_merger.log_and_exit")
    def test_check_for_duplication_and_exit_if_founde(self, mock_log_and_exit):
        """Tests _check_for_duplication_and_exit_if_found()"""

        self.parsed_content = [
            ET.fromstring(_FILE1_RCF_CONTENT),
            ET.fromstring(_FILE2_RCF_CONTENT)
        ]

        self.merger.merge_contents(self.parsed_content)
        mock_log_and_exit.assert_not_called()

        self.parsed_content = [
            ET.fromstring(_FILE1_RCF_CONTENT),
            ET.fromstring(_FILE1_RCF_CONTENT)
        ]

        self.merger.merge_contents(self.parsed_content)
        mock_log_and_exit.assert_called_once_with(RC_RCF_RULE_GROUP_NOT_UNIQUE)
