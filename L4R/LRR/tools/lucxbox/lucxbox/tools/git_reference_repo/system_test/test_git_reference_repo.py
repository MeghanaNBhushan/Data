"""
system tests for the creation and maintenance of reference repos
These are not run automatically - needs to be run manually:
pytest -m system
"""

import glob
import hashlib
import os
import random
import stat
import string
import subprocess

import pytest

import lucxbox.tools.git_reference_repo.git_reference_repo as git_reference_repo

GIT_EXECUTABLE = git_reference_repo.GIT_CMD
random.seed(192837465)


class GitDummyRepo:
    """
    creates a dummy repo with a random number of files and commits for testing purposes
    """

    def __init__(self, directory):
        if not os.path.isdir(directory):
            os.makedirs(directory)
        self.__dir = directory
        with open(os.devnull, 'w') as fnull:
            subprocess.check_call([GIT_EXECUTABLE, "init"], cwd=self.__dir, stdout=fnull)
            ## add some dummy files
            for i in range(random.randint(5, 10)):
                dummy_filename = os.path.join(self.__dir, "dummy_file_{:02d}".format(i))
                with open(dummy_filename, "wt") as dummy_git_fh:
                    dummy_git_fh.write(
                        ''.join([random.choice(string.printable) for _ in range(random.randint(20, 20000))]))
                # add
                subprocess.check_call([GIT_EXECUTABLE, "add", os.path.basename(dummy_filename)],
                                      cwd=self.__dir, stdout=fnull)
                # commit
                subprocess.check_call([GIT_EXECUTABLE, "commit", "-m", "dummy commit {}".format(i)],
                                      cwd=self.__dir, stdout=fnull,
                                      env={"GIT_AUTHOR_NAME": "pytest",
                                           "GIT_AUTHOR_EMAIL": "none@nowhere.org",
                                           "GIT_COMMITTER_NAME": "pytest",
                                           "GIT_COMMITTER_EMAIL": "none@nowhere.org"})

    @property
    def url(self):
        return "file://" + self.path

    @property
    def path(self):
        return os.path.join(self.__dir, ".git")

    def add_submodule(self, name, url):
        subprocess.check_call([GIT_EXECUTABLE, "submodule", "add", url, name], cwd=self.__dir)
        subprocess.check_call([GIT_EXECUTABLE, "commit", "-m", "added dummy submodule"], cwd=self.__dir,
                              env={"GIT_AUTHOR_NAME": "pytest",
                                   "GIT_AUTHOR_EMAIL": "none@nowhere.org",
                                   "GIT_COMMITTER_NAME": "pytest",
                                   "GIT_COMMITTER_EMAIL": "none@nowhere.org"})


def get_count_objects(repo_path):
    co_str = subprocess.check_output([GIT_EXECUTABLE, "count-objects", "-v"], cwd=repo_path)
    partitioned_lines = (line.partition(':') for line in co_str.decode('utf-8').splitlines())
    return {p[0].strip(): p[2].strip() for p in partitioned_lines}


@pytest.mark.system
def test_no_submodules(tmpdir_factory):
    """
    Test for cloning a repo with a references repo
    - a dummy repo is created
    - a reference repo is created from that dummy
    - a clone of the dummy repo is created using the reference repo
    - check that the "alternate" pointer exists and points to the
        reference repo
    """
    src_repo_dir = tmpdir_factory.mktemp("src").strpath
    ref_repo_dir = tmpdir_factory.mktemp("ref").strpath
    clone_repo_dir = tmpdir_factory.mktemp("clone").strpath
    with open(os.devnull, "w") as fnull:
        src_repo = GitDummyRepo(os.path.join(src_repo_dir, "a"))
        ref_repo = git_reference_repo.Refrepo(ref_repo_dir, src_repo.url, free_storage_new=2, free_storage_update=2)
        ref_repo.update()
        subprocess.check_call([GIT_EXECUTABLE, "clone", "--reference", ref_repo.path, src_repo.url],
                              cwd=clone_repo_dir, stdout=fnull)
        src_kv = get_count_objects(src_repo.path)
        ref_kv = get_count_objects(ref_repo.path)
        clone_kv = get_count_objects(os.path.join(clone_repo_dir, "a"))

        ## check if the alternate pointer exists and points to the reference repo
        assert os.path.normpath(clone_kv["alternate"]) == os.path.join(ref_repo.path, "objects"), \
            "The alternate pointer of the clone is invalid"
        ## the ref repo should have the same number of objects as the source repo
        assert src_kv["count"] == ref_kv["in-pack"], \
            "the number of objects in source repo ({}) and reference repo ({}) differs".format(src_kv["count"],
                                                                                               ref_kv["in-pack"])
        ## the clone repo should have no objects, there is no delta to the refrepo at this point
        assert clone_kv["in-pack"] == '0', \
            "The clone has {} objects in-pack but should have no delta to reference repo".format(clone_kv["in-pack"])
        assert clone_kv["count"] == '0', \
            "The clone has {} object counts but should have no delta to reference repo".format(clone_kv["count"])
        ## check if the clone actually has some files in the checkout
        assert os.path.isfile(os.path.join(clone_repo_dir, "a", "dummy_file_00"))


