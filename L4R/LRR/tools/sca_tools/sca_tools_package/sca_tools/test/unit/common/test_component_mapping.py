"""Test for swq.common/component_mapping.py"""
import io

from unittest import TestCase
from unittest.mock import patch, mock_open

from swq.common.component_mapping import ComponentMapper, no_regex_matches, \
    matches_wildcard_pattern


def _generate_codeowners_file_content():
    return io.StringIO('\
*.py @a\n\
*.cmd @b @a\n\
*.bat @c\n\
*.cmake @d\n\
\n\
**/cool*/** @e\n\
**/ws/** @f\n\
**/abc/** @f\n')


def _generate_codeowners_file_one_content():
    return io.StringIO('\
*.py @a\n\
*.cmd @b @a\n\
*.bat @c\n\
*.cmake @d\n\
\n')


def _generate_codeowners_file_two_content():
    return io.StringIO('\
**/cool*/** @e\n\
**/ws/** @f\n\
**/abc/** @f\n')


class TestComponentMapping(TestCase):
    """Test class for the component mapper"""
    def setUp(self):
        self.codeowners_file = ['codeowners.txt']
        self.mock_logger = patch("swq.common.component_mapping.LOGGER")
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)

    def test_no_regex_matches(self):
        """ Test no_regex_matches"""
        regexp = ['[0-9]+']
        check_string = 'foo'

        result = no_regex_matches(regexp, check_string)
        self.assertTrue(result)

        check_string = '1234'
        result = no_regex_matches(regexp, check_string)
        self.assertFalse(result)

    def test_component_mapper(self):
        """Test component mapper"""
        with patch('builtins.open',
                   return_value=_generate_codeowners_file_content(),
                   create=True), \
            patch('os.path.exists') as mock_path_exists, \
            patch('swq.common.component_mapping.log_and_exit') \
            as mock_log_and_exit:

            mock_path_exists.return_value = False
            component_mapper = ComponentMapper(self.codeowners_file)
            mock_log_and_exit.assert_called_once()

        with patch('builtins.open',
                   return_value=_generate_codeowners_file_content(),
                   create=True), \
            patch('os.path.exists') as mock_path_exists, \
            patch('swq.common.component_mapping.log_and_exit') \
            as mock_log_and_exit:

            mock_path_exists.return_value = True
            component_mapper = ComponentMapper(self.codeowners_file)
            mock_log_and_exit.assert_not_called()

            # Expect one additional component("") and team("undefined")
            # for not defined paths
            self.assertTrue(len(component_mapper.components) == 7)
            self.assertTrue(component_mapper.components[0].pattern == "*.py")
            self.assertTrue("a" in component_mapper.components[0].team)
            self.assertTrue(component_mapper.components[1].pattern == "*.cmd")
            self.assertTrue("a" in component_mapper.components[1].team)
            self.assertTrue("b" in component_mapper.components[1].team)
            self.assertTrue(component_mapper.components[2].pattern == "*.bat")
            self.assertTrue("c" in component_mapper.components[2].team)
            self.assertTrue(
                component_mapper.components[3].pattern == "*.cmake")
            self.assertTrue("d" in component_mapper.components[3].team)

        # Test with multiple codeowner files
        self.codeowners_file = ['codeowners1', 'codeowners2']
        with patch('builtins.open',
                   return_value=_generate_codeowners_file_one_content(),
                   create=True) as file_one_mock, \
            patch('os.path.exists') as mock_path_exists, \
            patch('swq.common.component_mapping.log_and_exit') \
            as mock_log_and_exit:

            file_two_mock = mock_open()
            file_two_mock.return_value = \
                _generate_codeowners_file_two_content()
            handlers = (file_one_mock.return_value, file_two_mock.return_value)
            file_one_mock.side_effect = handlers

            mock_path_exists.return_value = True
            component_mapper = ComponentMapper(self.codeowners_file)
            mock_log_and_exit.assert_not_called()

            self.assertTrue(len(component_mapper.components) == 7)
            self.assertTrue(component_mapper.components[0].pattern == "*.py")
            self.assertTrue("a" in component_mapper.components[0].team)
            self.assertTrue(component_mapper.components[1].pattern == "*.cmd")
            self.assertTrue("a" in component_mapper.components[1].team)
            self.assertTrue("b" in component_mapper.components[1].team)
            self.assertTrue(component_mapper.components[2].pattern == "*.bat")
            self.assertTrue("c" in component_mapper.components[2].team)
            self.assertTrue(
                component_mapper.components[3].pattern == "*.cmake")
            self.assertTrue("d" in component_mapper.components[3].team)

    def test_get_teams_for_path(self):
        """Test get_teams_for_path()"""
        with patch('builtins.open',
                   return_value=_generate_codeowners_file_content(),
                   create=True), \
            patch('os.path.exists') as mock_path_exists, \
            patch('swq.common.component_mapping.log_and_exit'):

            mock_path_exists.return_value = True
            component_mapper = ComponentMapper(self.codeowners_file)

            filepath = 'C:/ws/test.py'
            expected_teams = [['a'], ['f']]
            self.assertTrue(
                component_mapper.get_teams_for_path(filepath) ==
                expected_teams)
            filepath = 'C:/ws/test.cmd'
            expected_teams = [["b", "a"], ["f"]]
            self.assertTrue(
                component_mapper.get_teams_for_path(filepath) ==
                expected_teams)
            filepath = '/ws/test.undefined'
            expected_teams = [['f']]
            self.assertTrue(
                component_mapper.get_teams_for_path(filepath) ==
                expected_teams)
            filepath = 'C:/ws/some/other/abc/test.py'
            expected_teams = [['a'], ['f'], ['f']]
            self.assertEqual(component_mapper.get_teams_for_path(filepath),
                             expected_teams)
            filepath = 'D:/tools/something.undefined'
            expected_teams = [["undefined"]]
            self.assertTrue(
                component_mapper.get_teams_for_path(filepath) ==
                expected_teams)

    def test_components_for_path(self):
        """Test components_for_path()"""
        with patch('builtins.open',
                   return_value=_generate_codeowners_file_content(),
                   create=True), \
            patch('os.path.exists') as mock_path_exists, \
            patch('swq.common.component_mapping.log_and_exit'):

            mock_path_exists.return_value = True
            component_mapper = ComponentMapper(self.codeowners_file)

            components = component_mapper.get_components_for_path(
                "/ws/test.py")
            self.assertTrue(len(components) == 2)
            self.assertTrue(components[0].pattern == "*.py")
            self.assertTrue("a" in components[0].team)
            self.assertTrue(components[1].pattern == "**/ws/**")
            self.assertTrue("f" in components[1].team)

            components = component_mapper.get_components_for_path(
                "C:/ws/test.cmd")
            self.assertEqual(len(components), 2)
            self.assertTrue(components[0].pattern == "*.cmd")
            self.assertTrue("a" in components[0].team)
            self.assertTrue("b" in components[0].team)
            self.assertTrue(components[1].pattern == "**/ws/**")
            self.assertTrue("f" in components[1].team)

    def test_apply_codeowners_globbing_rules(self):
        """Tests _apply_codeowners_globbing_rules()"""
        string = 'foo/bar/foobar/somefile.hpp'
        wildcard_expression = "*"
        self.assertTrue(matches_wildcard_pattern(string, wildcard_expression))

        wildcard_expression = "foo/bar/foobar/"
        self.assertTrue(matches_wildcard_pattern(string, wildcard_expression))

        wildcard_expression = "bar/"
        self.assertTrue(matches_wildcard_pattern(string, wildcard_expression))

        wildcard_expression = "somefile.hpp"
        self.assertTrue(matches_wildcard_pattern(string, wildcard_expression))

        wildcard_expression = "**/foobar/**"
        self.assertTrue(matches_wildcard_pattern(string, wildcard_expression))

        wildcard_expression = "*.hpp"
        self.assertTrue(matches_wildcard_pattern(string, wildcard_expression))

        wildcard_expression = "*/bar/foobar/somefile.hpp"
        self.assertTrue(matches_wildcard_pattern(string, wildcard_expression))

        wildcard_expression = "foo/bar"
        self.assertFalse(matches_wildcard_pattern(string, wildcard_expression))

        wildcard_expression = "bar/foobar/"
        self.assertFalse(matches_wildcard_pattern(string, wildcard_expression))
