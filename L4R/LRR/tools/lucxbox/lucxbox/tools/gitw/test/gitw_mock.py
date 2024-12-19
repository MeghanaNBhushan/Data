from typing import List


class PushError(Exception):
    pass


class Repo(): # pylint: disable=too-many-instance-attributes
    class Git():
        def __init__(self, ):
            self.added = []

        def add(self, *args):
            self.added.extend(args)

    def __init__(self, path="."):
        self.added_submodules = []
        self.git = self.Git()
        self.path = path
        self.ref_exists_result: List[bool] = []
        self.ref_exists_on_remote_result: List[bool] = []
        self.tag_exists_result: List[bool] = []
        self.branch_exists_result: List[bool] = []
        self.remote_branch_exists_result: List[bool] = []
        self.ref_to_push_exists_result: List[bool] = []
        self.is_ff_result: List[bool] = []

        self.submodule_list: List[str] = []
        self.ls_files_list: List[str] = []

        self.ref_to_push_exists: bool = False

        self.is_dirty_result: bool = False
        self.url: str = "ssh://git@sourcecode01.de.bosch.com:7999/project/repo_name.git"
        self.project: str = 'project'
        self.repo_name: str = 'repo_name'
        self.current_commit_sha: str = ''

    def ref_exists(self):
        return self.ref_exists_result.pop()

    def tag_exists(self):
        return self.tag_exists_result.pop()

    def branch_exists(self):
        return self.branch_exists_result.pop()

    def setup_logger(self, *args, **kwargs):
        pass

    def fetch(self, *args, **kwargs):
        pass

    def checkout(self, *args, **kwargs):
        pass

    def remove_all_content(self, *args, **kwargs):
        pass

    @classmethod
    def create_commit(cls):
        return "nEwCoMiT"

    def create_tag(self, *args, **kwargs):
        pass

    def is_dirty(self):
        return self.is_dirty_result

    @classmethod
    def get_commit_sha(cls):
        return "commit-sha"

    def remote_branch_exists(self):
        return self.remote_branch_exists_result.pop()

    def set_branch_to_ref(self, *args, **kwargs):
        pass

    def is_ff(self, *args, **kwargs):
        pass

    def ref_exists_on_remote(self):
        return self.ref_exists_on_remote_result.pop()

    def push(self, **kwargs):
        ref_exists = self.ref_to_push_exists_result.pop()
        if ref_exists and not kwargs['force']:
            raise PushError

    def ls_files(self, pattern):
        return [file for file in self.ls_files_list if file.startswith(pattern)]

    @classmethod
    def get_submodule_url(cls, submodule_path: str):
        return "ssh://" + submodule_path + ".git"

    @classmethod
    def get_submodule_sha(cls, submodule_path: str):
        return "commit-sha-" + submodule_path

    def add_submodule(self, path: str, url: str, revision: str):
        self.added_submodules.append(f"{path}__{url}__{revision}")
