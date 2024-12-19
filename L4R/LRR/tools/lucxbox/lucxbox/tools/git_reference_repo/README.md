# git_reference_repo

A script to create and maintain a [reference repo](https://support.cloudbees.com/hc/en-us/articles/115001728812-Using-a-Git-reference-repository)
intended to be used by Jenkins to reduce git server load and worker disk space usage. Features include:
 - recursively adds submodules to the reference repository
 - recover from a corrupted reference repository
 - checks disk space requirements before creating a reference repository

## Example
```
./git_reference_repo.py -p /tmp/pj_dc_ref -g ssh://git@sourcecode.socialcoding.bosch.com:7999/pjdc/pj-dc_int.git
```

## Usage
```
usage: git_reference_repo.py [-h] --path PATH --git_repo GIT_REPO [--force]
                             [--storage_new STORAGE_NEW]
                             [--storage_update STORAGE_UPDATE] [-d] [-q]
                             [--version]

### Description: ### This script is intended to create and maintain a
reference repository based on https://support.cloudbees.com/hc/en-
us/articles/115001728812-Using-a-Git-reference-repository

optional arguments:
  -h, --help            show this help message and exit
  --path PATH, -p PATH  Path of the reference repo. If it exists, it will be
                        updated. If it's an empty directory a reference
                        repository will be created
  --git_repo GIT_REPO, -g GIT_REPO
                        The git repository for which a reference repository
                        should be created
  --force, -f           force the creation of a fresh reference repository,
                        don't attempt to update
  --storage_new STORAGE_NEW
                        required free disk space for a new reference
                        repository - in MiB.[default=5120]
  --storage_update STORAGE_UPDATE
                        required free disk space for a reference repository
                        update - in MiB[default=1023]
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit
```

## Unit-Tests and System-Tests
The unit tests are automatically tested on Jenkins and via the lucxbox script. The system tests need to be run
manually:
```bash
python[3] -m tools.git_reference_repo.system_test.test_git_reference_repo
```