import unittest
import time

from unittest import mock
from requests import Session
from modules.bitbucket import BitBucket
from modules import bitbucket


class TestBitbucket(unittest.TestCase):

    def setUp(self):
        self.url = 'https://bb.bosch.com'
        self.project = 'PJPH'
        self.repo = 'test_repo'
        user = 'testuser'
        password = 'test[assword'
        self.bitbucket = BitBucket(
            self.url, self.project, self.repo, user, password)

    def test_get_all_branches(self):
        with mock.patch.object(self.bitbucket, '_BitBucket__get_all_x',
                               return_value=['a', 'b', 'c']) as get_all_x:
            for branch in self.bitbucket.get_all_branches():
                pass
            get_all_x.assert_called_with(
                "branches", {"details": False, "order": "MODIFICATION"})

    def test_get_all_pull_requests(self):
        with mock.patch.object(self.bitbucket,
                               '_BitBucket__get_all_x') as get_all_x:
            for pull_request in self.bitbucket.get_all_pull_requests():
                pass
            get_all_x.assert_called_with(
                "pull-requests", {"state": "all"})

    def test_delete_branch_status_code_204(self):
        with mock.patch.object(Session, 'delete') as mock_delete:
            mock_delete.return_value.status_code = 204

            self.assertEqual(self.bitbucket.delete_branch('mock_branch'), 204)

    def test_delete_branch_status_code_429(self):
        with mock.patch.object(Session, 'delete') as mock_delete:
            mock_delete.return_value.status_code = 429
            with mock.patch.object(time, 'sleep', return_value=None):
                with mock.patch.object(bitbucket.logger, 'info'):

                    self.bitbucket.delete_branch('mock_branch')
                    self.assertEqual(mock_delete.call_count, 5)

    def test_delete_branch_status_code_400(self):
        with mock.patch.object(Session, 'delete') as mock_delete:
            mock_delete.return_value.status_code = 400

            self.assertEqual(self.bitbucket.delete_branch('mock_branch'), 400)

    def test_delete_branch_could_not_deleted(self):
        with mock.patch.object(Session, 'delete') as mock_delete:
            mock_delete.return_value.status_code = 404
            codes_in_use = [204, 429, 400]

            self.assertNotIn(self.bitbucket.delete_branch(
                'this-branch-does-not-exist-anywhere'), codes_in_use)

    def test_get_all_branches_status_code_200(self):
        with mock.patch.object(Session, 'get') as mock_get:
            mock_get.return_value.status_code = 200

            self.assertTrue(type(list(
                self.bitbucket.get_all_branches())) is list)

    def test_get_all_branches_status_code_429(self):
        with mock.patch.object(Session, 'get') as mock_get:
            with mock.patch.object(time, 'sleep', return_value=None):
                with mock.patch.object(bitbucket.logger, 'info'):
                    mock_get.return_value.status_code = 429
                    self.assertTrue(type(list(
                        self.bitbucket.get_all_branches())) is list)
                    self.assertEqual(mock_get.call_count, 5)

    def test_get_all_branches_status_code_401(self):
        with mock.patch.object(Session, 'get') as mock_get:
            mock_get.return_value.status_code = 401

            with self.assertRaises(ConnectionError):
                self.assertTrue(type(list(
                     self.bitbucket.get_all_branches())) is list)

    def test_get_all_branches_status_code_404(self):
        with mock.patch.object(Session, 'get') as mock_get:
            mock_get.return_value.status_code = 404

            with self.assertRaises(ConnectionError):
                self.assertTrue(type(list(
                    self.bitbucket.get_all_branches())) is list)


if __name__ == '__main__':
    unittest.main()