@pytest.mark.skipif('JENKINS_URL' in os.environ, reason='Skipped on Jenkins, because an SSH private key would have to be provided.')
@pytest.mark.system
def test_lucxbox_refrepo(tmpdir_factory):
    """
    test with a real bitbucket repo. Access should work because we somehow got this test.
    """
    ref_repo_dir = tmpdir_factory.mktemp("ref").strpath
    clone_repo_dir = tmpdir_factory.mktemp("clone").strpath
    with open(os.devnull, "w") as fnull:
        src_repo_url = "ssh://git@sourcecode.socialcoding.bosch.com:7999/lucx/lucxbox.git"
        ref_repo = git_reference_repo.Refrepo(ref_repo_dir, src_repo_url, free_storage_new=20, free_storage_update=20)
        ref_repo.update()
        subprocess.check_call([GIT_EXECUTABLE, "clone", "--reference", ref_repo.path, src_repo_url],
                              cwd=clone_repo_dir, stdout=fnull)
        co_kv = get_count_objects(os.path.join(clone_repo_dir, "lucxbox"))
        ## check if the alternate pointer exists and points to the reference repo
        assert os.path.normpath(co_kv["alternate"]) == os.path.join(ref_repo.path, "objects"), \
            "The alternate pointer of the clone is invalid"
        rf_kv = get_count_objects(ref_repo.path)
        ## check if the clone actually has fewer objects
        assert co_kv["size-pack"] < rf_kv["size-pack"], \
            "The clone doesn't have fewer size-packs than the reference repo"


