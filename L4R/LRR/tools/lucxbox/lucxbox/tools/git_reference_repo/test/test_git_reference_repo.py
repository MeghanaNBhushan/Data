"""
unit tests for the creation and maintenance of reference repos
"""

import hashlib
import os
import unittest
from unittest import mock


import lucxbox.tools.git_reference_repo.git_reference_repo as git_reference_repo


def ref_remote_name(sm_name, sm_url):
    """the reference repo adds a hash to make remote names unique"""
    return sm_name + "_" + hashlib.md5(sm_url.encode()).hexdigest()[:5]


class TestGITReferenceRepos(unittest.TestCase):
    """ Test class for git reference repos """

    @mock.patch("lucxbox.tools.git_reference_repo.git_reference_repo.LOGGER", create=True)
    @mock.patch("os.makedirs")
    @mock.patch("shutil.rmtree")
    @mock.patch("lucxbox.tools.git_reference_repo.git_reference_repo.free_diskspace")
    def test_no_submodules(self, free_diskspace, rmtree, makedirs, logger):
        """
        Test for cloning a repo with a references repo
        """
        free_diskspace.return_value = 5*2**20
        makedirs.return_value = None
        rmtree.return_value = None
        ref_repo = git_reference_repo.Refrepo("fantasy/dir", "ssh://git@foo.bar/repo/test.git", free_storage_new=2, free_storage_update=2)
        with mock.patch.object(ref_repo, '_Refrepo__run_git_clone', return_value=None) as clone_method, \
             mock.patch.object(ref_repo, '_Refrepo__get_gitmodules', return_value="") as modules_method, \
             mock.patch.object(ref_repo, '_Refrepo__get_gitremotes', return_value=[]) as remotes_method, \
             mock.patch.object(ref_repo, '_Refrepo__check_integrity', return_value=0) as integrity_method:
            ref_repo.update()
            clone_method.assert_called_once_with('test.git')
            modules_method.assert_called_once_with('origin/HEAD')
            remotes_method.assert_called_once_with()
            integrity_method.assert_called_once_with()
        self.assertEqual(len(logger.error.mock_calls), 0)

    @mock.patch("lucxbox.tools.git_reference_repo.git_reference_repo.LOGGER", create=True)
    @mock.patch("os.makedirs")
    @mock.patch("shutil.rmtree")
    @mock.patch("lucxbox.tools.git_reference_repo.git_reference_repo.free_diskspace")
    def test_with_submodules(self, free_diskspace, rmtree, makedirs, logger):
        """
        Test for cloning a repo with submodules using a reference repo
           a  <- main repo
           |
           +--b (sm0) <- submodule
           |
           +--c (sm1) <- submodule
           |
           +--d (sm2) <- submodule
        """
        free_diskspace.return_value = 5*2**20
        makedirs.return_value = None
        rmtree.return_value = None
        submodule_str = "[submodule \"sm0\"]\n    path = sm0\n    url = file:///tmp/b/.git\n" + \
                        "[submodule \"sm1\"]\n    path = sm1\n    url = file:///tmp/c/.git\n" + \
                        "[submodule \"sm2\"]\n    path = sm2\n    url = file:///tmp/d/.git\n"
        ref_repo = git_reference_repo.Refrepo("fantasy/dir", "ssh://git@foo.bar/repo/test.git", free_storage_new=2, free_storage_update=2)
        with mock.patch.object(ref_repo, '_Refrepo__run_git_clone', return_value=None) as clone_method, \
             mock.patch.object(ref_repo, '_Refrepo__get_gitmodules', side_effect=[submodule_str, "", "", ""]) as modules_method, \
             mock.patch.object(ref_repo, '_Refrepo__get_gitremotes', return_value=[]) as remotes_method, \
             mock.patch.object(ref_repo, '_Refrepo__check_integrity', return_value=0) as integrity_method, \
             mock.patch.object(ref_repo, '_Refrepo__run_git_addremote', return_value=None) as addremote_method, \
             mock.patch.object(ref_repo, '_Refrepo__run_git_addremote', return_value=None) as addremote_method, \
             mock.patch.object(ref_repo, '_Refrepo__get_git_fetch_config', return_value=""), \
             mock.patch.object(ref_repo, '_Refrepo__set_git_remote_fetch_config', return_value=None) as setfetch_method, \
             mock.patch.object(ref_repo, '_Refrepo__run_git_fetch', return_value=None) as fetch_method:
            ref_repo.update()
            clone_method.assert_called_once_with('test.git')
            self.assertEqual(modules_method.call_count, 4) # main repo + 3 submodules
            remotes_method.assert_called_once_with() # no existing reference repo, call it once - returns nothing
            integrity_method.assert_called_once_with()
            addremote_method.assert_any_call(ref_remote_name("sm0", "file:///tmp/b/.git"), "file:///tmp/b/.git")
            addremote_method.assert_any_call(ref_remote_name("sm1", "file:///tmp/c/.git"), "file:///tmp/c/.git")
            addremote_method.assert_any_call(ref_remote_name("sm2", "file:///tmp/d/.git"), "file:///tmp/d/.git")
            self.assertEqual(addremote_method.call_count, 3)
            setfetch_method.assert_any_call(ref_remote_name("sm0", "file:///tmp/b/.git"))
            setfetch_method.assert_any_call(ref_remote_name("sm1", "file:///tmp/c/.git"))
            setfetch_method.assert_any_call(ref_remote_name("sm2", "file:///tmp/d/.git"))
            self.assertEqual(setfetch_method.call_count, 3)
            fetch_method.assert_any_call(ref_remote_name("sm0", "file:///tmp/b/.git"))
            fetch_method.assert_any_call(ref_remote_name("sm1", "file:///tmp/c/.git"))
            fetch_method.assert_any_call(ref_remote_name("sm2", "file:///tmp/d/.git"))
            self.assertEqual(fetch_method.call_count, 3)
        self.assertEqual(len(logger.error.mock_calls), 0)

    @mock.patch("lucxbox.tools.git_reference_repo.git_reference_repo.LOGGER", create=True)
    @mock.patch("os.makedirs")
    @mock.patch("lucxbox.tools.git_reference_repo.git_reference_repo.free_diskspace")
    def test_insufficient_space_new(self, free_diskspace, makedirs, logger):
        """
        Test for cloning a repo with a references repo
        - we try to create a reference repo but require too much space
        - check that an exception is raised
        """
        makedirs.return_value = None
        free_diskspace.return_value = 1*2**20 # 1MiB free
        ref_repo = git_reference_repo.Refrepo("fantasy/dir", "ssh://git@foo.bar/repo/test.git", free_storage_new=10 ** 30)
        with self.assertRaises(IOError):
            ref_repo.update()
        self.assertEqual(len(logger.error.mock_calls), 0)

    @mock.patch("lucxbox.tools.git_reference_repo.git_reference_repo.LOGGER", create=True)
    @mock.patch("os.makedirs")
    @mock.patch("os.path.exists")
    @mock.patch("shutil.rmtree")
    @mock.patch("lucxbox.tools.git_reference_repo.git_reference_repo.free_diskspace")
    def test_insufficient_space_update(self, free_diskspace, rmtree, path_exists, makedirs, logger):
        """
        Test for cloning a repo with a references repo
        - update the reference repo but require too much space
        - check that an exception is raised
        """
        free_diskspace.return_value = 2*2**20 # 2MiB free
        makedirs.return_value = None
        rmtree.return_value = None
        path_exists.side_effect = [False, False, True] # initial ref repo doesn't exist, for the update it exists
        ref_repo = git_reference_repo.Refrepo("fantasy/dir", "ssh://git@foo.bar/repo/test.git",
                                              free_storage_new=1, free_storage_update=10**30)
        with mock.patch.object(ref_repo, '_Refrepo__run_git_clone', return_value=None) as clone_method, \
             mock.patch.object(ref_repo, '_Refrepo__get_gitmodules', return_value="") as modules_method, \
             mock.patch.object(ref_repo, '_Refrepo__get_gitremotes', return_value=[]) as remotes_method, \
             mock.patch.object(ref_repo, '_Refrepo__check_integrity', return_value=0) as integrity_method:
            ref_repo.update()
            clone_method.assert_called_once_with('test.git')
            modules_method.assert_called_once_with('origin/HEAD')
            remotes_method.assert_called_once_with()
            integrity_method.assert_called_once_with()
            path_exists.assert_any_call("fantasy/dir")
            path_exists.assert_any_call("fantasy/dir" + os.path.sep + "test.git")
            with self.assertRaises(IOError):
                ref_repo.update()
        self.assertEqual(len(logger.error.mock_calls), 0)

    @mock.patch("lucxbox.tools.git_reference_repo.git_reference_repo.LOGGER", create=True)
    @mock.patch("os.makedirs")
    @mock.patch("os.path.exists")
    @mock.patch("shutil.rmtree")
    @mock.patch("lucxbox.tools.git_reference_repo.git_reference_repo.free_diskspace")
    def test_refrepo_corruption(self, free_diskspace, rmtree, path_exists, makedirs, logger):
        """
        Test if the script can recover corruption of the reference repo
        """
        free_diskspace.return_value = 2*2**20 # 2MiB free
        makedirs.return_value = None
        rmtree.return_value = None
        path_exists.side_effect = [False, False, True, True] # initial ref repo doesn't exist, for the update it exists
        ref_repo = git_reference_repo.Refrepo("fantasy/dir", "ssh://git@foo.bar/repo/test.git", free_storage_new=1, free_storage_update=1)
        with mock.patch.object(ref_repo, '_Refrepo__run_git_clone', return_value=None) as clone_method, \
             mock.patch.object(ref_repo, '_Refrepo__update_refrepo', return_value=None) as update_method, \
             mock.patch.object(ref_repo, '_Refrepo__get_gitmodules', return_value="") as modules_method, \
             mock.patch.object(ref_repo, '_Refrepo__get_gitremotes', return_value=[]) as remotes_method, \
             mock.patch.object(ref_repo, '_Refrepo__check_integrity', side_effect=[0, 1, 0]) as integrity_method:
            ref_repo.update()
            path_exists.assert_any_call("fantasy/dir")
            path_exists.assert_any_call("fantasy/dir" + os.path.sep + "test.git")
            ref_repo.update()
            self.assertEqual(clone_method.call_count, 2)
            self.assertEqual(integrity_method.call_count, 3)
            rmtree.assert_called_once_with("fantasy/dir" + os.path.sep + "test.git", onerror=mock.ANY)
            update_method.assert_called_once_with()
            self.assertEqual(modules_method.call_count, 2)
            self.assertEqual(remotes_method.call_count, 2)
        self.assertEqual(len(logger.error.mock_calls), 0)
        self.assertEqual(len(logger.warning.mock_calls), 1)


if __name__ == "__main__":
    unittest.main()
