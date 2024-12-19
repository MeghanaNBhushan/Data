""" Tests for coverity/exporters/state_exporter.py """

from json import loads
from unittest import TestCase, mock
from unittest.mock import patch
from swq.coverity.exporters import state_exporter
from swq.coverity.constants import \
    ERROR_EXPORT_TABLE_MAIN_EVENT_FILEPATH_INDEX, \
    PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX, EXPORT_DIR


class TestCoverityStateExporter(TestCase):
    """ TestCoverityStateExporter class """
    def setUp(self):
        self.config = mock.Mock(webapi_url='localhost',
                                webapi_view_name='test',
                                webapi_project_name='test_project',
                                project_root='/path/to/project/root',
                                webapi_coverity_user='user',
                                webapi_coverity_passcode='pass',
                                view_contents_export_filepath='view.json',
                                include_triage_history=None,
                                triage_store=None,
                                translation_units_blacklist=[],
                                export_formats=['csv'])

    def test_read_cov_format_errors(self):
        """ Test read_cov_format_errors """
        json_file = '/foo/bar/export.json'
        json_data = '{"issues": []}'
        expected_return = []
        with patch('swq.coverity.exporters.state_exporter.LOGGER'), \
                patch('swq.coverity.exporters.state_exporter.open_t',
                      new=mock.mock_open()) as mocked_open, \
                patch('swq.coverity.exporters.state_exporter.load') \
                as mock_json_load:
            mock_json_load.return_value = loads(json_data)
            return_value = state_exporter.read_cov_format_errors(json_file)
            mocked_open.assert_called_with(json_file)
            self.assertEqual(return_value, expected_return)

    def test_cov_format_errors_export(self):
        """ Test cov_format_errors_export """
        json_file = '/foo/bar/export.json'
        with patch('swq.coverity.exporters.state_exporter.LOGGER'), \
                patch.object(state_exporter, 'read_cov_format_errors') \
                as mock_read_cov_format_errors, \
                patch.object(state_exporter, '_create_exporters') \
                as mock_create_exporters, \
                patch.object(state_exporter, 'no_regex_matches') \
                as mock_no_regex_matches, \
                patch.object(state_exporter, 'generate_sheet'), \
                patch('swq.coverity.exporters.state_exporter.ComponentMapper'):

            mock_read_cov_format_errors.return_value = [[
                'path/to/file.cpp', 'sha', 1, 1, 'foo', 'foo', '', '', '',
                'm2', 'STATIC_C', 'C++', 239, 'bar', 'baz', 'Null pointer',
                'Null pointer', '476', 'Medium', 'Medium',
                'A null pointer dereference will occur.',
                'Explicit null dereferenced',
                'Dereference of an explicit null value',
                '/full/path/to/file.cpp'
            ]]

            self.config.export_formats = ['csv']
            state_exporter.cov_format_errors_export(self.config, json_file)
            mock_read_cov_format_errors.assert_called_with(json_file)
            mock_create_exporters.assert_called_with(self.config, EXPORT_DIR,
                                                     '/foo/bar')
            mock_create_exporters.reset_mock()

            self.config.translation_units_blacklist = ["/full"]
            mock_no_regex_matches.return_value = False
            state_exporter.cov_format_errors_export(self.config, json_file)
            calls_filtered = mock.call(self.config, 'export-filtered',
                                       '/foo/bar')
            calls_nonfiltered = mock.call(self.config, 'export', '/foo/bar')
            mock_create_exporters.assert_has_calls(
                [calls_filtered, calls_nonfiltered], any_order=True)
            mock_create_exporters.reset_mock()
            mock_no_regex_matches.return_value = True
            state_exporter.cov_format_errors_export(self.config, json_file)
            mock_no_regex_matches.assert_called_with(
                self.config.translation_units_blacklist,
                mock_read_cov_format_errors.return_value[0]
                [ERROR_EXPORT_TABLE_MAIN_EVENT_FILEPATH_INDEX])
            mock_create_exporters.reset_mock()

            self.config.export_formats = ['stdout']
            mock_no_regex_matches.return_value = False
            state_exporter.cov_format_errors_export(self.config, json_file)
            mock_create_exporters.assert_called_once_with(
                self.config, 'export-filtered', '/foo/bar')

            mock_create_exporters.reset_mock()

            self.config.export_formats = ['vscode']
            mock_no_regex_matches.return_value = False
            state_exporter.cov_format_errors_export(self.config, json_file)
            mock_create_exporters.assert_called_once_with(
                self.config, 'export-filtered', '/foo/bar')
            mock_create_exporters.reset_mock()

            self.config.export_formats = ['stdout']
            self.config.translation_units_blacklist = []
            mock_no_regex_matches.return_value = False
            state_exporter.cov_format_errors_export(self.config, json_file)
            mock_create_exporters.assert_called_once_with(
                self.config, 'export', '/foo/bar')
            mock_create_exporters.reset_mock()

            self.config.export_formats = ['vscode']
            mock_no_regex_matches.return_value = False
            state_exporter.cov_format_errors_export(self.config, json_file)
            mock_create_exporters.assert_called_once_with(
                self.config, 'export', '/foo/bar')
            mock_create_exporters.reset_mock()
            self.config.export_formats = ['csv']

    def test_read_cov_commit_defects(self):
        """ Test read_cov_commit_defects """
        json_file = '/foo/bar/export.json'
        json_data = '{"issueInfo": []}'
        expected_return = []
        with patch('swq.coverity.exporters.state_exporter.LOGGER'), \
                patch('swq.coverity.exporters.state_exporter.open_t',
                      new=mock.mock_open()) as mocked_open, \
                patch('swq.coverity.exporters.state_exporter.load') \
                as mock_json_load:
            mock_json_load.return_value = loads(json_data)
            return_value = state_exporter.read_cov_commit_defects(json_file)
            mocked_open.assert_called_with(json_file)
            self.assertEqual(return_value, expected_return)

    def test_cov_commit_defects_export(self):
        """ Test cov_commit_defects_export """
        json_file = '/foo/bar/export.json'
        with patch('swq.coverity.exporters.state_exporter.LOGGER'), \
                patch.object(state_exporter, 'read_cov_commit_defects') \
                as mock_read_cov_commit_defects, \
                patch.object(state_exporter, '_create_exporters') \
                as mock_create_exporters, \
                patch.object(state_exporter, 'generate_sheet'), \
                patch('swq.coverity.exporters.state_exporter.ComponentMapper'):
            state_exporter.cov_commit_defects_export(self.config, json_file)
            mock_read_cov_commit_defects.assert_called_with(json_file)
            mock_create_exporters.assert_called_with(self.config, EXPORT_DIR,
                                                     '/foo/bar')
            mock_create_exporters.reset_mock()
            with patch.object(state_exporter, 'no_regex_matches') \
                    as mock_no_regex_matches:
                mock_read_cov_commit_defects.return_value = [[
                    2915665, 'sha', False, 'date', 'Unspecified', None, None,
                    'False', 'Untargeted', 'Undecided', 'Unclassified',
                    'Unspecified', 'VALUE', '/full/path/to/file.cpp', '', '',
                    False, '', 3277, 'Message', 'mod', None
                ]]
                self.config.translation_units_blacklist = ["/full"]
                mock_no_regex_matches.return_value = False

                state_exporter.cov_commit_defects_export(
                    self.config, json_file)
                mock_create_exporters.assert_has_calls(
                    [mock.call(self.config, 'export-filtered', '/foo/bar')])
                state_exporter.cov_commit_defects_export(
                    self.config, json_file)
                mock_create_exporters.reset_mock()
                mock_no_regex_matches.return_value = True
                state_exporter.cov_commit_defects_export(
                    self.config, json_file)
                mock_no_regex_matches.assert_called_with(
                    self.config.translation_units_blacklist,
                    mock_read_cov_commit_defects.return_value[0]
                    [PREVIEW_EXPORT_TABLE_COLUMN_FILEPATH_INDEX])

    @patch.object(state_exporter, '_get_view_contents')
    @patch('swq.coverity.exporters.state_exporter.DefectServiceClient')
    @patch('swq.coverity.exporters.state_exporter.ConfigServiceClient')
    def test_coverity_connect_webapi_export(self, mock_config_service_client,
                                            mock_defect_service_client,
                                            mock_get_view_contents):
        """ Test coverity_connect_webapi_export """
        json_data = {'viewContentsV1': {'columns': [], 'rows': []}}
        with patch('swq.coverity.exporters.state_exporter.LOGGER'), \
                patch(
                        'swq.coverity.exporters.state_exporter.open_t') \
                as mocked_open, \
                patch.object(state_exporter, 'generate_sheet'), \
                patch('swq.coverity.exporters.state_exporter.dump'), \
                patch.object(state_exporter, '_create_exporters'):

            defect_instance = mock_defect_service_client.return_value
            config_instance = mock_config_service_client.return_value
            mock_get_view_contents.return_value = json_data
            state_exporter.coverity_connect_webapi_export(self.config)
            mocked_open.assert_called_with(
                self.config.view_contents_export_filepath, mode='w')
            mock_defect_service_client.assert_not_called()
            mock_config_service_client.assert_not_called()

            json_data = {
                'viewContentsV1': {
                    'columns': [{
                        'name': 'cid'
                    }, {
                        'name': 'status'
                    }],
                    'rows': [{
                        'cid': 708125,
                        'status': 'New'
                    }]
                }
            }
            mock_get_view_contents.return_value = json_data
            self.config.include_triage_history = True
            self.config.triage_store = 'Default'
            state_exporter.coverity_connect_webapi_export(self.config)
            mock_defect_service_client.assert_called_with(self.config)
            mock_config_service_client.assert_called_with(self.config)
            defect_instance.client.service.getTriageHistory.assert_not_called()

            json_data['viewContentsV1']['rows'][0]['status'] = 'Triaged'
            mock_get_view_contents.return_value = json_data
            self.config.include_triage_history = True
            self.config.triage_store = 'Default'
            state_exporter.coverity_connect_webapi_export(self.config)
            config_instance.client.factory.create.assert_called()
            defect_instance.client.service.getTriageHistory.assert_called()
