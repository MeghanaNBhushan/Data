import os
import sys
import shutil
import json
import zipfile

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog
from lucxbox.lib import portal
from lucxbox.lib import lucxutils


LOGGER = lucxlog.get_logger()


def read_json(json_file):
    """Reading the given json_file path and returns the parsed object"""
    LOGGER.debug("Reading json file '%s'", json_file)
    with open(json_file, 'r') as source_file:
        return json.load(source_file)


def write_json(json_file, data):
    LOGGER.debug("Writing json file '%s'", json_file)
    with open(json_file, 'w') as destination_file:
        json.dump(data, destination_file, indent=4)


def git_available():
    try:
        lucxutils.execute('git --version', shell=True)
        return True
    except FileNotFoundError:
        return False


def git_fetch_ref(root, ref):
    if ref == 'HEAD':
        LOGGER.debug("Ref is 'HEAD', not fetching origin")
        return
    cmd = 'git fetch --recurse-submodules=no origin ' + ref
    with portal.In(root):
        _, err, returncode = lucxutils.execute(cmd, shell=True)
    if returncode != 0:
        LOGGER.error('\n%s', err)
        sys.exit(1)


def delete_path(path):
    LOGGER.debug("Deleting path '%s'", path)
    if os.path.isdir(path):
        LOGGER.debug("Path '%s' is a directory", path)
        shutil.rmtree(path)
    elif os.path.isfile(path):
        LOGGER.debug("Path '%s' is a file", path)
        os.remove(path)


def git_checkout(root, paths, revision):
    paths = ' '.join(paths)
    cmd = "git checkout --force {} -- {}".format(revision, paths)
    with portal.In(root):
        _, err, returncode = lucxutils.execute(cmd, shell=True)
    if returncode != 0:
        LOGGER.error('\n%s', err)
        sys.exit(1)


def git_reset(root, path, revision):
    cmd = "git reset {} {}".format(revision, path)
    with portal.In(root):
        _, err, returncode = lucxutils.execute(cmd, shell=True)
        if returncode != 0:
            LOGGER.error('\n%s', err)
            sys.exit(1)


def git_apply_diff(root, paths, base, target):
    paths = ' '.join(paths)
    patch_file = "{}_to_{}.patch".format(base[:6], target[:6])
    cmd_create_patch = "git diff {}..{} -- {}".format(base, target, paths)
    cmd_apply = "git apply -3 {}".format(patch_file)

    with portal.In(root):
        LOGGER.info("Creating patch file '%s'", os.path.abspath(patch_file))
        with open(patch_file, 'w') as patch_file_stream:
            _, err, returncode = lucxutils.execute(cmd_create_patch, stdout=patch_file_stream, shell=True)
        if returncode != 0:
            LOGGER.error('\n%s', err)
            return 1

        LOGGER.info("Applying patch '%s'", os.path.abspath(patch_file))
        _, err, returncode = lucxutils.execute(cmd_apply, shell=True)
        if returncode != 0:
            LOGGER.error("Patching not successfull. Might have conflicts to solve")
            LOGGER.error('\n%s', err)
            return 1
        os.remove(patch_file)
    return 0


def get_commits_of_file(reference, root, file, local):
    log_ref = 'origin/' + reference
    if local:
        log_ref = reference
    if reference == 'HEAD':
        log_ref = 'HEAD'
    LOGGER.debug("Getting changed commits of file '%s' in '%s'", file, root)
    cmd = 'git log --pretty=format:"%h" --abbrev=40 {} -- {}'.format(log_ref, file)
    with portal.In(root):
        out, err, returncode = lucxutils.execute(cmd, shell=True)
    if returncode != 0:
        LOGGER.error('\n%s', err)
        sys.exit(1)
    commits = out.split('\n')
    return commits


def get_version_from_commit(root, file, commit, version_type):
    cmd = 'git diff "{commit}^..{commit}" -- {file}'.format(commit=commit, file=file)
    with portal.In(root):
        out, err, returncode = lucxutils.execute(cmd, shell=True)
        if returncode != 0:
            LOGGER.warning('\n%s', err)
            LOGGER.warning("Diff failed, might be the first repository commit")
            # The hardcoded commit is the magic git root commit of every repository
            cmd = "git diff {}..{} -- {}".format('4b825dc642cb6eb9a060e54bf8d69288fbee4904', commit, file)
            out, err, returncode = lucxutils.execute(cmd, shell=True)
            if returncode != 0:
                LOGGER.error('\n%s', err)
                sys.exit(1)
    lines = out.split('\n')
    for line in lines:
        if '+' in line:
            version_id = version_type + '_name'
            if version_id in line:
                return line.split('"')[-2]
    return None


def get_versions_from_commits(root, file, commits, version_type):
    LOGGER.debug("Getting versions (%s) from commits %s", version_type, tuple(commits))
    versions = []
    for commit in commits:
        versions.append(get_version_from_commit(root, file, commit, version_type))
        LOGGER.debug("Found new version '%s'", versions[-1])
    return versions


def get_git_ls_files(root, ls_files_args):
    if not git_available():
        LOGGER.debug("Git not available in PATH. Returned ignore files will be empty!")
        return []
    cmd = 'git ls-files ' + ls_files_args
    with portal.In(root):
        out, err, returncode = lucxutils.execute(cmd, shell=True)
    ls_files = []
    if returncode != 0:
        LOGGER.debug("%s failed", cmd)
        LOGGER.debug("Stderr:\n%s", err)
        LOGGER.debug("Returned files will be empty!")
        return ls_files
    ls_files_relative = out.split()
    for ls_file_relative in ls_files_relative:
        ls_files.append(os.path.join(root, ls_file_relative.strip()))
        LOGGER.debug("Added git ls-file file '%s'", ls_files[-1])
    return ls_files


