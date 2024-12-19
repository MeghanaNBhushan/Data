""" Test for submodule changedfiles """

import os
import unittest
from unittest import mock
from unittest.mock import MagicMock
from shutil import copyfile
import git
from lucxbox.tools.submodule_changedfiles import submodule_changedfiles
from lucxbox.tools.gitw import gitw


def return_revision_sample(*_args):
    return "1", "2"


def return_revision_none(*_args):
    return None, None


class TestSubmoduleChangedfiles(unittest.TestCase):
    """ Test class for submodule changedfiles """

    def __init__(self, *args, **kwargs):
        super(TestSubmoduleChangedfiles, self).__init__(*args, **kwargs)
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.resource_dir = os.path.join(self.script_dir, "resources")
        self.repo_dir = os.path.abspath(self.script_dir + "../../../../../")
        self.is_submodule_path = True
        self.mock_repo = gitw.Repo(self.repo_dir)
        self.original_changed_files = [
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\jenkins\\configs\\default_vag_e3_mrr.yaml",
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\jenkins\\configs\\inc\\stage\\checkout_scm.yaml",
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\jenkins\\scripts\\include_changed_files_of_submodules.py",
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\ip_ra5"
        ]
        self.submodule_changed_files = [
            "per/EnsRObjExternalSensor/src/runnables/per_sppExtRObjRunnable.cpp",
            "per/mal/src/modules/types/algorithms/outOfSpec.cpp",
            "per/mal/src/modules/types/algorithms/outOfSpec.hpp",
            "per/mal/src/modules/types/calcMal.cpp",
            "per/mal/src/modules/types/calcMal.hpp",
            "per/mal/src/modules/types/malConstants.hpp"
        ]
        self.updated_changed_files = [
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\ip_ra5\\per\\EnsRObjExternalSensor\\src\\runnables\\per_sppExtRObjRunnable.cpp",
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\ip_ra5\\per\\mal\\src\\modules\\types\\algorithms\\outOfSpec.cpp",
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\ip_ra5\\per\\mal\\src\\modules\\types\\algorithms\\outOfSpec.hpp",
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\ip_ra5\\per\\mal\\src\\modules\\types\\calcMal.cpp",
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\ip_ra5\\per\\mal\\src\\modules\\types\\calcMal.hpp",
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\ip_ra5\\per\\mal\\src\\modules\\types\\malConstants.hpp",
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\jenkins\\configs\\default_vag_e3_mrr.yaml",
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\jenkins\\configs\\inc\\stage\\checkout_scm.yaml",
            "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\jenkins\\scripts\\include_changed_files_of_submodules.py"
        ]

    def get_resource_path(self, path: str):
        return os.path.join(self.resource_dir, path)

    def abspath_return_value(self, *args):
        if self.is_submodule_path:
            self.is_submodule_path = False
            return "C:\\JT\\ws\\commonrepo@1\\repo\\1r1v_fw\\" + args[0]
        return args[0].replace("/", "\\")

    def test_changed_files_from_file(self):
        # Existing changed files file
        changed_files_file = self.get_resource_path("origin_changed_files_file.txt")
        changed_files = submodule_changedfiles.get_changed_files_from_file(changed_files_file)
        self.assertEqual(self.original_changed_files, changed_files)

        # Empty changed files file
        changed_files_file = self.get_resource_path("tmp_changed_files_file.txt")
        changed_files = submodule_changedfiles.get_changed_files_from_file(changed_files_file)
        self.assertEqual([], changed_files)

        # Non-existing changed files file
        changed_files_file = self.get_resource_path("non_existing_file.txt")
        with self.assertRaises(Exception) as raise_context:
            submodule_changedfiles.get_changed_files_from_file(changed_files_file)
        self.assertEqual(str(raise_context.exception), 'Could not read changed files file')

    @mock.patch("os.path.abspath")
    def test_append_changed_files_ok(self, mock_abspath):
        self.is_submodule_path = True
        mock_abspath.side_effect = self.abspath_return_value

        origin_changed_files_file = self.get_resource_path("origin_changed_files_file.txt")
        changed_files = submodule_changedfiles.get_changed_files_from_file(origin_changed_files_file)
        expected_changed_files_file = self.get_resource_path("expected_changed_files_file.txt")
        expected_changed_files = submodule_changedfiles.get_changed_files_from_file(expected_changed_files_file)
        changed_files = submodule_changedfiles.append_submodule_changed_files(changed_files, self.submodule_changed_files,
                                                                              "ip_ra5")
        self.assertEqual(expected_changed_files, changed_files)

    @mock.patch("os.path.abspath")
    def test_append_changed_files_fail(self, mock_abspath):
        mock_abspath.side_effect = self.abspath_return_value

        origin_changed_files_file = self.get_resource_path("origin_changed_files_file.txt")
        changed_files = submodule_changedfiles.get_changed_files_from_file(origin_changed_files_file)
        with self.assertRaises(ValueError) as raise_context:
            self.is_submodule_path = True
            submodule_changedfiles.append_submodule_changed_files(changed_files, self.submodule_changed_files,
                                                                  "ip_ra51")
        self.assertEqual(str(raise_context.exception), 'list.remove(x): x not in list')

    def test_update_changed_files_file(self):
        # Test for existing dir
        tmp_changed_files_file = self.get_resource_path("tmp_changed_files_file_empty.txt")
        origin_changed_files_file = self.get_resource_path("origin_changed_files_file.txt")
        expected_changed_files = submodule_changedfiles.get_changed_files_from_file(origin_changed_files_file)
        submodule_changedfiles.update_changed_files_file(tmp_changed_files_file, expected_changed_files)
        actual_changed_files = submodule_changedfiles.get_changed_files_from_file(tmp_changed_files_file)
        self.assertEqual(expected_changed_files, actual_changed_files)

        # Test for non-existing dir
        non_existing_file = self.get_resource_path(os.path.relpath("non_existing/tmp_changed_files_file.txt"))
        with self.assertRaises(Exception) as raise_context:
            submodule_changedfiles.update_changed_files_file(non_existing_file, [])
        self.assertEqual(str(raise_context.exception), 'Could not write changed files file')

    @mock.patch("os.path.abspath")
    @mock.patch("lucxbox.tools.submodule_changedfiles.submodule_changedfiles.get_submodule_changed_revision")
    @mock.patch("lucxbox.tools.submodule_changedfiles.submodule_changedfiles.get_submodule_changed_files")
    def test_update_changed_files(self, mock_get_sub_changed_files, mock_get_sub_changed_revision, mock_abspath):
        # Test for case not changed revision, expected no error
        mock_get_sub_changed_revision.side_effect = return_revision_none
        submodule_changedfiles.update_submodule_changed_files("non_existing.txt", "test_submodule", "test_commit")

        # Test for case empty submodule changed file, expected no error
        mock_get_sub_changed_revision.side_effect = return_revision_sample
        mock_get_sub_changed_files.return_value = []
        submodule_changedfiles.update_submodule_changed_files("non_existing.txt", "test_submodule", "test_commit")

        # Test positive case
        mock_get_sub_changed_revision.side_effect = return_revision_sample
        mock_get_sub_changed_files.return_value = self.submodule_changed_files
        mock_abspath.side_effect = self.abspath_return_value
        origin_file = self.get_resource_path("origin_changed_files_file.txt")
        tmp_file = self.get_resource_path("tmp_changed_files_file.txt")
        copyfile(origin_file, tmp_file)
        self.is_submodule_path = True
        submodule_changedfiles.update_submodule_changed_files(tmp_file, "ip_ra5", "test_commit")
        actual_changed_files = submodule_changedfiles.get_changed_files_from_file(tmp_file)
        self.assertEqual(self.updated_changed_files, actual_changed_files)
        submodule_changedfiles.update_changed_files_file(tmp_file, [])

    @mock.patch("lucxbox.tools.gitw.gitw.Repo")
    @mock.patch("os.getcwd")
    def test_get_sub_changed_revision(self, mock_getcwd, mock_repo):
        mock_getcwd.return_value = self.repo_dir
        mock_repo.return_value = self.mock_repo

        # Test invalid dest commit id
        with self.assertRaises(git.GitCommandError):
            submodule_changedfiles.get_submodule_changed_revision("invalid", "test")
        with self.assertRaises(git.GitCommandError):
            submodule_changedfiles.get_submodule_changed_revision("", "test")

        # Test with invalid submodule path
        with self.assertRaises(git.GitCommandError):
            submodule_changedfiles.get_submodule_changed_revision("develop", "")

        # Test with no updated revision
        old_rev, new_rev = submodule_changedfiles.get_submodule_changed_revision("develop", "test")
        self.assertEqual(None, old_rev)
        self.assertEqual(None, new_rev)

        # Test with updated revision
        self.mock_repo.git = MagicMock()
        self.mock_repo.git.diff = MagicMock()
        self.mock_repo.git.diff.return_value = """diff --git a/ip_ra5 b/ip_ra5
index 1e4633fcf..5cd43fda4 160000
--- a/ip_ra5
+++ b/ip_ra5
@@ -1 +1 @@
-Subproject commit 1e4633fcf1ec60e487651b5169bc2e1532a704b7
+Subproject commit 5cd43fda4be82b1b6c333a4ba917c1314934136e
"""
        old_rev, new_rev = submodule_changedfiles.get_submodule_changed_revision("develop", "test")
        self.assertEqual("1e4633fcf1ec60e487651b5169bc2e1532a704b7", old_rev)
        self.assertEqual("5cd43fda4be82b1b6c333a4ba917c1314934136e", new_rev)

    @mock.patch("lucxbox.tools.gitw.gitw.Repo")
    def test_get_sub_changed_files(self, mock_repo):
        mock_repo.return_value = self.mock_repo

        # Test invalid parameter
        with self.assertRaises(git.GitCommandError):
            submodule_changedfiles.get_submodule_changed_files("test", "invalid1", "invalid2")

        self.mock_repo.git = MagicMock()
        self.mock_repo.remote = MagicMock()
        self.mock_repo.git.diff = MagicMock()

        # Test with no submodule changed files
        self.mock_repo.git.diff.return_value = ""
        result = submodule_changedfiles.get_submodule_changed_files("ip_ra5", "1", "2")
        self.assertEqual(len(result), 0)

        self.mock_repo.git.diff.return_value = """\
per/EnsRObjExternalSensor/src/runnables/per_sppExtRObjRunnable.cpp
per/mal/src/modules/types/algorithms/outOfSpec.cpp
per/mal/src/modules/types/algorithms/outOfSpec.hpp
per/mal/src/modules/types/calcMal.cpp
per/mal/src/modules/types/calcMal.hpp
per/mal/src/modules/types/malConstants.hpp
"""
        result = submodule_changedfiles.get_submodule_changed_files("ip_ra5", "1", "2")
        self.assertEqual(result, self.submodule_changed_files)

    @mock.patch("os.getcwd")
    def test_invalid_repo(self, mock_getcwd):
        mock_getcwd.return_value = self.get_resource_path("invalid_dir")
        with self.assertRaises(git.InvalidGitRepositoryError):
            submodule_changedfiles.get_submodule_changed_revision("invalid", "invalid")
        with self.assertRaises(git.InvalidGitRepositoryError):
            submodule_changedfiles.get_submodule_changed_files("invalid_dir", "invalid", "invalid")

if __name__ == "__main__":
    unittest.main()
