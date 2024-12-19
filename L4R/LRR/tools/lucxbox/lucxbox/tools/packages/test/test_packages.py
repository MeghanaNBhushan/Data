""" Test for a python project """

import unittest
from unittest import mock
import os

import lucxbox.tools.packages.package as package
import lucxbox.tools.packages.helper as helper

HERE = os.path.abspath(os.path.dirname(__file__))


# pylint: disable=unused-argument
def f_not_found_exception(exception, shell=False):
    raise FileNotFoundError


class TestMethods(unittest.TestCase):

    @mock.patch("lucxbox.tools.packages.packages.LOGGER", create=True)
    def test_get_packages(self, _):
        found_packages = package.get_packages(os.path.join(HERE, 'data'), 'rb_package.json')
        self.assertEqual(len(found_packages), 1)
        found_packages = package.get_packages(os.path.join(HERE, 'data'), 'my_package.json')
        self.assertEqual(len(found_packages), 1)

    @mock.patch("lucxbox.tools.packages.packages.LOGGER", create=True)
    def test_get_disk_hash(self, _):
        found_packages = package.get_packages(os.path.join(HERE, 'data'), 'rb_package.json', False, None, None, "update")
        print(found_packages[0].get_disk_hash())
        self.assertEqual(found_packages[0].get_disk_hash(), "92c8e646fea506f94b3ce4e5dd324c8f::V2")

    # pylint: disable=invalid-name
    @mock.patch('lucxbox.lib.lucxutils.execute', side_effect=f_not_found_exception)
    def test_package_git_available_negative(self, _):
        self.assertFalse(helper.git_available())

    # pylint: disable=invalid-name
    @mock.patch('lucxbox.lib.lucxutils.execute', return_value='git version 2.19.2.windows.1')
    def test_package_git_available_positive(self, _):
        self.assertTrue(helper.git_available())

    def test_package_git_fetch_ref(self):
        with mock.patch("lucxbox.lib.lucxutils.execute") as execute_mock:
            execute_mock.return_value = ('', '', 0)
            helper.git_fetch_ref('.', 'develop')
            expected = ('git fetch --recurse-submodules=no origin develop',)
            self.assertEqual(execute_mock.call_args[0], expected)

    def test_package_git_checkout(self):
        with mock.patch("lucxbox.lib.lucxutils.execute") as execute_mock:
            execute_mock.return_value = ('', '', 0)
            helper.git_checkout('.', ['asdf'], '1234')
            expected = ('git checkout --force 1234 -- asdf',)
            self.assertEqual(execute_mock.call_args[0], expected)

    # pylint: disable=invalid-name
    def test_package_get_commits_of_file(self):
        out = '1234\n5678'
        with mock.patch("lucxbox.lib.lucxutils.execute") as execute_mock:
            execute_mock.return_value = (out, '', 0)
            commits = helper.get_commits_of_file('HEAD', '.', 'test.txt', False)
            expected = ('git log --pretty=format:"%h" --abbrev=40 HEAD -- test.txt',)
            self.assertEqual(execute_mock.call_args[0], expected)
            self.assertEqual(commits[0], out.split()[0])
            self.assertEqual(commits[1], out.split()[1])

    # pylint: disable=invalid-name
    def test_package_get_version_from_commit(self):
        out = r'+   semantic_name: "1.2.3"'
        with mock.patch("lucxbox.lib.lucxutils.execute") as execute_mock:
            execute_mock.return_value = (out, '', 0)
            version = helper.get_version_from_commit('.', 'test.txt', "1234", "semantic")
            expected = ('git diff "1234^..1234" -- test.txt',)
            self.assertEqual(execute_mock.call_args[0], expected)
            self.assertIsNotNone(version)
            self.assertEqual(version, '1.2.3')

    # pylint: disable=invalid-name
    def test_package_get_versions_from_commits(self):
        with mock.patch("lucxbox.tools.packages.helper.get_version_from_commit") as get_version_mock:
            get_version_mock.return_value = '1.2.3'
            versions = helper.get_versions_from_commits('.', 'test.txt', ['1234'], 'semantic')
            self.assertEqual(versions[0], '1.2.3')
            self.assertEqual(len(versions), 1)


    def test_get_hash_version_from_md5(self):
        assert package.get_hash_version_from_md5("asdf") == 1
        assert package.get_hash_version_from_md5("asdf::V1") == 1
        assert package.get_hash_version_from_md5("asdf::V2") == 2
        with self.assertRaises(ValueError):
            package.get_hash_version_from_md5("asdf::A2")


if __name__ == "__main__":
    unittest.main()