@pytest.mark.system
def test_with_submodules(tmpdir_factory):
    """
    Test for cloning a repo with submodules using a reference repo
        a  <- main repo
        |
        +--b (sm0) <- submodule
        |
        +--c (sm1) <- submodule
        |
        +--d (sm2) <- submodule

    - a dummy repo is created
    - several other repos are created and added as submodule to the dummy repo
    - a reference repo is created from the dummy repo
    - a clone is made from the dummy repo using the reference repository
    - check that the clone and all submodules have the alternate pointer and that
        it points to the reference repo
    """
    src_repo_dir = tmpdir_factory.mktemp("src").strpath
    ref_repo_dir = tmpdir_factory.mktemp("ref").strpath
    clone_repo_dir = tmpdir_factory.mktemp("clone").strpath
    with open(os.devnull, "w") as fnull:
        # set up the test repos
        src_repo = GitDummyRepo(os.path.join(src_repo_dir, "a"))
        submodules = [GitDummyRepo(os.path.join(src_repo_dir, x)) for x in ["b", "c", "d"]]
        for sm_num, submodule in enumerate(submodules):
            src_repo.add_submodule("sm{}".format(sm_num), submodule.url)
        # create the reference repos
        ref_repo = git_reference_repo.Refrepo(ref_repo_dir, src_repo.url, free_storage_new=2, free_storage_update=2)
        ref_repo.update()
        # create the clone
        subprocess.check_call([GIT_EXECUTABLE, "clone", "--reference", ref_repo.path, src_repo.url],
                              cwd=clone_repo_dir, stdout=fnull)
        clone_git_dir = os.path.join(clone_repo_dir, "a")
        subprocess.check_call([GIT_EXECUTABLE, "submodule", "init"],
                              cwd=clone_git_dir, stdout=fnull)
        subprocess.check_call([GIT_EXECUTABLE, "submodule", "update", "--reference", ref_repo.path],
                              cwd=clone_git_dir, stdout=fnull)

        # run the checks
        clone_kv = get_count_objects(clone_git_dir)
        assert os.path.normpath(clone_kv["alternate"]) == os.path.join(ref_repo.path, "objects"), \
            "The alternate pointer of the clone is invalid"
        assert clone_kv["in-pack"] == '0', \
            "The clone has {} objects in-pack but should have no delta to reference repo".format(clone_kv["in-pack"])
        assert clone_kv["count"] == '0', \
            "The clone has {} object counts but should have no delta to reference repo".format(clone_kv["count"])
        ## check if the clone actually has some files in the checkout
        assert os.path.isfile(os.path.join(clone_repo_dir, "a", "dummy_file_00"))
        for sm_num in range(len(submodules)):
            # submodules
            sm_kv = get_count_objects(os.path.join(clone_git_dir, "sm{}".format(sm_num)))
            assert os.path.normpath(clone_kv["alternate"]) == os.path.join(ref_repo.path, "objects"), \
                "The alternate pointer of the clone is invalid"
            assert sm_kv["in-pack"] == '0', \
                "The submodule clone has {} objects in-pack but ".format(sm_kv["in-pack"]) + \
                "should have no delta to reference repo"
            assert sm_kv["count"] == '0', \
                "The submodule clone has {} object counts but ".format(sm_kv["count"]) + \
                "should have no delta to reference repo"
            ## check if the clone actually has some files in the checkout
            assert os.path.isfile(os.path.join(clone_repo_dir, "a", "sm{}".format(sm_num), "dummy_file_00"))


