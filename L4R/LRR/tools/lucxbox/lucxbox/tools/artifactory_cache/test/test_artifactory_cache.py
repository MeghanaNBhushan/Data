""" Test for a python project """
import unittest
from unittest.mock import patch
from lucxbox.tools.artifactory_cache import artifactory_cache


class TestArtifactoryCache(unittest.TestCase):

    @patch.object(artifactory_cache.ArtifactCache, 'get_artifact')
    def test_works_with_required_args(self, get_mock):
        args = ['-u', 'testuser', '-p', 'securepassword', '-a', 'some/artifact/path']
        artifactory_cache.main(args)
        self.assertTrue(get_mock.called)

    @patch.object(artifactory_cache.ArtifactCache, 'clear')
    def test_clear_only_works(self, clear_mock):
        args = ['--clear']
        artifactory_cache.main(args)
        self.assertTrue(clear_mock.called)

    def test_no_args_fails(self):
        args = []
        with self.assertRaises(SystemExit) as sys_exit:
            artifactory_cache.main(args)
        self.assertEqual(sys_exit.exception.code, 2)

    def test_missing_user_fails(self):
        args = ["-a", "some/artifact/path"]
        with self.assertRaises(SystemExit) as sys_exit:
            artifactory_cache.main(args)
        self.assertEqual(sys_exit.exception.code, 2)

    def test_no_artifact_path_fails(self):
        args = ['-u', "testuser"]
        with self.assertRaises(SystemExit) as sys_exit:
            artifactory_cache.main(args)
        self.assertEqual(sys_exit.exception.code, 2)

    @patch.object(artifactory_cache.ArtifactCache, 'get_artifact')
    @patch.object(artifactory_cache.ArtifactCache, 'clear')
    def test_clear_and_artifact(self, clear_mock, get_mock):
        args = ['-u', 'testuser', '-p', 'securepassword', '-a', 'some/artifact/path', '--clear']
        artifactory_cache.main(args)
        self.assertTrue(clear_mock.called)
        self.assertTrue(get_mock.called)


if __name__ == "__main__":
    unittest.main()
