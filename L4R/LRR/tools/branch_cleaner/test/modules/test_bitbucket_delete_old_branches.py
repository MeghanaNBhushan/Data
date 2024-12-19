import datetime
import unittest
import bitbucket_delete_old_branches
import modules.functions

from unittest import mock
from modules.bitbucket import BitBucket
from bitbucket_delete_old_branches import BranchDeleter


class TestBranchDeleter(unittest.TestCase):

    def setUp(self):
        self.url = 'https://bb.bosch.com'
        self.project = 'PJPH'
        self.repo = 'test_repo'
        user = 'testuser'
        password = 'test[assword'

        self.older_than_days = 1
        self.days_after_merge = 1
        self.force = False
        self.dry_run = True
        self.total_branches_before = 0
        self.whitelisted_branches = []
        self.old_branches = []
        self.repository = 'pj-ph_jlr_my20_bsw'
        self.branch_deleter = BranchDeleter(self.url,
                                            self.project,
                                            self.repository,
                                            user, password,
                                            self.older_than_days,
                                            self.days_after_merge,
                                            self.force,
                                            self.dry_run)

    def test_branch_is_not_ahead(self):
        mock_branch = {
            "metadata": {
                'com.atlassian.bitbucket.server.bitbucket-branch:ahead-behind-'
                'metadata-provider': {
                    "ahead": 12,
                    "behind": 34
                }
            }
        }

        self.assertFalse(self.branch_deleter.branch_is_not_ahead(mock_branch))

    def test_get_branch_head_age_days(self):
        mock_branch = {
            "metadata": {
                "com.atlassian.bitbucket.server.bitbucket-branch:latest-"
                "commit-metadata":
                    {
                        "authorTimestamp": 1429562672000,
                    }
            },
            "displayId": "dc82ee974d8"
        }

        self.assertIsNotNone(self.branch_deleter.
                             get_branch_head_age_days(mock_branch))

    def test_delete_old_branches_dry_run_true(self):
        self.branch_deleter.old_branches = [
            {"displayId": 'branch-1',
             "id": 1},
            {"displayId": 'branch-2',
             "id": 2}
        ]

        with mock.patch.object(BitBucket, 'delete_branch') as mock_delete:
            mock_delete.return_value = True
            with mock.patch.object(bitbucket_delete_old_branches.logger,
                                   'info') as mock_logger:
                self.branch_deleter.delete_old_branches()
                self.assertEqual(mock_logger.call_count, 2)

    def test_delete_old_branches_dry_run_false(self):
        self.branch_deleter.old_branches = [
            {"displayId": 'branch-1',
             "id": 1},
            {"displayId": 'branch-2',
             "id": 2}
        ]

        with mock.patch.object(BitBucket, 'delete_branch') as mock_delete:
            mock_delete.return_value = True
            with mock.patch.object(bitbucket_delete_old_branches.logger,
                                   'info'):
                self.branch_deleter.dry_run = False
                self.branch_deleter.delete_old_branches()
                self.assertEqual(mock_delete.call_count, 4)

    def test_delete_old_branches_status_code_400(self):
        self.branch_deleter.old_branches = [
            {"displayId": 'branch-1',
             "id": 1},
            {"displayId": 'branch-2',
             "id": 2}
        ]

        with mock.patch.object(BitBucket, 'delete_branch') as mock_delete:
            mock_delete.return_value = 400
            with mock.patch.object(bitbucket_delete_old_branches.logger,
                                   'info'):
                self.branch_deleter.dry_run = False
                self.branch_deleter.delete_old_branches()
                self.assertEqual(mock_delete.call_count, 2)

    def test_branch_pr_activity_not_older_than_days_true(self):
        mock_branch = {
            "metadata": {
                'com.atlassian.bitbucket.server.bitbucket'
                '-ref-metadata:outgoing-pull-request-metadata': {
                    "pullRequest": {
                        "id": 1,
                        "state": "OPENED",
                        "fromRef": {
                            "id": "refs/heads/new-branch",
                            "displayId": "new-branch",
                        }
                    }
                }
            },
            "displayId": "new-branch"
        }
        days = 1000

        result = self.branch_deleter. \
            branch_pr_activity_not_older_than_days(mock_branch, days)
        self.assertTrue(result)

    def test_branch_pr_activity_not_older_than_days_false(self):
        mock_branch = {
            "id": 1,
            "metadata": {
                'com.atlassian.bitbucket.server.bitbucket'
                '-ref-metadata:outgoing-pull-request-metadata': {
                    "id": 1,
                    "state": "all",
                    "fromRef": {
                        "id": "refs/heads/new-branch",
                        "displayId": "new-branch",
                    }
                }
            },
            "displayId": "new-branch"
        }
        days = 1000

        with mock.patch.object(BitBucket,
                               'get_all_pull_requests') as mock_get_pr, \
            mock.patch.object(BranchDeleter,
                              'pr_last_activity_not_older_than_days') \
                as mock_pr_act:
            mock_get_pr.return_value = ['a', 'b']
            mock_pr_act.return_value = False
            result = self.branch_deleter. \
                branch_pr_activity_not_older_than_days(mock_branch, days)
            self.assertFalse(result)

    def test_branch_pr_activity_not_older_than_days_else_true(self):
        mock_branch = {
            "id": 1,
            "metadata": {
                'com.atlassian.bitbucket.server.bitbucket'
                '-ref-metadata:outgoing-pull-request-metadata': {
                    "id": 1,
                    "state": "all",
                    "fromRef": {
                        "id": "refs/heads/new-branch",
                        "displayId": "new-branch",
                    }
                }
            },
            "displayId": "new-branch"
        }
        days = 1000

        with mock.patch.object(BitBucket,
                               'get_all_pull_requests') as mock_get_pr, \
            mock.patch.object(BranchDeleter,
                              'pr_last_activity_not_older_than_days') \
                as mock_pr_act:
            mock_get_pr.return_value = ['a', 'b']
            mock_pr_act.return_value = True
            result = self.branch_deleter. \
                branch_pr_activity_not_older_than_days(mock_branch, days)
            self.assertTrue(result)

    def test_pr_last_activity_not_older_than_days_true(self):
        mock_pr = {
            "id": 1,
            "state": "OPENED",
            "createdDate": 1524528879329,
            "updatedDate": 1524528930110,
            "fromRef": {
                "id": "refs/heads/new-branch",
                "displayId": "new-branch",
            }
        }
        days = 5

        target_time = datetime.datetime(2020, 8, 6)
        with mock.patch.object(datetime, 'datetime') as mock_time:
            mock_time.return_value = target_time
        result = self.branch_deleter. \
            pr_last_activity_not_older_than_days(mock_pr, days)
        self.assertTrue(result)

    def test_pr_last_activity_not_older_than_days_default_false(self):
        mock_pr = {
            "id": 1,
            "state": "MERGED",
            "createdDate": 1524528879329,
            "updatedDate": 1524528930110,
            "fromRef": {
                "id": "refs/heads/new-branch",
                "displayId": "new-branch",
            }
        }
        days = 1000

        target_time = datetime.datetime(2020, 8, 6)
        with mock.patch.object(datetime, 'datetime') as mock_time:
            mock_time.return_value = target_time
            result = self.branch_deleter. \
                pr_last_activity_not_older_than_days(mock_pr, days)
            self.assertFalse(result)

    def test_pr_last_activity_not_older_than_days_check_declined_true(self):
        mock_pr = {
            "id": 1,
            "state": "DECLINED",
            "createdDate": 1524528879329,
            "updatedDate": 1524528930110,
            "fromRef": {
                "id": "refs/heads/new-branch",
                "displayId": "new-branch",
            }
        }
        days = 1000

        target_time = datetime.datetime(2020, 8, 6)
        with mock.patch.object(datetime, 'datetime') as mock_time:
            mock_time.return_value = target_time
            result_true = self.branch_deleter. \
                pr_last_activity_not_older_than_days(mock_pr, days)
            self.assertTrue(result_true)

    def test_pr_last_activity_not_older_than_days_check_declined_false(self):
        mock_pr = {
            "id": 1,
            "state": "DECLINED",
            "createdDate": 1524528879329,
            "updatedDate": 1524528930110,
            "fromRef": {
                "id": "refs/heads/new-branch",
                "displayId": "new-branch",
            }
        }
        days = 1

        target_time = datetime.datetime(2020, 8, 6)
        with mock.patch.object(datetime, 'datetime') as mock_time:
            mock_time.return_value = target_time
            result_false = self.branch_deleter. \
                pr_last_activity_not_older_than_days(mock_pr, days)
            self.assertFalse(result_false)

    def test_run_no_branches_found(self):
        mock_br = [{
            "id": 1,
            "metadata": {
                'com.atlassian.bitbucket.server.bitbucket'
                '-branch:latest-commit-metadata': {
                    "id": 1,
                    "state": "all",
                    "fromRef": {
                        "id": "refs/heads/new-branch",
                        "displayId": "new-branch",
                    },
                    "authorTimestamp": 1429562672000,
                }
            },
            "displayId": "develop"
        }]

        with mock.patch.object(BitBucket,
                               '_BitBucket__get_all_x') as get_all_x, \
            mock.patch.object(bitbucket_delete_old_branches.logger,
                              'info') as mock_logger:
            get_all_x.return_value = mock_br
            self.branch_deleter.run()
            self.assertEqual(mock_logger.call_count, 4)

    def test_run_no_branches_commit_age_days_greater(self):
        mock_br = [{
            "id": 1,
            "metadata": {
                'com.atlassian.bitbucket.server.bitbucket'
                '-branch:latest-commit-metadata': {
                    "id": 1,
                    "state": "all",
                    "fromRef": {
                        "id": "refs/heads/new-branch",
                        "displayId": "new-branch",
                    },
                    "authorTimestamp": 1596622204,
                },
                'com.atlassian.bitbucket.server.bitbucket-'
                'branch:ahead-behind-metadata-provider': {
                    "ahead": 12,
                    "behind": 34
                }
            },
            "displayId": "feature"
        }]

        target_time = datetime.datetime(2020, 8, 6)
        with mock.patch.object(datetime,
                               'datetime') as mock_time, \
            mock.patch.object(BitBucket,
                              '_BitBucket__get_all_x') as get_all_x,\
            mock.patch.object(modules.functions,
                              'input', return_value='N'), \
            mock.patch.object(bitbucket_delete_old_branches.logger,
                              'info') as mock_logger:
            mock_time.return_value = target_time
            get_all_x.return_value = mock_br

            self.branch_deleter.run()
            self.assertEqual(mock_logger.call_count, 4)

    def test_run_force_is_false(self):
        self.branch_deleter.old_branches = [
            {"displayId": 'develop',
             "id": 1},
            {"displayId": 'branch-2',
             "id": 2}
        ]

        with mock.patch.object(BitBucket,
                               'get_all_branches') as mock_get, \
            mock.patch.object(bitbucket_delete_old_branches.logger,
                              'info') as mock_logger, \
            mock.patch.object(modules.functions,
                              'input', return_value='N'):
            self.branch_deleter.run()
            self.assertEqual(mock_get.call_count, 2)
            self.assertEqual(mock_logger.call_count, 4)

    def test_run_force_is_true(self):
        self.branch_deleter.old_branches = [
            {"displayId": 'develop',
             "id": 1},
            {"displayId": 'branch-2',
             "id": 2}
        ]
        self.branch_deleter.force = True

        with mock.patch.object(BitBucket,
                               'get_all_branches') as mock_get, \
            mock.patch.object(bitbucket_delete_old_branches.logger,
                              'info') as mock_logger, \
            mock.patch.object(BranchDeleter,
                              'delete_old_branches', return_value=False):
            self.branch_deleter.run()
            self.assertEqual(mock_get.call_count, 2)
            self.assertEqual(mock_logger.call_count, 5)

    def test_run_locked_branches(self):
        mock_br = [{
            "id": 1,
            "metadata": {
                'com.atlassian.bitbucket.server.bitbucket-branch:ahead-behind-'
                'metadata-provider': {
                    "ahead": 12,
                    "behind": 34
                },
                'com.atlassian.bitbucket.server.bitbucket'
                '-branch:latest-commit-metadata': {
                    "authorTimestamp": 1429562672000,
                }
            },
            "displayId": "this-branch-is-locked"
        }]

        with mock.patch.object(BitBucket,
                               '_BitBucket__get_all_x') as get_all_x, \
            mock.patch.object(BitBucket,
                              'delete_branch') as mock_get, \
            mock.patch.object(bitbucket_delete_old_branches.logger,
                              'info'), \
            mock.patch.object(modules.functions,
                              'input') as mock_input:
            get_all_x.return_value = mock_br
            mock_get.return_value = 400
            mock_input.return_value = 'y'

            self.branch_deleter.dry_run = False
            self.branch_deleter.run()
            self.assertEqual(len(self.branch_deleter.locked_branches), 1)

    def test_run_deleted_branches(self):
        mock_br = [{
            "id": 1,
            "metadata": {
                'com.atlassian.bitbucket.server.bitbucket-branch:ahead-behind-'
                'metadata-provider': {
                    "ahead": 12,
                    "behind": 34
                },
                'com.atlassian.bitbucket.server.bitbucket'
                '-branch:latest-commit-metadata': {
                    "authorTimestamp": 1429562672000,
                }
            },
            "displayId": "this-branch-is-locked"
        }]

        with mock.patch.object(BitBucket,
                               '_BitBucket__get_all_x') as get_all_x, \
            mock.patch.object(BitBucket,
                              'delete_branch') as mock_get, \
            mock.patch.object(bitbucket_delete_old_branches.logger,
                              'info'), \
            mock.patch.object(modules.functions,
                              'input') as mock_input:
            get_all_x.return_value = mock_br
            mock_get.return_value = False
            mock_input.return_value = 'y'

            self.branch_deleter.dry_run = False
            self.branch_deleter.run()
            self.assertEqual(self.branch_deleter.deleted_branches, 1)


if __name__ == '__main__':
    unittest.main()