@pytest.mark.system
def test_with_recursive_submodules(tmpdir_factory):
    """
    Test for cloning a repo with submodules of submodules using a reference repo
        a  <- main repo
        |
        +--b (sm_b) <- submodule
        |  |
        |  +--c (sm_c) <- submodule of submodule
        |  |
        |  +--d (sm_d) <- submodule of submodule
        |
        +--e (sm_e) <- submodule

    - check that the clone and all submodules have the alternate pointer and that
        it points to the reference repo
    """
    src_repo_dir = tmpdir_factory.mktemp("src").strpath
    ref_repo_dir = tmpdir_factory.mktemp("ref").strpath
    clone_repo_dir = tmpdir_factory.mktemp("clone").strpath
    with open(os.devnull, "w") as fnull:
        # setup of the source repos
        repo = {x: GitDummyRepo(os.path.join(src_repo_dir, x)) for x in ["a", "b", "c", "d", "e"]}
        repo["b"].add_submodule("sm_c", repo["c"].url)
        repo["b"].add_submodule("sm_d", repo["d"].url)
        repo["a"].add_submodule("sm_b", repo["b"].url)
        repo["a"].add_submodule("sm_e", repo["e"].url)
        # create reference repo
        ref_repo = git_reference_repo.Refrepo(ref_repo_dir, repo["a"].url, free_storage_new=2, free_storage_update=2)
        ref_repo.update()
        # create the clone
        subprocess.check_call([GIT_EXECUTABLE, "clone", "--reference", ref_repo.path, repo["a"].url],
                              cwd=clone_repo_dir, stdout=fnull)
        clone_git_dir = os.path.join(clone_repo_dir, "a")
        subprocess.check_call([GIT_EXECUTABLE, "submodule", "init"],
                              cwd=clone_git_dir, stdout=fnull)
        subprocess.check_call([GIT_EXECUTABLE, "submodule", "update", "--reference", ref_repo.path],
                              cwd=clone_git_dir, stdout=fnull)
        subprocess.check_call([GIT_EXECUTABLE, "submodule", "init"],
                              cwd=os.path.join(clone_git_dir, "sm_b"), stdout=fnull)
        subprocess.check_call([GIT_EXECUTABLE, "submodule", "update", "--reference", ref_repo.path],
                              cwd=os.path.join(clone_git_dir, "sm_b"), stdout=fnull)

        # base repo
        clone_kv = get_count_objects(clone_git_dir)
        assert os.path.normpath(clone_kv["alternate"]) == os.path.join(ref_repo.path, "objects"), \
            "The alternate pointer of the clone is invalid"
        assert clone_kv["in-pack"] == '0', \
            "The clone has {} objects in-pack but should have no delta to reference repo".format(clone_kv["in-pack"])
        assert clone_kv["count"] == '0', \
            "The clone has {} object counts but should have no delta to reference repo".format(clone_kv["count"])
        ## check if the clone actually has some files in the checkout
        assert os.path.isfile(os.path.join(clone_repo_dir, "a", "dummy_file_00"))
        # submodule b + e
        for subm in ["sm_b", "sm_e"]:
            sm_kv = get_count_objects(os.path.join(clone_git_dir, subm))
            assert os.path.normpath(sm_kv["alternate"]) == os.path.join(ref_repo.path, "objects"), \
                "The alternate pointer of the submodule clone is invalid"
            assert sm_kv["in-pack"] == '0', \
                "The submodule clone has {} objects in-pack but ".format(sm_kv["in-pack"]) + \
                "should have no delta to reference repo"
            assert sm_kv["count"] == '0', \
                "The submodule clone has {} object counts but ".format(sm_kv["count"]) + \
                "should have no delta to reference repo"
            ## check if the clone actually has some files in the checkout
            assert os.path.isfile(os.path.join(clone_repo_dir, "a", subm, "dummy_file_00"))

        # sub-submodule c + d
        for ssm in ["sm_c", "sm_d"]:
            ssm_kv = get_count_objects(os.path.join(clone_git_dir, "sm_b", ssm))
            assert os.path.normpath(ssm_kv["alternate"]) == os.path.join(ref_repo.path, "objects"), \
                "The alternate pointer of the sub-submodule clone is invalid"
            assert ssm_kv["in-pack"] == '0', \
                "The sub-submodule clone has {} objects in-pack but ".format(ssm_kv["in-pack"]) + \
                "should have no delta to reference repo"
            assert ssm_kv["count"] == '0', \
                "The sub-subclone has {} object counts but ".format(ssm_kv["count"]) + \
                "should have no delta to reference repo"
            ## check if the clone actually has some files in the checkout
            assert os.path.isfile(os.path.join(clone_repo_dir, "a", "sm_b", ssm, "dummy_file_00"))


@pytest.mark.system
def test_with_submodule_url_change(tmpdir_factory):
    """
    Test for cloning a repo with submodule which changes the url
        a  <- main repo
        |
        +--b (sm0) <- submodule
    """
    src_repo_dir = tmpdir_factory.mktemp("src").strpath
    ref_repo_dir = tmpdir_factory.mktemp("ref").strpath
    with open(os.devnull, "w") as fnull:
        # set up the test repos
        src_repo = GitDummyRepo(os.path.join(src_repo_dir, "a"))
        submodule_orig = GitDummyRepo(os.path.join(src_repo_dir, "b_orig"))
        submodule_newurl = GitDummyRepo(os.path.join(src_repo_dir, "b_new"))
        src_repo.add_submodule("sm0", submodule_orig.url)
        # create the reference repos
        ref_repo = git_reference_repo.Refrepo(ref_repo_dir, src_repo.url, free_storage_new=2, free_storage_update=2)
        ref_repo.update()
        # change the url of sm0
        subprocess.check_call([GIT_EXECUTABLE, "config", "--file=.gitmodules",
                               "submodule.sm0.url", submodule_newurl.url],
                              cwd=src_repo.path + "/..", stdout=fnull)
        subprocess.check_call([GIT_EXECUTABLE, "config", "--file=.gitmodules",
                               "submodule.sm0.branch", "master"],
                              cwd=src_repo.path + "/..", stdout=fnull)
        subprocess.check_call([GIT_EXECUTABLE, "submodule", "sync"],
                              cwd=src_repo.path + "/..", stdout=fnull)
        subprocess.check_call([GIT_EXECUTABLE, "submodule", "update", "--init", "--remote"],
                              cwd=src_repo.path + "/..", stdout=fnull)
        subprocess.check_call([GIT_EXECUTABLE, "add", ".gitmodules", "sm0"],
                              cwd=src_repo.path + "/..")
        subprocess.check_call([GIT_EXECUTABLE, "commit", "-m", "submodule sm0 got a new url"],
                              cwd=src_repo.path + "/..",
                              env={"GIT_AUTHOR_NAME": "pytest",
                                   "GIT_AUTHOR_EMAIL": "none@nowhere.org",
                                   "GIT_COMMITTER_NAME": "pytest",
                                   "GIT_COMMITTER_EMAIL": "none@nowhere.org"})
        # update the reference repo
        ref_repo.update()
        # check if the new URL is a remote of the reference repo
        ref_remotes_str = subprocess.check_output([GIT_EXECUTABLE, "remote", "-v"],
                                                  cwd=ref_repo.path).decode("utf-8")
        ref_remotes = [os.path.normpath(line.split("\t")[1].split(" ")[0]) for line in ref_remotes_str.splitlines()]
        assert os.path.normpath(submodule_newurl.url) in ref_remotes


