# Changelog

## Upcoming changes

# 3.5.4
- Allowing atomicwrites requirement >= 1.3
- Forwarding debug to yaml executor
- Supporting flat in yaml executor


# 3.5.3

- Updated Bitbucket summary table. PJRV-17278
- Fixed yaml_executor paramters. LUCX-464

# 3.5.2

- Adapted Post & Pre parsing to new lucx syntax.
- Adapted `yaml_executor.py` to lucxbau version 21.X

# 3.5.1

- Updated python library versions of matplotlib and pandas for compatibility with python3.8

# 3.5.0

- Fixed component mapping for relative paths
- Improved git related finder methods
- Respecting line endings for hash methods
- Added new tool compiler_delta_check
- Added new cli options to compiler_warnings tool
- Added gitw tool
- packages tool has an added hashing algorithm version
- qacw tool accepts changed files
- Added tool repository miner
- Yaml executor has a new argument for the encoding of the commands output

# 3.4.0

- Fixing encoding for lucxutils.execute
- Adding changed files line support for compiler_warnings
- Adding Git.cmd support for yaml_executor

# 3.3.3

- Ignore Unicode coding error. LUCX-309
- Ignore notes in compiler warnings analysis. NRCSTWO-131357
- Fixed ^ problem on windows + Adapted unit tests. NRCSTWO-133430
- Added option for multiple component files. NRCSTWO-132357

## 3.3.2

- Removed Exception for yaml_executer failed stage. LUCX-274
- Replaced checkout by checkout_helper. NRCSTWO-129960
- Removed include files from warning analysis. NRCSTWO-130319
- add compiler warnings check in pr pipeline. NRCSTWO-123551
- Printing hash values. NRCSTWO-128239

## 3.3.1

- yaml_executor resolved log_dir path. LUCX-274

## 3.3.0

- updated cashew script for backslash replace. VIDEOGENTHREE-66737

## 3.2.7

Bugfixes:
- `yaml_executor` fixed pre and post execution. LUCX-251
- Removed unnecessary tcc init output. LUCX-237

## 3.2.6

Features:
- `yaml_executor`: added lucx-dir parameter. LUCX-235

## 3.2.5

Bugfix:
- `lucxutils`: execute() will now buffer the stdout correctly separated by lines. LUCX-166

## 3.2.4

Bugfix:
- `teams_mapping`: removed get csv dialect functionality for delimiter and hardcoded comma as default delimiter PJPH-41932

Features:
- `teams_mapping`: parse components with gitignore way within one level of precedence, the last matching pattern decides the outcome PJPH-40373
- `compiler_warnings`: parse components with gitignore way within one level of precedence, the last matching pattern decides the outcome PJPH-40373 
- `packages`: status short default, no seperate update checksum without updating version LUCX-158
- `yaml_executor`: yaml executor to support credentials in commands
- `yaml_executor`: support post postsuccess postfail in yaml executor
- `yaml_executor`: transformed the executionOrder calculation into proper classes.

## 3.2.3

Features:
- `yaml_executor`: Nodes and Stages with same execution order will now resolve according to parsing order. LUCX-143

## 3.2.2

Bugfix:
- `compiler_warnings`: fixed additional `\r` on Windows for compiler_warnings_to_csv.py

Features:
- `yaml_executor`: Steps can now print their output continuously. LUCX-117

## 3.2.1

Features:
- `yaml_executor`: Log files with same step names won't overwrite each other. LUCX-104

## 3.2.0

Features:
- `yaml_executor`: Lucx Yaml files can be executed locally. DACX-850
- `tccw_wrapper`: The environment from TCC's init.bat can be reused in python. DACX-855

## 3.1.0

Features:
- `batcodecheckw`: Added support for batch linting with BatCodeCheck. NRCSTWO-89911

## 3.0.0

Features:
- `cppcheckw`: **MAJOR** Rename arguments and prevent exitting with error when no sources are supplied NRCSTWO-48808
- `cashew`: Remove unnecessary log entry DACX-765
- `pr_stats`: corrected import paths DACX-745
- `tccw`: Consider os version for hashing and improve error message DACX-770
- `tccw`: removed logging of 'expanded_command' DACX-771

## 2.5.1

- `cppcheckw`: Changed behaviour for non-existing source files to warning instead of error

## 2.5.0

- `cashew`: BTS-4225 Update to use ccache for GHS, add possibility to generate logfile
- `flux_checker`: DACX-754 Add parameter to pass FQM executable

## 2.4.1

Features:
- `cppcheckw`: Added support for multiple named parameters with same name in the config file

## 2.4.0

Features:
- Add version information to all tools DACX-730
- `pr_stats`: Added Pull Request Statistics generation DACX-476

## 2.3.1

Features:
- `tccw`: Add workaround for tcc execution issue BTS-4216

## 2.3.0

Features:
- `tccw`: If mirror feature is used in TCC the caching is disabled.
- `tccw`: Improved error message.

## 2.2.0

