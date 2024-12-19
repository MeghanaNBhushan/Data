""" Package Class """

import sys
import os
import datetime
import fnmatch
import hashlib
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog
from lucxbox.lib import lucxutils
from lucxbox.lib import finder
from lucxbox.lib import portal

from lucxbox.lib.lucxprint import Printer, Status
from lucxbox.lib.color_string import Color

from lucxbox.tools.packages.helper import get_git_ls_files
from lucxbox.tools.packages.helper import filter_submodule_packages
from lucxbox.tools.packages.helper import get_submodules
from lucxbox.tools.packages.helper import read_json, write_json
from lucxbox.tools.packages.helper import git_checkout, git_available, git_reset
from lucxbox.tools.packages.helper import git_fetch_ref
from lucxbox.tools.packages.helper import get_versions_and_commits
from lucxbox.tools.packages.helper import get_repository_revision


LOGGER = lucxlog.get_logger()


class InvalidPackageException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def get_packages(root, package_file_name, time_based=False, packages_filter=None, type_filter=None, init_type="status"):
    with portal.In(root):
        package_files = finder.get_files_with_ending(
            [package_file_name], ['.git'])
        package_files = filter_submodule_packages(package_files, get_submodules(root))
        LOGGER.debug("Found '%d' package files with name '%s' in '%s'", len(
            package_files), package_file_name, root)
    packages = []
    for package_file in package_files:
        new_package = None
        if packages_filter:
            if fnmatch.fnmatch(read_json(os.path.join(root, package_file))['name'], packages_filter):
                try:
                    new_package = Package(root, package_file, time_based, init_type)
                except InvalidPackageException:
                    pass
        else:
            try:
                new_package = Package(root, package_file, time_based, init_type)
            except InvalidPackageException:
                pass
        if new_package:
            if not type_filter:
                packages.append(new_package)
            else:
                if type_filter in new_package.get_types():
                    packages.append(new_package)
                else:
                    LOGGER.debug("Package %s was filtered by type", new_package.get_name())
    if not packages:
        LOGGER.error("No packages found")
        sys.exit(1)
    return packages

def get_hash_version_from_md5(md5):
    """Gets the version from an md5 hash.
    The version can be specified by appending "::VN" to the hash
    """
    split = md5.split('::')
    if len(split) == 1:
        return 1
    version = int(split[1].replace('V', ''))
    return version

def add_hash_calc_version(md5, version):
    if version == 1:
        return md5
    return f"{md5}::V{version}"

