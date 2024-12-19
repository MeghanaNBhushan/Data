# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_custom_help.py
# ----------------------------------------------------------------------------
"""Tests for qac/custom_help.py"""

from os import path
from unittest import TestCase, mock
from unittest.mock import patch
from swq.qac import custom_help as custom_help_module
from swq.qac.custom_help import replace_token_in_file, set_bosch_custom_help, \
    set_builtin_qac_help, set_component_path_in_xml


class TestCustomHelp(TestCase):
    """Tests class for custom help"""
    def setUp(self):
        self.config = mock.Mock(
            qac_home_path='qac/home',
            acf_file=mock.Mock(),
            vcf_file='vcf.file',
            ncf_file=mock.Mock(),
            rcf_file=mock.Mock(),
            user_messages=mock.Mock(),
            custom_help_path='custom_help')

    def test_set_bosch_custom_help(self):
        """Tests set_bosch_custom_help()"""
        with patch.object(custom_help_module, 'replace_token_in_file') \
            as mocked_replace_token_in_file:

            in_filepath = 'filepath'
            out_filepath = in_filepath
            bosch_help_keyword = '__bosch_help__'

            # custom_help_path was not defined
            custom_help_path = ''

            set_bosch_custom_help(in_filepath, custom_help_path)

            mocked_replace_token_in_file.assert_not_called()

            # custom_help_path was defined
            custom_help_path = 'custom/help/path'

            set_bosch_custom_help(in_filepath, custom_help_path)

            mocked_replace_token_in_file.assert_called_once_with(
                bosch_help_keyword, custom_help_path, in_filepath,
                out_filepath
            )

            # reset mocks
            mocked_replace_token_in_file.reset_mock()

            # custom_help_path was defined
            in_filepath = 'filepath'
            out_filepath = in_filepath
            custom_help_path = 'custom/help/path'
            bosch_help_keyword = '__bosch_help__'

            set_bosch_custom_help(in_filepath, custom_help_path)

            mocked_replace_token_in_file.assert_called_once_with(
                bosch_help_keyword, custom_help_path, in_filepath,
                out_filepath
            )

    def test_set_builtin_qac_help(self):
        """Test set_builtin_qac_help()"""
        with patch.object(custom_help_module, 'replace_token_in_file') \
            as mocked_replace_token_in_file:

            qa_help_keyword = "__qa_help__"
            in_filepath = 'filepath'
            out_filepath = in_filepath

            set_builtin_qac_help(in_filepath, self.config.qac_home_path)

            mocked_replace_token_in_file.assert_called_once_with(
                qa_help_keyword, self.config.qac_home_path,
                in_filepath, out_filepath)

    def test_replace_token_in_file(self):
        """Tests replace_token_in_file() method"""
        token = '_token_'
        file_content = token + '\nsomething'
        open_mock = mock.mock_open(read_data=file_content)
        in_filepath = 'some/input/path'
        out_filepath = 'some/output/path'

        # token exists in file
        with patch.object(custom_help_module, 'open_t', new=open_mock) \
            as mocked_open:
            replace_token_in_file(token, 'replaced', in_filepath,
                                  out_filepath)

            expected_open_read_calls = [mock.call(in_filepath)]
            expected_open_write_calls = [mock.call(out_filepath, mode='wt')]

            expected_write_modified_calls = [
                mock.call().write('replaced\nsomething'),
            ]

            mocked_open.assert_has_calls(expected_open_read_calls)
            mocked_open.assert_has_calls([mock.call().read()])
            mocked_open.assert_has_calls(expected_open_write_calls)
            mocked_open.assert_has_calls(expected_write_modified_calls)

        file_content = 'notatoken\nsomething'
        open_mock = mock.mock_open(read_data=file_content)

        # token not exists in file
        with patch.object(custom_help_module, 'open_t', new=open_mock) \
            as mocked_open:
            replace_token_in_file(token, 'replaced', in_filepath,
                                  out_filepath)

            expected_open_read_calls = [mock.call(in_filepath)]

            mocked_open.assert_has_calls(expected_open_read_calls)
            mocked_open.return_value.write.assert_not_called()

        file_content = token + '\n' + token + '\nsomething'
        open_mock = mock.mock_open(read_data=file_content)

        # token exists in file more than one time
        with patch.object(custom_help_module, 'open_t', new=open_mock) \
            as mocked_open:
            replace_token_in_file(token, 'replaced', in_filepath,
                                  out_filepath)

            expected_open_read_calls = [mock.call(in_filepath)]
            expected_open_write_calls = [mock.call(out_filepath, mode="wt")]

            expected_write_modified_calls = [
                mock.call().write('replaced\nreplaced\nsomething')
            ]

            mocked_open.assert_has_calls(expected_open_read_calls)
            mocked_open.assert_has_calls([mock.call().read()])
            mocked_open.assert_has_calls(expected_open_write_calls)
            mocked_open.assert_has_calls(expected_write_modified_calls)

    def test_set_component_path_in_xml(self):
        """Tests set_component_path_in_xml()"""
        # no token in xml file
        xml_in_file = 'user_messages.xml'
        xml_in_content = """<message severity="6"/>"""
        xml_out_content = """<message severity="6"/>"""

        with patch.object(custom_help_module, 'open_t',
                          new=mock.mock_open(read_data=xml_in_content)) as \
                xml_in_file:
            set_component_path_in_xml(xml_in_file, self.config.qac_home_path)
            xml_in_file.return_value.write.assert_not_called()

        # contains token in file and component found
        component_path = 'some/path'
        xml_in_content = """<?xml version="1.0" encoding="UTF-8"?>
<user_messages>
  <messages component="qac">
    <message help="__component_path__/doc-en_US/messages/0010.html" id="0010" \
        level="QA_ERROR" severity="9">
      <text>[Q] Unable to open file '%s'.</text>
      <references></references>
    </message>
  </messages>
</user_messages>"""
        xml_out_content = """<?xml version="1.0" ?><user_messages>\t
  \t<messages component="qac">\t\t
    \t\t<message help="{}/doc-en_US/messages/0010.html" id="0010" \
level="QA_ERROR" severity="9">\t\t\t
      \t\t\t<text>[Q] Unable to open file '%s'.</text>\t\t\t
      \t\t\t<references/>\t\t\t
    \t\t</message>\t\t
  \t</messages>\t
</user_messages>""".format(component_path)
        with patch.object(custom_help_module, 'open_t',
                          new=mock.mock_open(read_data=xml_in_content)) as \
                xml_in_file, \
            patch.object(custom_help_module,
                         'get_qac_installed_component_path') \
                            as mocked_get_qac_installed_component_path:
            mocked_get_qac_installed_component_path.return_value = \
                component_path
            set_component_path_in_xml(xml_in_file, self.config.qac_home_path)
            xml_in_file.assert_has_calls([mock.call().write(xml_out_content)])

        # contains token in file and component does not found
        component_path = None
        xml_in_content = """<?xml version="1.0" encoding="UTF-8"?>
<user_messages>
  <messages component="qac">
    <message help="__component_path__/doc-en_US/messages/0010.html" id="0010" \
        level="QA_ERROR" severity="9">
      <text>[Q] Unable to open file '%s'.</text>
      <references></references>
    </message>
  </messages>
</user_messages>"""
        xml_out_content = """<?xml version="1.0" ?><user_messages>\t
  \t<messages component="qac">\t\t
    \t\t<message help="{}/doc-en_US/messages/0010.html" id="0010" \
level="QA_ERROR" severity="9">\t\t\t
      \t\t\t<text>[Q] Unable to open file '%s'.</text>\t\t\t
      \t\t\t<references/>\t\t\t
    \t\t</message>\t\t
  \t</messages>\t
</user_messages>""".format('__component_path__')
        with patch('swq.common.filesystem.filesystem_utils.open',
                    new=mock.mock_open(read_data=xml_in_content)) as \
                xml_in_file, \
            patch.object(custom_help_module,
                         'get_qac_installed_component_path') \
                            as mocked_get_qac_installed_component_path:
            mocked_get_qac_installed_component_path.return_value = \
                component_path
            set_component_path_in_xml(xml_in_file, self.config.qac_home_path)
            xml_in_file.assert_has_calls([mock.call().write(xml_out_content)])
