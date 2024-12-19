#!/usr/local/bin/ python3

"""
Copyright (c) 2009, 2016 Robert Bosch GmbH and its subsidiaries.
This program and the accompanying materials are made available under
the terms of the Bosch Internal Open Source License v4
which accompanies this distribution, and is available at
http://bios.intranet.bosch.com/bioslv4.txt
"""
import shutil
import unittest
import sys
import os
import logging
import tempfile
import git
from lucxbox.lib import lucxlog

try:
    from .. import gitw
except (ModuleNotFoundError, ImportError, ValueError):
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    import gitw

LOGGER = lucxlog.get_logger()
LOGGER.setLevel(logging.DEBUG)

stream_formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(stream_formatter)
LOGGER.addHandler(stream_handler)

REPORT_DIR = os.path.join(os.path.dirname(__file__), "reports")

SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
TEST_REPO_PATH = os.path.join(tempfile.gettempdir(), SCRIPT_NAME, "testEnv", "test_git_plus_repo")
TEST_REPO_URL = "ssh://git@sourcecode.socialcoding.bosch.com:7999/lucx/gitw_test_environment.git"

# versions we will test with
TAG_1 = 'Version-1'
TAG_1_SHA = '9465f3fd962'
TAG_2 = 'Version-2'
TAG_2_SHA = 'ed973e5eb78'  # two tags and one branch at this sha
TAG_3 = 'Version-3'
TAG_3_SHA = 'fce9897c252'  # no branch
INITIAL_COMMIT_TAG = 'initial_commit'
INITIAL_COMMIT_SHA = 'db64a6acfdc'

REMOTE_BRANCH_1 = 'origin/a-branch-to-test-with-DO-NOT-MODIFY'  # branch at TAG_2
REMOTE_BRANCH_1_SHA = TAG_2_SHA
REMOTE_BRANCH_2 = 'origin/another-branch-to-test-with-DO-NOT-MODIFY'  # branch but no tags
REMOTE_BRANCH_2_SHA = 'aa0c9ab04f8'
REMOTE_BRANCH_INITIAL = 'origin/initial-branch-to-test-with-DO-NOT-MODIFY'  # branch at initial commit
REMOTE_BRANCH_3 = 'origin/no_submodules'
REMOTE_BRANCH_3_SHA = 'aa0c9ab04f8'

LOCAL_BRANCH_1 = 'a-local-branch-to-test-with'  # local branch at TAG_1
LOCAL_BRANCH_1_SHA = TAG_1_SHA
LOCAL_BRANCH_2 = 'another-local-branch-to-test-with'  # branch but no tags
LOCAL_BRANCH_2_SHA = REMOTE_BRANCH_2_SHA

LOCAL_BRANCH_3 = 'a-local-branch3-test'
LOCAL_BRANCH_3_SHA = 'aa0c9ab04f8'

LOCAL_BRANCH_4 = 'a-local-branch4-test'
LOCAL_BRANCH_4_SHA = 'aa0c9ab04f8'

DEFAULT_VERSION = INITIAL_COMMIT_TAG

TEMP_FILE = os.path.join(TEST_REPO_PATH, 'temp_file.txt')
DUMP_FILE = os.path.join(TEST_REPO_PATH, 'dump.txt')