# pylint: disable=too-many-instance-attributes, too-many-public-methods
class Package:
    """ Package Class """

    # pylint: disable=too-many-branches, too-many-locals, too-many-statements
    def __init__(self, root, package_file, time_based=False, init_type="status"):
        LOGGER.debug("Creating new package from file '%s'", package_file)
        self._root_abs = os.path.dirname(os.path.abspath(os.path.join(root, package_file)))
        self._pf = os.path.basename(package_file)
        self._pf_abs = os.path.join(self._root_abs, self._pf)
        self._pf_data = read_json(self._pf_abs)
        self._versions = {}
        self._data_entry = 'semantic'
        if time_based:
            self._data_entry = 'time_based'

        self._hash_dirs = [self._root_abs]
        if "directories" in self._pf_data:
            LOGGER.debug("Directories given in package file")
            self._hash_dirs = []
            for directory in self._pf_data['directories']:
                self._hash_dirs.append(os.path.abspath(os.path.join(self._root_abs, directory)))
        self._exclude_dirs = []
        if "directories_exclude" in self._pf_data:
            for exclude_dir in self._pf_data['directories_exclude']:
                self._exclude_dirs.append(os.path.abspath(os.path.join(self._root_abs, exclude_dir)))

        self._exclude_file_ext = [self._pf]
        if "file_extensions_exclude" in self._pf_data:
            for file_ext_exclude in self._pf_data['file_extensions_exclude']:
                self._exclude_file_ext.append(file_ext_exclude)

        self._files = []
        if "files" in self._pf_data:
            for additional_files in self._pf_data['files']:
                self._files.append(os.path.abspath(os.path.join(self._root_abs, additional_files)))

        self._types = []
        if "types" in self._pf_data:
            self._types = self._pf_data['types']

        self._remote = {}
        self._remote_url = None
        self._remote_clone = None
        self._remote_path = None
        self._remote_includes = None
        if "remote" in self._pf_data:
            self._remote = self._pf_data['remote']
            self._remote_url = self._remote['url']
            self._remote_clone = self._remote['clone']
            self._remote_path = self._remote['path']
            self._remote_includes = self._remote['includes']

        self._sync = {}
        self._sync_git_ref = None
        self._sync_md5 = None
        if "sync" in self._pf_data:
            self._sync = self._pf_data['sync']
            self._sync_git_ref = self._sync['git_ref']
            self._sync_md5 = self._sync['md5']

        self._pf_name = self._pf_data['name']
        self._pf_version = self._pf_data['version'][self._data_entry + '_name']
        self._pf_md5 = self._pf_data['version'][self._data_entry + '_md5']
        self._pf_md5_version = get_hash_version_from_md5(self._pf_md5)

        if init_type == "status":
            self._hash_calc_version = self._pf_md5_version
        elif init_type == "update":
            self._hash_calc_version = 2
        else:
            LOGGER.error("Unsupported package init type: %s", init_type)
            sys.exit(1)

        LOGGER.debug("Hash Calculation Version: %d", self._hash_calc_version)

        self._only_tracked_files = None
        self._exclude_files = []
        submodules = get_submodules(self._root_abs)

        self._submodules = {}

        for hash_dir in self._hash_dirs:
            for submodule in submodules:
                if submodule.startswith(hash_dir) and submodule not in self._exclude_dirs:
                    self._submodules[os.path.relpath(submodule, self._root_abs)] = get_repository_revision(submodule)
                    if self._hash_calc_version > 1:
                        self._exclude_dirs.append(submodule)

        self._md5 = self.calculate_md5()
        self._md5 = add_hash_calc_version(self._md5, self._hash_calc_version)
        LOGGER.debug("Root:               '%s'", self._root_abs)
        LOGGER.debug("Name:               '%s'", self._pf_name)
        LOGGER.debug("Version:            '%s'", self._pf_version)
        LOGGER.debug("Hash-Calc Version:  '%d'", self._hash_calc_version)
        LOGGER.debug("MD5 (Package File): '%s'", self._pf_md5)
        LOGGER.debug("MD5 (On Disk):      '%s'", self._md5)

        self._md5_needs_update = (self._md5 != self._pf_md5)
        LOGGER.debug("Needs update:        '%s'", self._md5_needs_update)

    def _write_data(self):
        write_json(self._pf_abs, self._pf_data)

    def calculate_md5(self, only_tracked_files=True):
        universal_lineendings = False
        if self._hash_calc_version > 1:
            universal_lineendings = True

        if only_tracked_files:
            self._only_tracked_files = True
            for hash_dir in self._hash_dirs:
                self._exclude_files += get_git_ls_files(hash_dir, '--exclude-standard --others --ignored')
                self._exclude_files += get_git_ls_files(hash_dir, '--exclude-standard --others')
        else:
            self._only_tracked_files = False

        md5 = lucxutils.dirs_hash(self._hash_dirs, exclude_file_ext=self._exclude_file_ext, exclude_dirs=self._exclude_dirs,
                                  n_threads=4, exclude_files=self._exclude_files, universal_lineendings=universal_lineendings)
        if self._files:
            files_hash = lucxutils.get_threaded_hashes(self._files, 4, universal_lineendings)
            package_hash = md5 + files_hash
            md5 = hashlib.md5(package_hash.encode()).hexdigest()

        submodules_hash = ""
        for submodule, commit in self._submodules.items():
            LOGGER.debug("Adding submodule '%s' with commit '%s'", submodule, commit)
            submodules_hash += commit

        if submodules_hash:
            LOGGER.debug("Adding submodule hash")
            package_hash = md5 + submodules_hash
            md5 = hashlib.md5(package_hash.encode()).hexdigest()
        return md5

    def get_next_time_based_version(self):
        now = datetime.datetime.now()
        year = str(now.year)
        month = str(now.month)
        splitted = self._pf_version.split('.')
        if len(splitted) == 3:
            current_year = splitted[0]
            current_month = splitted[1]
            current_increment = splitted[2]
            if current_year == year and current_month == month:
                return "{}.{}.{}".format(year, month, int(current_increment) + 1)
        return "{}.{}.{}".format(year, month, 1)

    def update_package_file_hash(self):
        self._pf_data['version'][self._data_entry + '_md5'] = self._md5
        self._write_data()

    def update_name(self, name):
        self._pf_data['version'][self._data_entry + '_name'] = name
        self._write_data()

    def update_version(self, version):
        if self._pf_data['version'][self._data_entry + '_name'] != version:
            self._pf_data['version'][self._data_entry + '_name'] = version
            self._write_data()
            LOGGER.info("VERSION :: %s :: %s -> %s [UPDATED]", self._pf_name, self._pf_version, version)
        else:
            LOGGER.info("VERSION :: %s :: %s == %s", self._pf_name, self._pf_version, version)

    def update_remote_config(self, url, clone, path, includes):
        self._remote['url'] = url
        self._remote['clone'] = clone
        self._remote['path'] = path
        self._remote['includes'] = includes
        self._remote_url = url
        self._remote_clone = clone
        self._remote_path = path
        self._remote_includes = includes
        self._pf_data['remote'] = self._remote
        self._write_data()

    def update_sync_status(self, ref, md5):
        self._sync['git_ref'] = ref
        self._sync['md5'] = md5
        self._sync_git_ref = ref
        self._sync_md5 = md5
        self._pf_data['sync'] = self._sync
        self._write_data()

    def validate_version(self, version):
        if version not in self._versions:
            LOGGER.error("Version '%s' not found in the history of the package", version)
            LOGGER.error("Versions: %s", tuple(self._versions))
            sys.exit(1)

    def get_package_file_sources(self, version):
        self.validate_version(version)
        LOGGER.info("Version '%s' found. Checking out package file '%s'", version, self._pf_abs)
        git_checkout(self._root_abs, [self._pf], self._versions[version])
        pf_content = read_json(self._pf_abs)
        git_reset(self._root_abs, self._pf, 'HEAD')
        git_checkout(self._root_abs, [self._pf], 'HEAD')
        sources = []
        if "directories" in pf_content:
            sources = pf_content['directories']
        else:
            sources = ['.']
        if "files" in pf_content:
            sources += pf_content['files']
        return sources

    def get_checkout_commands(self, version, paths):
        ref = self._versions[version]
        path_arg = " ".join(paths)
        commands = ["git checkout {} -- {}".format(ref, path_arg)]

        return commands

    def print_checkout_commands(self, version):
        sources = self.get_package_file_sources(version)
        source_paths = []
        for source in sources:
            abs_path = os.path.abspath(os.path.join(self._root_abs, source))
            rel = os.path.relpath(abs_path)
            source_paths.append(rel.replace('\\', '/'))
        commands = ["rm -rf {}".format(" ".join(source_paths))]
        commands += self.get_checkout_commands(version, source_paths)

        rel_pf = os.path.relpath(self._root_abs)

        if self._submodules:
            commands.append("git submodule update --init --recursive {}".format(rel_pf))
        LOGGER.info("Checkout commands (Git Bash):\n\n%s", "\n\n".join(commands))

    def scan_versions_from_ref(self, local, reference='develop'):
        if not git_available():
            LOGGER.error("Cannot scan for versions without 'git' in PATH")
            sys.exit(1)
        if not local:
            git_fetch_ref(self._root_abs, reference)
        self._versions = get_versions_and_commits(reference, self._root_abs, self._pf, self._data_entry, local)

    def erase(self):
        for obj in os.listdir(self._root_abs):
            path = os.path.join(self._root_abs, obj)
            if path == self._pf_abs:
                continue
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    def needs_hash_update(self):
        return self._md5_needs_update

    def get_package_file_hash(self):
        return self._pf_md5

    def get_disk_hash(self):
        return self._md5

    def get_name(self):
        return self._pf_name

    def get_version(self):
        return self._pf_version

    def get_versions(self):
        return self._versions

    def get_hash_calc_version(self):
        return self._hash_calc_version

    def get_types(self):
        return self._types

    def get_submodules(self):
        return self._submodules

    def get_abs_path(self):
        return self._root_abs

    def get_remote_config(self):
        return self._remote_url, self._remote_clone, self._remote_path, self._remote_includes

    def get_sync_git_ref(self):
        return self._sync_git_ref

    def get_sync_md5(self):
        return self._sync_md5

    def pretty_print(self):
        printer = Printer(box_color=Color.grey)
        printer.title(self._pf_name, color=Color.cyan)

        printer.print(content='Package file', color=Color.cyan)
        printer.print(content=self._pf_abs, offset=4)

        printer.print(content='Version (' + self._data_entry + ')', color=Color.cyan)
        printer.print(content=self._pf_version, offset=4)
        printer.print(content='Hash calculation version', color=Color.cyan)
        printer.print(content=str(self._hash_calc_version), offset=4)
        printer.print(content='Checksum', color=Color.cyan)
        printer.print(content='Package file', offset=4, color=Color.cyan)
        printer.print(content=self.get_package_file_hash(), offset=8)

        if self.needs_hash_update():
            printer.print(content='Disk', offset=4, color=Color.yellow, status=Status.warning, status_content='MODIFIED')
            printer.print(content=self.get_disk_hash(), offset=8, color=Color.yellow)
        else:
            printer.print(content='Disk', offset=4, color=Color.cyan, status=Status.okay)
            printer.print(content=self.get_disk_hash(), offset=8)

        if self._hash_dirs:
            printer.print(content='Directories', color=Color.cyan)
            for directory in self._hash_dirs:
                printer.print(content=directory, offset=4)

        if self._files:
            printer.print(content='Files', color=Color.cyan)
            for hash_file in self._files:
                printer.print(content=hash_file, offset=4)

        if self._exclude_dirs:
            printer.print(content='Directories excluded', color=Color.cyan)
            for directory in self._exclude_dirs:
                printer.print(content=directory, offset=4)

        if self._exclude_file_ext:
            printer.print(content='File extensions excluded', color=Color.cyan)
            for file_ext in self._exclude_file_ext:
                printer.print(content=file_ext, offset=4)

        if self._exclude_files:
            printer.print(content='Files excluded', color=Color.cyan)
            for file_excluded in self._exclude_files:
                printer.print(content=file_excluded, offset=4)

        if self._types:
            printer.print(content='Types', color=Color.cyan)
            for package_type in self._types:
                printer.print(content=package_type, offset=4)

        if self._submodules:
            printer.print(content='Submodules', color=Color.cyan)
            for submodule, commit in self._submodules.items():
                content = "{} {}".format(submodule, commit)
                printer.print(content=content, offset=4)

        if self._remote:
            printer.print(content='Remote', color=Color.cyan)
            for key, value in self._remote.items():
                content = "{} {}".format(key, value)
                printer.print(content=content, offset=4)

        if self._sync:
            printer.print(content='Sync', color=Color.cyan)
            for key, value in self._sync.items():
                content = "{} {}".format(key, value)
                printer.print(content=content, offset=4)

        printer.divider()
