""" Test for a python project """
import os
import unittest
from unittest.mock import call, patch

from lucxbox.tools.lucxbau_yaml_checker import lucxbau_yaml_checker

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), 'resources')
CONFIG_DIR = os.path.join(RESOURCES_DIR, 'configs')


class TestYamlChecker(unittest.TestCase):
    def setUp(self):
        self.jar_path = "dummy/path/to/lucxbau.jar"
        self.yaml_checker = lucxbau_yaml_checker.YamlChecker(self.jar_path)

    def test_fail_missing_config_file(self):
        with self.assertRaises(SystemExit) as sys_exit:
            self.yaml_checker.check_configs("not/a/file.yaml")
        self.assertEqual(404, sys_exit.exception.code)

    def test_fail_missing_config_dir(self):
        with self.assertRaises(SystemExit) as sys_exit:
            self.yaml_checker.check_configs("not/a/dir/")
        self.assertEqual(404, sys_exit.exception.code)

    def test_fail_empty_config_dir(self):
        config = os.path.join(CONFIG_DIR, 'empty')
        with self.assertRaises(SystemExit) as sys_exit:
            self.yaml_checker.check_configs(config)
        self.assertEqual(404, sys_exit.exception.code)

    def test_works_with_existing_file(self):
        config = os.path.join(CONFIG_DIR, "config.yaml")
        with patch.object(self.yaml_checker, 'config_file_ok', return_value=True) as config_ok:
            self.yaml_checker.check_configs(config)
        self.assertTrue(config_ok.called)
        config_ok.assert_called_with(config)

    def test_works_with_existing_dir(self):
        with patch.object(self.yaml_checker, 'config_file_ok', return_value=True) as config_ok:
            self.yaml_checker.check_configs(CONFIG_DIR)
        config_ok.assert_has_calls([call(os.path.join(CONFIG_DIR, "config.yaml")),
                                    call(os.path.join(CONFIG_DIR, "default.yml")),
                                    call(os.path.join(CONFIG_DIR, "inc", "dummy.yml"))],
                                   any_order=True)
        self.assertEqual(3, config_ok.call_count)

    def test_works_with_excluded_dir(self):
        with patch.object(self.yaml_checker, 'config_file_ok', return_value=True) as config_ok:
            self.yaml_checker.check_configs(CONFIG_DIR, excludes=[os.path.join(CONFIG_DIR, 'inc')])
        self.assertEqual(2, config_ok.call_count)
        config_ok.assert_has_calls([call(os.path.join(CONFIG_DIR, "config.yaml")),
                                    call(os.path.join(CONFIG_DIR, "default.yml"))])

    def test_config_check_jar_call(self):
        config_to_check = "dummy.yml"
        with patch.object(lucxbau_yaml_checker.subprocess, 'run', return_value=True) as subprocess:
            self.yaml_checker.config_file_ok(config_to_check)
        expected_command = 'java -jar \"' + self.jar_path + '\" -f "' + os.path.abspath(config_to_check) + '" --debug --verbose'
        subprocess.assert_called_with(expected_command, shell=True, check=True)


class TestLucxbauYamlChecker(unittest.TestCase):
    def test_missing_file_version_fail(self):
        jenkinsfile = os.path.join(RESOURCES_DIR, "not_a_file")
        with self.assertRaises(SystemExit) as sys_exit:
            lucxbau_yaml_checker.get_version_from_jenkinsfile(jenkinsfile)
        self.assertEqual(404, sys_exit.exception.code)

    def test_no_version_fail(self):
        jenkinsfile = os.path.join(RESOURCES_DIR, "Jenkinsfile-broken")
        with self.assertRaises(SystemExit) as sys_exit:
            lucxbau_yaml_checker.get_version_from_jenkinsfile(jenkinsfile)
        self.assertEqual(1, sys_exit.exception.code)

    def test_get_version_working_1(self):
        jenkinsfile = os.path.join(RESOURCES_DIR, "Jenkinsfile-1")
        expected_result = '1.2.3'
        version = lucxbau_yaml_checker.get_version_from_jenkinsfile(jenkinsfile)
        self.assertEqual(expected_result, version)

    def test_get_version_working_2(self):
        jenkinsfile = os.path.join(RESOURCES_DIR, "Jenkinsfile-2")
        expected_result = '1.2.3'
        version = lucxbau_yaml_checker.get_version_from_jenkinsfile(jenkinsfile)
        self.assertEqual(expected_result, version)

    def test_get_version_working_3(self):
        jenkinsfile = os.path.join(RESOURCES_DIR, "Jenkinsfile-3")
        expected_result = 'ft/my_branch/LUCX-234-test'
        version = lucxbau_yaml_checker.get_version_from_jenkinsfile(jenkinsfile)
        self.assertEqual(expected_result, version)

    def test_excluded_file(self):
        result = lucxbau_yaml_checker.is_file_excluded("a/b/c/file.yml", ['a/b/'])
        self.assertTrue(result)

    def test_not_excluded_file(self):
        result = lucxbau_yaml_checker.is_file_excluded("x/y/z/file.yml", ['a/b/'])
        self.assertFalse(result)

    def test_multiple_excludes_1(self):
        result = lucxbau_yaml_checker.is_file_excluded("x/y/z/file.yml", ['a/b/', 'x/y/another-dir'])
        self.assertFalse(result)

    def test_multiple_excludes_2(self):
        result = lucxbau_yaml_checker.is_file_excluded("x/y/z/file.yml",
                                                       ['a/b/', 'x/another-dir', 'x/y/z'])
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
