# submodule_changedfiles.py

-----------------------
```
usage: submodule_changedfiles.py [-h] -cf CHANGED_FILES_FILE -sub
                               SUBMODULE_RELATIVE_PATH -dci DEST_COMMIT_ID

A Compiler warnings delta checker.

optional arguments:
  -h, --help            show this help message and exit
  -cf CHANGED_FILES_FILE, --changed-files-file CHANGED_FILES_FILE
                        Name of the file containing list of changed files
  -sub SUBMODULE_RELATIVE_PATH, --submodule-relative-path SUBMODULE_RELATIVE_PATH
                        Relative path of submodule in main repository
  -dci DEST_COMMIT_ID, --dest-commit-id DEST_COMMIT_ID
                        Main repository commit id. Ex: ^ENV:LUCX_TARGET_BRANCH_COMMIT;
```

#Submodule Changed Files HowTo

### 1. Description

Submodule changed files was created to append changed files from submodule if PR updated
revision on that submodule.

### 2. Requirements for script execution
Python version = Python >=3.6