class TestGitw(unittest.TestCase):  # pylint: disable=too-many-public-methods
    @classmethod
    def setUpClass(cls):
        cls.repo = TestGitwSubmodules.prepare_and_get_repo()
        cls.repo.create_branch(LOCAL_BRANCH_1, LOCAL_BRANCH_1_SHA, force=True)
        cls.repo.create_branch(LOCAL_BRANCH_2, LOCAL_BRANCH_2_SHA, force=True)
        cls.repo.create_branch(LOCAL_BRANCH_3, LOCAL_BRANCH_3_SHA, force=True)
        cls.repo.create_branch(LOCAL_BRANCH_4, LOCAL_BRANCH_4_SHA, force=True)
        open(os.path.join(TEMP_FILE), 'w').close()
        open(os.path.join(DUMP_FILE), 'w').close()

    def setUp(self):
        self.repo.checkout(DEFAULT_VERSION, force=True, submodules=True)

    def test___log_prefix__(self):
        expected_prefix = "LUCX::gitw_test_environment"
        prefix = self.repo.__log_prefix__
        self.assertEqual(expected_prefix, prefix)

    def test_url(self):
        self.assertEqual(TEST_REPO_URL, self.repo.url)

    def test_repo_name(self):
        self.assertEqual("gitw_test_environment", self.repo.repo_name)

    def test_project(self):
        self.assertEqual("LUCX", self.repo.project)

    def test_current_commit_sha(self):
        self.assertEqual(INITIAL_COMMIT_SHA, self.repo.current_commit_sha)

    def test_get_commit_sha(self):
        self.assertEqual("db64a6acfdc88ec80bab90d6e7151f197c9888ca", self.repo.get_commit_sha(),
                         "Mismatch for 'HEAD'")
        self.assertEqual("db64a", self.repo.get_commit_sha(digit_count=5), "Mismatch for 'HEAD'")
        # Branch
        self.assertEqual(REMOTE_BRANCH_1_SHA, self.repo.get_commit_sha(REMOTE_BRANCH_1, digit_count=11),
                         f"Mismatch for '{REMOTE_BRANCH_1}'")
        # Tag
        self.assertEqual(TAG_1_SHA, self.repo.get_commit_sha(TAG_1, digit_count=11),
                         f"Mismatch for '{TAG_1}'")
        # sha no clue qhy someone would do that but giving a sha sha also works
        self.assertEqual(TAG_1_SHA, self.repo.get_commit_sha(TAG_1_SHA, digit_count=11),
                         "Mismatch for SHA test")

    def test_tags_on_commit(self):
        # no tag
        expected = []
        self.assertEqual(expected, self.repo.tags_on_commit(REMOTE_BRANCH_2_SHA), 'No-tag (sha) mismatch')
        self.assertEqual(expected, self.repo.tags_on_commit(REMOTE_BRANCH_2), 'No-tag (branch) mismatch')
        # one tag
        expected = [INITIAL_COMMIT_TAG]
        self.assertEqual(expected, self.repo.tags_on_commit(), 'One-tag (HEAD) mismatch')
        self.assertEqual(expected, self.repo.tags_on_commit(INITIAL_COMMIT_SHA), 'One-tag (sha) mismatch')
        self.assertEqual(expected, self.repo.tags_on_commit(INITIAL_COMMIT_TAG), 'One-tag (tag) mismatch')
        self.assertEqual(expected, self.repo.tags_on_commit(REMOTE_BRANCH_INITIAL),
                         'One-tag (branch) mismatch')
        # multiple tags
        expected = ['Second-Tag-For-Test', TAG_2]
        self.assertEqual(expected, self.repo.tags_on_commit(TAG_2_SHA),
                         'Multiple-tags (sha) mismatch')
        self.assertEqual(expected, self.repo.tags_on_commit(TAG_2),
                         'Multiple-tags (tag) mismatch')
        self.assertEqual(expected, self.repo.tags_on_commit(REMOTE_BRANCH_1),
                         'Multiple-tags (branch) mismatch')

    def test_local_branches_on_commit(self):
        expected = []
        self.assertEqual(expected, self.repo.local_branches_on_commit(), 'No-branch (HEAD) mismatch')
        self.assertEqual(expected, self.repo.local_branches_on_commit(TAG_2), 'No-branch (tag) mismatch')
        self.assertEqual(expected, self.repo.local_branches_on_commit(TAG_2_SHA), 'No-branch (sha) mismatch')
        self.assertEqual(expected, self.repo.local_branches_on_commit(REMOTE_BRANCH_INITIAL),
                         'No-branch (branch) mismatch')

        expected = [LOCAL_BRANCH_1]
        self.assertEqual(expected, self.repo.local_branches_on_commit(LOCAL_BRANCH_1_SHA), 'One-branch (sha) mismatch')
        self.assertEqual(expected, self.repo.local_branches_on_commit(TAG_1), 'One-branch (tag) mismatch')
        self.assertEqual([LOCAL_BRANCH_3, LOCAL_BRANCH_4, LOCAL_BRANCH_2], self.repo.local_branches_on_commit(REMOTE_BRANCH_2),
                         'One-branch (branch) mismatch')

    def test_remote_branches_on_commit(self):
        expected = []
        self.assertEqual(expected, self.repo.remote_branches_on_commit(TAG_1), 'No-branch (tag) mismatch')
        self.assertEqual(expected, self.repo.remote_branches_on_commit(TAG_1_SHA), 'No-branch (sha) mismatch')

        expected = [REMOTE_BRANCH_INITIAL]
        self.assertEqual(expected, self.repo.remote_branches_on_commit(), 'One-branch (HEAD) mismatch')
        self.assertEqual(expected, self.repo.remote_branches_on_commit(INITIAL_COMMIT_SHA), 'One-branch (sha) mismatch')
        self.assertEqual(expected, self.repo.remote_branches_on_commit(INITIAL_COMMIT_TAG), 'One-branch (tag) mismatch')
        self.assertEqual(expected, self.repo.remote_branches_on_commit(REMOTE_BRANCH_INITIAL),
                         'One-branch (branch) mismatch')

        expected = [REMOTE_BRANCH_1, 'origin/second-branch-to-test-with-DO-NOT-MODIFY']
        self.assertEqual(expected, self.repo.remote_branches_on_commit(REMOTE_BRANCH_1),
                         'Multiple-branches (branch) mismatch')
        self.assertEqual(expected, self.repo.remote_branches_on_commit(TAG_2),
                         'Multiple-branches (sha) mismatch')
        self.assertEqual(expected, self.repo.remote_branches_on_commit(TAG_2_SHA),
                         'Multiple-branches (tag) mismatch')

    def test_branches_on_commit(self):
        expected = [LOCAL_BRANCH_3, LOCAL_BRANCH_4, LOCAL_BRANCH_2, REMOTE_BRANCH_2, REMOTE_BRANCH_3]
        self.assertEqual(expected, self.repo.branches_on_commit(REMOTE_BRANCH_2),
                         'Multiple-branches (branch) mismatch')
        self.assertEqual(expected, self.repo.branches_on_commit(LOCAL_BRANCH_2_SHA),
                         'Multiple-branches (sha) mismatch')
        expected = [LOCAL_BRANCH_1]
        self.assertEqual(expected, self.repo.branches_on_commit(TAG_1),
                         'Multiple-branches (tag) mismatch')

    def test_fetch(self):
        self.assertIsNone(self.repo.fetch())

    def test_set_url(self):
        self.assertIsNone(self.repo.set_url(TEST_REPO_URL))

    def test_commit_has_tag(self):
        self.assertTrue(self.repo.commit_has_tag(INITIAL_COMMIT_SHA))
        self.assertTrue(self.repo.commit_has_tag(INITIAL_COMMIT_TAG))
        self.assertTrue(self.repo.commit_has_tag(REMOTE_BRANCH_INITIAL))

        self.assertFalse(self.repo.commit_has_tag(LOCAL_BRANCH_2))
        self.assertFalse(self.repo.commit_has_tag(REMOTE_BRANCH_2_SHA))

        self.assertTrue(self.repo.commit_has_tag(REMOTE_BRANCH_INITIAL, tag=INITIAL_COMMIT_TAG))
        self.assertFalse(self.repo.commit_has_tag(REMOTE_BRANCH_INITIAL, tag='NOT-A-TAG'))
        self.assertFalse(self.repo.commit_has_tag(REMOTE_BRANCH_2_SHA, tag=INITIAL_COMMIT_TAG))

    def test_commit_has_branch(self):
        self.assertTrue(self.repo.commit_has_branch(INITIAL_COMMIT_SHA))
        self.assertTrue(self.repo.commit_has_branch(INITIAL_COMMIT_TAG))

        self.assertTrue(self.repo.commit_has_branch(TAG_3))
        self.assertFalse(self.repo.commit_has_branch(TAG_3_SHA))

        self.assertTrue(self.repo.commit_has_branch(INITIAL_COMMIT_TAG, branch=REMOTE_BRANCH_INITIAL))
        self.assertFalse(self.repo.commit_has_branch(INITIAL_COMMIT_SHA, branch='NOT-A-BANCH'))
        self.assertFalse(self.repo.commit_has_branch(REMOTE_BRANCH_2_SHA, branch=INITIAL_COMMIT_TAG))

    def test_tidy(self):
        self.repo.tidy()
        self.assertFalse(os.path.isfile(TEMP_FILE))

    def test_clean(self):
        self.assertIsNone(self.repo.clean())

    def test_checkout(self):
        old_commit = INITIAL_COMMIT_SHA
        self.repo.checkout(TAG_1, force=True, submodules=True)
        self.assertNotEqual(self.repo.current_commit_sha, old_commit)

    def test_checkout_branch(self):
        self.repo.checkout_branch(TAG_3, 'develop', force=True)
        self.assertEqual("76e859f544d", self.repo.current_commit_sha)

    def test_reset(self):
        self.repo.reset(hard=True)
        self.assertFalse(os.path.isfile(DUMP_FILE))

    def test_branch_exists(self):
        self.assertTrue(self.repo.branch_exists(LOCAL_BRANCH_1))
        self.assertTrue(self.repo.branch_exists(REMOTE_BRANCH_INITIAL))
        self.assertFalse(self.repo.branch_exists('NOT-A-BANCH'))
        self.assertFalse(self.repo.branch_exists(LOCAL_BRANCH_1_SHA))

    def test_local_branch_exists(self):
        self.assertTrue(self.repo.local_branch_exists(LOCAL_BRANCH_1))
        self.assertFalse(self.repo.local_branch_exists(REMOTE_BRANCH_INITIAL))
        self.assertFalse(self.repo.local_branch_exists('NOT-A-BANCH'))

    def test_remote_branch_exists(self):
        self.assertFalse(self.repo.remote_branch_exists(LOCAL_BRANCH_1))
        self.assertTrue(self.repo.remote_branch_exists(REMOTE_BRANCH_INITIAL))
        self.assertFalse(self.repo.remote_branch_exists('NOT-A-BANCH'))

    def test_tag_exists(self):
        self.assertTrue(self.repo.tag_exists(TAG_1))

    def test_tag_not_exists(self):
        self.assertFalse(self.repo.tag_exists("NEW_TAG_1"))

    def test_remote_tag_exists(self):
        self.assertTrue(self.repo.remote_tag_exists(TAG_2))

    def test_remote_tag_not_exists(self):
        self.assertFalse(self.repo.remote_tag_exists("NEW_TAG_2"))

    def test_remove_all_content(self):
        self.repo.remove_all_content()
        expected = ['.git']
        self.assertEqual(expected, os.listdir(TEST_REPO_PATH))

    def test_create_commit(self):
        self.assertNotEqual(self.repo.current_commit_sha, self.repo.create_commit("New commit for test"))

    def test_push(self):
        self.repo.push(ref=LOCAL_BRANCH_3)
        self.assertTrue(self.repo.remote_branch_exists(LOCAL_BRANCH_3))
        self.repo.remove_branch(LOCAL_BRANCH_3, force=True)
        # delete branch LOCAL_BRANCH_3
        remote = self.repo.remote()
        remote.push(refspec=(':' + LOCAL_BRANCH_3))

    def test_set_branch_to_ref(self):
        self.repo.set_branch_to_ref(LOCAL_BRANCH_2)
        self.assertEqual(LOCAL_BRANCH_2_SHA, self.repo.get_commit_sha(REMOTE_BRANCH_2_SHA, digit_count=11))

    def test_remove_branch(self):
        self.assertTrue(self.repo.branch_exists(LOCAL_BRANCH_4))
        self.repo.remove_branch(LOCAL_BRANCH_4, force=True)
        self.assertFalse(self.repo.branch_exists(LOCAL_BRANCH_4))
        # re-create branch
        self.repo.create_branch(LOCAL_BRANCH_4)

    def test_create_branch(self):
        new_branch = "NEW_BRANCH"
        self.repo.create_branch(new_branch, force=True)
        self.assertTrue(self.repo.branch_exists(new_branch))
        self.repo.remove_branch(new_branch, force=True)

    def test_ref_exists(self):
        self.assertTrue(self.repo.ref_exists(LOCAL_BRANCH_1))
        self.assertTrue(self.repo.ref_exists(REMOTE_BRANCH_1))
        self.assertTrue(self.repo.ref_exists(TAG_1))

        self.assertFalse(self.repo.ref_exists("origin/NO_BRANCH"))
        self.assertFalse(self.repo.ref_exists("NO_TAG"))


