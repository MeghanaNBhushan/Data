# Packages

Packages are a mechanism to version directories of a git repository.
It is based on a small package json file that specifies what directories and files should
be included in the package. By default all files and directories below the package file are considered recursively.
All files are getting hashed and hashes are concatenated and hashed again to build the final package hash.
A common use case is to use the packages mechanism to track directories across repositories where no SCM link exists.
Another use case is to create inner directory release cycles and use semantic versioning on a directory basis.
A release could then check for all packages being in a clean state for their semantic versioning number.

-----------------------
```
usage: packages.py [-h] [-d] [-q] [-p PACKAGE_FILE_NAME] [-r ROOT]
                   [-f PACKAGES_FILTER] [-t] [-y FILTER_TYPE]
                   {compare,status,update,checkout-helper,create} ...

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  -p PACKAGE_FILE_NAME, --package-file-name PACKAGE_FILE_NAME
                        The packages file name that indicates a package.
                        Default is 'rb_package.json'
  -r ROOT, --root ROOT  Root path of searching for packages
  -f PACKAGES_FILTER, --filter PACKAGES_FILTER
                        Restrict the packages by a wildcard for the package
                        name, e.g. pf.if.*
  -t, --time-based      Time based package versioning. Default is semantic
  -y FILTER_TYPE, --filter-type FILTER_TYPE
                        Filters the packages to only consider the ones with
                        the given type

Package sub commands:
  {compare,status,update,checkout-helper,create,remote,sync}
    compare             Package comparing for different roots
    status              Packages status
    update              Updating package information
    checkout-helper     Package Checkout Helper
    create              Package creation
    remote              Add remote configuration
    sync                Sync package with remote
```

-----------------------
```
usage: packages.py status [-h] [--fail-on-diff] [-l] [-r REFERENCE]
                          [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  --fail-on-diff, -f    Fail the script when packages were changed
  -l, --long            Long status - every package detail
  -r REFERENCE, --reference REFERENCE
                        Reference root to check against trusted package file
                        checksums
  -o OUTPUT, --output OUTPUT
                        Status output to file in an easier parseable format

-----------------------

usage: packages.py update [-h] [-n NAME]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name of the version. E.g. a semantic one like "1.0.0"
```

-----------------------
```
usage: packages.py checkout-helper [-h] (-l | -v VERSION) [-r REFERENCE] [-n]

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            Lists available versions of the package. Exits
                        afterwards
  -v VERSION, --version VERSION
                        Version to be searched and checked out
  -r REFERENCE, --reference REFERENCE
                        The branch to fetch and start parsing the package
                        history and finding the version.The default is "HEAD"
                        which does not fetch from origin.
  -n, --no-fetch        Do not fetch reference from origin
```

-----------------------
```
usage: packages.py compare [-h] -r COMPARE_ROOT

optional arguments:
  -h, --help            show this help message and exit
  -r COMPARE_ROOT, --root COMPARE_ROOT
                        Root of the other packages to compare
```

-----------------------
```
usage: packages.py create [-h] [-n NAME] [-d DIRECTORIES [DIRECTORIES ...]]
                          [-e EXCLUDE_DIRECTORIES [EXCLUDE_DIRECTORIES ...]]
                          [-f EXCLUDE_FILE_EXTENSIONS [EXCLUDE_FILE_EXTENSIONS ...]]
                          [-t TYPES [TYPES ...]] [-s FILES [FILES ...]]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  The name of the component. When not given, path from
                        cwd will be used
  -d DIRECTORIES [DIRECTORIES ...], --directories DIRECTORIES [DIRECTORIES ...]
                        Directories to include in the package. Default is ".".
                        Paths are relative to the root of the package!
  -e EXCLUDE_DIRECTORIES [EXCLUDE_DIRECTORIES ...], --exclude-directories EXCLUDE_DIRECTORIES [EXCLUDE_DIRECTORIES ...]
                        Directories to exclude from the package checksum.
                        Paths are relative to the root of the package!
  -f EXCLUDE_FILE_EXTENSIONS [EXCLUDE_FILE_EXTENSIONS ...], --exclude-file-extensions EXCLUDE_FILE_EXTENSIONS [EXCLUDE_FILE_EXTENSIONS ...]
                        File extensions to be excluded from checksum (e.g.
                        ".txt .md")
  -t TYPES [TYPES ...], --types TYPES [TYPES ...]
                        Types to assign to this package
  -s FILES [FILES ...], --files FILES [FILES ...]
                        Additional files to include in the package. Paths are
                        relative to the root of the package!
```

-----------------------
```
usage: packages.py remote [-h] -u URL -c CLONE [-p PATH]
                          [-i INCLUDES [INCLUDES ...]]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The url of the remote repository
  -c CLONE, --clone CLONE
                        The clone directory of the remote repository
  -p PATH, --path PATH  The path in the remote repository from where to
                        include files
  -i INCLUDES [INCLUDES ...], --includes INCLUDES [INCLUDES ...]
                        The wildcard patterns to include files from remote
                        repository

-----------------------
```
usage: packages.py sync [-h] [-c REF | -t REF]

optional arguments:
  -h, --help            show this help message and exit
  -c REF, --commit REF  The commit to checkout from remote repository
  -t REF, --tag REF     The tag to checkout from remote repository
```

-----------------------

## Package file format

* Required
  * `name`: The name of the package
  * `version`: The version of the package.
    * Contains entries for semantic and time based `name` as well as `md5`.
  * `md5`: The md5 hash of the package. Can be initally blank and can be updated using the tool `update` functionality

* Optional
  * `directories`: Specify a list of directores relative to the package file. When not given, the package file root is taken
  * `directories_exclude`: Specify a list of directories relative to the package file to be excluded
  * `file_extensions_exclude`: Specify a list of file extensions to be excluded
  * `types`: Specify a list of freely defined types the package has. This can be used later to filter all packages commands for a specific type
  * `files`: Specify an additional list of files to include in the package
  * `remote`: The remote config of the package.
    * Contains entries to link the package content to files in another repository. The remote config requires the repository `url`, the local directory for the `clone` and the `path` in the repository used as an offset to apply the wildcard patterns in the `includes` list.
  * `sync`: Status after the synchronization with the remote repository.
    * Contains entries for `md5` and the `git_ref` of the last sync.

```json
{
    "name": "jenkins jobs + configs",
    "version": {
        "semantic_name": "1.0.0",
        "semantic_md5": "12312",
        "time_based_name": "2020.4.3",
        "time_based_md5": "1231241241"
    },
    "directories": [
        "jenkinsfiles",
        "configs"
    ],
    "files": [
        "test.txt",
        "configs/config.cmd"
    ],
    "directories_exclude": [
        "configs/teams"
    ],
    "file_extensions_exclude": [
        ".txt"
    ],
    "types": [
        "component",
        "package",
        "integration-point"
    ],
    "remote": {
        "url": "ssh://git@sourcecode.socialcoding.bosch.com:7999/project/repository.git",
        "clone": "some_dir/git/repository",
        "path": ".",
        "includes": [
            "**"
        ]
    },
    "sync": {
        "git_ref": "1231241241",
        "md5": "1231241241"
    }
}
```