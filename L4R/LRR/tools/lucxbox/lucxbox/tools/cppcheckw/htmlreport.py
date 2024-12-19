#!/usr/bin/env python
"""Script for turning a cppcheck xml file into a browsable html report along with syntax highlighted source code."""
from __future__ import unicode_literals

import io
import sys
import os
import shutil
import re
import html

import xml.etree.ElementTree as et
from collections import Counter
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters.html import HtmlFormatter
from pygments.util import ClassNotFound
from lucxbox.lib import lucxlog
from lucxbox.tools.cppcheckw.resources import html_object

LOGGER = lucxlog.get_logger()


class Error:

    def __init__(self, id_, severity, msg, verbose=None, cwe=None, inconclusive=None, file=None, line=None, file0=None, info=None):
        self.id_ = id_
        self.severity = severity
        self.msg = msg
        self.verbose = verbose
        self.cwe = cwe
        if line is not None:
            self.line = int(line)
        self.info = info
        self.file = file
        self.inconclusive = inconclusive
        self.file0 = file0
        self.html_file = None

    def is_inconclusive(self):
        return self.inconclusive == 'true'

    def has_verbose(self):
        return (self.verbose is not None) and (self.msg != self.verbose)


class AnnotateCodeFormatter(HtmlFormatter):
    errors = []

    def wrap(self, source, outfile):
        return self.wrap_code(super().wrap(source, outfile))

    def wrap_code(self, source):
        line_no = 0
        for i, text in source:
            if i == 1:
                line_no += 1
                gen_exp = (e for e in self.errors
                           if e.line == line_no)
                for error in gen_exp:
                    if error.is_inconclusive():
                        error_class = "inconclusive2"
                    else:
                        error_class = "error2"
                    if error.has_verbose():
                        error_msg = html.escape(error.verbose.replace("\\012", '\n'))
                    else:
                        error_msg = error.msg
                    if error.info:
                        error_info = html.escape('\nAdditional information: %s' % error.info)
                    else:
                        error_info = ""
                    index = text.rfind('\n')
                    text = text[:index] + html_object.HTML_ERROR_TEMPLATE % (error_class,
                                                                             error_msg,
                                                                             error_info,
                                                                             error.id_) + text[index + 1:]
            yield i, text


def update_dict_keys(dictionary):
    key_mapping = {"id": "id_"}
    for old_key, new_key in key_mapping.items():
        if old_key in dictionary:
            dictionary[new_key] = dictionary.pop(old_key)
    return dictionary


def group_by_attribute(object_list, attribute):
    result = {}
    for elem in object_list:
        key = vars(elem).get(attribute)
        if key not in result:
            result[key] = []
        result[key].append(elem)
    return result


def create_html_files(errors_grouped_by_file, source_dir, source_encoding, report_dir, cppcheck_version):
    # Generate a HTML file with syntax highlighted source code for each
    # file that contains one or more errors.
    LOGGER.debug('Processing errors')

    decode_errors = []

    html_file_num = 0

    for filename, errors in errors_grouped_by_file.items():

        if not filename:
            continue

        lines = []
        for error in errors:
            lines.append(error.line)

        # Read source files
        source_filename = os.path.join(source_dir, filename)
        try:
            with io.open(source_filename, 'r', encoding=source_encoding) as input_file:
                content = input_file.read()
        except IOError:
            LOGGER.error("Source file '%s' not found.\n", source_filename)
            sys.exit(1)
        except UnicodeDecodeError:
            LOGGER.debug("WARNING: Unicode decode error in '%s'.\n",
                         source_filename)
            decode_errors.append(source_filename[2:])  # "[2:]" gets rid of "./" at beginning
            continue

        # Append html report filename to error object
        html_filename = "%s.html" % html_file_num
        for error in errors:
            error.html_file = html_filename

        write_html_to_file(lines, errors, report_dir, filename, source_encoding,
                           source_filename, content, html_filename, cppcheck_version)
        html_file_num += 1
        LOGGER.debug('   %s', filename)

    return decode_errors


