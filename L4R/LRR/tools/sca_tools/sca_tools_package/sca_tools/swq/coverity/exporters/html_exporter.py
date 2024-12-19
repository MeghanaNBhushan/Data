# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: html_exporter.py
# ----------------------------------------------------------------------------
"""Routines to create a html formatted table out of list structures."""

from datetime import datetime

_HTML_STYLE = '''
html, body{
    width:98%;
    background: white;
    font-family: "Consolas", "Bitstream Vera Sans Mono", monospace !important;
}
table.report {
  font-family: "Times New Roman", Times, monospace;
  text-align: right;
  table-layout: fixed;
  margin-left: 2%;
  margin-right: 2%;
  width: 98%;
}
table.report td, table.report th {
  border: 1px solid #FFFFFF;
  padding: 2px 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  word-wrap: break-word;
}
table.report tr:nth-child(even) {
  background: #E0E4F5;
}
table.report thead {
  background: #06FA4;
}
table.report thead th {
  font-weight: bold;
  color: #FFFFFF;
  text-align: center;
  border-left: 2px solid #FFFFFF;
}
table.report thead th:first-child {
  border-left: none;
}
table.report tfoot {
  font-weight: bold;
  color: #333333;
  background: #E0E4F5;
  border-top: 3px solid #444444;
}
'''


def _create_table_from_list_of_lists(list_of_lists):
    yield '<table class=\"report\">'
    for row in list_of_lists:
        yield '  <tr><td>'
        yield '    </td><td>'.join([str(value) for value in row])
        yield '  </td></tr>'
    yield '</table>'


def _create_report_header(title, project_root, git_commit, coverity_version,
                          report_description: str):
    return '\n'.join([
        '<h1>Report {}</h1>', '<p><b>{}</b></p>', '<p><b>Date: </b>{}</p>',
        '<p><b>Git Commit: </b>{}</p>', '<p><b>Coverity version: </b>{}</p>'
    ]).format(title, report_description,
              datetime.now().strftime('%d/%m/%Y %H:%M:%S'), git_commit,
              coverity_version, project_root)


def create_html_from_list_of_lists(title, project_root, git_commit, version,
                                   list_of_lists, report_description: str):
    """Creates html file from list or lists"""
    html_table = '\n'.join(_create_table_from_list_of_lists(list_of_lists))
    html_table_style = '<style>\n{}\n</style>'.format(_HTML_STYLE)
    title_style = '<title>{}</title>'.format(title)
    report_header = _create_report_header(title, project_root, git_commit,
                                          version, report_description)
    return '\n'.join([
        '<!DOCTYPE html>', '<html>', '<head>', title_style, html_table_style,
        '</head>', '<body>', report_header, html_table, '</body>', '</html>'
    ])
