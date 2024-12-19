# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_qac_project_creation_config.py
# ----------------------------------------------------------------------------
"""Test for qac/config/qac_project_creation_config.py"""
from unittest import TestCase, mock
from swq.qac.config.qac_project_creation_config import QACProjectCreationConfig

_EXPECTED_RESULT_FILE = 'result.xml'


class ConfigMergerMock(mock.Mock):
    """Mock for config merger class"""
    def run(self):
        """Mock for run() method of config merger class"""
        return _EXPECTED_RESULT_FILE


class TestQACProjectCreationConfig(TestCase):
    """Test class for the qac.config.qac_project_creation_config"""
    def setUp(self):
        self.output_folder_path = 'project_dir'
        self.config_merger = ConfigMergerMock()

    def test_qac_project_creation_config(self):
        """Tests methods of qac_project_creation_config.py"""
        input_config_files = 'config/file1.xml'
        expected_result_string = 'file1.xml'
        config_object = QACProjectCreationConfig(input_config_files,
                                                 self.output_folder_path,
                                                 self.config_merger)
        return_value = config_object.get_input_filepaths()
        self.assertEqual(return_value, input_config_files)
        return_value = config_object.get_input_filenames_as_string()
        self.assertEqual(return_value, expected_result_string)
        self.config_merger.assert_not_called()

        input_config_files = ['config/file1.xml']
        expected_result_string = 'file1.xml'
        config_object = QACProjectCreationConfig(input_config_files,
                                                 self.output_folder_path,
                                                 self.config_merger)
        return_value = config_object.get_input_filepaths()
        self.assertEqual(return_value, input_config_files[0])
        return_value = config_object.get_input_filenames_as_string()
        self.assertEqual(return_value, expected_result_string)
        self.config_merger.assert_not_called()

        input_config_files = ['config/file1.xml', 'config/file2.xml']
        expected_result_string = 'file1.xml,file2.xml'
        config_object = QACProjectCreationConfig(input_config_files,
                                                 self.output_folder_path,
                                                 self.config_merger)
        return_value = config_object.get_input_filepaths()
        self.assertEqual(return_value, input_config_files)
        return_value = config_object.get_input_filenames_as_string()
        self.assertEqual(return_value, expected_result_string)
        self.config_merger.assert_called_once_with(self.output_folder_path,
                                                   input_config_files)

        return_value = config_object.get_result_filepath()
        self.assertEqual(return_value, _EXPECTED_RESULT_FILE)

        input_config_files = None
        config_object = QACProjectCreationConfig(input_config_files,
                                                 self.output_folder_path,
                                                 self.config_merger)
        return_value = config_object.get_input_filepaths()
        self.assertEqual(return_value, None)
        return_value = config_object.get_input_filenames_as_string()
        self.assertEqual(return_value, None)
        return_value = config_object.get_result_filepath()
        self.assertEqual(return_value, None)
