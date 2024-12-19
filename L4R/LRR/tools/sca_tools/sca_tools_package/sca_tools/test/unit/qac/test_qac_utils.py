# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_qac_utils.py
# ----------------------------------------------------------------------------
""" Tests for qac/qac_utils.py """
from os import path
import xml.etree.ElementTree as ET

from unittest import TestCase, mock
from unittest.mock import patch
from swq import qac
from swq.qac import qac_utils
from swq.common.return_codes import RC_QAC_CONFIGURATION_INCONSISTENT, \
    RC_QAC_MODULES_VERSION_MISMATCH


class TestQacUtils(TestCase):
    """ TestQacUtils class """
    def setUp(self):
        self.config = mock.Mock(qac_bin_path='qac/bin/path',
                                acf_file='acf.xml',
                                qac_modules=[],
                                custom_config_path='custom/config')

    @patch('swq.qac.qac_utils.QacVersion')
    def test_has_summary_export_true(self, mock_qac_version):
        """ Test has_summary_export_false() return true """
        instance = mock_qac_version.return_value
        instance.major_minor.return_value = (2019, 2)
        instance.is_helix.return_value = True
        self.assertTrue(qac_utils.has_summary_export(self.config))

        instance.major_minor.return_value = (2019, 1)
        self.assertFalse(qac_utils.has_summary_export(self.config))

        instance.is_helix.return_value = False
        instance.major_minor.return_value = (2, 4)
        self.assertFalse(qac_utils.has_summary_export(self.config))

    def test_get_components_from_acf_file(self):
        """Test get_components_from_acf_file()"""
        acf_filepath = 'foo'
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<acf xmlversion="2.0.0">
  <components>
    <component version="4.6.0" target="C++" name="qacpp"/>
    <component version="9.8.0" target="C" name="qac"/>
  </components>
