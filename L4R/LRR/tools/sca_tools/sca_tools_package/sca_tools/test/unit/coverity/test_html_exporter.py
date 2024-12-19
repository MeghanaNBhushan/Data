""" Tests for coverity/exporters/html_exporter.py """

from datetime import datetime
from unittest import TestCase
from unittest.mock import patch
from swq.coverity.exporters import html_exporter


class TestCoverityHtmlExporter(TestCase):
    """ TestCoverityHtmlExporter class """
    def test_create_html_from_list_of_lists(self):
        """ Test create_html_from_list_of_lists """
        title = 'Title'
        project_root = '/project/root'
        git_commit = 'abc123'
        version = '1.0'
        list_of_lists = [['row1'], ['row2']]
        report_description = 'Description'
        expected_return = '''<!DOCTYPE html>
<html>
<head>
<title>Title</title>
<style>

</style>
</head>
<body>
<h1>Report Title</h1>
<p><b>Description</b></p>
<p><b>Date: </b>01/01/2020 12:00:00</p>
<p><b>Git Commit: </b>abc123</p>
<p><b>Coverity version: </b>1.0</p>
<table class="report">
  <tr><td>
row1
  </td></tr>
  <tr><td>
row2
  </td></tr>
</table>
</body>
</html>'''
        with patch('swq.coverity.exporters.html_exporter._HTML_STYLE', ''), \
                patch('swq.coverity.exporters.html_exporter.datetime') \
                as dt_mock:

            dt_mock.now.return_value = datetime(2020, 1, 1, 12, 0, 0)
            return_value = html_exporter.create_html_from_list_of_lists(
                title, project_root, git_commit, version, list_of_lists,
                report_description)
            self.assertEqual(return_value, expected_return)
