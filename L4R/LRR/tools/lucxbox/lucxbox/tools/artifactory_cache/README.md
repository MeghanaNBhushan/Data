# artifactory_cache

Provides and downloads artifacts (files and folders) from artifactory.
Artifacts are downloaded to a local cache. When a required artifact
is already in the cache it is taken from there to save download time and traffic.

-----------------------

usage: artifactory_cache.py [-h] [-u USER] [-a ARTIFACT_PATH] [-p PASSWORD] [--url URL] [-o OUTPUT_PATH] [--clear] [--track-changes] [-d] [-q]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User name for Artifactory (default: None)
  -a ARTIFACT_PATH, --artifact-path ARTIFACT_PATH
                        The artifact path and filename to fetch (default: None)
  -p PASSWORD, --password PASSWORD
                        User password or API key for Artifactory (API-key can also be provided using an environment variable 'ARTIFACTORY_API_KEY' (default: None)
  --url URL             Base URL of Artifactory (default: https://rb-artifactory.bosch.com/artifactory)
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        The output filename and path for the artifact (default: None)
  --clear               Clear artifactory cache before download (default: False)
  --track-changes       Re-download cached files if the local file hash does not match the remote hash. Use this for changing artifact like 'latest' (default: False)
  -d, --debug           Print debug information (default: INFO)
  -q, --quiet           Print only errors (default: INFO)