def get_versions_and_commits(reference, root, package_file_name, version_type, local):
    commits = get_commits_of_file(reference, root, package_file_name, local)
    versions = get_versions_from_commits(root, package_file_name, commits, version_type)
    mapping = {}
    for i, version in enumerate(versions):
        if not version:
            LOGGER.debug("Commit '%s' has changed package file but not the version", commits[i])
            continue
        if version in mapping:
            LOGGER.warning("Version has been changed in more than one commit!")
            continue
        mapping[version] = commits[i]
    return mapping


def get_git_root():
    if not git_available():
        LOGGER.warning("git not available - cannot determine git root")
        return None
    git_root, _, returncode = lucxutils.execute('git rev-parse --show-toplevel', shell=True)
    if returncode == 0:
        return git_root.strip()
    return None


def get_repository_revision(path):
    LOGGER.debug("Getting working tree revision in '%s'", path)
    with portal.In(path):
        cmd = "git rev-parse HEAD"
        cmd_out, err, returncode = lucxutils.execute(cmd, shell=True)
        if returncode != 0:
            LOGGER.error(cmd)
            LOGGER.error(err)
            sys.exit(1)
        revision = cmd_out.strip()
        cmd = "git diff-files --quiet"
        _, _, returncode = lucxutils.execute(cmd, shell=True)
        if returncode:
            revision += "-dirty"
        return revision


def get_submodules(path):
    submodules = []
    git_root = get_git_root()
    if not git_root:
        return submodules
    with portal.In(git_root):
        if not os.path.exists('.gitmodules'):
            return submodules
        cmd = 'git config --file .gitmodules --name-only --get-regexp path'
        cmd_out, err, returncode = lucxutils.execute(cmd, shell=True)
        if returncode != 0:
            LOGGER.error(cmd)
            LOGGER.error(err)
            return submodules
        submodule_lines = cmd_out.split('\n')
        for submodule_line in submodule_lines:
            if not submodule_line.strip():
                continue
            LOGGER.debug("Gitmodule entry '%s'", submodule_line)
            submodule_path = submodule_line.split('.')[1]
            submodule_path = os.path.abspath(os.path.join(git_root, submodule_path))
            if submodule_path.startswith(os.path.abspath(path)):
                submodules.append(submodule_path)
                LOGGER.debug("Adding submodule '%s'", submodules[-1])
            else:
                LOGGER.debug("Submodule '%s' not below '%s'", submodule_path, path)
    return submodules


def filter_submodule_packages(package_files, submodules):
    filtered_package_files = []
    for package_file in package_files:
        package_file_abs = os.path.abspath(package_file)
        in_submodule = None
        for submodule in submodules:
            if package_file_abs.startswith(submodule):
                in_submodule = submodule
        if in_submodule:
            LOGGER.debug("Filtered '%s' (submodule '%s')", package_file, in_submodule)
        else:
            filtered_package_files.append(package_file)
    return filtered_package_files


def clone_repository(clone, url):
    working_dir = os.path.normpath(os.path.join(clone, ".."))
    if not os.path.isdir(working_dir):
        os.makedirs(working_dir, exist_ok=True)
    repository_name = os.path.basename(clone)
    cmd = "git clone --no-checkout {0} {1}".format(url, repository_name)
    with portal.In(working_dir):
        _, err, returncode = lucxutils.execute(cmd, shell=True)
    if returncode != 0:
        LOGGER.error('\n%s', err)
        sys.exit(1)


def fetch_repository(working_dir, ref):
    cmd = "git fetch --tags --prune --prune-tags --no-recurse-submodules origin {0}".format(ref)
    with portal.In(working_dir):
        _, err, returncode = lucxutils.execute(cmd, shell=True)
    if returncode != 0:
        LOGGER.error('\n%s', err)
        sys.exit(1)


def clean_repository(working_dir):
    cmd = "git clean -xffd"
    with portal.In(working_dir):
        _, err, returncode = lucxutils.execute(cmd, shell=True)
    if returncode != 0:
        LOGGER.error('\n%s', err)
        sys.exit(1)


def archive_package_files(working_dir, archive_name, ref, include_path):
    cmd = "git archive --format=zip --output={0}.zip {1} {2}".format(archive_name, ref, include_path)
    with portal.In(working_dir):
        _, err, returncode = lucxutils.execute(cmd, shell=True)
    if returncode != 0:
        LOGGER.error('\n%s', err)
        sys.exit(1)


def extract_archive(archive_path, extract_path):
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    os.remove(archive_path)


def move_files(source_dir, target_dir, offset):
    offset_path = os.path.join(source_dir, offset)
    for (dirpath, _, filenames) in os.walk(offset_path):
        for filename in filenames:
            source_file_path = os.path.join(dirpath, filename)
            rel_file_path = os.path.relpath(source_file_path, offset_path)
            if '.git' + os.sep in rel_file_path:
                continue
            target_file_path = os.path.join(target_dir, rel_file_path)
            target_file_dir = os.path.dirname(target_file_path)
            if not os.path.isdir(target_file_dir):
                os.makedirs(target_file_dir)
            shutil.move(source_file_path, target_file_path)
