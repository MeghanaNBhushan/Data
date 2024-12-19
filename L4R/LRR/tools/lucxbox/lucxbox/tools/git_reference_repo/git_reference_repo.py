#!/usr/bin/env python3

"""
Script to create and update reference repositories
Works on Linux and Windows
"""

import argparse
import configparser
import ctypes
import hashlib
import io
import os
import shutil
import stat
import subprocess
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxargs, lucxlog

GIT_CMD = "git"

LOGGER = lucxlog.get_logger()


class Refrepo:
    """
    a class representing a reference repository
    """

    def __init__(self, dirname, git_url,
                 free_storage_new=5120, free_storage_update=1024):
        """
        :param dirname: pathname under which the reference repo is updated or created
        :param git_repo: string referencing the parent repository
        :param free_storage_new: MiB of free storage for a new reference repository, used for checking
        :param free_storage_update: MiB of free storage for a reference respository update, used for checking
        """
        self.__git_url = git_url
        self.__path = dirname
        self.__repopath = os.path.join(
            self.__path, os.path.basename(self.__git_url))
        self.__minimum_space_fresh = free_storage_new * \
            (2**20)  # convert MiB to bytes
        self.__minimum_space_update = free_storage_update * \
            (2**20)  # convert MiB to bytes
        self.__remote_tags_refspec_template = "+refs/tags/*:refs/remotes/{}/tags/*"

    @property
    def path(self):
        return self.__repopath

    def update(self, force_fresh=False):
        """
        if a reference repository doesn't exist this method creates one.
        if it finds an existing one, it updates it.
        :param force_fresh: always creates a new reference repository, even if it finds an existing one
        """

        def remove_readonly(func, path, _):
            os.chmod(path, stat.S_IWRITE)
            func(path)

        if not os.path.exists(self.__repopath) or force_fresh:
            # create a new reference repo
            if force_fresh:
                shutil.rmtree(self.__repopath, onerror=remove_readonly)
            self.__create_new_refrepo()
        else:
            self.__update_refrepo()

        max_retry = 2
        integrity_count = 0
        while self.__check_integrity() != 0 and integrity_count < max_retry:
            # hmm, we've got a corrupted reference repo. Try again from scratch
            integrity_count += 1
            LOGGER.warning("git fsck failed - retry no %d/%d",
                           integrity_count, max_retry)
            shutil.rmtree(self.__repopath, onerror=remove_readonly)
            self.__create_new_refrepo()
        if integrity_count == max_retry:
            # didn't seem to help, give up
            raise EnvironmentError("Reference repository under {} is corrupt. ".format(self.__repopath) +
                                   "Attempted to repair {} times to no avail.".format(integrity_count))
        # if we made it here without exception give a good return code
        return 0

    def __create_new_refrepo(self):
        LOGGER.info("Creating a new reference repo under %s", self.__repopath)
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        if self.__disk_space_available(self.__minimum_space_fresh):
            reponame = os.path.basename(self.__git_url)
            self.__run_git_clone(reponame)
            self.__update_submodules()
        else:
            raise IOError("Insufficient disk space to create reference repository under {}. ".format(self.__path) +
                          "Free Space {:.1f}GB but requires {:.1f}GB".format(free_diskspace(self.__path) / (2**30),
                                                                             self.__minimum_space_fresh / (2**30)))

    def __update_submodules(self):
        """
        This functions looks at the .gitmodules to figure out which submodules exist in a repository.
        The repositories referred to by the submodules are added as remote to the reference repository
        as described in the cloudbees instructions. After they were added as remote those repos are fetched.
        Of those fetched repos we again look at their .gitmodules and add the next level of submodules as
        remote and fetch them .. and so on.
        We keep a set() of fetched repo urls in case a repo is used multiple times in the submodule tree to
        avoid adding it twice.
        """
        def get_submodule_list(ref=""):
            """
            returns a list of tuples with module name and url of the submodule
            """
            try:
                gitmodules_str = self.__get_gitmodules(ref)
                gitmodules = "\n".join([x.strip() for x in gitmodules_str.splitlines()])
                cfg = configparser.ConfigParser()
                with io.StringIO(gitmodules) as gitmodules_fp:
                    cfg.read_file(gitmodules_fp)
                return [(x.split('"')[1], cfg.get(x, 'url')) for x in cfg.sections()]
            except subprocess.CalledProcessError:
                # repo doesn't seem to have any submodules
                msg = "fatal: Path '.gitmodules' does not exist in '{}'".format(ref)
                LOGGER.info('The repository does not have any submodules. The error message "%s" can be ignored.', msg)
                return []

        def get_existing_submodule_urls():
            "returns a tuple (url, remote_name)"
            # origin is not a submodule repo url
            for remote in [x.strip() for x in self.__get_gitremotes() if x != "origin"]:
                yield (subprocess.check_output([GIT_CMD, "remote", "get-url", remote],
                                               cwd=self.__repopath).decode('utf-8').strip(), remote)

        def tags_refspec_configured_for(name):
            fetch_refspecs = self.__get_git_fetch_config(name)
            return self.__remote_tags_refspec_template.format(name) in fetch_refspecs.split()

        LOGGER.info(
            "Updating submodules of reference repo under %s", self.__repopath)
        updated_submodules = set()
        # figure which submodules we currently have in the .gitmodules
        # We need to look at .gitmodules in the reference repo. Since it's a bare
        # repo we need to use "git show" to obtain its content. For the base
        # repo we can use FETCH_HEAD:.gitmodules while on the submodule-remotes
        # we use HEAD:.gitmodules (if you find a way to use HEAD:.gitmodules for
        # both please let me know. Using "git remote set-head origin --auto"
        # didn't work hence the different handling)
        #
        # UPD: as we started to fetch origin's references as well as ones for submodules
        # and store them in refs/remotes/origin/ set-head works fine to set HEAD for origin.
        # So now we can use 'origin/HEAD' to get list of submodules.
        current_git_submodules = get_submodule_list("origin/HEAD")
        # which submodules have we already added as remote to the reference repo
        existing_git_submodule_urls = dict(get_existing_submodule_urls())
        for sm_name, sm_url in current_git_submodules:
            if sm_url not in updated_submodules:
                try:
                    # submodules of submodules may use the same name but point to different
                    # repos (e.g. generic names such as "tools"). Therefore add a suffix
                    # to make the submodule name unique but deterministic -> hash
                    uniq_sm_name = sm_name + "_" + \
                        hashlib.md5(sm_url.encode()).hexdigest()[:5]
                    if sm_url not in existing_git_submodule_urls:
                        self.__run_git_addremote(uniq_sm_name, sm_url)
                    else:
                        uniq_sm_name = existing_git_submodule_urls[sm_url]
                    # Make sure that refspec for tags is configured for the submodule
                    if not tags_refspec_configured_for(uniq_sm_name):
                        self.__set_git_remote_fetch_config(uniq_sm_name)
                    self.__run_git_fetch(uniq_sm_name)
                    updated_submodules.add(sm_url)
                    # append the remote submodules while iterating
                    current_git_submodules += get_submodule_list(
                        uniq_sm_name + "/HEAD")
                except subprocess.CalledProcessError as excp_err:
                    LOGGER.error(
                        "submodule update of '%s %s' failed\n - error was '%s'", sm_name, sm_url, excp_err)

    def __update_refrepo(self):
        LOGGER.info("Updating reference repo under %s", self.__repopath)
        if self.__disk_space_available(self.__minimum_space_update):
            subprocess.check_call(
                [GIT_CMD, "fetch", "origin", "+refs/heads/*:refs/remotes/origin/*", "--prune"], cwd=self.__repopath)
            self.__run_git_set_head("origin")
            self.__update_submodules()
        else:
            raise IOError("Insufficient disk space to update reference repository under {}. ".format(self.__path) +
                          "Free Space {:.1f}GB but requires {:.1f}GB".format(free_diskspace(self.__path) / (2**30),
                                                                             self.__minimum_space_update / (2**30)))

    def __check_integrity(self):
        returncode = subprocess.call([GIT_CMD, "fsck"], cwd=self.__repopath)
        LOGGER.debug("git fsck rc = %d", returncode)
        return returncode

    def __disk_space_available(self, limit):
        "returns True if available space is >= limit"
        return free_diskspace(self.__path) >= limit

    # git functions
    def __run_git_clone(self, reponame):
        subprocess.check_call(
            [GIT_CMD, "clone", "--bare", self.__git_url, reponame], cwd=self.__path)
        subprocess.check_call([GIT_CMD, "fetch", "origin", "+refs/heads/*:refs/remotes/origin/*", "--prune"],
                              cwd=self.__repopath)  # sets FETCH_HEAD
        subprocess.check_call([GIT_CMD, "config", "remote.origin.fetch", "'refs/heads/*:refs/heads/*'"],
                              cwd=self.__repopath)
        self.__run_git_set_head("origin")

    def __get_gitmodules(self, ref):
        return subprocess.check_output([GIT_CMD, "show", ref + ":.gitmodules"], cwd=self.__repopath).decode('utf-8')

    def __get_gitremotes(self):
        return subprocess.check_output([GIT_CMD, "remote"], cwd=self.__repopath).decode('utf-8').splitlines()

    def __run_git_addremote(self, name, url):
        subprocess.check_call(
            [GIT_CMD, "remote", "add", name, url], cwd=self.__repopath)

    def __run_git_fetch(self, name):
        subprocess.check_call(
            [GIT_CMD, "fetch", name, "--prune"], cwd=self.__repopath)
        self.__run_git_set_head(name)

    def __run_git_set_head(self, name):
        # set HEAD as in the remote so that we can look at HEAD:.gitmodules for further
        # submodules
        subprocess.check_call(
            [GIT_CMD, "remote", "set-head", name, "--auto"], cwd=self.__repopath)

    def __get_git_fetch_config(self, name):
        return subprocess.check_output(
            [GIT_CMD, "config", "--get-all", "remote.{}.fetch".format(name)],
            cwd=self.__repopath).decode(sys.stdout.encoding)

    def __set_git_remote_fetch_config(self, name):
        subprocess.check_call(
            [GIT_CMD, "config", "--add", "remote.{}.fetch".format(name),
             self.__remote_tags_refspec_template.format(name)], cwd=self.__repopath)


