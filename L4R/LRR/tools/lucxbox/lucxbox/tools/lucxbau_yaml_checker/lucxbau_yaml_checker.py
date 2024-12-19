""" Template for a python project """

import argparse
import glob
import subprocess
import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxargs, lucxlog
from lucxbox.tools.artifactory_cache import ArtifactoryCache

LOGGER = lucxlog.get_logger()

LUCXBAU_JAR_CACHE = os.path.abspath(os.path.join(os.path.expanduser('~'), '.lucxbau-jar-cache'))
ARTIFACTORY_URL = "https://rb-artifactory.bosch.com/artifactory/lucx-generic-local/lucxbau/"
JAR_NAME = 'lucxbau.jar'

LIST_PREFIX = "\n  - "


class YamlChecker:
    def __init__(self, jar_path):
        self.jar_path = jar_path

    def config_file_ok(self, config):
        LOGGER.debug("Checking config '%s'", config)
        config = os.path.abspath(config)
        command = 'java -jar \"' + self.jar_path + '\" -f "' + config + '" --debug --verbose'
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError:
            LOGGER.warning("Problem found in config file '%s'", config)
            LOGGER.info("To reproduce run the following command:\n   %s", command)
            return False

        LOGGER.info("Config file '%s' is ok", config)
        return True

    def all_configs_in_dir_ok(self, config_path, excludes):
        configs = self._get_configs_to_check(config_path, excludes)
        configs_with_problem = []
        for config in configs:
            if not self.config_file_ok(config):
                configs_with_problem.append(config)

        if configs_with_problem:
            LOGGER.warning("Found %d config(s) with problems:%s%s", len(configs_with_problem),
                           LIST_PREFIX, LIST_PREFIX.join(configs_with_problem))
            return False
        return True

    def check_configs(self, config_path, excludes=None):
        excludes = excludes if excludes else []
        config_path = os.path.abspath(config_path)
        if not os.path.exists(config_path):
            LOGGER.error("Specified config location '%s' does not exist", config_path)
            sys.exit(404)

        configs_ok = False
        if os.path.isfile(config_path):
            configs_ok = self.config_file_ok(config_path)
        elif os.path.isdir(config_path):
            configs_ok = self.all_configs_in_dir_ok(config_path, excludes)

        if configs_ok:
            LOGGER.info("All checked configs are ok")
            return

        LOGGER.error("One or more configs have a problem")
        sys.exit(1)

    @staticmethod
    def _get_configs_to_check(config_path, excludes):
        config_path = os.path.abspath(config_path)
        excluded_paths = [os.path.abspath(path) for path in excludes]
        all_yaml_files = get_all_yaml_files_in_dir(config_path)

        relevant_files = []
        excluded_files = []
        for file in all_yaml_files:
            if is_file_excluded(file, excluded_paths):
                excluded_files.append(file)
            else:
                relevant_files.append(file)

        if not relevant_files:
            LOGGER.error("No configs to check found in '%s'", config_path)
            sys.exit(404)

        LOGGER.debug("A total of %d configs in '%s' were excluded:%s%s", len(excluded_files), config_path,
                     LIST_PREFIX, LIST_PREFIX.join(excluded_files))
        LOGGER.info("Found %d configs to check in '%s'", len(relevant_files), config_path)
        LOGGER.debug("Configs to check:%s%s", LIST_PREFIX, LIST_PREFIX.join(relevant_files))
        return relevant_files


def parse_args(args):
    desc = "Please add some description."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-u', '--user',
                        help='User name for Artifactory')
    parser.add_argument('-p', '--password',
                        help="User password or API key for Artifactory "
                             "(API-key can also be provided using an environment variable 'ARTIFACTORY_API_KEY'")
    parser.add_argument('-c', "--config",
                        default='jenkins/configs/',
                        help="Path to the config(s) to check. "
                             "When a directory is provided all contained configs are checked.")
    parser.add_argument('-x', "--exclude", nargs='+',
                        default=['jenkins/configs/inc'],
                        help="Path to exclude when checking configs in a folder recursively")
    parser.add_argument('-j', "--jenkinsfile", default="Jenkinsfile",
                        help="Path to the Jenkinsfile to read the LUCxBau version from")

    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    args = parser.parse_args(args)
    return args


def get_all_yaml_files_in_dir(config_path):
    configs_in_dir = []
    configs_in_dir.extend(glob.glob(os.path.join(config_path, '**', '*.yaml'), recursive=True))
    configs_in_dir.extend(glob.glob(os.path.join(config_path, '**', '*.yml'), recursive=True))
    return configs_in_dir


def is_file_excluded(file, excluded_paths):
    for exclude in excluded_paths:
        if file.startswith(exclude):
            LOGGER.debug("File '%s' is excluded by '%s'", file, exclude)
            return True
    LOGGER.debug("File '%s' is not excluded", file)
    return False


def get_version_from_jenkinsfile(jenkinsfile):
    if not os.path.isfile(jenkinsfile):
        LOGGER.error("The Jenkinsfile '%s' does not exist", os.path.abspath(jenkinsfile))
        sys.exit(404)

    regex = r'''^ *@?[Ll]ibrary[ \(]['"]\w+@([\w.\/\-_]+)['"].*'''
    version_pattern = re.compile(regex, re.MULTILINE)
    with open(jenkinsfile, 'r') as file:
        text = file.read()
    try:
        version = version_pattern.findall(text)[0]
        LOGGER.info("Found version '%s' in '%s'", version, jenkinsfile)
        return version
    except IndexError:
        LOGGER.error("Could not find LUCxBau version in '%s' using regex '%s'", jenkinsfile, regex)
        sys.exit(1)


def get_jar_path_for_version(lucxbau_version, user, password):
    LOGGER.info("Obtaining %s for LUCxBau %s", JAR_NAME, lucxbau_version)
    artifactory_cache = ArtifactoryCache.ArtifactCache(user=user, password=password,
                                                       cache_dir=LUCXBAU_JAR_CACHE, artifactory_url=ARTIFACTORY_URL)
    artifact_path_on_artifactory = os.path.join(lucxbau_version, JAR_NAME)
    try:
        return artifactory_cache.get_artifact_path_in_cache(artifact_path_on_artifactory)
    except FileNotFoundError as fnfe:
        LOGGER.error("Obtaining %s for LUCxBau %s failed with message:\n%s", JAR_NAME, lucxbau_version, fnfe)
        sys.exit(1)


def main(args):
    args = parse_args(args)
    LOGGER.setLevel(args.log_level)

    lucxbau_version = get_version_from_jenkinsfile(args.jenkinsfile)
    jar_path = get_jar_path_for_version(lucxbau_version, args.user, args.password)
    yaml_checker = YamlChecker(jar_path)
    yaml_checker.check_configs(args.config, args.exclude)


if __name__ == "__main__":
    main(sys.argv[1:])
