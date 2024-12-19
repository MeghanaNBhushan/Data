# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_project_state.py
# ----------------------------------------------------------------------------
""" Tests for qac/project_state.py """

import os
import json
import xml.etree.ElementTree as ET

from datetime import date
from unittest import TestCase, mock
from unittest.mock import patch
from swq.common.report.constants import LICENSE_WARNING
from swq.qac import project_state
from swq.qac.project_state import ProjectState
from swq.common.return_codes import RC_INVALID_FILEPATH


class TestProjectState(TestCase):
    """ TestProjectState class """
    def setUp(self):
        self.config = mock.Mock(project_git_commit='123',
                                project_root='project/root',
                                qac_project_path='project/path',
                                cli_version_string=None,
                                compiler_list=["GNU_GCC.cct"],
                                acf_file=mock.MagicMock(),
                                ncf_file=mock.MagicMock(),
                                rcf_file=mock.MagicMock(),
                                vcf_file='file.vcf',
                                codeowners_file=None,
                                user_messages=mock.MagicMock(),
                                project_reports_path='project/reports',
                                project_diagnostics_path='project/path/diag',
                                local_baseline_cache_dir_path='cache/baseline',
                                local_baseline_path='baseline',
                                local_baseline_cache_filepath='file.sup',
                                )
        self.project_state = ProjectState(self.config)

    def test_parse_file_root(self):
        """ Test _parse_file_root """
        with patch('swq.qac.project_state.LOGGER'), \
                patch('swq.qac.project_state.normalize_path'), \
                patch.object(ProjectState, '_generate_consolidated_json') \
                as mock_generate_consolidated_json, \
                patch.object(ProjectState,
                             '_add_violations_per_file_to_dict'), \
                patch.object(ProjectState, '_add_summary_per_file_to_dict'), \
                patch('os.path.exists') as mock_path_exists:

            mock_path_exists.return_value = False
            self.project_state.create()
            mock_generate_consolidated_json.assert_called_with(None)

            xml_content = '<?xml version="1.0" encoding="UTF-8"?>\
<AnalysisData>\
<dataroot type="per-file">\
<File path="/src/stack.cpp">\
</File>\
</dataroot>\
</AnalysisData>'

            with patch('swq.qac.project_state.etree_parse') as mock_etree,\
                    patch('swq.qac.project_state.calculate_sha256'):
                mocked_getroot = mock.Mock()
                attrs = {'getroot.return_value': ET.fromstring(xml_content)}
                file_root = attrs['getroot.return_value'].find('dataroot')
                mocked_getroot.configure_mock(**attrs)
                mock_etree.return_value = mocked_getroot
                mock_path_exists.return_value = True
                self.project_state.create()
                mock_generate_consolidated_json.assert_called_with(file_root)

    def test_generate_consolidated_json(self):
        """ Test _generate_consolidated_json """
        with patch('swq.qac.project_state.LOGGER'), \
                patch('swq.qac.project_state.normalize_path'), \
                patch.object(ProjectState, '_parse_file_root') \
                as mock_parse_file_root, \
                patch.object(ProjectState,
                             '_add_violations_per_file_to_dict') \
                as mock_add_violations_per_file_to_dict, \
                patch.object(ProjectState, '_add_summary_per_file_to_dict'):

            mock_parse_file_root.return_value = None
            self.project_state.create()
            mock_add_violations_per_file_to_dict.assert_called_with({})
            mock_add_violations_per_file_to_dict.reset_mock()

            xml_content = '<?xml version="1.0" encoding="UTF-8"?>\
<AnalysisData>\
<dataroot type="per-file">\
<File path="/src/stack.cpp">\
</File>\
</dataroot>\
</AnalysisData>'

            xml_parsed = ET.fromstring(xml_content)
            file_root = xml_parsed.find('dataroot')
            mock_parse_file_root.return_value = file_root
            self.project_state.create()
            mock_add_violations_per_file_to_dict.assert_called_with({})
            mock_add_violations_per_file_to_dict.reset_mock()

            xml_content = '<?xml version="1.0" encoding="UTF-8"?>\
<AnalysisData>\
<dataroot type="per-file">\
<File path="/src/stack.cpp">\
<Json>/project/data/1.json</Json>\
</File>\
</dataroot>\
</AnalysisData>'

            json_data = '{}'
            xml_parsed = ET.fromstring(xml_content)
            file_root = xml_parsed.find('dataroot')
            mock_parse_file_root.return_value = file_root
            with patch('swq.common.filesystem.filesystem_utils.open',
                       new=mock.mock_open(read_data=json_data)):
                self.project_state.create()
                mock_add_violations_per_file_to_dict.assert_called_with({})
                mock_add_violations_per_file_to_dict.reset_mock()

            json_data = '{"key": "value"}'
            with patch('swq.common.filesystem.filesystem_utils.open',
                       new=mock.mock_open(read_data=json_data)), \
                    patch('os.path.normpath') as mock_normpath, \
                    patch('swq.qac.project_state.normalize_path') \
                    as mock_normalize_path, \
                    patch.object(project_state, '_create_file_metrics') \
                    as mock_create_file_metrics:

                mock_normalize_path.return_value = None
                self.project_state.create()
                mock_add_violations_per_file_to_dict.assert_called_with({})
                mock_add_violations_per_file_to_dict.reset_mock()

                filepath = '/src/stack.cpp'
                mock_normpath.return_value = filepath
                mock_normalize_path.return_value = filepath
                mock_create_file_metrics.return_value = 'foo'
                project_data = {}
                project_data[filepath] = mock_create_file_metrics.return_value
                self.project_state.create()
                mock_create_file_metrics.assert_called_with(
                    filepath, json.loads(json_data))
                mock_add_violations_per_file_to_dict.assert_called_with(
                    project_data)
                mock_add_violations_per_file_to_dict.reset_mock()

    @patch('os.path.exists')
    @patch('swq.qac.project_state.walk')
    @patch('swq.qac.project_state.etree_parse')
    def test_add_violations_per_file_to_dict(self, mock_etree, mock_os_walk,
                                             mock_path_exists):
        """ Test _add_violations_per_file_to_dict """

        with patch('swq.qac.project_state.LOGGER'), \
                patch.object(ProjectState, '_parse_file_root'), \
                patch('swq.qac.project_state.normalize_path') \
                as mock_normalize_path, \
                patch.object(ProjectState, '_generate_consolidated_json') \
                as mock_generate_consolidated_json, \
                patch.object(ProjectState,
                             '_add_summary_per_file_to_dict'), \
                patch.object(project_state,
                             '_log_error_if_file_not_in_analysis'), \
                patch('swq.qac.project_state.export_diagnostics'), \
                patch('swq.qac.project_state.log_and_exit') \
                as mock_log_and_exit, \
                patch('swq.qac.project_state.calculate_sha256'):

            mock_path_exists.return_value = False
            result = self.project_state.create()
            mock_log_and_exit.assert_called_with(RC_INVALID_FILEPATH)
            mock_log_and_exit.reset_mock()

            xml_content = '\
<Output>\
    <File>\
        <Name>src\\stack.cpp</Name>\
        <Diag id="1">\
            <Line>7</Line>\
            <Column>1</Column>\
            <Producer>qacpp-4.5.0</Producer>\
            <MsgText>This C style comment, comments out source code.</MsgText>\
            <Severity>5</Severity>\
            <SuppMask>0</SuppMask>\
            <SuppJust></SuppJust>\
            <RuleGroup>MCPP Rule 2,severitylevels</RuleGroup>\
            <RuleNum>Rule 2-7-2,severitylevel5</RuleNum>\
        </Diag>\
    </File>\
</Output>'

            expected_result = {
                'line': '7',
                'column': '1',
                'msgtext': 'This C style comment, comments out source code.',
                'severity': '5',
                'suppmask': '0',
                'suppjust': '',
                'producer': 'qacpp-4.5.0',
                'rulenum': 'Rule 2-7-2,severitylevel5'
            }

            mock_path_exists.return_value = True
            mock_os_walk.return_value = [('src', [], ['stack.cpp-diag.xml'])]
            mocked_getroot = mock.Mock()
            attrs = {'getroot.return_value': ET.fromstring(xml_content)}
            mocked_getroot.configure_mock(**attrs)
            mock_etree.return_value = mocked_getroot
            mock_generate_consolidated_json.return_value = {}
            analyzed_file = os.path.join('src', 'stack.cpp')
            mock_normalize_path.return_value = analyzed_file
            result = self.project_state.create()
            for key, expected_value in expected_result.items():
                self.assertEqual(
                    result['analysis'][analyzed_file]['findings'][0].get(key),
                    expected_value)
            mock_log_and_exit.assert_not_called()

    def test_add_summary_per_file_to_dict(self):
        """ Test _add_summary_per_file_to_dict """

        with patch('swq.qac.project_state.LOGGER'), \
                patch.object(ProjectState, '_parse_file_root'), \
                patch('swq.qac.project_state.normalize_path') \
                as mock_normalize_path, \
                patch.object(ProjectState, '_generate_consolidated_json') \
                as mock_generate_consolidated_json, \
                patch.object(ProjectState,
                             '_add_violations_per_file_to_dict'), \
                patch('os.path.exists') as mock_path_exists, \
                patch('swq.qac.project_state.etree_parse') as mock_etree, \
                patch.object(project_state,
                             '_log_error_if_file_not_in_analysis') \
                as mock_log_error_if_file_not_in_analysis, \
                patch.object(ProjectState, '_parse_analyse_logs') \
                as mock_parse_analyse_logs, \
                patch('swq.qac.project_state.calculate_sha256'):

            mock_path_exists.return_value = False
            self.project_state.create()
            mock_etree.assert_not_called()

            analyzed_file = '/src/stack.cpp'
            xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<File>
