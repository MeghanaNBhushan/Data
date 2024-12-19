# compiler_warnings

-----------------------
```
usage: compiler_warnings.py [-h] [-d] [-q] [--version] --compiler-log
                            COMPILER_LOG
                            [--components-file [COMPONENT_FILES [COMPONENT_FILES ...]]]
                            [--add-package-info ADD_PACKAGE_INFO]
                            [--to-excel TO_EXCEL] [--to-csv TO_CSV]
                            [--to-json TO_JSON] [--root-directory ROOT_DIR]
                            [--target-directory TARGET_DIRS [TARGET_DIRS ...]]
                            --compiler {clang,greenhills,msvc,prqa_exceptions}
                            [--types-db TYPES_DB] [--jobs JOBS]
                            [--gitignore-mapping]
                            [--changed-files CHANGED_FILES [CHANGED_FILES ...]]
                            [--output OUTPUT] [--use-relative-paths]
                            [--black-list BLACK_LIST [BLACK_LIST ...]]
                            [--threshold THRESHOLD | --threshold-file THRESHOLD_FILE]

A Compiler warnings parser with excel export possibilities.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit
  --compiler-log COMPILER_LOG, -cl COMPILER_LOG
                        Path to compiler log file to parse the warnings from
                        (globbing is allowed).
  --components-file [COMPONENT_FILES [COMPONENT_FILES ...]], -cf [COMPONENT_FILES [COMPONENT_FILES ...]]
                        Use COMPONENT files to map files to components/teams
  --add-package-info ADD_PACKAGE_INFO, -p ADD_PACKAGE_INFO
                        Add package and sw layer info when mapping components/teams
  --to-excel TO_EXCEL, -te TO_EXCEL
                        Whether to export the results to excel
  --to-csv TO_CSV, -tc TO_CSV
                        Whether to export the results to csv
  --to-json TO_JSON, -tj TO_JSON
                        Whether to export the results to json
  --root-directory ROOT_DIR, -rd ROOT_DIR
                        Path to root of repository to get file list
  --target-directory TARGET_DIRS [TARGET_DIRS ...], -td TARGET_DIRS [TARGET_DIRS ...]
                        List of paths (seperated by space) to include warning
                        only from specified locations
  --compiler {clang,greenhills,msvc,prqa_exceptions}, -c {clang,greenhills,msvc,prqa_exceptions}
                        Compiler
  --types-db TYPES_DB, -tdb TYPES_DB
                        Compiler warning types database file (json).
  --jobs JOBS, -j JOBS  Number of threads
  --gitignore-mapping, -g
                        Switch to enable of team mapping that implements
                        gitignore specification - within one level of
                        precedence, the last matching pattern decides the
                        outcome
  --changed-files CHANGED_FILES [CHANGED_FILES ...], -ch CHANGED_FILES [CHANGED_FILES ...]
                        Files containing a list of changed files
  --output OUTPUT, -o OUTPUT
                        Output file to log the warnings existing on the
                        changed files
  --use-relative-paths  Use relative file paths when mapping components
  --black-list BLACK_LIST [BLACK_LIST ...], -bl BLACK_LIST [BLACK_LIST ...]
                        Mention the black list files for which warnings are
                        not be considered
  --threshold THRESHOLD, -t THRESHOLD
                        Threshold of allowed overall warnings before script
                        returns non-zero exit code
  --threshold-file THRESHOLD_FILE, -tf THRESHOLD_FILE
                        Threshold file which lists thresholds for each warning
                        name. Threshold file is a json.
```


#Threshold Generator HowTo

### 1. Description

threshold_generator.py were created for updating existing warnings json configuration.
Configuration files updating only with new values of warnings. Script has additional
functionality for debugging which may be useful. List of possibilities bellow:

Updating json config files.
Displaying difference between logs and configuration.
Displaying full list of warnings in log files.

### 2. How configuration file and log file related?

Incoming parameters is path to directories.
Script matches config files and logs based on their names.
It means that config files must be named in that way: thresholds_{cfg_name}.json
And at the same time logs should have names: {some_text(N_(1_1))}_{cfg_name}.log to successfully
match each other. As example:

thresholds_apu_entry_c.json will match N(2_6)_(3_10)__S(2_3)_(1_1)__dai_entry_c_cmd_dai_apu_entry_c.log


### 3. Use cases.
To run this script you need three incoming parameters. Two of them is directories with
configuration files and log files. Third one is --action. Depends on value of this parameter script will work
in specific way. Action could take 3 different values: {show, diff, gen}
##### 3.1 Show
Displaying all errors in log files with counter.
##### 3.2 Diff
Difference displaying between list of warnings inside of configuration files
and new unique warnings inside log files.
##### 3.3 Gen
Gen is using for update configuration files with new warnings from log files.
If you need to implement new threshold configuration file in to the system all you need is
add new empty file to configuration directory with name  regarding with name agreements from P.2 of this description.
If json structure of configuration file were broken after running of script file will be rewrite in proper
way.

### 4. Requirements for script execution

Python version = Python 2.7.2
Modules List = os, argparse, json, re.

