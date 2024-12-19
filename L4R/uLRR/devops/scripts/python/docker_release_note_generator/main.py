__copyright__ = """
@copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""

import pickle
import os
import argparse
from release_notes import *
from pdf_generator import pdf


"""
This script generates release notes for a Docker release based on the provided version, commit ID, commit URL, and Docker directory.
It retrieves the release notes object, adds a new release to it, compares the changes in Dockerfiles, apt packages, and pip packages, generates a PDF report, and saves the release notes object to a pickle file.

Usage:
    python main.py --version <version> --commit_id <commit_id> --commit_url <commit_url> --docker_dir <docker_dir> --pkl_dir <pkl_dir>
"""


def get_release_notes_object(version: str, pkl_dir: str) -> Release_notes:
    """
    Retrieves the release notes object based on the provided version and pkl_dir.
    
    If the release_notes.pkl file exists in the pkl_dir, it loads the existing release_notes object.
    Otherwise, it creates a new release_notes object with an initial dummy release.
    
    If the provided version already exists in the release_notes object, it removes the latest release.
    
    Args:
        version (str): The version to retrieve the release notes for.
        pkl_dir (str): The directory where the release_notes.pkl file is located.
        
    Returns:
        Release_notes: The release notes object.
    """

    if os.path.exists(f"{pkl_dir}/release_notes.pkl"):
        print(f"Loading existing release_notes object from {pkl_dir}/release_notes.pkl")
        with open(f"{pkl_dir}/release_notes.pkl", "rb") as f:
            release_notes = pickle.load(f)
        
    else:
        print("No release_notes.pkl found, creating new release_notes object with initial dummy release 0.0.0")
        release_notes = Release_notes()
        release_notes.add_release("0.0.0", "0000000", "https://github.boschdevcloud.com/Half-Dome/ad-radar-sensor/commit/", "/tmp","Manual")

    if version == release_notes.get_latest_release_version():
        print(f"Version {version} already exists in release_notes object. Removing release...")
        release_notes.releases.pop()
    
    return release_notes


def safe_release_notes_object(release_notes: Release_notes, pkl_dir: str):
    """
    Save the release_notes object to a pickle file.

    Args:
        release_notes (Release_notes): The release notes object to be saved.
        pkl_dir (str): The directory where the pickle file will be saved.
    """

    print(f"Saving release_notes object to release_notes.pkl")
    with open(f"{pkl_dir}/release_notes.pkl", "wb") as f:
        pickle.dump(release_notes, f)


if __name__  == "__main__":
    
    argparse = argparse.ArgumentParser()
    argparse.add_argument("--version", help="Version of the release")
    argparse.add_argument("--commit_id", help="Commit ID of the release")
    argparse.add_argument("--commit_url", help="Commit URL of the release")
    argparse.add_argument("--docker_dir", help="Docker directory of the release")
    argparse.add_argument("--pkl_dir", help="Directory where release_notes.pkl is stored")
    argparse.add_argument("--build_reason", help="Reason for the build")


    args = argparse.parse_args()

    version = args.version
    commit_id = args.commit_id
    commit_url = args.commit_url
    docker_dir = args.docker_dir
    pkl_dir = args.pkl_dir
    build_reason = args.build_reason
    print("Script startet with arguments:")
    for key, value in vars(args).items():
        print(f" - {key}: {value}")

    release_notes = get_release_notes_object(version, pkl_dir)
    release_notes.add_release(version, commit_id, commit_url, docker_dir, build_reason)

    dockerfile_changes = release_notes.compare_dockerfiles()
    apt_package_changes = release_notes.compare_apt_packages()
    pip_package_changes = release_notes.compare_pip_packages()

    pdf_generator = pdf(os.path.dirname(os.path.realpath(__file__)))
    pdf_generator.generate_pdf(release_notes.get_latest_release_version(), release_notes.get_latest_release_commit_id(), release_notes.get_latest_release_commit_url(), release_notes.get_latest_release_docker_dir(), release_notes.get_latest_release_build_reason(), dockerfile_changes, apt_package_changes, pip_package_changes)
    
    safe_release_notes_object(release_notes, pkl_dir)
    
    