class TestGitwSubmodules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = cls.prepare_and_get_repo()
        cls.repo.checkout(TAG_1, force=True, submodules=True)

    def setUp(self):
        self.checkout_done = False

    def tearDown(self) -> None:
        if self.checkout_done:
            self.repo.checkout(TAG_1, force=True, submodules=True)

    def test_submodule_list(self):
        expected = ['example/example_submodule', 'example/example_submodule2', 'root_submodule']
        self.assertEqual(expected, self.repo.submodule_list)
        self.repo.checkout(TAG_3, force=True, submodules=True)
        self.checkout_done = True
        expected = 9
        self.assertEqual(expected, len(self.repo.submodule_list))

    def test_get_submodule_commit(self):
        # checkout revision with submodules
        submodule = 'root_submodule'
        expected = self.repo.get_commit("db64a6acfdc")
        self.assertEqual(expected, self.repo.get_submodule_commit(submodule),
                         "Current sha mismatch")

        # testing with branch, tag and sha
        refs = [REMOTE_BRANCH_INITIAL, TAG_3, TAG_1_SHA]
        for ref in refs:
            # as we use the main repo as submodule the main repo commit for the reference has to match in the submodule
            expected = self.repo.get_commit(ref)
            self.assertEqual(expected, self.repo.get_submodule_commit(submodule, ref),
                             f"ref '{ref}' given -> submodule sha mismatch")

    def test_get_submodule_workspace_sha(self):  # pylint: disable=invalid-name
        # checkout revision with submodules
        submodule = 'root_submodule'
        expected = self.repo.get_commit_sha("db64a6acfdc")
        self.assertEqual(expected, self.repo.get_submodule_workspace_sha(submodule),
                         "Original submodule sha mismatch")
        # change local submodule sha
        self.repo.set_submodule_revision(submodule, "77e61bd34f2")
        expected = self.repo.get_commit_sha("77e61bd34f2")
        self.assertEqual(expected, self.repo.get_submodule_workspace_sha(submodule),
                         "Modified submodule sha mismatch")

    def test_get_submodule_sha(self):
        # checkout revision with submodules
        submodule = 'example/example_submodule'
        expected = self.repo.get_commit_sha("a7ed5abf4a5")
        self.assertEqual(expected, self.repo.get_submodule_sha(submodule),
                         "Original submodule sha mismatch")
        self.repo.set_submodule_revision(submodule, "77e61bd34f2")
        self.assertEqual(expected, self.repo.get_submodule_sha(submodule),
                         "Modified submodule sha mismatch")

    def test_get_submodule_url(self):
        submodule = 'example/example_submodule'
        expected = TEST_REPO_URL
        self.assertEqual(expected, self.repo.get_submodule_url(submodule))
        # pylint: disable=fixme
        # ToDo check with submodule that is not the same repo

    def test_get_submodule_tags(self):
        self.assertEqual(['use-as-submodule-1'], self.repo.get_submodule_tags('example/example_submodule'))
        self.assertEqual(['initial_commit'], self.repo.get_submodule_tags('root_submodule'))

    def test_get_submodule(self):
        submodule = 'example/example_submodule'
        expected = submodule
        self.assertEqual(expected, self.repo.get_submodule(submodule).name)

    def test_update_submodule(self):
        pass

    def test_update_submodules(self):
        pass

    def test_add_submodule(self):
        submodule = 'example/example_submodule2'
        self.assertIsNone(self.repo.add_submodule(submodule, TEST_REPO_URL))
        self.assertEqual(self.repo.get_submodule(submodule).name, submodule)

    def test_set_submodule_revision(self):
        submodule = 'example/example_submodule'
        expected = self.repo.get_commit_sha("a7ed5abf4a5")
        self.assertEqual(expected, self.repo.get_submodule_sha(submodule))
        self.repo.set_submodule_revision(submodule, "77e61bd34f2")
        self.assertEqual(expected, self.repo.get_submodule_sha(submodule))

    def test_create_tag_in_submodule(self):
        submodule = 'root_submodule'
        tag = 'TAG_SUBMODULE'
        self.repo.create_tag_in_submodule(submodule, tag=tag, ref="3591442e59b", force=True)
        self.assertTrue(self.repo.get_submodule(submodule).repo.tag_exists(tag))

    @classmethod
    def prepare_and_get_repo(cls, is_retry: bool = False):
        try:
            if os.path.isdir(TEST_REPO_PATH):
                os.system('rmdir /S /Q "{}"'.format(TEST_REPO_PATH))
            repo = gitw.Repo(TEST_REPO_PATH, TEST_REPO_URL)
            repo.fetch(tags=True, prune_tags=True, prune=True, force=True)
            return repo
        except git.GitCommandError as gce:
            if is_retry:
                raise gce
            LOGGER.debug("Removing test environment in '%s' and retrying setup of test repository", TEST_REPO_PATH)
            shutil.rmtree(TEST_REPO_PATH)
            cls.prepare_and_get_repo(is_retry=True)  # pylint: disable=undefined-variable


if __name__ == '__main__':
    LOGGER.info("Running tests...")
    unittest.main()