Features:
- `qacw`: Added new `-M`/`--messages-output-format` parameter to control the format of `--messages-output`.
- Added a new tool `artifactoryw`. The tool provides functionality for removing artefacts from artifactory according to specified retention period starting from creation or last downloaded date.
- `artifactoryw`: Added new parameters `--include-path-pattern` and `--exclude-list` for `artifactoryw clean`.
- `lucxbox`: Relaxed minimal required Python version to also support Python 3.5. It is still recommended to use Python 3.6 or higher. But on OSD4 only Python 3.5 is installed by default. It will therefore be supported as long as OSD4 is widely used.
- `cppcheckw`: Added wrapper for tool Cppcheck. Cppcheck is a static analysis tool for C/C++ code. More information on http://cppcheck.sourceforge.net/

## 2.1.0

Features:
- `compiler_warnings`: Added "Column" to warning parser output.
- `compiler_warnings`: Cluster duplicate file warnings.
- `tccw`: Local TCC runs are now cached.
- `cashew`: Set object timeout before starting cleanup.
- `qacw`: Add the option to analyze and report only selected sources listed in a file.
- `qacw`: added function to combine csv reports for qac and qacpp analysis

## 2.0.0

Features:
- `lucxbox`: Removed Python 2.7 compatibility
  - Build self-contained executables for all LUCxBox tools with `PyInstaller`.
  - These will be distributed as a TCC tool and allow projects which still use Python 2.7 to also use the LUCxBox tools.

## 1.16.0

Features:
- `lucxbox`: Made LUCxBox a pip-installable package
  - After installation, LUCxBox tools are available as executables.
- `qacw`: Added option to output messages compatible with the HIVE SonarQube QA Framework plugin `-m`/`--messages-output`.

## 1.15.1

Bugfix:
- `qacw`: Several tool improvements
  - build will now fail if essential licenses or components are not available, print warnings otherwise.
  - Fixed duplicated logging issue for some scripts.
  - Allowed JSON files for `sync` command.

## 1.15.0

Features:
- `lucxbox`: use py.test test discovery in lucxbox
- `flux_checker`: Updated flux checker lucxbox tool to use flux 1.1 release
- `compiler_warnings`: Added grep as compiler parser.
- `compiler_warnings`: Added info sheet to warnings analysis
- `qacw`: change delimiter of csv files

## 1.14.0

Features:
- `compiler_warnings`: Added team column to compiler warning excel file.

## 1.13.0

Features:
- `qacw`: Added csv report for qac team warnings file. This is especially useful for very large reports, as Excel has a maximum of 1.048.576 lines.
   If this number is exceeded the report is simply aborted.

## 1.12.1

Features:
- `qacw`: Improved logging output in error case.

Bugfixes:
- `compiler_warnings`: Fix compiler warning severity.

## 1.12.0

Features:
- `qacw`: Added option to force a clean build `-c`/`--clean`.
- `qacw`: Added option to perform an Inter TU Dataflow analysis `-I`/`--inter-tu-dataflow` .
- `qacw`: Remapped C as CPP files as C coding rule config is not yet available from EPG. Otherwise C files cannot be analyzed.
- `qacw`: Added components info to warnings spreadsheet.
- `lib/lucxutils`: Allowed saving of stdout and stderr to custom location.

## 1.11.0

Features:
- `qacw`: Additionally allowed setting of custom installation location aside from usual environment variable `PRQA_HOME`.
   Example: `python qacw.py -p C:\PRQA\PRQA-Framework-2.3.0 project ...`

## 1.10.1

Bugfix:
- QAC executable could not be found without `.exe` extension on windows.

## 1.10.0

Features:
- `cashew`: consider `.obj` files for max path length check.
- `qacw`: added file report

Bugfixes:
- `qacw`: fixed missing db entry bug

## 1.9.0

Features:
- `tccw`: Enhanced error message in tcc.
- `git_reference_repo`: Handle naming clash or url change for submodules in git refrepo.
- `cashew`: Add path to hash creation to support local builds.

## 1.8.0

Features:
- Added feature to map qac warnings to teams. The result will be stored in an excel spreadsheet.
- Remove duplicate warnings in `compiler_warnings` tool and show occurrences instead.
- PRQA analysis now separates the creation of the project and the actual analysis into two commands `python qacw.py project setup` and `python qacw project analyze`.

## 1.7.0

Feature:
- Adding new tool `flux_checker`
- Adding super cool new function `parallel_execute` to luxutils module. The function takes a list of commands and you can define with how many threads parallel they should be executed.

## 1.6.0

Feature:
- Added compiler warning types database file handling to `compiler_warnings` tool. VIDEOGENTHREE-27833
- Documentation updated for `dauerlaufw` tool. DACX-414
- INTERNAL Improved performance in `matches_wildcard_pattern` library function. DACX-417
- INTERNAL Adding coverage report and coverage checks to lucxbox. DACX-413

Bugfix:
- Fixing `git_lfs_check` for python3. DACX-415

## 1.5.0

- Integrate Coverity script into LUCx box. HIVE-943
- Add TCC wrapper. DACX-389

## 1.4.0

- Added QAC Analysis and upload

## 1.3.0

- Adding new parameter `--compress` and `--clcache-object-timeout` to `cashew`.
- `cachew` is now performing cache cleanup before running the build.

## 1.2.0

- Add stats and size as parameter to cashew. DACX-347
- Adding new tool `copyright_checker`. DACX-354
- Adding new tool `dauerlaufw`.

## 1.1.1

- Fix bug in `git_lfs_check`.

## 1.1.0

- Adding tool `cashew`.

## 1.0.0

- Initial tag