</acf>'''

        expected_components = ['qacpp-4.6.0', 'qac-9.8.0']

        with patch('swq.qac.qac_utils.etree_parse') as mock_etree:
            mocked_getroot = mock.Mock()
            attrs = {'getroot.return_value': ET.fromstring(xml_content)}
            mocked_getroot.configure_mock(**attrs)
            mock_etree.return_value = mocked_getroot

            self.assertEqual(
                qac_utils.get_components_from_acf_file(acf_filepath),
                expected_components)

    def test_check_if_component_version_matches_and_exit_otherwise(self):
        """Test check_if_component_version_matches_and_exit_otherwise()"""
        with patch('swq.qac.qac_utils.LOGGER'), \
            patch('swq.qac.qac_utils.log_and_exit') as mock_log_and_exit:
            # Versions match
            first_component = 'qacpp-4.7.0'
            second_component = 'qacpp-4.7.0'
            qac_utils.check_if_component_version_matches_and_exit_otherwise(
                first_component, second_component)
            mock_log_and_exit.assert_not_called()

            # Versions mismatch
            first_component = 'qacpp-4.6.0'
            second_component = 'qacpp-4.7.0'
            qac_utils.check_if_component_version_matches_and_exit_otherwise(
                first_component, second_component)
            mock_log_and_exit.assert_called_once_with(
                RC_QAC_MODULES_VERSION_MISMATCH)

    def test_verify_components_compatibility(self):
        """Test verify_components_compatibility()"""

        with patch('swq.qac.qac_utils.LOGGER'), \
            patch('swq.qac.qac_utils.get_components_from_acf_file') \
            as mock_get_components_from_acf_file, \
            patch('swq.qac.qac_utils.get_qac_installed_component_path') \
            as mock_get_qac_installed_component_path, \
            patch('swq.qac.qac_utils.path') as mock_os_path, \
            patch('swq.qac.qac_utils.log_and_exit') as mock_log_and_exit, \
            patch('swq.qac.qac_utils.'
                  'check_if_component_version_matches_and_exit_otherwise') \
            as mock_qac_check_component_version:

            # Component is not present in ACF
            self.config.acf_file = mock.Mock()
            mock_get_components_from_acf_file.return_value = \
                ['qacpp-4.7.0']
            self.config.qac_modules = ['baseline-1.1.0']
            mock_get_qac_installed_component_path.return_value = 'some/path'
            mock_os_path.basename.return_value = 'qacpp-4.7.0'
            qac_utils.verify_components_compatibility(self.config)
            mock_log_and_exit.assert_called_once_with(
                RC_QAC_CONFIGURATION_INCONSISTENT)
            mock_log_and_exit.reset_mock()
            mock_qac_check_component_version.reset_mock()

            # Component is present in ACF, but the version is differ from
            # components folder
            mock_get_components_from_acf_file.return_value = \
                ['qacpp-4.7.0']
            self.config.qac_modules = ['qacpp-4.7.0']
            mock_get_qac_installed_component_path.return_value = 'some/path'
            mock_os_path.basename.return_value = 'qacpp-4.6.0'
            qac_utils.verify_components_compatibility(self.config)
            mock_qac_check_component_version.assert_called()
            mock_log_and_exit.assert_not_called()
            mock_log_and_exit.reset_mock()
            mock_qac_check_component_version.reset_mock()

            # Component from ACF cannot be found in componets folder
            mock_get_components_from_acf_file.return_value = \
                ['qacpp-4.7.0']
            self.config.qac_modules = ['qacpp-4.7.0']
            mock_get_qac_installed_component_path.return_value = None
            mock_os_path.basename.return_value = 'qacpp-4.6.0'
            qac_utils.verify_components_compatibility(self.config)
            mock_qac_check_component_version.assert_not_called()
            mock_log_and_exit.assert_not_called()

    def test_get_module_toolchain(self):
        """Test get_module_toolchain()"""
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<acf xmlversion="2.0.0">
  <components>
    <component version="4.6.0" target="C++" name="qacpp"/>
    <component version="1.1.0" target="C_CPP" name="namecheck"/>
  </components>
</acf>'''

        qacpp_module = 'qacpp-4.6.0'
        namecheck_module = 'namecheck-1.1.0'

        expected_cpp_toolchain = 'C++'
        expected_c_cpp_toolchain = 'C/C++'

        self.config.acf_file = mock.Mock()
        with patch('swq.qac.qac_utils.etree_parse') as mock_etree:
            mocked_getroot = mock.Mock()
            attrs = {'getroot.return_value': ET.fromstring(xml_content)}
            mocked_getroot.configure_mock(**attrs)
            mock_etree.return_value = mocked_getroot

            self.assertEqual(
                qac_utils.get_module_toolchain(self.config, qacpp_module),
                expected_cpp_toolchain)

            self.assertEqual(
                qac_utils.get_module_toolchain(self.config, namecheck_module),
                expected_c_cpp_toolchain)

    def test_resolve_filepath_list_from_path_or_pattern(self):
        """Test resolve_filepath_list_from_path_or_pattern()"""
        with patch('swq.qac.qac_utils.glob') as mock_glob:
            mock_glob.return_value = ["test/test/test.py", "test/test.py"]
            self.assertEqual(
                qac_utils.resolve_filepath_list_from_path_or_pattern(
                    "test.py"), ["test.py"])
            self.assertEqual(
                qac_utils.resolve_filepath_list_from_path_or_pattern(
                    "test/**/*.py"), ["test/test/test.py", "test/test.py"])

    def test_get_files_from_analyze_list(self):
        """Test get_files_from_analyze_list()"""
        self.config.get_absolute_path_or_relative_to_project_root = lambda x: x

        with patch('swq.qac.qac_utils.glob') as mock_glob, \
            patch('swq.qac.qac_utils.get_list_of_files_from_file') \
                    as mock_get_list_of_files_from_file:
            mock_glob.return_value = ["test/test/test.py", "test/test.py"]
            mock_get_list_of_files_from_file.return_value = [
                "test.py", "test/**/*.py"
            ]
            self.assertEqual(
                qac_utils.get_files_from_analyze_list(self.config),
                ["test.py", "test/test/test.py", "test/test.py"])

    @patch('swq.qac.qac_utils.QacVersion')
    def test_optimize_helix_project(self, mock_qac_version):
        """Tests optimize_helix_project()"""
        instance = mock_qac_version.return_value
        file_path = path.join(self.config.custom_config_path,
                              'helix_optimization.txt')
        m_open = mock.mock_open()
        with patch('swq.common.filesystem.filesystem_utils.open', m_open)\
                as mocked_open,\
                patch.object(qac.qac_commands,
                             'delete_file_to_optimize_project') \
                as mock_delete_file_to_optimize_project:

            self.config.disable_optimization = True
            instance.is_helix.return_value = True
            qac_utils.optimize_helix_project(self.config)
            mocked_open.assert_not_called()
            mock_delete_file_to_optimize_project.assert_not_called()

            instance.is_helix.return_value = False
            qac_utils.optimize_helix_project(self.config)
            mocked_open.assert_not_called()
            mock_delete_file_to_optimize_project.assert_not_called()

            self.config.disable_optimization = False
            instance.is_helix.return_value = False
            qac_utils.optimize_helix_project(self.config)
            mocked_open.assert_not_called()
            mock_delete_file_to_optimize_project.assert_not_called()

            instance.is_helix.return_value = True
            qac_utils.optimize_helix_project(self.config)
            mocked_open.assert_called_once_with(file_path,
                                                mode='wt',
                                                buffering=mock.ANY,
                                                encoding='utf-8',
                                                errors=mock.ANY,
                                                newline=mock.ANY,
                                                closefd=mock.ANY,
                                                opener=mock.ANY)
            handle = m_open()
            handle.write.assert_called_once()
            mock_delete_file_to_optimize_project.assert_called_once_with(
                self.config, file_path)

    def test_check_if_return_code_in_skip_list(self):
        """Tests check_if_return_code_in_skip_list()"""
        with patch('swq.qac.qac_utils.log_and_exit') as mock_log_and_exit:
            # skip code is in skip_exit_on_build_return_codes list
            self.config.skip_exit_on_build_return_codes = [0]
            message = ''
            return_code = 0
            exit_code = 1

            qac_utils.check_if_return_code_in_skip_list(
                self.config, return_code, message, exit_code)
            mock_log_and_exit.assert_not_called()

            # skip code is not in skip_exit_on_build_return_codes
            self.config.skip_exit_on_build_return_codes = [1]
            message = ''
            return_code = 2
            exit_code = 1

            qac_utils.check_if_return_code_in_skip_list(
                self.config, return_code, message, exit_code)
            mock_log_and_exit.assert_called_once_with(exit_code)
