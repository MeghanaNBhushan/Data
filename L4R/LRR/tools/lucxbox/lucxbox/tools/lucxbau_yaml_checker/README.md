# lucxbau_yaml_checker

Checks the LUCxBox yaml configs for errors.

This script can eiter check a single config or all configs inside a given directory.
For directories, it is also possible to exclude certain paths inside that directory.

The version of the LUCxBau Library in use is read from the Jenkisfile.
For the found version te needed `lucxbau.jar` is taken from a local cache.
In cases were the required version is not in the cache it is automatically downloaded from  artifyctory.

-----------------------

usage: lucxbau_yaml_checker.py [-h] [-u USER] [-p PASSWORD] [-c CONFIG] [-x EXCLUDE [EXCLUDE ...]] [-j JENKINSFILE] [-d] [-q] [--version]

Please add some description.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User name for Artifactory
  -p PASSWORD, --password PASSWORD
                        User password or API key for Artifactory (API-key can also be provided using an environment variable 'ARTIFACTORY_API_KEY'
  -c CONFIG, --config CONFIG
                        Path to the config(s) to check. When a directory is provided all contained configs are checked.
  -x EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        Path to exclude when checking configs in a folder recursively
  -j JENKINSFILE, --jenkinsfile JENKINSFILE
                        Path to the Jenkinsfile to read the LUCxBau version from
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit