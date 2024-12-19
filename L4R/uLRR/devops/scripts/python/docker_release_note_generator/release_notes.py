__copyright__ = """
@copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""

import difflib
import os

class Release_notes:
    """
    Class representing release notes for a project.
    """

    def __init__(self) -> None:
        self.commit_history = {}
        self.releases = []

    def add_release(self, version: str, commit_id: str, commit_url: str, docker_dir: str, build_reason:str) -> None:
        """
        Adds a new release to the list of releases.

        Args:
            version (str): The version of the new release.
            commit_id (str): The commit ID associated with the new release.
            commit_url (str): The URL of the commit associated with the new release.
            docker_dir (str): The directory of the Dockerfile for the new release.

        Returns:
            None
        """

        print(f"Adding new release {version}")
        self.releases.append(Release(version, commit_id, commit_url, docker_dir, build_reason))
        self.commit_history[version] = {commit_id: commit_url}

    def get_latest_release_version(self) -> str:
        """
        Returns the version of the latest release in the list.

        Returns:
            str: The version of the latest release in the list.
        """
        return self.releases[-1].version

    def get_latest_release_commit_id(self) -> str:
        """
        Returns the commit ID of the latest release in the list.

        Returns:
            str: The commit ID of the latest release in the list.
        """
        return self.releases[-1].commit_id

    def get_latest_release_commit_url(self) -> str:
        """
        Returns the commit URL of the latest release in the list.

        Returns:
            str: The commit URL of the latest release in the list.
        """
        return self.releases[-1].commit_url

    def get_latest_release_docker_dir(self) -> str:
        """
        Returns the docker directory of the latest release in the list.

        Returns:
            str: The docker directory of the latest release in the list.
        """

        return self.releases[-1].docker_dir
    
    def get_latest_release_build_reason(self) -> str:
        """
        Returns the build reason of the latest release in the list.

        Returns:
            str: The Build Reason of the latest release in the list.
        """
        return self.releases[-1].build_reason
    
    def compare_dockerfiles(self) -> list:
        """
        Compare the dockerfiles of the previous and latest releases and return the changes as a list.

        Returns:
            list: A list of changes between the previous and latest dockerfiles.
        """

        print("Comparing dockerfiles...")
        previous_dockerfile = self.releases[-2].dockerfile
        latest_dockerfile = self.releases[-1].dockerfile
        dockerfile_changes = difflib.unified_diff(previous_dockerfile, latest_dockerfile, fromfile="previous_dockerfile", tofile="latest_dockerfile", lineterm="")
        dockerfile_changes_list = [i.strip() for i in dockerfile_changes]
        return dockerfile_changes_list

    def __compare_package_lists(self, old_packages: dict, new_packages: dict) -> dict:
        """
        Compares two package lists and returns the changes between them.

        Args:
            old_packages (dict): The dictionary representing the old package list.
            new_packages (dict): The dictionary representing the new package list.

        Returns:
            dict: A dictionary containing the changes between the two package lists.
                  The dictionary has the following structure:
                  {
                      "added": [list of added packages],
                      "updated": [list of updated packages],
                      "removed": [list of removed packages]
                  }
        """

        changes = {"added": [], "updated": [], "removed": []}

        old_set, new_set = set(old_packages), set(new_packages)

        added_packages = new_set - old_set
        removed_packages = old_set - new_set

        changes["added"].extend(added_packages)
        changes["removed"].extend(removed_packages)

        for package in new_set & old_set:
            if old_packages[package] != new_packages[package]:
                update_info = f"{package} changed from {old_packages[package]} to {new_packages[package]}"
                changes["updated"].append(update_info)

        return changes

    def compare_apt_packages(self) -> dict:
        """
        Compare the apt packages between the last two releases.

        Returns:
            A dictionary containing the differences between the apt package lists.
        """

        print("Comparing apt packages...")
        return self.__compare_package_lists(self.releases[-2].apt_package_list, self.releases[-1].apt_package_list)

    def compare_pip_packages(self) -> dict:
        """
        Compare the pip packages between the second last and last releases.

        Returns:
            A dictionary containing the comparison result.
        """

        print("Comparing pip packages...")
        return self.__compare_package_lists(self.releases[-2].pip_package_list, self.releases[-1].pip_package_list)


class Release:
    """
    Represents a release of a Docker image.

    Attributes:
        version (str): The version of the release.
        commit_id (str): The commit ID associated with the release.
        commit_url (str): The URL to the commit associated with the release.
        docker_dir (str): The directory containing the Dockerfile and package lists.
        dockerfile (list): The parsed contents of the Dockerfile.
        apt_package_list (dict): The parsed contents of the apt package list.
        pip_package_list (dict): The parsed contents of the pip package list.
    """

    def __init__(self, version, commit_id, commit_url, docker_dir, build_reason) -> None:
        self.version = version 
        self.commit_id = commit_id
        self.commit_url = commit_url
        self.docker_dir = docker_dir
        self.build_reason = build_reason
        self.dockerfile = self.__parse_dockerfile()
        self.apt_package_list = self.__parse_package_list("apt_packages.txt")
        self.pip_package_list = self.__parse_package_list("pip_packages.txt")

    def __parse_dockerfile(self) -> list:
        """
        Parses the Dockerfile and returns its contents as a list of lines.

        Returns:
            list: The parsed contents of the Dockerfile.
        """

        parsed_file = []
        if os.path.exists(f"{self.docker_dir}/Dockerfile"):
            print(f"Parsing Dockerfile -> {self.docker_dir}/Dockerfile")
            with open(f"{self.docker_dir}/Dockerfile", "r") as file:
                for line in file:
                    if line == "\n": continue
                    parsed_file.append(line.strip())
            return parsed_file
        else:
            print(f"Dockerfile not found -> {self.docker_dir}/Dockerfile")
            print("Parsed Dockerfile will be empty")
            return []

    def __parse_package_list(self, filename: str) -> dict:
        """
        Parses a package list file and returns its contents as a dictionary.

        Args:
            filename (str): The name of the package list file.

        Returns:
            dict: The parsed contents of the package list file.
        """
        
        parsed_file = {}
        if os.path.exists(f"{self.docker_dir}/{filename}"):
            print(f"Parsing {filename} -> {self.docker_dir}/{filename}")
            with open(f"{self.docker_dir}/{filename}", "r") as file:
                for line in file:
                    if line[:1] == "#": continue
                    if line[-1:] == "\n": line = line[:-1]
                    if "==" in line:
                        app, version = line.split("==")
                    elif "=" in line:
                        app, version = line.split("=")
                    else:
                        app = line
                        version = "latest"
                    parsed_file[app] = version
            return parsed_file
        else:
            print(f"{filename} not found -> {self.docker_dir}/{filename}")
            print(f"Parsed {filename} will be empty")
            return {}
