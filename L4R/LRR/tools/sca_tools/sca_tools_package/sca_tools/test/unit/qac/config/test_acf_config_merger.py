# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_acf_config_merger.py
# ----------------------------------------------------------------------------
"""Test for qac/config/acf_config_merger.py"""
import xml.etree.ElementTree as ET

from os import path

from unittest import TestCase, mock
from unittest.mock import patch
from swq.common.return_codes import RC_MESSAGE_ID_NOT_UNIQUE, \
    RC_FILE_PARSE_FAILED
from swq.qac.config import acf_config_merger
from swq.qac.config.acf_config_merger import AcfConfigMerger

_FILE1_XML_CONTENT = '\
<acf xmlversion="2.0.0">\
  <components>\
    <component version="4.7.0" target="C++" name="qacpp"/>\
    <component version="2.3.0" target="C++" name="ascm"/>\
  </components>\
  <component_settings>\
    <input_to component="qacpp" target="C++" version="4.7.0">\
      <option argument="A" name="-threshold " />\
      <option argument="B" name="-threshold " />\
    </input_to>\
    <input_to component="ascm" target="C++" version="2.3.0">\
    </input_to>\
  </component_settings>\
</acf>'

_FILE2_XML_CONTENT = '\
<acf xmlversion="2.0.0">\
  <components>\
    <component version="4.8.0" target="C++" name="qacpp"/>\
    <component version="2.3.1" target="C_CPP" name="ascm"/>\
  </components>\
  <component_settings>\
    <input_to component="qacpp" target="C++" version="4.7.0">\
      <option argument="C" name="-threshold " />\
      <option argument="D" name="-threshold " />\
    </input_to>\
    <input_to component="ascm" target="C++" version="2.3.0">\
      <option argument="extension::header=[\'impl\']" name="-po " />\
    </input_to>\
  </component_settings>\
</acf>'

_NON_XML_FILE_CONTENT = 'foo-bar'


class TestAcfConfigMerger(TestCase):
    """Test class for the qac.config.acf_config_merger"""
    def setUp(self):
        self.output_folder_path = 'project_dir'
        self.input_config_files = ['file1.acf', 'file2.acf']
        self.result_file = 'merged_analysis_configs.acf'
        self.merger = AcfConfigMerger(self.output_folder_path,
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

    def test_merge_content(self):
        """Tests merge_content()"""
        with patch('xml.etree.ElementTree.parse'),\
                patch('swq.qac.config.xml_config_merger.ET'):
            input_to_xpath = 'input_to[@component=\'qacpp\']'
            option_xpath = f'component_settings/{input_to_xpath}/option'
            expected_xpaths = [
                "components/component[@name='qacpp'][@version='4.7.0']",
                "components/component[@name='ascm'][@version='2.3.0']",
                "components/component[@name='qacpp'][@version='4.8.0']",
                "components/component[@name='ascm'][@version='2.3.1']",
                f"{option_xpath}[@argument='A']",
                f"{option_xpath}[@argument='B']",
                f"{option_xpath}[@argument='C']",
                f"{option_xpath}[@argument='D']"
            ]
            return_value = self.merger.merge_contents(self.parsed_content)
            self.assertEqual(
                all(return_value.findall(xpath) for xpath in expected_xpaths),
                True)

    @patch("swq.qac.config.xml_config_merger.LOGGER")
    def test_parse_content(self, _):
        """Tests _parse_content()"""
        with patch.object(AcfConfigMerger, 'merge_contents'),\
                patch.object(AcfConfigMerger, '_write_output_file'),\
                patch('xml.etree.ElementTree.parse') as mock_etree_parse,\
                patch('swq.qac.config.xml_config_merger.log_and_exit')\
                as mock_log_and_exit:
            parsed_xml = ET.fromstring(_FILE1_XML_CONTENT)
            mock_etree_parse.return_value = parsed_xml.find('acf')

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
