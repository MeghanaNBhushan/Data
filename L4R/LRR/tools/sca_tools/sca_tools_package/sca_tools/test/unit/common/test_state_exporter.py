"""Tests for qac/exporters/state_exporter.py"""

import os
from datetime import datetime
from unittest.mock import patch
from unittest import TestCase, mock
from swq.common.export.sheet import Sheet
from swq.common.return_codes import RC_CONFIG_PARSING_ERROR
from swq.qac.exporters.state_exporter import export_view_summary, \
    export_view_html_summary, export_analysis_report, export_reports, \
    QAVIEW_TABLE_COLUMN_SEVERITY_LEVEL_INFO_INDEX
from swq.qac.constants import QAVIEW_TABLE_COLUMN_IDS_INDEX
from swq.qac.constants import SCA_TOOL_DIR, EXPORT_DIR


class TestStateExporter(TestCase):
    """Test State exporter methods"""
    class MockZipf:
        """Mocked ZIP class"""
        def __init__(self):
            self.files = [
                mock.Mock(filename='foo.csv'),
                mock.Mock(filename='bar.csv')
            ]

        def __iter__(self):
            return iter(self.files)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return True

    def setUp(self):
        self.qac_project_path = os.path.join('path', 'to', 'qac')
        self.config = mock.Mock(export_format="xlsx",
                                qac_project_path=self.qac_project_path,
                                project_root="path/to/project/root",
                                compiler_list=[],
                                acf_file=mock.MagicMock(),
                                rcf_file=mock.MagicMock(),
                                user_messages=mock.MagicMock(),
                                cli_version_string="0.0.1",
                                project_git_commit="commit",
                                local_baseline_cache_dir_path="baseline",
                                local_baseline_path="baseline",
                                generate_html=True,
                                metrics_filter_list=None,
                                codeowners_file=None,
                                only_last_team=None,
                                with_metrics=False,
                                with_full_subdiagnostics=False)

        self.config.rcf_file.get_input_filenames_as_string.return_value =\
            'rcf_file.rcf'
        self.config.user_messages.get_input_filenames_as_string.return_value =\
            'user_messages.xml'
        self.git_commit = '1234'

    @patch("swq.qac.exporters.state_exporter.open_t")
    @patch("swq.qac.exporters.state_exporter._get_open_closed_issues_from_all")
    @patch("swq.qac.exporters.state_exporter.XlsxExporter")
    @patch("swq.qac.exporters.state_exporter.CsvExporter")
    @patch("swq.qac.exporters.state_exporter.ZippedCsvExporter")
    def test_create_exporters(self, zipped_csv, csv, xlsx, get_open_closed,
                              mock_open_t):
        """Test _create_exporters() method"""
        xlsx.return_value = mock.Mock(create_sheet=Sheet, append_rows=0)
        zipped_csv.return_value = mock.Mock(create_sheet=Sheet, append_rows=0)
        csv.return_value = mock.Mock(create_sheet=Sheet, append_rows=0)

        get_open_closed.return_value = ["key", "value"]

        self.config.export_formats = ["xlsx"]
        export_view_summary(self.config, "")
        xlsx.assert_called()
        mock_open_t.assert_called()
        zipped_csv.assert_not_called()
        csv.assert_not_called()

        xlsx.reset_mock()
        zipped_csv.reset_mock()
        csv.reset_mock()
        mock_open_t.reset_mock()

        self.config.export_formats = ["csv"]
        export_view_summary(self.config, "")
        mock_open_t.assert_called()
        xlsx.assert_not_called()
        zipped_csv.assert_not_called()
        csv.assert_called()

        mock_open_t.reset_mock()
        xlsx.reset_mock()
        zipped_csv.reset_mock()
        csv.reset_mock()

        self.config.export_formats = ["csv_zip"]
        export_view_summary(self.config, "")
        mock_open_t.assert_called()
        xlsx.assert_not_called()
        zipped_csv.assert_called()
        csv.assert_not_called()

        mock_open_t.reset_mock()
        xlsx.reset_mock()
        zipped_csv.reset_mock()
        csv.reset_mock()

        self.config.export_formats = ["html"]
        export_view_summary(self.config, "")
        mock_open_t.assert_called()
        xlsx.assert_not_called()
        zipped_csv.assert_not_called()
        csv.assert_not_called()

        mock_open_t.reset_mock()
        xlsx.reset_mock()
        zipped_csv.reset_mock()
        csv.reset_mock()

        self.config.export_formats = ["csv", "xlsx"]
        export_view_summary(self.config, "")
        mock_open_t.assert_called()
        xlsx.assert_called()
        csv.assert_called()
        zipped_csv.assert_not_called()

    @patch("swq.qac.exporters.state_exporter.open_t")
    @patch("swq.qac.exporters.state_exporter._create_exporters")
    @patch("swq.qac.exporters.state_exporter.calculate_aggregated_summary")
    @patch("swq.qac.exporters.state_exporter.get_warning_summary_per_rule_text"
           )
    @patch("swq.qac.exporters.state_exporter."
           "get_warning_summary_per_producer_component")
    def test_get_open_closed_issues_from_all(self, get_message_summary,
                                             get_warning_summary, count_number,
                                             create_exporters, mock_open_t):
        """Test _get_open_closed_issues_from_alls() method"""

        create_exporters.return_value = [
            mock.Mock(create_sheet=Sheet, append_rows=mock.Mock())
        ]
        csv_values = {"key": "value"}
        get_message_summary.return_value = csv_values
        get_warning_summary.return_value = csv_values
        count_number.return_value = csv_values

        export_view_summary(self.config, csv_values)
        count_number.assert_called_with(csv_values,
                                        self.config.with_full_subdiagnostics)
        mock_open_t.assert_called()

    @patch("swq.qac.exporters.state_exporter.open_t")
    @patch("swq.qac.exporters.state_exporter._create_exporters")
    @patch("swq.qac.exporters.state_exporter."
           "aggregate_warnings_summary_per_entity")
    @patch("swq.qac.exporters.state_exporter."
           "get_warning_summary_per_producer_component")
    def test_get_warning_summary_per_rule_text(self, get_message_summary,
                                               compile_warning_summary,
                                               create_exporters, mock_open_t):
        """Test get_warning_summary_per_rule_text() method"""

        create_exporters.return_value = [
            mock.Mock(create_sheet=Sheet, append_rows=mock.Mock())
        ]
        csv_values = {"key": "value"}
        column_id = QAVIEW_TABLE_COLUMN_SEVERITY_LEVEL_INFO_INDEX
        get_message_summary.return_value = csv_values
        compile_warning_summary.return_value = csv_values

        export_view_summary(self.config, csv_values)
        mock_open_t.assert_called()
        compile_warning_summary.assert_called_with(
            csv_values, column_id, self.config.with_full_subdiagnostics)

    @patch("swq.qac.exporters.state_exporter."
           "aggregate_warnings_summary_per_entity")
    @patch("swq.qac.exporters.state_exporter.get_warning_summary_per_rule_text"
           )
    def test_get_warning_summary_per_producer_component(
            self, get_warning_summary, compile_warning_summary):
        """Test get_warning_summary_per_producer_component() method"""

        csv_values = {"key": "value"}
        column_id = QAVIEW_TABLE_COLUMN_IDS_INDEX
        get_warning_summary.return_value = csv_values
        compile_warning_summary.return_value = csv_values
        with patch('swq.qac.exporters.state_exporter._create_exporters') as \
            mocked_create_exporters, \
            patch("swq.qac.exporters.state_exporter.open_t") as mock_open_t:
            mocked_create_exporters.return_value = [mock.Mock()]
            export_view_summary(self.config, csv_values)
            compile_warning_summary.assert_called_with(
                csv_values, column_id, self.config.with_full_subdiagnostics)
            mock_open_t.assert_called()

    @patch("swq.qac.exporters.state_exporter.export_view_html_summary")
    @patch("swq.qac.exporters.state_exporter._create_exporters")
    @patch("swq.qac.exporters.state_exporter._get_open_closed_issues_from_all")
    @patch("swq.qac.exporters.state_exporter.get_warning_summary_per_rule_text"
           )
    @patch("swq.qac.exporters.state_exporter."
           "get_warning_summary_per_producer_component")
    def test_export_view_summary(self, get_message_summary,
                                 get_warning_summary, get_open_closed,
                                 create_exporters,
                                 export_view_html_summary_mock):
        """Test export_view_summary() method"""
        get_message_summary.return_value = [1]
        get_warning_summary.return_value = [1]
        get_open_closed.return_value = [1]

        create_exporters.return_value = [
            mock.Mock(create_sheet=mock.Mock(), append_rows=mock.Mock())
        ]

        instance = create_exporters.return_value[0]

        csv_values = {"key": "value"}

        export_view_summary(self.config, csv_values)
        export_view_html_summary_mock.assert_called()

        get_open_closed.assert_called_with(
            csv_values, self.config.with_full_subdiagnostics)
        instance.create_sheet.assert_called_with('summary')
        instance.create_sheet.return_value.append_rows.assert_called_with([1])
        instance.save.assert_called()

    @patch("swq.qac.exporters.state_exporter.path")
    @patch("swq.qac.exporters.state_exporter._get_open_closed_issues_from_all")
    @patch("swq.qac.exporters.state_exporter.create_html_from_list_of_lists")
    def test_export_view_html_summary(self, create, get_open_closed, path):
        """Test export_view_html_summarys() method"""
        get_open_closed.return_value = 1
        create.return_value = 2
        path.join.return_value = os.path.join(self.config.qac_project_path,
                                              "qacli-view-summary.html")
        path.join.return_value = path.join.return_value.replace('\\', '/')
        path.basename.return_value = 0

        csv_values = {"key": "value"}

        # pylint: disable=W0622
        with patch("swq.qac.exporters.state_exporter.LOGGER") as logger, \
            patch("builtins.open", new_callable=mock.mock_open,
                  read_data="data") as mocked_open:
            export_view_html_summary(self.config, csv_values)
            logger.info.assert_called()
            mocked_open.assert_called_with(
                "path/to/qac/qacli-view-summary.html",
                mode='w+t',
                buffering=mock.ANY,
                encoding='utf-8',
                errors=mock.ANY,
                newline=mock.ANY,
                closefd=mock.ANY,
                opener=mock.ANY)
            mocked_open.return_value.write.assert_called_with(2)

        path.join.assert_called_with(self.config.qac_project_path,
                                     SCA_TOOL_DIR, EXPORT_DIR,
                                     "qacli-view-summary.html")

    @patch("swq.qac.exporters.state_exporter._create_exporters")
    @patch("swq.qac.exporters.state_exporter._get_open_closed_issues_from_all")
    @patch("swq.qac.exporters.state_exporter.get_warning_summary_per_rule_text"
           )
    @patch("swq.qac.exporters.state_exporter."
           "get_warning_summary_per_producer_component")
    def test_export_analysis_report(self, get_message_summary,
                                    get_warning_summary, get_open_closed,
                                    create_exporters):
        """Test export_analysis_report() method"""
        with patch("swq.qac.exporters.state_exporter.datetime") as dt_mock,\
                patch("swq.qac.exporters.state_exporter.path") as path, \
                patch("swq.qac.exporters.state_exporter.LICENSE_WARNING",
                      "license"):
            dt_mock.now.return_value = datetime(2020, 2, 1, 10, 9, 8)
            get_message_summary.return_value = [1]
            get_warning_summary.return_value = [1]
            get_open_closed.return_value = [1]
            csv_values = ["key", "value80"]

            create_exporters.return_value = [
                mock.Mock(create_sheet=mock.Mock(),
                          append_rows=mock.Mock(),
                          enable_filters=mock.Mock())
            ]

            instance = create_exporters.return_value[0]

            path.exists = mock.Mock(return_value=False)
            export_analysis_report(self.config, self.config.project_git_commit,
                                   csv_values)

            instance.create_sheet.assert_any_call("info")
            instance.create_sheet.assert_any_call("summary")
            instance.create_sheet.assert_any_call("view")

            create_exporters.assert_called_with(self.config, 'qacli', 'view')

            append_rows = instance.create_sheet.return_value.append_rows
            append_rows.assert_any_call([1])
            append_rows.assert_any_call(csv_values)
            append_rows.assert_any_call(
                [['License', 'license'], ['Date', '01/02/2020 10:09:08'],
                 ['Git Commit', 'commit'], ['QAC version', '0.0.1'],
                 ['Project root', 'path/to/project/root'], ['ACF', mock.ANY],
                 ['RCF', mock.ANY], ['CCT', mock.ANY],
                 ['User Messages', mock.ANY],
                 ['Cache Baseline path', 'baseline'],
                 ['Local Baseline path', 'baseline'],
                 ['Local Baseline sha', '']])
            instance.create_sheet.return_value.enable_filters.assert_called()

    @patch(
        "swq.qac.exporters.state_exporter._convert_state_to_severity_summary")
    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_metrics")
    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_analysis")
    @patch("swq.qac.exporters.state_exporter.ZipFile")
    def test_export_reports(self, zipfile, file_analysis, file_metrics,
                            serverity_summary):
        """Test export_reports() method"""
        serverity_summary.return_value = 0
        file_metrics.return_value = 0
        file_analysis.return_value = 0
        mock_open_fn = mock.mock_open(read_data='{"analysis":"sample"}')
        zipfile.return_value = TestStateExporter.MockZipf()
        zipfile.return_value.open = mock_open_fn
        with patch('swq.qac.exporters.state_exporter.LOGGER') as logger, \
                patch("builtins.open", mock_open_fn):
            export_reports(self.config)
            logger.info.assert_called()

        serverity_summary.assert_called_with(self.config, None, 'sample', True)
        file_metrics.assert_not_called()
        file_analysis.assert_called_with(self.config, None, 'sample')

    @patch(
        "swq.qac.exporters.state_exporter._convert_state_to_severity_summary")
    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_metrics")
    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_analysis")
    @patch("swq.qac.exporters.state_exporter.ZipFile")
    def test_export_reports_metrics_true(self, zipfile, file_analysis,
                                         file_metrics, serverity_summary):
        """Test export_reports() method"""
        serverity_summary.return_value = 0
        file_metrics.return_value = 0
        file_analysis.return_value = 0
        mock_open_fn = mock.mock_open(read_data='{"analysis":"sample"}')
        zipfile.return_value = TestStateExporter.MockZipf()
        zipfile.return_value.open = mock_open_fn
        with patch('swq.qac.exporters.state_exporter.LOGGER') as logger, \
                patch("builtins.open", mock_open_fn):
            self.config.with_metrics = True
            export_reports(self.config)
            logger.info.assert_called()

        serverity_summary.assert_called_with(self.config, None, 'sample', True)
        file_metrics.assert_called_with(self.config, 'sample')
        file_analysis.assert_called_with(self.config, None, 'sample')

    @patch(
        "swq.qac.exporters.state_exporter._convert_state_to_severity_summary")
    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_metrics")
    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_analysis")
    @patch("swq.qac.exporters.state_exporter.ZipFile")
    def test_export_reports_metrics_non_analysis(self, zipfile, file_analysis,
                                                 file_metrics,
                                                 serverity_summary):
        """Test export_reports() method"""
        serverity_summary.return_value = 0
        file_metrics.return_value = 0
        file_analysis.return_value = 0
        mock_open_fn = mock.mock_open(read_data='{"non-analysis":"sample"}')
        zipfile.return_value = TestStateExporter.MockZipf()
        zipfile.return_value.open = mock_open_fn

        with patch('swq.qac.exporters.state_exporter.LOGGER') \
            as logger, \
                patch("builtins.open", mock_open_fn), \
                patch("swq.qac.exporters.state_exporter.log_and_exit") \
                as mock_log_and_exit:
            mock_log_and_exit.return_value = 0
            export_reports(self.config)
            mock_log_and_exit.assert_called_with(RC_CONFIG_PARSING_ERROR)
            logger.info.assert_called()

    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_metrics")
    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_analysis")
    @patch("swq.qac.exporters.state_exporter.ZipFile")
    @patch("swq.qac.exporters.state_exporter._create_exporters")
    def test_convert_state_to_severity_summary(self, create_exporters, zipfile,
                                               file_analysis, file_metrics):
        """Test _convert_state_to_severity_summary() method"""
        file_metrics.return_value = 0
        file_analysis.return_value = 0
        mock_open_fn = mock.mock_open(
            read_data='{"analysis":{"path":' + '{"summary":{"severities"' +
            ':{"0":1, "1":0,"2":0,"3":0,' + '"4":0,"5":1, "6":1, "7":1,' +
            '"8":1, "9":1},' + '"analysis_error_count":1,' +
            '"analysis_exit_status":"1",' + '"severities_total":"6",' +
            '"analysis_log":[{"module":' + '"sample1", "analysis_code":' +
            '"0"},{"module":"sample2",' + '"analysis_code":"0"}],' +
            '"item1":"1", "item2":"2"},' + '"filename":"file"}},' +
            '"git_commit":"1234"}')
        zipfile.return_value = TestStateExporter.MockZipf()
        zipfile.return_value.open = mock_open_fn
        self.config.generate_html = True
        create_exporters.return_value = [
            mock.Mock(create_sheet=mock.Mock(), append_rows=mock.Mock())
        ]
        instance = create_exporters.return_value[0].create_sheet
        append_rows = instance.return_value.append_rows

        with patch('swq.qac.exporters.state_exporter.LOGGER') \
            as logger, \
                patch("swq.qac.exporters.state_exporter." +
                      "_create_html_file_from_list_of_lists") \
                as create_html, \
                patch("swq.qac.exporters.state_exporter.LICENSE_WARNING",
                      "warn"), \
                patch("builtins.open", mock_open_fn):
            export_reports(self.config)
            logger.info.assert_called()
            create_html.assert_called_with(
                self.config, '1234',
                'Static Code Analysis ' + 'Summary Report', mock.ANY,
                [[
                    'filename', 'analysis_error_count', 'analysis_exit_status',
                    'severities_total', 'module_outputs', 'module_error_count',
                    'severity0', 'severity1', 'severity2', 'severity3',
                    'severity4', 'severity5', 'severity6', 'severity7',
                    'severity8', 'severity9'
                ], ['Total', 1, '-', 6, '-', 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                 [
                     'path', 1, '1', '6', 'sample1:0,sample2:0', 0, 1, 0, 0, 0,
                     0, 1, 1, 1, 1, 1
                 ]], 'warn')

        instance.assert_called_with('summary')
        create_exporters.assert_called_with(self.config, "report", "summary")
        append_rows.assert_called_with([[
            'filename', 'analysis_error_count', 'analysis_exit_status',
            'severities_total', 'module_outputs', 'module_error_count',
            'severity0', 'severity1', 'severity2', 'severity3', 'severity4',
            'severity5', 'severity6', 'severity7', 'severity8', 'severity9'
        ], ['Total', 1, '-', 6, '-', 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                                        [
                                            'path', 1, '1', '6',
                                            'sample1:0,sample2:0', 0, 1, 0, 0,
                                            0, 0, 1, 1, 1, 1, 1
                                        ]])

        create_exporters.return_value[0].save.assert_called()

    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_metrics")
    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_analysis")
    @patch("swq.qac.exporters.state_exporter.ZipFile")
    @patch("swq.qac.exporters.state_exporter._create_exporters")
    def test_convert_state_to_severity_summary_non_analysis(
            self, create_exporters, zipfile, file_analysis, file_metrics):
        """Test _convert_state_to_severity_summary() method"""
        file_metrics.return_value = 0
        file_analysis.return_value = 0
        mock_open_fn = mock.mock_open(
            read_data='{"analysis":{"path":' + '{"summary":{"severities"' +
            ':{"0":1, "1":0,"2":0,"3":0,' + '"4":0,"5":1, "6":1, "7":1,' +
            '"8":1, "9":1},' + '"analysis_error_count":1,' +
            '"analysis_exit_status":"1",' + '"severities_total":"6",' +
            '"item1":"1", "item2":"2"},' + '"filename":"file"}},' +
            '"git_commit":"1234"}')
        zipfile.return_value = TestStateExporter.MockZipf()
        zipfile.return_value.open = mock_open_fn
        self.config.generate_html = True
        create_exporters.return_value = [
            mock.Mock(create_sheet=mock.Mock(),
                      append_rows=mock.Mock(),
                      enable_filters=mock.Mock(),
                      save=mock.Mock())
        ]

        instance = create_exporters.return_value[0].create_sheet
        append_rows = instance.return_value.append_rows

        with patch('swq.qac.exporters.state_exporter.LOGGER') \
            as logger, \
                patch("swq.qac.exporters.state_exporter." +
                      "_create_html_file_from_list_of_lists") \
                as create_html, \
                patch("swq.qac.exporters.state_exporter.LICENSE_WARNING",
                      "warn"), \
                patch("builtins.open", mock_open_fn):
            export_reports(self.config, summary_details=False)
            logger.info.assert_called()
            create_html.assert_called_with(
                self.config, '1234',
                'Static Code Analysis ' + 'Summary Report', mock.ANY, [[
                    'filename', 'analysis_error_count', 'analysis_exit_status',
                    'severities_total', 'module_outputs', 'module_error_count',
                    'severity0', 'severity1', 'severity2', 'severity3',
                    'severity4', 'severity5', 'severity6', 'severity7',
                    'severity8', 'severity9'
                ], ['Total', 1, '-', 6, '-', 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1]],
                '')

        instance.assert_called_with('summary')
        create_exporters.assert_called_with(self.config, "report", "summary")
        append_rows.assert_called_with([[
            'filename', 'analysis_error_count', 'analysis_exit_status',
            'severities_total', 'module_outputs', 'module_error_count',
            'severity0', 'severity1', 'severity2', 'severity3', 'severity4',
            'severity5', 'severity6', 'severity7', 'severity8', 'severity9'
        ], ['Total', 1, '-', 6, '-', 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1]])

        create_exporters.return_value[0].save.assert_called()

    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_metrics")
    @patch("swq.qac.exporters.state_exporter._convert_state_to_file_analysis")
    @patch("swq.qac.exporters.state_exporter.ZipFile")
    @patch("swq.qac.exporters.state_exporter._create_exporters")
    def test_convert_state_to_severity_summary_no_generate(
            self, create_exporters, zipfile, file_analysis, file_metrics):
        """Test _convert_state_to_severity_summary() method"""
        file_metrics.return_value = 0
        file_analysis.return_value = 0
        mock_open_fn = mock.mock_open(
            read_data='{"analysis":{"path":' + '{"summary":{"severities"' +
            ':{"0":1, "1":0,"2":0,"3":0,' + '"4":0,"5":1, "6":1, "7":1,' +
            '"8":1, "9":1},' + '"analysis_error_count":1,' +
            '"analysis_exit_status":"1",' + '"severities_total":"6",' +
            '"item1":"1", "item2":"2"},' + '"filename":"file"}},' +
            '"git_commit":"1234"}')
        zipfile.return_value = TestStateExporter.MockZipf()
        zipfile.return_value.open = mock_open_fn
        self.config.generate_html = False
        create_exporters.return_value = [
            mock.Mock(create_sheet=mock.Mock(),
                      append_rows=mock.Mock(),
                      save=mock.Mock())
        ]
        instance = create_exporters.return_value[0].create_sheet
        append_rows = instance.return_value.append_rows

        with patch('swq.qac.exporters.state_exporter.LOGGER') \
            as logger, \
                patch("swq.qac.exporters.state_exporter." +
                      "_create_html_file_from_list_of_lists") \
                as create_html, \
                patch("swq.qac.exporters.state_exporter.LICENSE_WARNING",
                      "warn"), \
                patch("builtins.open", mock_open_fn):
            export_reports(self.config, summary_details=False)
            logger.info.assert_called()
            create_html.assert_not_called()

        instance.assert_called_with('summary')
        create_exporters.assert_called_with(self.config, "report", "summary")
        append_rows.assert_called_with([[
            'filename', 'analysis_error_count', 'analysis_exit_status',
            'severities_total', 'module_outputs', 'module_error_count',
            'severity0', 'severity1', 'severity2', 'severity3', 'severity4',
            'severity5', 'severity6', 'severity7', 'severity8', 'severity9'
        ], ['Total', 1, '-', 6, '-', 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1]])

        create_exporters.return_value[0].save.assert_called()

    @patch("swq.qac.exporters.state_exporter.ZipFile")
    @patch("swq.qac.exporters.state_exporter._create_exporters")
    def test_convert_state_to_file_metrics(self, mock_create_exporters,
                                           zipfile):
        """Test _convert_state_to_file_metrics() method"""
        json_data = '''
{
    "git_commit":"1234",
    "analysis":
    {
        "file.cpp":
        {
            "submetrics":
            [{
                "name":"someName",
                "type": "class",
                "line": 21,
                "metrics":
                {
                    "STCBO": "2",
                    "STMTH": "5"
                }
            }]
        }
    }
}'''

        expected_rows = [[
            'path', 'entity_name', 'entity_line', 'entity_type', 'metric_name',
            'metric_value'
        ], ['file.cpp', 'someName', 21, 'class', 'STCBO', '2'],
                         ['file.cpp', 'someName', 21, 'class', 'STMTH', '5']]

        expected_filtered_rows = [[
            'path', 'entity_name', 'entity_line', 'entity_type', 'metric_name',
            'metric_value'
        ], ['file.cpp', 'someName', 21, 'class', 'STMTH', '5']]

        row_with_team_components = [
            'file.cpp', 'someName', 21, 'class', 'STMTH', '5', 'core_team',
            'core'
        ]
        expected_rows_with_team_mapping = [[
            'path', 'entity_name', 'entity_line', 'entity_type', 'metric_name',
            'metric_value', 'Team', 'Components'
        ], row_with_team_components]

        mock_open_fn = mock.mock_open(read_data=json_data)
        zipfile.return_value = TestStateExporter.MockZipf()
        zipfile.return_value.open = mock_open_fn
        self.config.generate_html = False
        self.config.with_metrics = True

        with patch("swq.qac.exporters.state_exporter.LOGGER"), \
            patch("swq.qac.exporters.state_exporter." +
                  "_convert_state_to_file_analysis"), \
            patch("swq.qac.exporters.state_exporter." +
                  "_convert_state_to_severity_summary"), \
            patch("swq.qac.exporters.state_exporter." +
                  "_create_html_file_from_list_of_lists") as create_html,\
            patch("swq.qac.exporters.state_exporter.ComponentMapper"), \
            patch(
                "swq.qac.exporters.state_exporter.add_team_components_to_row")\
                as mock_add_team_components:
            mock_create_exporters.return_value = [
                mock.Mock(create_sheet=mock.Mock(), append_rows=mock.Mock())
            ]
            instance = mock_create_exporters.return_value[0].create_sheet
            append_rows = instance.return_value.append_rows

            export_reports(self.config, summary_details=False)
            instance.assert_called_with('metrics')
            mock_create_exporters.assert_called_with(self.config, "report",
                                                     "metrics")
            create_html.assert_not_called()
            append_rows.assert_called_with(expected_rows)

            self.config.metrics_filter_list = ['STMTH']
            export_reports(self.config, summary_details=False)
            append_rows.assert_called_with(expected_filtered_rows)

            self.config.codeowners_file = 'codeowners.txt'
            self.config.generate_html = True
            mock_add_team_components.return_value = row_with_team_components
            export_reports(self.config, summary_details=False)
            append_rows.assert_called_with(expected_rows_with_team_mapping)
            create_html.assert_not_called()