def write_html_to_file(lines, errors, report_dir, filename, source_encoding,
                       source_filename, content, html_filename, cppcheck_version):
    # Open file specific html and write Header
    html_formatter = AnnotateCodeFormatter(linenos=True,
                                           style='colorful',
                                           hl_lines=lines,
                                           lineanchors='line',
                                           encoding=source_encoding)
    html_formatter.errors = errors

    with io.open(os.path.join(report_dir, html_filename), 'w', encoding='utf-8') as output_file:
        output_file.write(html_object.HTML_HEAD_TEMPLATE %
                          (html_formatter.get_style_defs('.highlight'),
                           re.split(r"[\\/]", filename)[-1]))
        output_file.write("<table>\n<tr><th align='left'>Id</th><th>Severity</th><th>Line</th></tr>\n")
        for error in sorted(errors, key=lambda k: k.line):
            output_file.write("<tr><td align='left'>%s</td><td align='left'>%s</td>"
                              "<td align='right'><a href='%s#line-%s'> %s</a></td></tr>\n" % (error.id_,
                                                                                              error.severity,
                                                                                              html_filename,
                                                                                              error.line,
                                                                                              error.line))
        output_file.write('</table>')
        output_file.write(html_object.HTML_HEAD_END_TEMPLATE)

        # Get lexer for source file
        try:
            lexer = guess_lexer_for_filename(source_filename, '')
        except ClassNotFound:
            LOGGER.debug("Couldn't determine lexer for the file '%s'. Won't be able to syntax "
                         "highlight this file.", source_filename)
            output_file.write("\n <tr><td colspan='5'> Could not generated content because "
                              "pygments failed to retrieve the determine code type.</td></tr>")
            return

        if source_encoding is not None:
            lexer.encoding = source_encoding

        output_file.write(
            highlight(content, lexer, html_formatter).decode(
                source_encoding))
        output_file.write(html_object.HTML_FOOTER_TEMPLATE % cppcheck_version)


def write_index_html(errors_grouped_by_file, report_dir, decode_errors, cppcheck_version):
    with io.open(os.path.join(report_dir, '_index.html'), 'w') as output_file:

        stats = []
        for filename, errors in errors_grouped_by_file.items():
            for error in errors:
                stats.append(error.id_)  # get the stats

        occurrences = Counter(stats).most_common()

        stat_html = ""

        # Write check box for each error id occurring with amount of occurrences
        for (id_, occurrence) in occurrences:
            stat_html += "            <tr><td><input type='checkbox' onclick='toggle_class_visibility(this.id)'" \
                         " id='{id_}' name='{id_}' checked></td><td>{occ}</td><td>{id_}</td></tr>".format(id_=id_, occ=occurrence)

        output_file.write(html_object.HTML_HEAD_TEMPLATE.replace("Back to Summary:", "Defect summary:", 1) % ('', 'Index'))
        output_file.write('       <table>\n'
                          '           <tr><th>Show</th><th>#</th><th>Defect ID</th></tr>\n'
                          '<label><input type="checkbox" onclick="show_all(this.checked)" id="show_all" checked> Show all</label>\n'
                          + stat_html +
                          '           <tr><td></td><td>' + str(len(stats)) + '</td><td>total</td></tr>\n'
                                                                             '       </table>\n'
                                                                             '       <a href="_stats.html">Statistics</a></p>')
        output_file.write(html_object.HTML_HEAD_END_TEMPLATE)
        output_file.write('       <table class="indextable">\n'
                          '       <tr><th>Line</th><th>Id</th><th>CWE</th><th>Severity</th><th>Message</th></tr>')

        for filename, errors in errors_grouped_by_file.items():
            if not filename:
                continue
            if filename in decode_errors:  # don't print a link but a note
                output_file.write("\n       <tr><td colspan='5'>%s</td></tr>" % filename)
                output_file.write("\n       <tr><td colspan='5'> Could not generated due to "
                                  "UnicodeDecodeError</td></tr>")
                continue

            if filename.endswith('*'):  # assume unmatched suppression
                output_file.write("\n       <tr><td colspan='5'>%s</td></tr>" % filename)
            else:
                output_file.write("\n       <tr><td colspan='5'><a href='%s'>%s</a></td></tr>" % (errors[0].html_file, filename))

            output_file.write(get_error_class_string(filename, errors))

        output_file.write('\n       </table>')
        output_file.write(html_object.HTML_FOOTER_TEMPLATE % cppcheck_version)


