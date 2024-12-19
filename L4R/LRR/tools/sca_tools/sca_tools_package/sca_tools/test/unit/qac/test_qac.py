# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_qac.py
# ----------------------------------------------------------------------------
""" Tests for qac/qac.py """

from os import path
from shutil import Error
from unittest import TestCase, mock
from unittest.mock import patch
from swq.qac import qac


class TestQac(TestCase):
    """ TestQac class """
    def setUp(self):
        self.config = mock.Mock(
            project_root='not/existing/path',
            helper_logs_path='helper/logs',
            qac_project_path='qac/project/path')

    @patch('swq.qac.qac.LOGGER', create=True)
    @patch('swq.qac.qac.QacVersion')
    @patch.object(qac, 'safe_delete_dirtree')
    @patch.object(qac, 'copytree')
    def test_report(self, mock_copytree, mock_safe_delete_dirtree,
                    mock_qac_version, logger):
        """ Test report() """

        instance = mock_qac_version.return_value
        mock_safe_delete_dirtree.return_value = None
        mock_copytree.return_value = None

        with patch.object(qac.qac_commands, 'export_report')\
                as mock_qac_command_export_report:
            mock_qac_command_export_report.return_value = ['Command Output', 0]

            instance.major_minor.return_value = (2019, 2)
            instance.is_helix.return_value = True
            report_path = path.join(self.config.qac_project_path, "report")
            report_type = 'RCR'
            copy_to_report = False
            self.assertEqual(
                qac.report(self.config, report_type, copy_to_report),
                report_path)
            mock_qac_command_export_report.assert_called_with(
                self.config,
                report_type,
                parallel=False,
                ignore_dependencies=True)
            logger.error.assert_not_called()

            instance.major_minor.return_value = (2020, 2)
            self.assertEqual(
                qac.report(self.config, report_type, copy_to_report),
                report_path)
            mock_qac_command_export_report.assert_called_with(
                self.config,
                report_type,
                parallel=True,
                ignore_dependencies=True)
            logger.error.assert_not_called()

            instance.major_minor.return_value = (2018, 2)
            self.assertEqual(
                qac.report(self.config, report_type, copy_to_report),
                report_path)
            mock_qac_command_export_report.assert_called_with(
                self.config,
                report_type,
                parallel=False,
                ignore_dependencies=False)
            logger.error.assert_not_called()

            copy_to_report = True
            self.assertEqual(
                qac.report(self.config, report_type, copy_to_report),
                report_path)
            logger.error.assert_not_called()

            mock_safe_delete_dirtree.side_effect = Error('Boom!')
            self.assertEqual(
                qac.report(self.config, report_type, copy_to_report),
                report_path)
            logger.error.assert_called()

    @patch('swq.qac.qac.LOGGER', create=True)
    def test_upload_to_qa_verify(self, logger):
        """ Test upload_to_qa_verify() """

        with patch.object(qac.qac_commands, 'upload_qaf_project') \
            as mock_upload_qaf_project,\
                patch.object(qac, 'save_output') as mock_save_output:
            mock_upload_qaf_project.return_value = ['Output', 0]
            mock_save_output.return_value = None

            qac.upload_to_qa_verify(self.config)
            mock_upload_qaf_project.assert_called_once_with(self.config)
            mock_save_output.assert_called()

            mock_upload_qaf_project.return_value = ['Output', 1]
            qac.upload_to_qa_verify(self.config)
            logger.error.assert_called()
