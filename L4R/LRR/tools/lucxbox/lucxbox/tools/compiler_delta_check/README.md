# compiler_delta_check.py

-----------------------
```
usage: compiler_delta_check.py [-h] [-d] [-q] [--version] -cf CHANGED_FILES --warnings-baseline-file WARNINGS_BASELINE_FILE
                               --warnings-file WARNINGS_FILE [--output-html OUTPUT_HTML] [--output-json OUTPUT_JSON]
                               [--summary-json SUMMARY_JSON] [-tf THRESHOLD_FILE] --build-variant BUILD_VARIANT
                               [--ignore-type IGNORE_TYPE [IGNORE_TYPE ...]] [--prid PRID] [--build-number BUILD_NUMBER]
                               [--target-branch TARGET_BRANCH] [--source-branch SOURCE_BRANCH]

A Compiler warnings delta checker.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit
  -cf CHANGED_FILES, --changed-files CHANGED_FILES
                        Name of the file containing list of changed files
  --warnings-baseline-file WARNINGS_BASELINE_FILE
                        Input file containing baseline
  --warnings-file WARNINGS_FILE
                        Input file containing current warnings
  --output-html OUTPUT_HTML
                        Output HTML report file name
  --output-json OUTPUT_JSON
                        Output JSON report file name
  --summary-json SUMMARY_JSON
                        JSON file name of summary
  -tf THRESHOLD_FILE, --threshold-file THRESHOLD_FILE
                        JSON file containing thresholds for tools
  --build-variant BUILD_VARIANT
                        Build variant
  --ignore-type IGNORE_TYPE [IGNORE_TYPE ...]
                        Remove specified warning type from comparison
  --prid PRID           Pull request ID
  --build-number BUILD_NUMBER
                        Build number
  --target-branch TARGET_BRANCH
                        Target branch name or commit id. Default is develop
  --source-branch SOURCE_BRANCH
                        Current branch or commit id. Default is current HEAD
```

#Compiler Delta Check HowTo

### 1. Description

compiler_delta_check was created to generate delta check in case of multiple compiler
warnings already exist in the project. Currently the script does not track code
movement. This means that it tracks only number of warnings with the specific message
grouped by file names. It also tries to track file renames using git, but currently
renamed/moved files should not have any changed in them.

The script takes all its inputs as files and can optionally generate output reports
in HTML and JSON formats. It can also generate summary report in JSON format with
several fields that can be used to create comment on the Bitbucket pull request page.

### 2. Requirements

The script works with baselines and compiler warnings list in json format. This files
can be generated with compiler_warnings script.

JSON schema for the inputs and outputs can be found in schemas directory.

### 3. Requirements for script execution
Python version = Python >=3.6