<Name>{}</Name>
<Severity id="0">0</Severity>
<Severity id="1">0</Severity>
<Severity id="2">0</Severity>
<Severity id="3">0</Severity>
<Severity id="4">0</Severity>
<Severity id="5">1</Severity>
<Severity id="6">0</Severity>
<Severity id="7">0</Severity>
<Severity id="8">0</Severity>
<Severity id="9">0</Severity>
<SeverityTotal>1</SeverityTotal>
<AnalysisErrorCount>0</AnalysisErrorCount>
<AnalysisExitStatus>1</AnalysisExitStatus>
</File>'''.format(analyzed_file)
            analysis = {}
            analysis[analyzed_file] = {'summary': 'foo'}

            mock_path_exists.return_value = True
            mock_generate_consolidated_json.return_value = analysis
            mocked_getroot = mock.Mock()
            attrs = {'getroot.return_value': ET.fromstring(xml_content)}
            mocked_getroot.configure_mock(**attrs)
            mock_etree.return_value = mocked_getroot
            mock_normalize_path.return_value = analyzed_file
            analysis_output = {}
            analysis_output[analyzed_file] = 'analysis output'
            mock_parse_analyse_logs.return_value = analysis_output
            result = self.project_state.create()
            mock_normalize_path.assert_called_with(self.config.project_root,
                                                   analyzed_file)
            mock_log_error_if_file_not_in_analysis.assert_called_with(
                analysis, analyzed_file)
            self.assertEqual(
                result['analysis'][analyzed_file]['summary'].get(
                    'analysis_log'), analysis_output[analyzed_file])

    def test_create_without_vcf_and_ncf_files(self):
        """ Test create() method without providing vcf and ncf files """
        config = self.config
        config.vcf_file = None
        config.ncf_file = None
        project_state_without_vcf_and_ncf = ProjectState(config)

        with patch('swq.qac.project_state.LOGGER'), \
                patch('swq.qac.project_state.normalize_path') \
                as mock_normalize_path, \
                patch.object(ProjectState, '_generate_consolidated_json') \
                as mock_generate_consolidated_json, \
                patch.object(ProjectState,
                             '_add_violations_per_file_to_dict') \
                as mock_add_violations_per_file_to_dict, \
                patch.object(ProjectState, '_add_summary_per_file_to_dict') \
                as mock_add_summary_per_file_to_dict, \
                patch.object(ProjectState, '_parse_file_root') \
                as mock_parse_file_root, \
                patch('swq.qac.project_state.datetime') as mock_datetime:
            expected_date = date(2020, 1, 1)
            expected_normailzed_path = 'normalized_path'
            mock_normalize_path.return_value = expected_normailzed_path
            mock_parse_file_root.return_value = 'file_root'
            mock_datetime.date.return_value = expected_date
            mock_generate_consolidated_json.return_value = 'json'

            actual_result = project_state_without_vcf_and_ncf.create()

            expected_state_analysis_argument = 'json'
            expected_file_root_argument = 'file_root'
            expected_result = {
                'license': LICENSE_WARNING,
                'git_commit':
                self.config.project_git_commit,
                'project_root':
                self.config.project_root,
                'prqa_project_relative_path':
                expected_normailzed_path,
                'cli_version':
                self.config.cli_version_string,
                'timestamp':
                mock_datetime.now().strftime('%Y_%m_%d_%H_%M_%S'),
                'acf':
                self.config.acf_file.get_input_filenames_as_string(),
                'cct':
                self.config.compiler_list[0],
                'ncf':
                '',
                'rcf':
                self.config.rcf_file.get_input_filenames_as_string(),
                'vcf':
                None,
                'user_messages':
                self.config.user_messages.get_input_filenames_as_string(),
                'cache_baseline_path':
                self.config.local_baseline_cache_dir_path,
                'local_baseline_path':
                self.config.local_baseline_path,
                'local_baseline_sha': '',
                'analysis':
                expected_state_analysis_argument
            }
            mock_generate_consolidated_json.assert_called_with(
                expected_file_root_argument)
            mock_add_violations_per_file_to_dict.assert_called_with(
                expected_state_analysis_argument)
            mock_add_summary_per_file_to_dict.assert_called_with(
                expected_state_analysis_argument)
            mock_parse_file_root.assert_called_once()

            self.assertEqual(actual_result, expected_result)
