""" Test for a python project """
import os
import unittest
from unittest.mock import call, patch

from lucxbox.tools.artifactory_cache import ArtifactoryCache

SCRIPT_DIR = os.path.dirname(__file__)
CACHE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "resources", "test_cache"))


class TestArtifactoryCacheClass(unittest.TestCase):
    def setUp(self) -> None:
        self.cache = ArtifactoryCache.ArtifactCache("testuser", "testpassword", cache_dir=CACHE_DIR)

    def test_clear_existing_file(self):
        with patch.object(ArtifactoryCache.os, 'remove') as remove_mock, \
                patch.object(ArtifactoryCache.shutil, 'rmtree') as rmtree_mock:
            self.cache.clear("a/a1/file-a1.txt")
        self.assertTrue(remove_mock.called)
        self.assertFalse(rmtree_mock.called)

    def test_clear_existing_dir(self):
        with patch.object(ArtifactoryCache.os, 'remove') as remove_mock, \
                patch.object(ArtifactoryCache.shutil, 'rmtree') as rmtree_mock:
            self.cache.clear("a/a1/")
        self.assertFalse(remove_mock.called)
        self.assertTrue(rmtree_mock.called)

    def test_clear_all(self):
        with patch.object(ArtifactoryCache.os, 'remove') as remove_mock, \
                patch.object(ArtifactoryCache.shutil, 'rmtree') as rmtree_mock:
            self.cache.clear()
        self.assertFalse(remove_mock.called)
        rmtree_mock.assert_called_with(CACHE_DIR)

    def test_no_clear_missing_file(self):
        with patch.object(ArtifactoryCache.os, 'remove') as remove_mock, \
                patch.object(ArtifactoryCache.shutil, 'rmtree') as rmtree_mock:
            self.cache.clear("a/missing.txt")
        self.assertFalse(remove_mock.called)
        self.assertFalse(rmtree_mock.called)

    def test_download_missing_file(self):
        artifact = "some/missing/file.txt"
        artifactory_list = [artifact]
        with patch.object(self.cache, 'download_file_to_cache') as download_mock, \
                patch.object(self.cache, 'get_list_from_artifactory', return_value=artifactory_list):
            self.cache.check_and_update_cache(artifact)
        download_mock.assert_called_with(artifact)

    def test_download_missing_dir(self):
        artifact = "some/missing"
        artifactory_list = [os.path.join(artifact, "file-a.txt"), os.path.join(artifact, "file-b.txt")]
        with patch.object(self.cache, 'download_file_to_cache') as download_mock, \
                patch.object(self.cache, 'get_list_from_artifactory', return_value=artifactory_list):
            self.cache.check_and_update_cache(artifact)
        download_mock.assert_has_calls([call(entry) for entry in artifactory_list])

    def test_download_missing_in_dir(self):
        artifact = "a/a1/"
        artifactory_list = [os.path.join(artifact, "file-a1.txt"),
                            os.path.join(artifact, "file-a2.txt"),
                            os.path.join(artifact, "file-a3.txt")]
        with patch.object(self.cache, 'download_file_to_cache') as download_mock, \
                patch.object(self.cache, 'get_list_from_artifactory', return_value=artifactory_list):
            self.cache.check_and_update_cache(artifact)
        download_mock.assert_has_calls([call(entry) for entry in artifactory_list[1:]])

    def test_no_download_complete_dir(self):
        artifact = "a/a2/"
        artifactory_list = [os.path.join(artifact, "file-a2-1.txt"), os.path.join(artifact, "file-a2-2.txt")]
        with patch.object(self.cache, 'download_file_to_cache') as download_mock, \
                patch.object(self.cache, 'get_list_from_artifactory', return_value=artifactory_list):
            self.cache.check_and_update_cache(artifact)
        self.assertFalse(download_mock.called)

    def test_no_download_existing_file(self):
        artifact = "a/file-a.txt"
        with patch.object(self.cache, 'download_file_to_cache') as download_mock, \
                patch.object(self.cache, 'get_list_from_artifactory') as list_mock:
            self.cache.check_and_update_cache(artifact)
        self.assertFalse(download_mock.called)
        self.assertFalse(list_mock.called)

    def test_copy_from_cache(self):
        pass


if __name__ == "__main__":
    unittest.main()
