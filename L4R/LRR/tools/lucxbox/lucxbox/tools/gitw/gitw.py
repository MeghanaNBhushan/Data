#!/usr/bin/env python3

"""
Copyright (c) 2009, 2016 Robert Bosch GmbH and its subsidiaries.
This program and the accompanying materials are made available under
the terms of the Bosch Internal Open Source License v4
which accompanies this distribution, and is available at
http://bios.intranet.bosch.com/bioslv4.txt
"""

import os
import sys
import shutil
from typing import Union
from typing import Tuple
from functools import wraps
import git
import gitdb

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog

LOGGER = lucxlog.get_logger()


def call_log_for_class_logger(function_name):

    @wraps(function_name)
    def wrapper(*args, **kwargs):
        LOGGER.info('Entering function "%s"', function_name.__name__)

        result = function_name(*args, **kwargs)

        LOGGER.info('Exiting function "%s"', function_name.__name__)
        # Return the return value
        return result
    return wrapper


class Repo(git.Repo): # pylint: disable=too-many-public-methods
    """Extension of the normal git.Repo class to make some functionaries easier to access"""
    def __init__(self, path: str = '.',
                 url: str = None,
                 search_parent_directories: bool = False):
        """
        @param path: path to the repo, default '.'
        @param url: url of the repo. Used to clone or check for in existing repo,
        default is 'None' which will not clone nor do any check for a existing repo
        @param search_parent_directories: if True, all parent directories will be searched for a valid repo as well
        """
        self.default_logger_name = f"{__name__}@{os.path.abspath(path)}"
        self.path = path
        self.__prepare_repo__(url)
        super().__init__(path, search_parent_directories=search_parent_directories)
        self.__check_repo_url__(url)
        self.__submodule_helpers__ = dict()

    @property
    def __log_prefix__(self) -> str:
        """
        @return: Prefix to put in front of LOG messages to identify which repo we log from
        """
        return f"{self.project}::{self.repo_name}"

    @call_log_for_class_logger
    def __prepare_repo__(self, url: str = None):
        """Prepares the local repository for use.
        When a local repository exists we will use it.

        If no local repository exists the url is used to clone the repo. When no url was provided can not clone and
        raise an InvalidGitRepositoryError

        @raise git.InvalidGitRepositoryError
        @param url: optional, url of repo. Used to clone or check if existing repo url matches
        """
        if is_git_repo(self.path):
            LOGGER.debug("Local repository in '%s' already exists", self.path)
            return

        if not url:
            LOGGER.error("No existing repository found in '%s' and no url to clone from provided", self.path)
            raise git.InvalidGitRepositoryError

        #  before cloning make sure the provided folder does not exists or is empty
        if os.path.isdir(self.path) and os.listdir(self.path):
            LOGGER.error("Directory '%s' exists (with content) but is not a git repository", self.path)
            raise git.InvalidGitRepositoryError

        # clone repository
        try:
            LOGGER.debug("Trying to clone '%s' repository in '%s'", url, self.path)

            git.Repo.clone_from(url=url, to_path=self.path, recursive=True)
        except git.exc.GitCommandError:
            # handling error when ref is causing problems while cloning (e.g. tag)
            git.Repo.clone_from(url, self.path)

    @call_log_for_class_logger
    def __check_repo_url__(self, url: str, allow_base_url_change: bool = False):
        """Check if the default remote url of the repository matches the given one.
        If the url does not match we raise a InvalidGitRepositoryError exception

        It is possible to update a local remote url in case repo name and project in both urls are equal (NOT default)

        @param url: url the repo is expected to have
        @param allow_base_url_change: if true we will update a not matching url if the repo-name and project-key match
        @raise git.InvalidGitRepositoryError
        """
        if not url:
            LOGGER.debug("No URL specified, so we use the one of the local repository")
            return

        if url != self.url:
            # Check if repo and project are equal in both urls
            if allow_base_url_change \
                    and self.project == get_project_from_url(url) \
                    and self.repo_name == get_repo_name_from_url(url):
                LOGGER.warning("Local remote url '%s' does not math the expected one url '%s'", self.url, url)
                LOGGER.info("Project '%s' and repository name '%s' are equal in both urls", self.project,
                            self.repo_name)
                LOGGER.info("Assuming a related repository was found and setting remote URL to '%s'", url)
                self.set_url(url)
                return

            LOGGER.error("Local remote url '%s' of repo in '%s' does not match the given url '%s'", self.url,
                         self.path, url)
            raise git.InvalidGitRepositoryError
        LOGGER.debug("Local remote url '%s' of repo in '%s' is matching the given url '{url}'", self.url, self.path)

    @classmethod
    @call_log_for_class_logger
    def __silent_logger__(cls, message: str, silent: bool):
        """Helper to control to if to log to info or debug
        @param message: message to log
        @param silent: if true we will log to debug instead of info
        """
        if silent:
            LOGGER.debug(message)
        else:
            LOGGER.info(message)

    @property
    def url(self) -> str:
        """
        @return: URL of the default remote
        """
        return self.remote().url

    @property
    def repo_name(self) -> str:
        """
        @return: name of the repository (taken from the url of te default remote)
        """
        return get_repo_name_from_url(self.url)

    @property
    def project(self) -> str:
        """
        @return: project-key of the repository (taken from the url of te default remote)
        """
        return get_project_from_url(self.url)

    @property
    def current_commit_sha(self) -> str:
        """@return: str, the first 11 digits of the sha sha (same length as shown in bitbucket)"""
        return self.get_commit_sha(digit_count=11)

    @call_log_for_class_logger
    def get_commit_sha(self, ref: str = 'HEAD', digit_count: int = None) -> str:
        """Gives the sha sha for teh given reference
        @param ref: str, reference (branch | tag | (shortened) sha)
        @param digit_count: int, number of digits for the returned sha (default is 'all')
        @return: str, sha sha of the reference (with the requested number of digits)
        """
        commit = str(self.get_commit(ref))
        if digit_count:
            commit = commit[0:digit_count]
        return commit

    @call_log_for_class_logger
    def get_commit(self, ref: str = 'HEAD') -> git.Commit:
        """returns the git sha object for the given reference
        @param ref: str, reference to get the sha object for
        @return: git.Commit, commit object of the reference
        """
        try:
            commit = self.commit(ref)
        except gitdb.exc.BadName:
            # maybe ref is a branch
            commit = self.head(ref).commit # pylint: disable=not-callable
        except IndexError:
            # maybe ref is a tag
            commit = self.tag(ref).commit
        return commit

    @call_log_for_class_logger
    def tags_on_commit(self, ref: str = 'HEAD') -> list:
        """Returns a list of tags assigned to the current sha
        @param ref: str, reference to get the tags for
        @return: list, tags at the commit of the given reference
        """
        # convert ref to sha (also works if sha given)
        sha = self.get_commit(ref)
        tags = [tag.name for tag in self.tags if tag.commit == sha]
        if tags:
            LOGGER.debug("Tags at '%s': %s", ref, ', '.join(tags))
        else:
            LOGGER.debug("No tags at '%s'", ref)
        return tags

    @call_log_for_class_logger
    def local_branches_on_commit(self, ref: str = 'HEAD') -> list:
        """all local branches assigned to the current commit
        @param ref: reference
        @return: list, local branches at the sha of the given reference
        """
        # convert ref to sha (also works if sha given)
        sha = self.get_commit(ref)
        branches = [branch.name for branch in self.heads if branch.commit == sha]
        if branches:
            LOGGER.debug("Local Branches at '%s': %s", ref, ', '.join(branches))
        else:
            LOGGER.debug("No local branches at '%s'", ref)
        return branches

    @call_log_for_class_logger
    def remote_branches_on_commit(self, ref: str = 'HEAD') -> list:
        """all remote branches assigned to the current sha
        @param ref: reference
        @return: list, remote branches at the sha of the given reference
        """
        commit = self.get_commit(ref)
        branches = []
        for remote in self.remotes:
            for ref in remote.refs: # pylint: disable=redefined-argument-from-local
                if ref.commit == commit:
                    branches.append(ref.name)
        if branches:
            LOGGER.debug("Local Branches at '%s': %s", ref, ', '.join(branches))
        else:
            LOGGER.debug("No local branches at '%s'", ref)
        return branches

    @call_log_for_class_logger
    def branches_on_commit(self, reference: str = 'HEAD') -> list:
        """local and remote branches assigned to the current sha
        @param reference: reference
        @return: list, local and remote branches at the sha of the given reference
        """
        # convert ref to sha (also works if sha given)
        branches = []
        branches.extend(self.local_branches_on_commit(reference))
        branches.extend(self.remote_branches_on_commit(reference))

        if branches:
            LOGGER.debug("Branches at '%s': %s", reference, ', '.join(branches))
        else:
            LOGGER.debug("No branches at '%s'", reference)
        return branches

    @property
    @call_log_for_class_logger
    def submodule_list(self) -> list:
        """@return: (sorted) list with all submodules in the currently checked out revision"""
        submodules = []
        for submodule in self.submodules:
            submodules.append(submodule.path)

        # it is easier to check the result LOGGER output if the submodules are sorted
        return sorted(submodules)

    @call_log_for_class_logger
    def get_submodule_commit(self, submodule_path: str, ref: str = None) -> git.Commit:
        """
        @param submodule_path: path to the submodule
        @param ref: reference of the submodule sha
            default: the revision of the submodule in the current sha of the main repo
        @return:  sha object for the given ref
        """
        ref = ref if ref else self.get_submodule(submodule_path).hexsha
        module = self.get_submodule(submodule_path).module()
        try:
            return module.commit(ref)
        except gitdb.exc.BadName:
            # maybe ref is a branch
            return module.head(ref).commit
        except IndexError:
            # maybe ref is a tag
            return module.tag(ref).commit

    @call_log_for_class_logger
    def get_submodule_workspace_commit(self, submodule_path: str) -> git.Commit:
        """ Returns the sha object of the currently checked out submodule revision
        @param submodule_path: path of the submodule
        @return: sha object of the currently checked out submodule revision
        """
        return self.get_submodule_commit(submodule_path, 'HEAD')

    @call_log_for_class_logger
    def get_submodule_workspace_sha(self, submodule_path: str, digit_count: int = None) -> str:
        """Returns the sha sha of the currently checked out revision of the submodule
        @param submodule_path: path of the submodule
        @param digit_count: number of digits for the returned sha sha
        @return: sha sha of the currently checked out revision of the submodule
        """
        commit = str(self.get_submodule_workspace_commit(submodule_path))
        if digit_count:
            # return only a part of the sha
            commit = commit[0:digit_count]
        return commit

    @call_log_for_class_logger
    def get_submodule_sha(self, submodule_path: str, digit_count: int = None) -> str:
        """Returns the sha sha of the submodule revision in the current sha of the main repo
        @param submodule_path: path of the submodule
        @param digit_count: number of digits for the returned sha sha
        @return: sha sha of the submodule revision in the current sha of the main repo
        """
        sha = str(self.get_submodule_commit(submodule_path))
        if digit_count:
            # return only a part of the sha
            sha = sha[0:digit_count]
        return sha

    @call_log_for_class_logger
    def get_submodule_url(self, submodule_path: str) -> str:
        """Returns the url for a submodule
        @param submodule_path: path of the submodule
        @return: url of the submodule
        """
        return self.get_submodule(submodule_path).url

    @call_log_for_class_logger
    def get_submodule_tags(self, submodule_path: str, sha: str = None) -> list:
        """
        @param submodule_path: path of the submodule
        @param sha: commit sha to check for tags, default is the submodule revision in the main repo commit
        @return: all tags at the given (default=current) submodule commit
        """
        if not sha:
            sha = self.get_submodule_sha(submodule_path)
        submodule_repo = self.get_submodule(submodule_path).module()
        for remote in submodule_repo.remotes:
            remote.fetch(tags=True, prune_tags=True, force=True)
        tags = [tag.name for tag in submodule_repo.tags if str(tag.commit) == sha]

        if tags:
            LOGGER.debug("Tags in submodule '%s' at sha '%s': %s", submodule_path, sha, ', '.join(tags))
        else:
            LOGGER.debug("No tags in submodule '%s' at sha '%s'", submodule_path, sha)
        return tags

    @call_log_for_class_logger
    def get_submodule_changed_revision(self, dest_commit_id: str, submodule_path: str) -> Tuple[str, str]:
        """Returns old and new revision of updated submodule in PR
        @param dest_commit_id: commit hash id of destination branch of main repo
        @param submodule_path: path of the submodule
        @return: old and new revision of submodule
        """
        diff_revision = self.git.diff("--cached", dest_commit_id, "--submodule=short", "--", submodule_path)
        if 'Subproject commit' not in diff_revision:
            LOGGER.warning("Not found any changed files")
            return None, None
        revs = diff_revision.split("\n")
        for rev in revs:
            if "-Subproject commit " in rev:
                old_rev = rev.replace("-Subproject commit ", "")
                LOGGER.debug("Old revision: %s", old_rev)
                continue
            if "+Subproject commit " in rev:
                new_rev = rev.replace("+Subproject commit ", "")
                LOGGER.debug("New revision: %s", new_rev)
                continue
        return old_rev, new_rev

    @call_log_for_class_logger
    def fetch(self, remote: str = None, tags: bool = True, prune: bool = True, prune_tags: bool = False, force=False) -> None:
        """Fetches references from all/a given remote(s)

        @param remote: name of the remote to fetch from, default `None` will fetch from all remotes
        @param tags: whether to fetch tags
        @param prune: whether to prune
        @param prune_tags: whether to prune tags
        @param force: whether to fetch with force option
        """
        if remote:
            self.__fetch_from_remote__(remote, tags, prune, prune_tags, force)
            return

        LOGGER.info("Fetching references from all remotes")
        for remote in self.remotes: # pylint: disable=redefined-argument-from-local
            self.__fetch_from_remote__(remote.name, tags, prune, prune_tags, force)

    @call_log_for_class_logger
    def __fetch_from_remote__(self, remote: str = None, tags: bool = True, prune: bool = True, prune_tags: bool = False, force=False):
        remote = remote if type(remote) is str else remote.name  # pylint: disable=unidiomatic-typecheck
        try:
            LOGGER.info("Fetching references from remote '%s'", remote)
            LOGGER.debug("Fetching with tags=%s, prune=%s, prune_tags=%s, force=%s",
                         tags, prune, prune_tags, force)
            self.remote(remote).fetch(tags=tags, prune=prune, prune_tags=prune_tags, force=force)
        except git.GitCommandError:
            self.__run_gc__()
            self.git.remote("prune", remote)
            self.__fetch_from_remote__(remote, tags, prune, prune_tags, force)

    @call_log_for_class_logger
    def __run_gc__(self):
        self.git.gc(prune='now', aggressive=True)

    @call_log_for_class_logger
    def fetch_submodule(self, submodule_path: str, remote: str = None, tags: bool = True,
                        prune: bool = True, prune_tags: bool = False, force=False) -> None:
        """Fetches references from all/a given remote(s)

        @param submodule_path: path of the submodule
        @param remote: name of the remote to fetch from, default `None` will fetch from all remotes
        @param tags: whether to fetch tags
        @param prune: whether to prune
        @param prune_tags: whether to prune tags
        @param force: whether to fetch with force option
        """
        module = self.get_submodule(submodule_path).module()

        if remote:
            LOGGER.info("Fetching references for submodule '%s' from remote '%s'", submodule_path, remote)
            module.remote(remote).fetch(tags=tags, prune=prune, prune_tags=prune_tags, force=force)
        else:
            LOGGER.info("Fetching references for submodule '%s' from all remotes", submodule_path)
            for remote in module.remotes:  # pylint: disable=redefined-argument-from-local
                LOGGER.debug("Fetching submodule '%s' from remote '%s'", submodule_path, remote.name)
                remote.fetch(tags=tags, prune=prune, prune_tags=prune_tags, force=force)
        LOGGER.debug("Fetching submodule with tags=%s, prune=%s, prune_tags=%s",
                     tags, prune, prune_tags)

    @call_log_for_class_logger
    def set_url(self, url: str, remote: str = 'origin') -> None:
        """Sets the remote URL for a given remote

        @param url: url to set
        @param remote: name of the remote, default is 'origin'
        @raise InvalidGitRepositoryError
        """
        old_url = self.url
        self.remote(remote).set_url(url)
        if not self.url == url:
            LOGGER.error("Remote url update failed")
            raise git.InvalidGitRepositoryError
        LOGGER.info("Updated remote url of '%s': old: '%s' new: '%s'", remote, old_url, self.url)

    @call_log_for_class_logger
    def commit_has_tag(self, ref: str = "HEAD", tag: str = None) -> bool:
        """checks if the (current) commit has a tag assigned

        @param ref: (optional) reference to check (default: current comit)
        @param tag: (optional) specific tag to check for (default matches any tag)
        @return: boolean if tag exists or not
        """
        tags = self.tags_on_commit(ref)

        if tags and not tag:
            return True
        if tag and tag in tags:
            return True
        return False

    @call_log_for_class_logger
    def commit_has_branch(self, commit: str = None, branch: str = None) -> bool:
        """Checks if the (current) sha has a branch assigned.

        @param commit: (optional) sha to check (default: current sha)
        @param branch: (optional) specific branch to check for (default matches any branch)
        @return: boolean if branch exists or not
        """
        commit = commit if commit else self.current_commit_sha

        if self.branches_on_commit(commit):
            if branch and branch not in self.branches_on_commit():
                return False
            return True
        return False

    @call_log_for_class_logger
    def tidy(self) -> None:
        """Resets and cleans the complete repo (including submodules)"""
        LOGGER.debug("Resetting and cleaning up repository")
        self.git.reset("--hard")
        self.clean()
        self.update_submodules()

    @call_log_for_class_logger
    def clean(self) -> None:
        """Runs 'git clean -xffd' in the repo """
        LOGGER.debug("Cleaning up repository")
        self.git.clean("-xffd")

    @call_log_for_class_logger
    def checkout(self, ref: str, force: bool = True, submodules: bool = True) -> None:
        """Checks out the given reference
        @param ref: reference
        @param force: possibility  to force checkout
        @param submodules: also checkout matching submodule revisions, default is true
        """
        LOGGER.debug("Checking out '%s'", ref)
        self.git.checkout(ref, force=force)
        if submodules:
            self.update_submodules()

    @call_log_for_class_logger
    def checkout_branch(self, ref: str, branch_name: str, force: bool = False) -> None:
        if self.branch_exists(branch_name):
            if not force:
                LOGGER.error("Branch with name '%s' already exists", branch_name)
                raise git.CheckoutError
            self.delete_head(branch_name, force=True)
        LOGGER.info("Checking out branch '%s' at '%s'", branch_name, ref)
        self.git.checkout(ref, b=branch_name, force=True)
        self.update_submodules()

    @call_log_for_class_logger
    def reset(self, ref: str = "HEAD", hard: bool = False) -> None:
        """Resets the repository (to the given ref)"""
        LOGGER.info("Resetting repository to '%s'", ref)
        self.head.reset(ref, index=True, working_tree=True, hard=hard)

    @call_log_for_class_logger
    def branch_exists(self, branch: str) -> bool:
        if self.local_branch_exists(branch) or self.remote_branch_exists(branch):
            return True
        return False

    @call_log_for_class_logger
    def local_branch_exists(self, branch: str) -> Union[str, bool]:
        """
        Checks if a given branch exists in the repo

        @param branch: name of the branch to check
        @return: boolean if the branch exists or not
        """
        if branch in self.branches:
            LOGGER.debug("Branch '%s' exists at %s", branch, self.commit(branch))
            return str(self.commit(branch))
        LOGGER.debug("Branch '%s' does not exist", branch)
        return False

    @call_log_for_class_logger
    def remote_branch_exists(self, branch: str, remote: str = "origin") -> Union[str, bool]:
        """Checks if a remote branch exists (we assume the repo was recently fetched)"""
        # we assume we already have fetched recently...
        for ref in self.remote(remote).refs:
            if branch in ref.name:
                LOGGER.debug("Branch '%s' exists on the remote at %s", branch, ref.commit)
                return str(ref.commit)
        LOGGER.debug("Branch '%s' does not exist on the remote", branch)
        return False

    @call_log_for_class_logger
    def tag_exists(self, tag: str) -> Union[str, bool]:
        """Checks if a given tag exists in the repo"""
        if tag in self.tags:
            LOGGER.debug("Tag '%s' exists at %s", tag, self.commit(tag))
            return str(self.commit(tag))
        LOGGER.debug("Tag '%s' does not exist", tag)
        return False

    @call_log_for_class_logger
    def remote_tag_exists(self, tag: str, remote: str = "origin") -> Union[str, bool]:
        """Checks if a remote branch exists (we assume the repo was recently fetched)"""

        ls_remote = self.git.ls_remote(self.remote(remote).url, tags=True)
        tag_ref = f"refs/tags/{tag}"
        dereferenced_tag_ref = tag_ref + "^{}"
        if dereferenced_tag_ref in ls_remote:
            # if the dereferenced_tag_ref exists we want to use it
            # the tag_ref would point to the (annotated) tag and not to the sha
            tag_ref = dereferenced_tag_ref

        for line in ls_remote.splitlines():
            if tag_ref in line:
                commit = line.split("\t")[0].strip()
                LOGGER.debug("Tag '%s' exists in the remote '%s' at %s", tag, remote, commit)
                return commit
        LOGGER.debug("Tag '%s' does not exist on the remote '%s'", tag, remote)
        return False

    @call_log_for_class_logger
    def ref_exists(self, ref) -> Union[str, bool]:
        try:
            sha = self.git.rev_parse("--verify", ref)
            LOGGER.debug("Reference '%s' exists at %s", ref, sha)
            return sha
        except: # pylint: disable=bare-except
            LOGGER.debug("Reference '%s' does not exist", ref)
            return False

    @call_log_for_class_logger
    def ref_exists_on_remote(self, ref: str, remote: str = "origin") -> Union[str, bool]:
        # this does not support sha SHAs
        ls_remote = self.git.ls_remote(self.remote(remote).url, ref)

        if ls_remote:
            sha = ls_remote.split("\t")[0].strip()
            LOGGER.debug("Reference '%s' exists on remote '%s'", ref, sha)
            return sha
        LOGGER.debug("Reference '%s' does not exist on remote '%s'", ref, remote)
        return False

    @call_log_for_class_logger
    def get_submodule(self, name: str) -> git.Submodule:
        """Returns the git.Submodule for a given submodule path
        This adds more stability as there is a the possibility the 'name' of the submodule does not match the 'path'
         (e.g. when it was moved)
         In that case we check if a submodule with the 'path' for the given name exists instead of failing
         @param name: name/path of the submodule
         @return: the requested git.Submodule
         """
        try:
            return self.submodule(name)
        except ValueError as value_error:
            # the submodule path might not match the submodule name
            for module in self.submodules:
                if module.path == name:
                    return module
            raise value_error

    @call_log_for_class_logger
    def update_submodule(self, submodule: str, retry: bool = True, silent: bool = False) -> None:
        """Run submodule update for the given submodule"""
        try:
            submodule_git_dir = os.path.join(self.git_dir, 'modules', str(submodule))
            if os.path.isdir(submodule_git_dir):
                # update the url for the existing local repo
                self.__silent_logger__(f"Synchronizing submodule '{submodule}'", silent)
                self.git.submodule("sync", "--recursive", '--', submodule)

            self.__silent_logger__(f"Updating submodule '{submodule}'", silent)
            self.git.submodule("update", "--init", "--recursive", '--', submodule)

            self.__silent_logger__(f"Cleaning submodule '{submodule}'", silent)

            self.get_submodule(submodule).repo.git.clean("-xffd")
        except git.exc.GitError as git_error:
            if not retry:
                raise git_error

            LOGGER.debug("Retrying to update submodule '%s'", submodule)
            if os.path.isdir(submodule):
                LOGGER.debug(
                    "Removing existing submodule content in '%s'", submodule)
                shutil.rmtree(submodule)
            submodule_git_dir = os.path.join(self.git_dir, 'modules', str(submodule))
            if os.path.isdir(submodule_git_dir):
                LOGGER.debug(
                    "Removing existing submodule repository in '%s'", submodule_git_dir)
                shutil.rmtree(submodule_git_dir)
            self.update_submodule(submodule, retry=False, silent=True)

    @call_log_for_class_logger
    def update_submodules(self) -> None:
        """updates, cleans and resets all submodules"""
        LOGGER.info("Updating all submodules in repository")
        for submodule in self.submodule_list:
            self.update_submodule(submodule, silent=True)

    @call_log_for_class_logger
    def add_submodule(self, path: str, url: str, revision: str = None) -> None:
        LOGGER.info("Adding submodule '%s' with url '%s'", path, url)
        self.git.submodule("add", "--force", '--name', path, '--', url, path)
        LOGGER.debug("Initializing submodule '%s'", path)
        self.git.submodule("init", '--', path)
        self.update_submodule(path, silent=True)

        if revision:
            self.set_submodule_revision(path, revision)
        else:
            LOGGER.debug("Staging new revision for submodule '%s'", path)
            self.git.add(path)

    @call_log_for_class_logger
    def set_submodule_revision(self, submodule_path: str, revision: str) -> None:
        # setting current submodule to correct revision
        LOGGER.info("Setting submodule '%s' to revision '%s'", submodule_path, revision)
        # synchronizing submodule URLs to make sure submodule repo in .git/modules is up to date
        self.git.submodule("sync", "--recursive", '--', submodule_path)
        # fetching submodule to make sure we have needed sha
        self.get_submodule(submodule_path).module().remote().fetch(tags=True)
        self.get_submodule(submodule_path).module().head.reset(revision, index=True, working_tree=True)

        LOGGER.debug("Staging new revision for submodule '%s'", submodule_path)
        self.git.add(submodule_path)

    @call_log_for_class_logger
    def remove_all_content(self) -> None:
        """removes everything from the repository working tree (and adds the removal to the staging area)"""
        LOGGER.info("Removing all content from current sandbox")
        self.git.rm("*", force=True)
        self.git.clean("-xffd")

    @call_log_for_class_logger
    def create_tag_in_submodule(self, submodule: str, tag: str, message: str = "",
                                ref: str = "HEAD", force: bool = False) -> None:
        LOGGER.debug("Creating tag '%s' in submodule '%s' at reference '%s'", tag, submodule, submodule)
        self.get_submodule(submodule).repo.create_tag(tag, ref=ref, message=message, force=force)

    @call_log_for_class_logger
    def create_commit(self, message: str) -> str:
        """creates a new sha with teh given message"""
        self.index.commit(message, skip_hooks=True)
        LOGGER.info("Created new sha '%s' with message '%s'", self.current_commit_sha, message)

        return self.current_commit_sha

    @call_log_for_class_logger
    def push(self, ref: Union[None, str] = None, remote: str = 'origin',
             tags: bool = False, force: bool = False) -> None:
        """Push (the given reference) to the remote

        @param ref: reference to push (just running 'git push' if not provided)
        @param remote: remote to push to
        @param tags: whether to push tags
        @param force: whether to push with force
        """
        if not ref:
            self.git.push(remote, force=force, tags=tags)
            LOGGER.debug("Pushed to remote '%s'", remote)
            return

        self.git.push(remote, ref, force=force, tags=tags)
        LOGGER.debug("Pushed '%s' to remote '%s'", ref, remote)

    @call_log_for_class_logger
    def set_branch_to_ref(self, branch: str, ref: str = 'HEAD') -> None:
        """Forces the given branch to point at the given reference
        @param branch: name of branch
        @param ref: reference the branch should point at
        """
        LOGGER.debug("Moving branch '%s' at '%s'", branch, ref)
        self.create_head(branch, ref, force=True)

    @call_log_for_class_logger
    def remove_branch(self, branch: str, force: bool = False) -> None:
        """deletes a (local) branch
        @param branch: name of branch
        @param force: whether to forcefully delete the branch
        """
        LOGGER.debug("Deleting branch '%s'", branch)
        self.delete_head(branch, force=force)

    @call_log_for_class_logger
    def create_branch(self, branch: str, ref: str = 'HEAD', force: bool = False) -> None:
        """Creates a (new) branch

        @param branch: name of branch to create
        @param ref: reference to create the branch at
        @param force: whether to create the branch with force
        """
        LOGGER.debug("Creating branch '%s' at '%s'", branch, ref)
        self.create_head(branch, ref, force=force)

    @call_log_for_class_logger
    def is_ff(self, start_ref: str, end_ref: str) -> bool:
        """Checks if commit for a given reference can be reached from another one by  fast-forwarded

        @param start_ref: starting reference
        @param end_ref: end reference
        @return: bool whether the first commit is an ancestor of the second one
        """
        try:
            _ = self.git.merge_base('--is-ancestor', start_ref, end_ref)
            LOGGER.debug("'%s' is an ancestor of '%s'", start_ref, end_ref)
            return True
        except git.exc.GitCommandError:
            LOGGER.debug("'%s' is no ancestor of '%s'", start_ref, end_ref)
            return False

    @call_log_for_class_logger
    def delete_local_ref(self, ref: str) -> None:
        """Deletes a local reference

        @param ref: reference to delete (branch or tag)
        """
        try:
            self.git.tag('--delete', ref)
            LOGGER.debug("Deleted local tag '%s'", ref)
        except git.exc.GitCommandError:
            self.git.branch('-D', ref)
            LOGGER.debug("Deleted local branch '%s'", ref)

    @call_log_for_class_logger
    def delete_remote_ref(self, ref: str, remote: str = 'origin') -> None:
        """Deletes a reference on the remote

        @param ref: reference to delete (branch or tag)
        @param remote: name of the remote where to delete the reference, default is origin
        """
        self.git.push('--delete', remote, ref)
        LOGGER.debug("Deleted reference '%s' from remote '%s'", ref, remote)

    @call_log_for_class_logger
    def ls_files(self, *args, **kwargs):
        output = self.git.ls_files(args, kwargs)
        return output.splitlines()

    @call_log_for_class_logger
    def get_changed_files_of_commits(self, commit_id_1: str, commit_id_2: str) -> list:
        """Returns list changed files between two commits
        @param commit_id_1: commit hash id
        @param commit_id_2: commit hash id
        @return: List of relative path of changed files
        """
        self.remote().fetch(commit_id_1, tags=False)
        self.remote().fetch(commit_id_2, tags=False)
        diff_content = self.git.diff("--name-only", commit_id_1, commit_id_2)
        if not diff_content:
            LOGGER.info("No changed files")
            return []
        diff_files = diff_content.strip().splitlines()
        LOGGER.info("Found files: \n%s", "\n".join(diff_files))
        return diff_files

def get_repo_name_from_url(url: str) -> str:
    """Extracts the repository-name from a bitbucket ssh url
    @param url: ssh url of a bitbucket repo
    @return: repository name from the url
    """
    name = url.split("/")[-1].split(".")[-2]
    if name.endswith(".git"):
        name = name[:-4]
    return name


def get_project_from_url(url: str) -> str:
    """Extracts the project-key from a bitbucket ssh url
        @param url: ssh url of a bitbucket repo
        @return: project-key from the url
        """
    return url.split("/")[-2].upper()


def is_git_repo(path: str) -> bool:
    """Checks if a given path is a git repository or not

    @param path: path to check
    @return: bool, whether the given path is a git repository or not
    """
    try:
        _ = git.Repo(path).git_dir
        return True
    except (git.exc.InvalidGitRepositoryError, git.exc.NoSuchPathError):
        return False
