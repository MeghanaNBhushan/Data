# copyright_checker

-----------------------

usage: copyright_checker.py [-h] [--repo-name REPO_NAME]
                            [--root-folder ROOT_FOLDER] [-s] [-p, --print]
                            [--check-single-file CHECK_SINGLE_FILE | --check-file-of-files CHECK_FILE_OF_FILES]
                            [-d] [-q] [--version]

Process arguments.

optional arguments:

-h, --help            show this help message and exit
  --repo-name REPO_NAME
                        The repository name of the project
  --root-folder ROOT_FOLDER
                        the root folder of the directory to check.

-s, --subdir          Include sub directories in check? Default: False

-p, --print           Print results to console? Default: False
  --check-single-file CHECK_SINGLE_FILE
                        Set this if you wish to check a single file
  --check-file-of-files CHECK_FILE_OF_FILES
                        Path to file containing paths of files to check.

-d, --debug           Print debug information

-q, --quiet           Print only errors

--version             show program's version number and exit