def free_diskspace(dirname):
    """
    return the amount of free diskspace under a given path. Size is in bytes.
    :param dirname: string pathname
    """
    LOGGER.info("Running on %s", sys.platform)
    if os.name == "nt":
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        dir_stat = os.statvfs(dirname)
        return dir_stat.f_bavail * dir_stat.f_frsize


def parse_args():
    desc = "### Description: ###\n\n" + \
        "This script is intended to create and maintain a reference repository\n" + \
        "based on https://support.cloudbees.com/hc/en-us/articles/115001728812-Using-a-Git-reference-repository"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--path", "-p", help="Path of the reference repo. If it exists, it will be updated. " +
                        "If it's an empty directory a reference repository will be created",
                        required=True)
    parser.add_argument("--git_repo", "-g", help="The git repository for which a reference repository should be created",
                        required=True)
    parser.add_argument("--force", "-f", help="force the creation of a fresh reference repository, don't attempt to update",
                        required=False, action="store_true")
    parser.add_argument("--storage_new", help="required free disk space for a new reference repository - in MiB." +
                        "[default=5120]", required=False, default=5120, type=int)
    parser.add_argument("--storage_update", help="required free disk space for a reference repository update - in MiB" +
                        "[default=1023]", required=False, default=1202, type=int)
    parser = lucxargs.add_log_level(parser)
    parser = lucxargs.add_version(parser)
    return parser.parse_args()


def main():
    args = parse_args()
    ref_repo = Refrepo(args.path, args.git_repo)
    ref_repo.update(args.force)


if __name__ == "__main__":
    sys.exit(main())
