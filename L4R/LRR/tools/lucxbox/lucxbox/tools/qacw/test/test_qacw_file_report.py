""" Testing for qacw_file_report """

import os
import unittest
from unittest.mock import patch

from lucxbox.tools.qacw.qacw_file_report import _read_file_filters, _read_source_exts, _exec_qacli_view, \
    _read_analysis_results, _get_file_info


class TestQACFileReport(unittest.TestCase):
    """" Tests for the file report functionality """

    def test_read_file_filters(self):
        project_xml = _get_resource('data/qacw_file_report_project1.xml')

        self.assertEqual(['/opt', '/usr'], _read_file_filters(project_xml))

    def test_read_file_filters_rpath(self):
        project_xml = _get_resource('data/qacw_file_report_project2.xml')

        self.assertEqual(['/source/opt', '/other/usr'], _read_file_filters(project_xml))

    def test_read_source_exts(self):
        project_xml = _get_resource('data/qacw_file_report_project1.xml')

        self.assertEqual(['.c', '.cpp', '.cxx', '.cc', '.C', '.cp', '.c++'], _read_source_exts(project_xml))

    @patch('subprocess.call')
    def test_exec_qacli_view(self, mock_call):
        mock_call.side_effect = lambda *popenargs, **kwargs: _call_side_effect('text', 2, kwargs['stdout'])
        output_file = _exec_qacli_view('qacli', '/project')

        output_file.seek(0)
        self.assertEqual(b'text', output_file.read())
        mock_call.assert_called_once_with(
            'qacli view --qaf-project "/project" --medium STDOUT --format "%?g==2%(error%:%?u==0%(warning%: %)%);%F;%l;%c;%t"', shell=True,
            stdout=output_file)

    def test_read_analysis_results1(self):
        """
        Test to find parse errors
        """
        output_txt = _get_resource('data/qacw_file_report_view_output1.txt')

        with open(output_txt, 'rb') as test_output_file:
            results = _read_analysis_results(test_output_file)

        self.assertEqual({'/project/ara_sample_cache.hpp': [
            "/project/ara_sample_cache.hpp(39,10): Cannot find include file 'vfc/container/vfc_fixedvector.hpp', ignoring #include.",
            "/project/ara_sample_cache.hpp(282,5): 'vfc' is not a namespace or class."]}, results)

    def test_read_analysis_results2(self):
        """
        Test to find files without parse errors but with warnings
        """
        output_txt = _get_resource('data/qacw_file_report_view_output2.txt')

        with open(output_txt, 'rb') as test_output_file:
            results = _read_analysis_results(test_output_file)

        self.assertEqual({'/project/ara_sample_pool.hpp': []}, results)

    def test_read_analysis_results3(self):
        """
        Test to find files without any errors or warnings
        """
        output_txt = _get_resource('data/qacw_file_report_view_output3.txt')

        with open(output_txt, 'rb') as test_output_file:
            results = _read_analysis_results(test_output_file)

        self.assertEqual({'/project/sample.hpp': []}, results)

    def test_get_file_info(self):
        analyzed, cause, details = _get_file_info('/project/source.cpp', ['/project/build'], ['.cpp'], {'/project/source.cpp': []})

        self.assertEqual(True, analyzed)
        self.assertEqual('', cause)
        self.assertEqual([], details)

    def test_get_file_info_filter(self):
        analyzed, cause, details = _get_file_info('/project/build/generated.cpp', ['/project/build'], ['.cpp'],
                                                  {'/project/source.cpp': []})

        self.assertEqual(False, analyzed)
        self.assertEqual('ignored', cause)
        self.assertEqual(['ignored by filter /project/build'], details)

    def test_get_file_info_ext(self):
        analyzed, cause, details = _get_file_info('/project/README.txt', ['/project/build'], ['.cpp'], {'/project/source.cpp': []})

        self.assertEqual(False, analyzed)
        self.assertEqual('no source', cause)
        self.assertEqual([], details)

    def test_get_file_info_unknown(self):
        analyzed, cause, details = _get_file_info('/project/source2.cpp', ['/project/build'], ['.cpp'], {'/project/source.cpp': []})

        self.assertEqual(False, analyzed)
        self.assertEqual('unknown', cause)
        self.assertEqual([], details)

    def test_get_file_info_parse_error(self):
        analyzed, cause, details = _get_file_info('/project/source.cpp', ['/project/build'], ['.cpp'],
                                                  {'/project/source.cpp': ['Some error, "']})

        self.assertEqual(False, analyzed)
        self.assertEqual('parse error', cause)
        self.assertEqual(['Some error, "'], details)


def _get_resource(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


def _call_side_effect(text_to_write, exit_code_to_return, stdout_handle):
    stdout_handle.write(text_to_write.encode())
    return exit_code_to_return


if __name__ == "__main__":
    unittest.main()