def get_error_class_string(filename, errors):
    error_string = ""

    for error in sorted(errors, key=lambda k: k.line):
        error_class = ''

        if error.is_inconclusive():
            error_class = 'class="inconclusive"'
            error['severity'] += ", inconcl."

        if error.cwe:
            cwe_url = "<a href='https://cwe.mitre.org/data/definitions/" + error.cwe + ".html'>" + error.cwe + "</a>"
        else:
            cwe_url = ""

        if error.severity == 'error':
            error_class = 'class="error"'
        if error.id_ == 'missingInclude':
            error_string += '\n         <tr class="%s"><td></td><td>%s</td><td></td><td>%s</td><td>%s</td></tr>' % \
                            (error.id_, error.id_, error.severity, error.msg)
        elif (error.id_ == 'unmatchedSuppression') and filename.endswith('*'):
            error_string += '\n         <tr class="%s"><td></td><td>%s</td><td></td><td>%s</td><td %s>%s</td></tr>' % \
                            (error.id_, error.id_, error.severity, error_class, error.msg)
        else:
            error_string += '\n       <tr class="%s"><td>' \
                            '<a href="%s#line-%s">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td %s>%s</td></tr>' % \
                            (error.id_, error.html_file, error.line, error.line,
                             error.id_, cwe_url, error.severity, error_class, error.msg)
    return error_string


def write_statistics_html(errors_grouped_by_file, report_dir, occ_number):
    # Create a Counter for the total amount of occurrences of severities
    sev_counter = Counter()

    # Create a dictionary, with the severities and their number of occurrence in each file
    severities = {}
    for filename, errors in errors_grouped_by_file.items():
        if not filename:
            continue
        tmp_list = []
        for error in errors:
            tmp_list.append(error.severity)
        sev_counter.update(tmp_list)
        tmp_sev_counter = Counter(tmp_list)
        for sev in tmp_sev_counter:
            if sev not in severities:
                severities[sev] = Counter()
            severities[sev].update({filename: tmp_sev_counter[sev]})

    with io.open(os.path.join(report_dir, '_stats.html'), 'w') as stats_file:

        stats_file.write(html_object.HTML_HEAD_TEMPLATE % ('', 'Statistics'))
        stats_file.write(html_object.HTML_HEAD_END_TEMPLATE)

        # Get the occ_number amount of files with the most occurrences of each severity
        stats_file.write("<table>\n")
        for sev in sorted(severities.keys()):
            tmp_list = severities[sev].most_common(occ_number)

            stats_file.write("<tr><th colspan='2' align='left'>Top {0} files for severity '{1}', total findings: {2}</th></tr>\n"
                             .format(occ_number, sev, sev_counter[sev]))

            for (filename, occ) in tmp_list:
                html_file = errors_grouped_by_file[filename][0].html_file
                stats_file.write("<tr><td>%s</td><td><a href='%s'> %s </a></td></tr>\n" % (occ, html_file, filename))
            stats_file.write("<tr><td></td><td></td></tr>")

        stats_file.write("</table>\n")


def convert_to_html(xml_str, report_dir, source_dir=None, source_encoding='utf-8'):
    """
    Turns a cppcheck xml file into a browsable html report along
    with syntax highlighted source code.
    """

    if source_dir is None:
        source_dir = os.getcwd()

    # Parse xml
    root = et.fromstring(xml_str)

    # Get cppcheck version
    cppcheck_version = float(root.find("cppcheck").attrib['version'])

    # Create Error objects for each error
    errors = []
    for err in root.findall(".//error"):
        locations = [l for l in list(err) if l.tag == "location"]
        if locations:
            for loc in locations:
                errors.append(Error(**update_dict_keys(err.attrib), **loc.attrib))
        else:
            errors.append(Error(**update_dict_keys(err.attrib)))

    # Make sure that the report directory is created if it doesn't exist.
    LOGGER.debug('Creating %s directory', report_dir)
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    # Create a html report file for each source file
    errors_grouped_by_file = group_by_attribute(errors, 'file')
    decode_errors = create_html_files(errors_grouped_by_file, source_dir, source_encoding, report_dir, cppcheck_version)

    if decode_errors:
        LOGGER.debug("Generating html failed because of decoding errors for the following files: ")
        for filename in decode_errors:
            LOGGER.debug(filename)

    # Generate a master index.html file that will contain a list of
    # all the errors created.
    LOGGER.debug('Creating index.html')
    write_index_html(errors_grouped_by_file, report_dir, decode_errors, cppcheck_version)

    LOGGER.debug('Copying .css file')
    css_path = os.path.join(os.path.dirname(__file__), "resources", "style.css")
    shutil.copy(css_path, report_dir)

    LOGGER.debug("Creating _stats.html (statistics)")
    write_statistics_html(errors_grouped_by_file, report_dir, occ_number=10)

    print("Open '" + os.path.join(report_dir, '_index.html') + "' to see the results.")
