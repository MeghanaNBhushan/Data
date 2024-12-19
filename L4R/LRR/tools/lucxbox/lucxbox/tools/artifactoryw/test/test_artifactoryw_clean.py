""" Testing the artifactory_clean """

import argparse
import unittest
from unittest.mock import patch, Mock, call
from requests.exceptions import HTTPError

from lucxbox.tools.artifactoryw.artifactoryw_clean import clean, fetch_items_from_artifactory, _login, delete_item


class TestArtifactory(unittest.TestCase):
    def setUp(self):
        self.mock_logger = patch('lucxbox.tools.artifactoryw.artifactoryw_clean.LOGGER')
        self.mock_logger.start()
        self.addCleanup(self.mock_logger.stop)
        self.rt_url = 'http://localhost/artifactory'
        self.args = argparse.Namespace(
            artifactory_url=self.rt_url, artifactory_repository='rt_test_repository', username='user', password='pass')
        self.response_dict = {'results': [
            {'repo': 'rt_test_repository', 'path': 'zip-artifacts', 'name': 'file.zip'},
            {'repo': 'rt_test_repository', 'path': 'jar-artifacts', 'name': 'file.jar'},
            {'repo': 'rt_test_repository', 'path': 'pdf-artifacts', 'name': 'file.pdf'},
            {'repo': 'rt_test_repository', 'path': 'artifacts', 'name': 'file'}]}

    @patch('lucxbox.tools.artifactoryw.artifactoryw_clean.requests.Session')
    def test_fetch_items(self, mock_session):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = lambda: self.response_dict
        mock_session().post.return_value.__enter__ = lambda _: mock_response
        mock_session().post.return_value.__exit__ = lambda *args, **kwargs: None

        actual_items = fetch_items_from_artifactory(self.rt_url, 'test_repo', 'c', '2w', mock_session(), None)
        expected_items = self.response_dict['results']

        self.assertEqual(actual_items, expected_items)

    @patch('lucxbox.tools.artifactoryw.artifactoryw_clean.requests.Session')
    def test_fetch_items_not_found(self, mock_session):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError()
        mock_session().post.return_value.__enter__ = lambda _: mock_response
        mock_session().post.return_value.__exit__ = lambda *args, **kwargs: None

        self.assertRaises(
            HTTPError, fetch_items_from_artifactory, self.rt_url, 'test_repo', 'c', '2w', mock_session(), None)

    def test_login(self):
        actual_auth = _login('user', 'password')
        expected_auth = ('user', 'password')

        self.assertEqual(actual_auth.auth, expected_auth)

    @patch('lucxbox.tools.artifactoryw.artifactoryw_clean.requests.Session')
    def test_delete_item_with_dry_run(self, mock_session):
        self.args.retention_period = '2w'
        self.args.domain_field = 'c'
        self.args.include_path_pattern = 'path/to/item*'
        self.args.exclude_list = 'rt_test_repository/jar-artifacts/file.jar, rt_test_repository/pdf-artifacts/file.pdf'
        self.args.dry_run = True

        mock_response = Mock()
        mock_response.status_code = 200
        mock_session().delete.return_value.__enter__ = lambda _: mock_response
        mock_session().delete.return_value.__exit__ = lambda *args, **kwargs: None

        mock_response.json = lambda: self.response_dict
        mock_session().post.return_value.__enter__ = lambda _: mock_response
        mock_session().post.return_value.__exit__ = lambda *args, **kwargs: None

        clean(self.args)

        actual_post = mock_session().post.call_count
        expected_post = 1
        actual_delete = mock_session().delete.call_count
        expected_delete = 0

        self.assertTrue(mock_session().post.called)
        self.assertEqual(actual_post, expected_post)

        self.assertFalse(mock_session().delete.called)
        self.assertEqual(actual_delete, expected_delete)

    @patch('lucxbox.tools.artifactoryw.artifactoryw_clean.requests.Session')
    def test_delete_item_no_dry_run(self, mock_session):
        self.args.retention_period = '2d'
        self.args.domain_field = 'dl'
        self.args.include_path_pattern = None
        self.args.exclude_list = None
        self.args.dry_run = False

        mock_response = Mock()
        mock_response.status_code = 200
        mock_session().delete.return_value.__enter__ = lambda _: mock_response
        mock_session().delete.return_value.__exit__ = lambda *args, **kwargs: None

        mock_response.json = lambda: self.response_dict
        mock_session().post.return_value.__enter__ = lambda _: mock_response
        mock_session().post.return_value.__exit__ = lambda *args, **kwargs: None

        clean(self.args)

        actual_post = mock_session().post.call_count
        expected_post = 1
        actual_delete = mock_session().delete.call_count
        expected_delete = 4

        calls = [call('http://localhost/artifactory/rt_test_repository/zip-artifacts/file.zip', stream=True),
                 call('http://localhost/artifactory/rt_test_repository/jar-artifacts/file.jar', stream=True),
                 call('http://localhost/artifactory/rt_test_repository/pdf-artifacts/file.pdf', stream=True),
                 call('http://localhost/artifactory/rt_test_repository/artifacts/file', stream=True)]

        self.assertTrue(mock_session().post.called)
        self.assertEqual(actual_post, expected_post)

        self.assertTrue(mock_session().delete.called)
        self.assertEqual(actual_delete, expected_delete)

        mock_session().delete.assert_has_calls(calls)

    @patch('lucxbox.tools.artifactoryw.artifactoryw_clean.requests.Session')
    def test_delete_item_with_excludes(self, mock_session):
        self.args.retention_period = '2d'
        self.args.domain_field = 'dl'
        self.args.include_path_pattern = None
        self.args.exclude_list = 'rt_test_repository/jar-artifacts/file.jar, rt_test_repository/pdf-artifacts/file.pdf'
        self.args.dry_run = False

        mock_response = Mock()
        mock_response.status_code = 200
        mock_session().delete.return_value.__enter__ = lambda _: mock_response
        mock_session().delete.return_value.__exit__ = lambda *args, **kwargs: None

        mock_response.json = lambda: self.response_dict
        mock_session().post.return_value.__enter__ = lambda _: mock_response
        mock_session().post.return_value.__exit__ = lambda *args, **kwargs: None

        clean(self.args)

        actual_post = mock_session().post.call_count
        expected_post = 1
        actual_delete = mock_session().delete.call_count
        expected_delete = 2

        calls = [call('http://localhost/artifactory/rt_test_repository/zip-artifacts/file.zip', stream=True),
                 call('http://localhost/artifactory/rt_test_repository/artifacts/file', stream=True)]

        self.assertTrue(mock_session().post.called)
        self.assertEqual(actual_post, expected_post)

        self.assertTrue(mock_session().delete.called)
        self.assertEqual(actual_delete, expected_delete)

        mock_session().delete.assert_has_calls(calls)

    @patch('lucxbox.tools.artifactoryw.artifactoryw_clean.requests.Session')
    def test_delete_item_not_found(self, mock_session):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError()
        mock_session().delete.return_value.__enter__ = lambda _: mock_response
        mock_session().delete.return_value.__exit__ = lambda *args, **kwargs: None

        self.assertRaises(
            HTTPError, delete_item, self.rt_url, 'rt_test_repository', 'zip-artifacts', 'file.zip', mock_session())


if __name__ == "__main__":
    unittest.main()