@pytest.mark.system
def test_insufficient_space_new(tmpdir_factory):
    """
    Test for cloning a repo with a references repo
    - a dummy repo is created
    - we try to create a reference repo but require too much space
    - check that an exception is raised
    """
    src_repo_dir = tmpdir_factory.mktemp("src").strpath
    ref_repo_dir = tmpdir_factory.mktemp("ref").strpath
    src_repo = GitDummyRepo(os.path.join(src_repo_dir, "a"))
    ref_repo = git_reference_repo.Refrepo(ref_repo_dir, src_repo.url, free_storage_new=10 ** 30)
    with pytest.raises(IOError):
        ref_repo.update()


@pytest.mark.system
def test_insufficient_space_update(tmpdir_factory):
    """
    Test for cloning a repo with a references repo
    - a dummy repo is created
    - create a reference repo
    - update the reference repo but require too much space
    - check that an exception is raised
    """
    src_repo_dir = tmpdir_factory.mktemp("src").strpath
    ref_repo_dir = tmpdir_factory.mktemp("ref").strpath
    src_repo = GitDummyRepo(os.path.join(src_repo_dir, "a"))
    ref_repo = git_reference_repo.Refrepo(ref_repo_dir, src_repo.url, free_storage_new=1, free_storage_update=10 ** 30)
    ref_repo.update()
    with pytest.raises(IOError):
        ref_repo.update()


@pytest.mark.system
def test_refrepo_corruption(tmpdir_factory):
    """
    Test if the script can recover corruption of the reference repo
    - a dummy repo is created
    - create a reference repo
    - modify the object storage
    - check that the object has been restored after a refrepo update
    """
    src_repo_dir = tmpdir_factory.mktemp("src").strpath
    ref_repo_dir = tmpdir_factory.mktemp("ref").strpath
    src_repo = GitDummyRepo(os.path.join(src_repo_dir, "a"))
    ref_repo = git_reference_repo.Refrepo(ref_repo_dir, src_repo.url, free_storage_new=1, free_storage_update=1)
    ref_repo.update()
    # find a file from the object storage ..
    packfilename = glob.glob(os.path.join(ref_repo.path, "objects", "pack", "*.pack"))[0]
    # .. remember a hash from it ..
    with open(packfilename, "rb") as packfile:
        hash_orig = hashlib.md5(packfile.read()).hexdigest()
    orig_stat = os.stat(packfilename)
    os.chmod(packfilename, orig_stat.st_mode | stat.S_IWRITE)
    # .. corrupt it ..
    with open(packfilename, "ab") as packfile:
        packfile.seek(10)
        packfile.write(b'corrupt')
    os.chmod(packfilename, orig_stat.st_mode)
    # .. recover it ..
    ref_repo.update()
    with open(packfilename, "rb") as packfile:
        hash_recovered = hashlib.md5(packfile.read()).hexdigest()
    assert hash_orig == hash_recovered, "Didn't recover from repository corruption"
