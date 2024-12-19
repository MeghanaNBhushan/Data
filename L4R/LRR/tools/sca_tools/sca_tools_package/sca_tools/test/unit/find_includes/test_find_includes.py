"""Test find_includes/find_includes.py"""
import os
from sys import path
import test.unit.find_includes.file_system_mock as fs_mock

from unittest import TestCase, mock
from unittest.mock import patch, mock_open, call
from swq.find_includes.find_includes import FindIncludes

_CURRENT_PATH = os.getcwd()


# pylint: disable=R0904
class TestFindIncludes(TestCase):
    """ Test FindIncludes Class"""
    RELATIVE_INCLUDE_TEMPLATE = '#include "{}"\n'
    SYSTEM_INCLUDE_TEMPLATE = '#include <{}>\n'

    def setUp(self):
        self.config = mock.Mock(source_extensions=[".cpp", ".c", ".inl"],
                                header_extensions=[".hpp", ".h", ".inl"],
                                source_output_extensions=[".cpp", ".c"],
                                git_diff_filter="rd",
                                blacklist_pattern="",
                                merge_base="repo",
                                code_dirs_file=['dir1', 'dir2'],
                                project_root=fs_mock.REPO_PATH)
        self.find_includes = FindIncludes(self.config)
        if self.config.blacklist_pattern:
            pattern_string = self.config.blacklist_pattern[0]
            self.config.file_blacklist_pattern = r"{}".format(pattern_string)
        else:
            self.config.file_blacklist_pattern = ""

    def test_create_mapping_of_file_to_all_direct_includers(self):
        """Test create_mapping_of_file_to_all_direct_includers()"""
        with mock.patch('swq.common.filesystem.filesystem_utils.open',
                        fs_mock.my_mocked_open):
            with mock.patch('os.walk', new=fs_mock.my_mocked_os_walk):
                search_directories = [
                    fs_mock.DC_FW_SIT_SRC_REL_PATH,
                    fs_mock.DC_FW_SIT_SRC_REL_PATH,
                    fs_mock.DC_FW_INTERFACES_REL_PATH
                ]

                mapping = \
                    self.find_includes.\
                    create_mapping_of_file_to_all_direct_includers(
                        search_directories, '')

                for file_name in fs_mock.DIRECT_INCLUDERS_OF:
                    expected_file_paths = {
                        fs_mock.REPO_RELATIVE_FILE_PATHS[path]
                        for path in fs_mock.DIRECT_INCLUDERS_OF[file_name]
                    }
                    actual_file_paths = mapping(
                        fs_mock.REPO_RELATIVE_FILE_PATHS[file_name])
                    self.assertEqual(expected_file_paths, actual_file_paths)

                self.assertEqual(set(), mapping('non/existing/path'))

    def test_find_sources_for_header_files(self):
        """"Method that runs the test for the mock header files"""
        with mock.patch('swq.common.filesystem.filesystem_utils.open',
                        fs_mock.my_mocked_open):
            with mock.patch('os.walk', new=fs_mock.my_mocked_os_walk):
                # find_include_strategy='all'
                self.config.find_include_strategy = 'all'

                search_directories = [
                    fs_mock.DC_FW_SIT_SRC_REL_PATH,
                    fs_mock.DC_FW_INTERFACES_REL_PATH
                ]
                header_files = ''
                source_result_set = \
                    self.find_includes.find_sources_for_header_files(
                        header_files, search_directories, '')
                self.assertEqual(set(), source_result_set)

                header_files = [fs_mock.REPO_RELATIVE_FILE_PATHS['a.hpp']]
                source_result_set = \
                    self.find_includes.find_sources_for_header_files(
                        header_files, search_directories, '')
                self.assertEqual({fs_mock.REPO_RELATIVE_FILE_PATHS['a.cpp']},
                                 source_result_set)

                header_files = [fs_mock.REPO_RELATIVE_FILE_PATHS['b.hpp']]
                source_result_set = \
                    self.find_includes.find_sources_for_header_files(
                        header_files, search_directories, '')
                self.assertEqual(
                    {
                        fs_mock.REPO_RELATIVE_FILE_PATHS[file_name]
                        for file_name in ('a.cpp', 'c.cpp')
                    }, source_result_set)

                header_files = [
                    fs_mock.REPO_RELATIVE_FILE_PATHS[file_name]
                    for file_name in fs_mock.INDIRECT_CPP_INCLUDERS_OF
                ]
                source_result_set = \
                    self.find_includes.find_sources_for_header_files(
                        header_files, search_directories, '')
                self.assertEqual(
                    {
                        fs_mock.REPO_RELATIVE_FILE_PATHS[file_name]
                        for file_name in ('a.cpp', 'a.inl', 'c.cpp', 'e.cpp')
                    }, source_result_set)

                # find_include_strategy='minimal'
                self.config.find_include_strategy = 'minimal'

                header_files = ''
                source_result_set = \
                    self.find_includes.find_sources_for_header_files(
                        header_files, search_directories, '')
                self.assertEqual(set(), source_result_set)

                header_files = [fs_mock.REPO_RELATIVE_FILE_PATHS['a.hpp']]
                source_result_set = \
                    self.find_includes.find_sources_for_header_files(
                        header_files, search_directories, '')
                self.assertEqual({fs_mock.REPO_RELATIVE_FILE_PATHS['a.cpp']},
                                 source_result_set)

                header_files = [fs_mock.REPO_RELATIVE_FILE_PATHS['b.hpp']]
                source_result_set = \
                    self.find_includes.find_sources_for_header_files(
                        header_files, search_directories, '')
                self.assertEqual(1, len(source_result_set))
                self.assertEqual(
                    1,
                    len(
                        source_result_set & {
                            fs_mock.REPO_RELATIVE_FILE_PATHS[file_name]
                            for file_name in ('a.cpp', 'c.cpp')
                        }))

                header_files = [
                    fs_mock.REPO_RELATIVE_FILE_PATHS[file_name]
                    for file_name in fs_mock.INDIRECT_CPP_INCLUDERS_OF
                ]
                source_result_set = \
                    self.find_includes.find_sources_for_header_files(
                        header_files, search_directories, '')
                self.assertIn(fs_mock.REPO_RELATIVE_FILE_PATHS['a.cpp'],
                              source_result_set)

    def test_map_source_files_with_headers(self):
        """ Test map_source_files_with_headers() """
        with mock.patch('swq.common.filesystem.filesystem_utils.open',
                        fs_mock.my_mocked_open):
            with mock.patch('os.walk', new=fs_mock.my_mocked_os_walk):
                search_directories = [
                    fs_mock.DC_FW_SIT_SRC_REL_PATH,
                    fs_mock.DC_FW_INTERFACES_REL_PATH
                ]
                header_files = ''
                result = self.find_includes.map_source_files_with_headers(
                    header_files, search_directories, '')
                self.assertEqual(dict(), result)

                header_files = [fs_mock.REPO_RELATIVE_FILE_PATHS['a.hpp']]
                result = \
                    self.find_includes.map_source_files_with_headers(
                        header_files, search_directories, '')
                expexted_result = {
                    fs_mock.REPO_RELATIVE_FILE_PATHS['a.hpp']:
                    {fs_mock.REPO_RELATIVE_FILE_PATHS['a.cpp']}
                }
                self.assertEqual(expexted_result, result)

    def test_find_sources_which_include_header_file(self):
        """ Test find_sources_which_include_header_file()"""
        with mock.patch('swq.common.filesystem.filesystem_utils.open',
                        fs_mock.my_mocked_open):
            with mock.patch('os.walk', new=fs_mock.my_mocked_os_walk):
                search_directories = [
                    fs_mock.DC_FW_SIT_SRC_REL_PATH,
                    fs_mock.DC_FW_SIT_SRC_REL_PATH,
                    fs_mock.DC_FW_INTERFACES_REL_PATH
                ]
                mapping = \
                    self.find_includes.\
                    create_mapping_of_file_to_all_direct_includers(
                        search_directories, '')

                for filename in fs_mock.INDIRECT_CPP_INCLUDERS_OF:
                    expected_file_paths = {
                        fs_mock.REPO_RELATIVE_FILE_PATHS[path]
                        for path in fs_mock.INDIRECT_CPP_INCLUDERS_OF[filename]
                    }
                    actual_file_paths = set(
                        self.find_includes.
                        find_sources_which_include_header_file(
                            fs_mock.REPO_RELATIVE_FILE_PATHS[filename],
                            mapping))

                    self.assertEqual(expected_file_paths, actual_file_paths)

                self.assertEqual(
                    set(),
                    set(
                        self.find_includes.
                        find_sources_which_include_header_file(
                            '/non/existing/path.hpp', mapping)))

    def test_get_repo_relative_path_absolute_path(self):
        """Test convert_to_repo_relative_path()"""
        repo_relative_path_input = os.path.join('dc_fw', 'src', 'sit', 'foo',
                                                'bar', 'baz')
        root = os.path.abspath(os.sep)
        self.config.project_root = os.path.join(root, 'my', 'repo', 'path',
                                                repo_relative_path_input)
        self.find_includes = FindIncludes(self.config)
        repo_relative_path = self.find_includes.convert_to_repo_relative_path(
            'xyz')
        expected_result = os.path.normpath('xyz')
        self.assertEqual(expected_result, repo_relative_path)

    @patch('swq.find_includes.find_includes.LOGGER', create=True)
    @patch('os.path.relpath')
    def test_get_repo_relative_path_absolute_path_with_exception(
            self, relpath, logger):
        """Test convert_to_repo_relative_path()"""

        relpath.side_effect = ValueError('test')
        repo_relative_path_input = os.path.join('dc_fw', 'src', 'sit', 'foo',
                                                'bar', 'baz')
        root = os.path.abspath(os.sep)
        self.config.project_root = os.path.join(root, 'my', 'repo', 'path',
                                                repo_relative_path_input)
        self.find_includes = FindIncludes(self.config)

        repo_relative_path = self.find_includes.\
            convert_to_repo_relative_path('xyz')

        expected_result = os.path.normpath('xyz')
        logger.error.assert_called()

        self.assertEqual(expected_result, repo_relative_path)

    def test_get_repo_relative_path_absolute_path_with_subdirectories(self):
        """Test convert_to_repo_relative_path() with subdirectories"""
        repo_relative_path_input = os.path.join('dc_fw', 'inc')
        root = os.path.abspath(os.sep)
        self.config.project_root = os.path.join(root, 'my', 'repo', 'path',
                                                repo_relative_path_input)
        self.find_includes = FindIncludes(self.config)
        repo_relative_path = self.find_includes.convert_to_repo_relative_path(
            os.path.join('xyz', 'wyz', 'bla.hpp'))
        expected_result = os.path.normpath(
            os.path.join('xyz', 'wyz', 'bla.hpp'))
        self.assertEqual(expected_result, repo_relative_path)

    def test_is_code_file(self):
        """Test is_code_file()"""
        self.assertTrue(self.find_includes.is_code_file('foo/bar/baz.hpp'))
        self.assertTrue(self.find_includes.is_code_file('/foo/baz.cpp'))
        self.assertTrue(self.find_includes.is_code_file('file.h'))
        self.assertTrue(self.find_includes.is_code_file(r'C:\foo\baz.inl'))
        self.assertTrue(self.find_includes.is_code_file(r'C:\baz.c'))
        self.assertFalse(self.find_includes.is_code_file(r'C:\baz\foo'))
        self.assertFalse(self.find_includes.is_code_file(r'C:\baz\foo.txt'))
        self.assertFalse(self.find_includes.is_code_file(r'C:\baz\foo.cmake'))
        self.assertTrue(
            self.find_includes.is_source_code_file('/foo/bar/baz.cpp'))
        self.assertFalse(
            self.find_includes.is_source_code_file('/foo/bar/baz.hpp'))

    def test_parse_included_files_in_file_content(self):
        """Test parse_included_files_in_file_content()"""
        file_content = []
        included_files_result = list(
            self.find_includes.parse_included_files_in_file_content(
                file_content))
        self.assertEqual([], included_files_result)

    def test_is_header_code_file_hpp(self):
        """Test is_header_code_file() for baz.hpp"""
        self.assertTrue(
            self.find_includes.is_header_code_file('/foo/bar/baz.hpp'))

    def test_is_header_code_file_h(self):
        """Test is_header_code_file() for baz.h"""
        self.assertTrue(self.find_includes.is_header_code_file('/foo/baz.h'))

    def test_is_header_code_file_inl(self):
        """Test is_header_code_file() for baz.inl"""
        self.assertTrue(self.find_includes.is_header_code_file('baz.inl'))

    def test_is_header_code_file_nonheader(self):
        """Test is_header_code_file() for baz.cpp/baz.c/baz/cxx"""
        self.assertFalse(
            self.find_includes.is_header_code_file('/foo/bar/baz.cpp'))
        self.assertFalse(
            self.find_includes.is_header_code_file('/foo/bar/baz.c'))
        self.assertFalse(
            self.find_includes.is_header_code_file('/foo/bar/baz.cxx'))

    def test_is_test_file(self):
        """Test is_file_blacklisted()"""
        self.assertTrue(
            self.find_includes.is_file_blacklisted(
                r'C:\foo\bar\sit_test_foo.cpp', ".*(_test_).*"))
        self.assertFalse(
            self.find_includes.is_file_blacklisted(r'C:\foo\bar\per_xyz.cpp'))
        self.config.file_blacklist_pattern = "cpp"
        self.assertIsNone(
            self.find_includes.is_file_blacklisted(r'C:\foo\bar\per_xyz.cpp'))

    def test_parse_included_files_in_file_content_empty_file(self):
        """Test parse_included_files_in_file_content() without file content"""
        file_content = []
        included_files_result = list(
            self.find_includes.parse_included_files_in_file_content(
                file_content))
        self.assertEqual([], included_files_result)

    def test_parse_included_files_in_file_content_file_without_includes(self):
        """Test parse_included_files_in_file_content() with file content"""
        file_content = ['my line 1', 'my line 2\n', 'whatever']
        included_files_result = list(
            self.find_includes.parse_included_files_in_file_content(
                file_content))
        self.assertEqual([], included_files_result)

    def test_parse_included_files_in_file_content_file_invalid_includes(self):
        """Test parse_included_files_in_file_content() with invalid includes"""
        file_content = [
            'my line 1', 'my line 2\n', "#include 'foo/bar.baz'",
            '#include "foo/bar.baz', '#include >foo/bar.baz"'
        ]
        included_files_result = list(
            self.find_includes.parse_included_files_in_file_content(
                file_content))
        self.assertEqual([], included_files_result)

    def test_parse_included_files_in_file_content_file_one_relative_include(
            self):
        """Test parse_included_files_in_file_content() with relative include"""
        file_path_1 = 'someFile.hpp'
        file_content = [
            'my line 1', '#my line 2\n',
            self.RELATIVE_INCLUDE_TEMPLATE.format(file_path_1)
        ]
        included_files_result = list(
            self.find_includes.parse_included_files_in_file_content(
                file_content))
        self.assertEqual([file_path_1], included_files_result)

    def test_parse_included_files_in_file_content_file_two_relative_includes(
            self):
        """Test parse_included_files_in_file_content() with two relative
        includes"""
        file_path_1 = 'someFileA.hpp'
        file_path_2 = 'someFileB.hpp'
        file_content = [
            'my line 1', '#my line 2\n',
            self.RELATIVE_INCLUDE_TEMPLATE.format(file_path_1), '\n',
            self.RELATIVE_INCLUDE_TEMPLATE.format(file_path_2)
        ]
        included_files_result = list(
            self.find_includes.parse_included_files_in_file_content(
                file_content))
        self.assertEqual([file_path_1, file_path_2], included_files_result)

    def test_parse_included_files_in_file_content_file_mixed_includes(self):
        """Test parse_included_files_in_file_content() with mixed includes"""
        file_path_1 = 'vfc/core/someFileA.hpp'
        file_path_2 = 'dc_interfaces/sit/someFileB.hpp'
        file_path_3 = 'sit/modules/someFileC.hpp'
        file_path_4 = 'someFileD.hpp'
        file_content = [
            'my line 1', '#my line 2\n',
            self.SYSTEM_INCLUDE_TEMPLATE.format(file_path_1), '\n',
            self.RELATIVE_INCLUDE_TEMPLATE.format(file_path_2),
            self.RELATIVE_INCLUDE_TEMPLATE.format(file_path_3),
            self.RELATIVE_INCLUDE_TEMPLATE.format(file_path_4)
        ]
        included_files_result = list(
            self.find_includes.parse_included_files_in_file_content(
                file_content))
        self.assertEqual([file_path_1, file_path_2, file_path_3, file_path_4],
                         included_files_result)

    @patch('swq.common.command.command_decorator.run_command')
    def test_get_merge_base_hash(self, run_command):
        """Test get_merge_base_hash()"""
        self.find_includes._get_merge_base_hash()
        run_command.assert_called_with('git merge-base HEAD repo',
                                       build_shell=mock.ANY,
                                       fast_fail=mock.ANY,
                                       silent=mock.ANY,
                                       use_logger=mock.ANY,
                                       output_filepath=None,
                                       cwd=self.config.project_root)

    @patch('swq.common.command.command_decorator.run_command')
    def test_get_diff_using_merge_base_hash(self, run_command):
        """Test get_diff_using_merge_base_hash()"""
        self.find_includes._get_diff_using_merge_base_hash('hash')
        run_command.assert_called_with('git diff hash HEAD ' +
                                       '--name-only --diff-filter=rd',
                                       build_shell=mock.ANY,
                                       fast_fail=mock.ANY,
                                       silent=mock.ANY,
                                       use_logger=mock.ANY,
                                       output_filepath=None,
                                       cwd=self.config.project_root)

        diff_filter = "value"
        self.config.git_diff_filter = diff_filter
        self.find_includes._get_diff_using_merge_base_hash('hash')
        run_command.assert_called_with(
            f'git diff hash HEAD --name-only --diff-filter={diff_filter}',
            build_shell=mock.ANY,
            fast_fail=mock.ANY,
            silent=mock.ANY,
            use_logger=mock.ANY,
            output_filepath=None,
            cwd=self.config.project_root)

    @patch('swq.find_includes.find_includes.LOGGER', create=True)
    @patch('os.path.normpath')
    def test_get_file_diff_from_head_to_merge_base(self, normpath_method,
                                                   logger):
        """Test get_file_diff_from_head_to_merge_base()"""
        normpath_method.return_value = 'some/path'

        with patch.object(FindIncludes, '_get_merge_base_hash') \
                as mock_find_includes_get_merge_base_hash,\
                patch.object(FindIncludes, 'read_filepaths_from_lines')\
                as mock_find_influces_read_filepaths_from_lines,\
                patch.object(FindIncludes, '_get_diff_using_merge_base_hash')\
                as mock_find_includes_get_diff_using_merge_base_hash:
            mock_find_includes_get_merge_base_hash.return_value = ['hash', 0]
            mock_find_includes_get_diff_using_merge_base_hash.return_value = \
                ['some/path', 0]
            mock_find_influces_read_filepaths_from_lines.return_value = \
                ['some/path']
            value = self.find_includes.get_file_diff_from_head_to_merge_base()

            mock_find_includes_get_merge_base_hash.assert_called()
            mock_find_includes_get_diff_using_merge_base_hash.\
                assert_called_with('hash')
            mock_find_influces_read_filepaths_from_lines.\
                assert_called_with(['some/path'])
            logger.debug.assert_called()
            normpath_method.assert_called()
            self.assertEqual(value, ['some/path'])

    def test_read_filepaths_from_lines(self):
        """Test read_filepaths_from_lines()"""
        line_or_lines = 'line'
        return_value = \
            self.find_includes.read_filepaths_from_lines(line_or_lines)
        self.assertEqual(return_value, ['line'])
        line_or_lines = ['line', 'line', 'line']
        return_value = \
            self.find_includes.read_filepaths_from_lines(line_or_lines)
        self.assertEqual(return_value, ['line', 'line', 'line'])

    @patch('os.walk')
    def test_initialize_search_directories(self, walk):
        """Test initialize_search_directories()"""
        def generator():
            yield ('current_folder', ['.git', 'dir1',
                                      'dir2'], ['file1', 'file2'])

        return_value = self.find_includes.initialize_search_directories()

        self.config = mock.Mock(source_extensions=[".cpp", ".c", ".inl"],
                                header_extensions=[".hpp", ".h", ".inl"],
                                blacklist_pattern="",
                                code_dirs_file=False,
                                project_root="foo/bar")

        self.find_includes = FindIncludes(self.config)
        walk.return_value = generator()

        return_value = self.find_includes.initialize_search_directories()

        walk.assert_called()

        self.assertEqual(return_value, {'dir1', 'dir2'})

    @patch.object(FindIncludes, 'convert_to_repo_relative_path')
    def test_norm_filepaths(self, convert):
        """Test norm_filepaths()"""
        convert.return_value = 'bar/foo'

        return_value = \
            self.find_includes.norm_filepaths(
                ['root/foo/bar', 'root/bar/foo'])

        self.assertEqual(return_value, ['bar/foo', 'bar/foo'])
        convert.has_calls(
            [call('root', 'root/foo/bar'),
             call('root', 'root/bar/foo')])

    # pylint: disable=R0913
    @patch.object(FindIncludes, 'read_filepaths_from_lines')
    @patch.object(FindIncludes, 'norm_filepaths')
    @patch.object(FindIncludes, 'get_file_diff_from_head_to_merge_base')
    @patch('sys.stdin.readlines')
    def test_get_input_files(self, stdin_read, get_diff, norm_filepaths,
                             read_filepaths):
        """Test get_input_files()"""
        get_diff.return_value = 'foo'
        stdin_read.return_value = ['root/foo/bar', 'root/bar/foo']
        norm_filepaths.return_value = ['root/foo/bar', 'root/bar/foo']

        self.config = mock.Mock(source_extensions=[".cpp", ".c", ".inl"],
                                header_extensions=[".hpp", ".h", ".inl"],
                                blacklist_pattern="",
                                from_stdin=True,
                                project_root="root")
        self.find_includes = FindIncludes(self.config)

        return_value = \
            self.find_includes.get_input_files()
        stdin_read.assert_called()
        read_filepaths.assert_called_with(['root/foo/bar', 'root/bar/foo'])
        norm_filepaths.assert_called_with(['root/foo/bar', 'root/bar/foo'])
        # self.assertEqual(return_value, ['root/foo/bar', 'root/bar/foo'])

        self.config = mock.Mock(source_extensions=[".cpp", ".c", ".inl"],
                                header_extensions=[".hpp", ".h", ".inl"],
                                blacklist_pattern="",
                                from_stdin=False,
                                from_list=True,
                                project_root="root")
        self.find_includes = FindIncludes(self.config)
        return_value = \
            self.find_includes.get_input_files()
        # norm_filepaths.assert_called_with(0, 'root')
        self.assertEqual(return_value, ['root/foo/bar', 'root/bar/foo'])

        self.config = mock.Mock(source_extensions=[".cpp", ".c", ".inl"],
                                header_extensions=[".hpp", ".h", ".inl"],
                                blacklist_pattern="",
                                from_stdin=False,
                                from_list=False,
                                project_root="root")
        self.find_includes = FindIncludes(self.config)
        return_value = \
            self.find_includes.get_input_files()
        get_diff.assert_called()
        self.assertEqual(return_value, 'foo')

    @patch('swq.find_includes.find_includes.LOGGER', create=True)
    @patch('swq.find_includes.find_includes.remove_empty_lines_from_file')
    @patch('builtins.print')
    @patch('os.path.join')
    def test_create_output_producer(self, join, mocked_print, remove_lines,
                                    logger):
        """Test create_output_producer()"""
        mocked_print.return_value = 0

        self.config = mock.Mock(source_extensions=[".cpp", ".c", ".inl"],
                                header_extensions=[".hpp", ".h", ".inl"],
                                blacklist_pattern="",
                                to_stdout=True,
                                project_root="root")
        with patch('swq.find_includes.find_includes.create_dirs_if_necessary'):
            self.find_includes = FindIncludes(self.config)
        return_method = self.find_includes.create_output_producer()
        return_method(['foo', 'bar'])

        mocked_print.has_calls([call('foo'), call('bar')])

        join.return_value = os.path.normpath('root/foo')
        expected_output_file = join.return_value
        remove_lines.return_value = 0

        with patch('swq.common.filesystem.filesystem_utils.open',
                   new=mock_open(read_data=""),
                   create=True) as _file, \
            patch('swq.find_includes.find_includes.create_dirs_if_necessary'):
            self.config = mock.Mock(source_extensions=[".cpp", ".c", ".inl"],
                                    header_extensions=[".hpp", ".h", ".inl"],
                                    blacklist_pattern="",
                                    to_stdout=False,
                                    output_file="foo",
                                    project_root="root")
            self.find_includes = FindIncludes(self.config)
            return_method = self.find_includes.create_output_producer()
            return_method(['foo', 'bar'])
            logger.info.assert_called()
            logger.debug.assert_called()
            remove_lines.assert_called_with(expected_output_file)
            _file.assert_called_with(expected_output_file,
                                     mode='wt',
                                     buffering=mock.ANY,
                                     encoding='utf-8',
                                     errors=mock.ANY,
                                     newline=mock.ANY,
                                     closefd=mock.ANY,
                                     opener=mock.ANY)

    def test_check_config_parameters(self):
        """Test check_config_parameters()"""

        self.config = mock.Mock(source_extensions=[".cpp", ".c", ".inl"],
                                header_extensions=[".hpp", ".h", ".inl"],
                                blacklist_pattern="",
                                find_include_strategy='notall',
                                project_root="foo/bar")

        self.find_includes = FindIncludes(self.config)
        self.assertRaises(AssertionError,
                          self.find_includes.check_config_parameters)

        self.config = mock.Mock(source_extensions=[".cpp", ".c", ".inl"],
                                header_extensions=[".hpp", ".h", ".inl"],
                                blacklist_pattern="",
                                find_include_strategy='all',
                                project_root="foo/bar")

        self.find_includes = FindIncludes(self.config)
        try:
            self.find_includes.check_config_parameters()
        except AssertionError:
            self.fail('check_config_parameters raised AssertionError')

        self.config = mock.Mock(source_extensions=[".cpp", ".c", ".inl"],
                                header_extensions=[".hpp", ".h", ".inl"],
                                blacklist_pattern="",
                                find_include_strategy='minimal',
                                project_root="foo/bar")

        self.find_includes = FindIncludes(self.config)
        try:
            self.find_includes.check_config_parameters()
        except AssertionError:
            self.fail('check_config_parameters raised AssertionError')

    def test_is_3rd_party_include_contains(self):
        """Test is_3rd_party_include()"""

        include_path = ['vmc', 'dir']
        prefixes = ['vmc']

        return_value = self.find_includes.is_3rd_party_include(
            include_path, prefixes)

        self.assertEqual(return_value, True)

    def test_is_3rd_party_include_not_contains(self):
        """Test is_3rd_party_include()"""

        include_path = ['dir']
        prefixes = ['vmc']

        return_value = self.find_includes.is_3rd_party_include(
            include_path, prefixes)

        self.assertEqual(return_value, False)
