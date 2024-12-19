
# -*- coding: utf-8 -*-
"""
The artifacts_cache downloads artifacts from a given artifactory path and stores them in a local cache.
"""
import sys
import os
import shutil
import artifactory
from artifactory import ArtifactoryPath

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog


LOGGER = lucxlog.get_logger(__file__)

ARTIFACTORY_URL = 'https://rb-artifactory.bosch.com/artifactory'
CACHE_DIR = os.path.abspath(os.path.join(os.path.expanduser('~'), 'artifactory_cache'))


class ArtifactCache:
    """
        Provides the requested artifact from the cache at the specified destination.
        In cases where the artifact does not exist in the cache yet, it is downloaded to the cache automatically.

        :param artifactory_url: url to the jfrog artifactory
        :param user:user for artifactory access
        :param password: API-key or password to access artifactory
    """

    def __init__(self, user, password, artifactory_url=ARTIFACTORY_URL, cache_dir=CACHE_DIR, update_tracked_artifacts=False):
        self.artifactory_url = artifactory_url
        self.user = user
        self.password = password
        self.cache_dir = cache_dir
        self.update_tracked_artifacts = update_tracked_artifacts

    def clear(self, artifact_path=None):
        path_to_clear = self.__cache_path(artifact_path)
        if os.path.isdir(path_to_clear):
            LOGGER.warning("Removing cached directory '%s'", path_to_clear)
            shutil.rmtree(path_to_clear)
            return
        if os.path.isfile(path_to_clear):
            LOGGER.warning("Removing cached file '%s'", path_to_clear)
            os.remove(path_to_clear)

    def get_artifact(self, artifact_path, out_filepath):
        """
        Provides the requested artifact from the cache at the specified destination.
        In cases where the artifact does not exist in the cache yet, it downloaded to the cache first.

        :param artifact_path: relative path of the artifact
        :param out_filepath: local output path and filename of the artifact
        """

        LOGGER.info("Artifact '%s' -> '%s'", artifact_path, out_filepath)
        self.check_and_update_cache(artifact_path)
        self.copy_from_cache(artifact_path, out_filepath)

    def get_artifact_path_in_cache(self, artifact_path):
        """
        Returns the path of the requested artifact in the local cache.
        In cases where the artifact does not exist in the cache yet, it downloaded to the cache first.

        :param artifact_path: relative path of the artifact
        """

        self.check_and_update_cache(artifact_path)
        local_path = self.__cache_path(artifact_path)
        LOGGER.info("Artifact located at '%s'", local_path)
        return local_path

    def check_and_update_cache(self, artifact_path):
        """
        Checks that all files for a given artifact are available in the cache.
        Missing files are automatically downloaded to the cache.

        :param artifact_path: relative path of the artifact
        """
        cache_artifact_path = self.__cache_path(artifact_path)
        if os.path.exists(cache_artifact_path) and os.path.isfile(cache_artifact_path):
            LOGGER.debug("Artifact '%s' was found in the cache", artifact_path)
            return

        artifacts_in_artifactory = self.get_list_from_artifactory(artifact_path)
        for artifact in artifacts_in_artifactory:
            if not self.is_file_in_cache(artifact):
                self.download_file_to_cache(artifact)
                continue
            if self.update_tracked_artifacts:
                if not self.compare_md5_artifacts_cache(artifact_path):
                    self.download_file_to_cache(artifact)

        LOGGER.info("Updated Artifact '%s' in cache", artifact_path)

    def is_file_in_cache(self, file):
        """
        Checks if the cache already contains a specific file

        :param file: artifact to check
        :return: boolean if the file exists in the cache
        """
        if os.path.isfile(self.__cache_path(file)):
            LOGGER.debug("File '%s' found in the cache", file)
            return True
        LOGGER.debug("File '%s' is NOT in the cache", file)
        return False

    def get_list_from_artifactory(self, artifact_path):
        """
        Fetches a list of artifact filenames in artifactory for a certain artifact path

        :param artifact_path: path of the artifact
        :return: boolean weather all files exist locally
        """
        LOGGER.debug("Fetching list of files from artifactory for artifact '%s'", artifact_path)
        try:
            artifactory_path = self.__get_artifactory_path(self.__artifact_url(artifact_path))
            artifacts_on_server = [str(path).replace(self.artifactory_url, '').lstrip('/') for path in artifactory_path]
            LOGGER.debug("Artifact '%s' is a directory with %d file(s)", artifact_path, len(artifacts_on_server))
            return artifacts_on_server
        except NotADirectoryError:
            LOGGER.debug("Artifact '%s' is a single file", artifact_path)
            return [artifact_path]
        except Exception as ex:
            LOGGER.error("Failed while fetching list of files from artifactory for artifact '%s'", artifact_path)
            raise ex

    def download_file_to_cache(self, artifact_filepath):
        """
        Downloads the given artifact from artifactory to the local cache

        :param artifact_filepath: relative path and filename of the artifact
        """
        cache_filepath = os.path.join(CACHE_DIR, artifact_filepath)
        cache_dir = os.path.dirname(cache_filepath)

        # Ensure that the destination directory exists
        os.makedirs(cache_dir, exist_ok=True)

        artifact_url = self.__artifact_url(artifact_filepath)
        artifactory_path = self.__get_artifactory_path(artifact_url)
        LOGGER.info("Downloading '%s' to cache in '%s'", artifact_url, cache_filepath)

        artifactory_path.writeto(out=cache_filepath)

    def copy_from_cache(self, artifact_path, destination=None):
        """
        Copies the specified artifact from the cache to the destination

        :param artifact_path: artifact path and filename inside the cache
        :param destination: destination path and filename the artifact is copied to
        """
        destination = os.path.join(os.path.abspath('.'), artifact_path) if not destination else destination

        cache_path = os.path.join(self.cache_dir, artifact_path)
        LOGGER.debug("Copying artifact(s) '%s' from cache to '%s'", cache_path, destination)
        output_path = os.path.dirname(os.path.abspath(destination))
        os.makedirs(output_path, exist_ok=True)
        if os.path.isdir(cache_path):
            if os.path.exists(destination):
                shutil.rmtree(destination)
            shutil.copytree(cache_path, destination)
        else:
            shutil.copyfile(cache_path, destination)

    def compare_md5_artifacts_cache(self, artifact_path):
        local_artifact_md5 = artifactory.md5sum(self.get_artifact_path_in_cache(artifact_path))
        remote_artifact_path = self.__get_artifactory_path(self.__artifact_url(artifact_path))
        remote_artifact_md5 = remote_artifact_path.stat().md5
        if local_artifact_md5 == remote_artifact_md5:
            return True
        return False

    def __artifact_url(self, artifact):
        artifact = artifact.replace('\\', '/')
        artifact_url = f"{self.artifactory_url}/{artifact}"
        return artifact_url

    def __get_artifactory_path(self, artifact_url):
        if self.password:
            LOGGER.debug("Using authentication provided on commandline")
            auth = (self.user, self.password)
        else:
            LOGGER.debug("Using artifactory api key from env variable 'ARTIFACTORY_API_KEY'")
            auth = (self.user, os.getenv('ARTIFACTORY_API_KEY'))
        artifactory_path = ArtifactoryPath(artifact_url, auth=auth)
        return artifactory_path

    def __cache_path(self, artifact_path=None):
        if artifact_path:
            return os.path.join(self.cache_dir, artifact_path)
        return self.cache_dir
