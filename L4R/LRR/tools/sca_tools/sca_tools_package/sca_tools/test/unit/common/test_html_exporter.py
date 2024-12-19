""" Tests for qac/exporters/html_exporter.py """

from datetime import datetime
from unittest.mock import patch
from unittest import TestCase, mock
from swq.qac.exporters.html_exporter import create_html_from_list_of_lists


class TestSheet(TestCase):
    """Test Sheet Class"""
    def setUp(self):
        self.config = mock.Mock(title="title",
                                project_root="root",
                                git_commit="commit",
                                qac_version="version",
                                acf_file="acf_file",
                                rcf_file="rcf_file",
                                cct_file="cct_file",
                                user_messages="user_messages",
                                list_of_lists=[["string"]],
                                report_description="null")

    @patch("swq.qac.exporters.html_exporter._HTML_STYLE", "")
    @patch("swq.qac.exporters.html_exporter._create_report_header")
    def test_create_html_from_list_of_lists_mocked_report(self, create_report):
        """Test create_html_from_list_of_lists() method"""

        create_report.return_value = "null"

        return_value = \
            create_html_from_list_of_lists(self.config.title,
                                           self.config.project_root,
                                           self.config.git_commit,
                                           self.config.qac_version,
                                           self.config.acf_file,
                                           self.config.rcf_file,
                                           self.config.cct_file,
                                           self.config.user_messages,
                                           self.config.list_of_lists,
                                           self.config.report_description)

        create_report.assert_called_with(
            self.config.title, self.config.project_root,
            self.config.git_commit, self.config.qac_version,
            self.config.acf_file, self.config.rcf_file, self.config.cct_file,
            self.config.user_messages, self.config.report_description)
        self.assertEqual(
            return_value, '<!DOCTYPE html>\n<html>\n<head>\n<title>' +
            'title</title>\n<style>\n\n</style>\n</head>' +
            '\n<body>\nnull\n<table class="report">\n  <tr>' +
            '<td>\nstring\n  </td></tr>\n</table>\n</body>' + '\n</html>')

    @patch("swq.qac.exporters.html_exporter._create_table_from_list_of_lists")
    @patch("swq.qac.exporters.html_exporter._HTML_STYLE", "")
    @patch("swq.qac.exporters.html_exporter.datetime")
    def test_create_html_from_list_of_lists_mocked_table(
            self, dt_mock, create_table):
        """Test create_html_from_list_of_lists() method"""
        def yield_table():
            yield '<table class=\"report\">'
            yield '</table>'

        create_table.return_value = yield_table()
        dt_mock.now.return_value = datetime(2020, 2, 1, 10, 9, 8)

        return_value = \
            create_html_from_list_of_lists(self.config.title,
                                           self.config.project_root,
                                           self.config.git_commit,
                                           self.config.qac_version,
                                           self.config.acf_file,
                                           self.config.rcf_file,
                                           self.config.cct_file,
                                           self.config.user_messages,
                                           self.config.list_of_lists,
                                           self.config.report_description)

        create_table.assert_called_with(self.config.list_of_lists)

        self.assertEqual(
            return_value, '<!DOCTYPE html>\n<html>\n<head>\n<title>title' +
            '</title>\n<style>\n\n</style>\n</head>\n<body>' +
            '\n<h1>Report title</h1>\n<p><b>null</b></p>\n' +
            '<p><b>Date: </b>01/02/2020 10:09:08</p>\n<p>' +
            '<b>Git Commit: </b>commit</p>\n' +
            '<p><b>QAC version: </b>version</p>\n' +
            '<p><b>Project root: </b>root</p>\n' +
            '<p><b>ACF: </b>acf_file</p>\n' + '<p><b>RCF: </b>rcf_file</p>\n' +
            '<p><b>CCT: </b>cct_file</p>\n' +
            '<p><b>User Messages: </b>user_messages</p>\n' +
            '<table class="report">\n</table>\n</body>\n</html>')
