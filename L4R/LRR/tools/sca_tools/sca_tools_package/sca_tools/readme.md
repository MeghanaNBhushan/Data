# SWQ SCA Tools

Software Quality (SWQ) Static Code Analysis (SCA) Tools consists of a set of Python scripts aimed to help out projects to configure and automate their static code analysis tools use cases in a flexible and customizable way. This is an alternative to manually configuring the project from commandline and it's primary goal is to expedite the integration process and empower the user and shape the corresponding tool's implementation run as seamless as possible.

## Index

  * [About](#about)
  * [Maintainers](#maintainers)
  * [License](#license)
  * [Installation via PIP](#install)
  * [Pre-requisites](#pre-requisites)
  * [How to use it](#use)
    * Configuration Parameters
      * [Common](#common-configuration-parameters)
      * [qac](#qac-configuration-parameters)
      * [coverity](#coverity-configuration-parameters)
      * [find_includes](#find-includes-configuration-parameters)
      * [map_teams](#map-teams-configuration-parameters)
      * [compiler_warnings](#compiler-warnings-configuration-parameters)
    * Arguments
      * [General](#arguments-general)
      * [Common](#arguments-common)
      * [qac](#arguments-qac)
      * [coverity](#arguments-coverity)
      * [find_includes](#arguments-find-includes)
      * [map_teams](#arguments-map-teams)
      * [compiler_warnings](#arguments-compiler-warnings)
  * [How to build and test it](#build)
  * [How to build the python package](#build-python-package)
  * [How to contribute](#contribute)
  * [Used 3rd party Licenses](#licenses)
* [Feedback](#feedback)



## <a name="about">About</a>

  The goal is to have a "standalone" python script that covers all use cases from a project for the QAC/Coverity framework.
  It utilizes a configurable multi-level configuration including the possibility to use a JSON file adapted for the projects needs.
  It provides also possibility to find all source files which include given header files, directly or indirectly. This feature is called a delta analysis.

Contents of Interest:

  1. [sca_tools](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools/browse) as submodule of your project or directly add it to your VCS as a tracked file.
  2. [qac.json](#qac-example-json)

  The same script should also be used from Jenkins to have the same reliable configuration and results as a local run.

Check the following link for the [CHANGELOG](changelog.md).

## <a name="maintainers">Maintainers</a>

* [Pro XC DOIT Software Quality Team](mailto:CC-ADPJ-DoitSoftwareQualityTeam@bcn.bosch.com)

## <a name="license">License</a>

  >	Copyright (c) 2022 Robert Bosch GmbH. All rights reserved.

## <a name="install">Installation via PIP</a>
For installing sca_tools via the python package manager PIP, please invoke in the root folder of the repository.
  > pip3 install

Or run a similar command as the following:
 > python3 -m pip install git+ssh://git@sourcecode.socialcoding.bosch.com:7999/cdf/sca_tools.git@develop

 Afterwards, sca_tools can be used on the command line. Please execute:
  > sca_tools -h

Or
 > swq-sca-tools -h

for further information.

## <a name="pre-requisites">Pre-requisites</a>

Pre-requisites that must be fulfilled before running SCA Tools:

- `JQ` (JSON Query) tool must be installed on system and path to its executable must be added to the `PATH` environment variable.

SCA Tools uses `JQ` during reports generation, it does intermadiate transformation (in runtime) of aggregated project analysis JSON file into different type of simplified JSON, which is after exported as final report (using Python Pandas module).

SCA Tools subcommands that require `JQ`:
- `qac export_analysis`

## <a name="use">How to use it</a>

### Configuration JSONS and General Variable Handling

There are three ways to configure or pass information to SCA Tools:
- CLI arguments
- Environment variables
- JSON configuration file(s) (so called "Datastores" and a special hierarchy inside them, so called "Datastore Target")

#### CLI Arguments

Most of the common parameters can be passed as CLI arguments to SCA Tools. List of available arguments for each subcommand can be found in [this section](#sca-tools-py). Or simply run `sca_tools.py [subcommand] --help` to see available arguments.

#### Environment Variables

It is also possible to set SCA Tools parameters via environment variables, with the exclusion of usernames and passwords (QAV_PASSWORD, ...). If a value is list, then semi-colon (;) should be used as a delimiter, e.g. ENV_VAR="value1;value2;value3"

#### Datastores

SCA Tools is capable to read parameters from one or multiple JSON configuration file (hereby referred to as datastore). It is useful to store less
frequently changed parameters in datastores and simply provide one or more datastore to an SCA Tools via `-dp / --datastore_path` CLI argument.

Datastore consists of two configuration levels:

- general configuration level - mostly stores parameters that are used for all build variants withing the project
- target configuration level - mostly stores parameters which values can vary depending on project specifications (build variants, compilers, OS platforms, etc.).
Datastore target name is passed to SCA Tools via `-dt / --datastore_target` CLI argument.

See the example datastore configuration for QAC project [here](#qac-example-json).

#### Using multiple datastores

As mentioned above, SCA Tools supports more that one datastore to be passed at a time. All provided datastores are being merged into one single JSON in runtime.
If there are overlapping parameters - each following provided datastore will override the value of overlapping parameter.

Storing SCA Tools configuration parameters in several datastores can be useful in several cases:

- Common parameters
  - QAC/Coverity version specific
  - External sources like license servers, commit hosts, etc.
  - Logging
- Project specific parameters
  - Compiler / Software specific
  - Platform specific
  - Modules specific

Use case example of multiple datastores can be found in [SCA Mini Demo project](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_mini_demo/browse/tools/sca/qac)
#### Configuration parameters precedence

Below is the flow of hierarchical lookup for SCA Tools parameters:

  1. A value is looked up in the provided command line arguments;
  2. If not found, then it is searched at the environment variable level;
  3. If not found there, then finally it is looked up in the datastore target configuration level;
  4. If not found, then it is looked up in the datastore general configuration file level;

`Note: Please also notice that the variables started with '*' should be mandatory defined either from environment, configuration file or CLI arguments.`

#### <a name="common-configuration-parameters">Common Configuration Parameters</a>

| Key              | Command Line Argument     | Comment                                                                                                                                  | Example                     |
|------------------|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------|
| HELPER_LOGS_PATH | -hlp / --helper_logs_path | Absolute path or relative to PROJECT_ROOT to where the helper logs will be generated. Default is a path where SCA Tools were started     | build/local_path/logs/      |
| PROJECT_ROOT     | -pr / --project_root      | Absolute path to the root folder where all source files are encountered. It is used as a base path for many relative path configurations | C:/Users/jondoe/work/opencv |


During the parse step the comments done with '//' are removed so it is possible to keep a commented .json file.


#### <a name="qac-configuration-parameters">QAC Configuration Parameters</a>
| Key                                   | Command Line Argument                     | Comment                                                                                                                                                                                                                                                                                                                                                                                                 | Example                                                          |
| -                                     | -                                         | -                                                                                                                                                                                                                                                                                                                                                                                                       | -                                                                |
| *ACF_FILE                             |                                           | Path relative to project root or absolute to the ACF QAC configuration file                                                                                                                                                                                                                                                                                                                             | helix/acf/helix_ccda_config_cpp_1.4.acf                          |
| ANALYZE_FILE                          | -af / --analyze_file                      | Analyzes the given file                                                                                                                                                                                                                                                                                                                                                                                 |                                                                  |
| ANALYZE_LIST                          | -al / --analyze_list                      | Path to a file that contains list of files to be analyzed. Can be absolute or relative to `PROJECT_ROOT`. If used with JSON synchronization type, SCA performs automatic files filtering to avoid QAC exceptions during analysis                                                                                                                                                                        |                                                                  |
| ANALYZE_PARAMS                        |                                           | Customizes analysis parameters to QAC's commands                                                                                                                                                                                                                                                                                                                                                        | --file-based-analysis --force-complete                           |
| C_FILES_ANALYZED_AS_C                 | -caac / --c_files_analyzed_as_c           | If defined, that defines if C files are analysed as c or not. False by default                                                                                                                                                                                                                                                                                                                          | true or false                                                    |
| CLEANUP_ON_CREATE                     | -coc / --cleanup_on_create                | By default defined as False. A boolean to clean up the QAC_PROJECT_PATH before creating a new project (except for log files inside `QAC_PROJECT_PATH/sca_tools/logs`)                                                                                                                                                                                                                                   | true                                                             |
| CODEOWNERS_FILE                       | -cf / --codeowners_file                   | Absolute path or relative to PROJECT_ROOT to the codeowners file. Accepts single path or list of paths                                                                                                                                                                                                                                                                                                  | C:/path/to/codeowners.txt                                        |
| COMPILER_LIST                         |                                           | List of CCT files corresponding to the individual used targets                                                                                                                                                                                                                                                                                                                                          | helix/config/cct/GCC_C++11.cct                                   |
| CUSTOM_HELP_PATH                      |                                           | If specified this path will be replaced in the rcf file to provide custom help message                                                                                                                                                                                                                                                                                                                  | build/armclang_a53_helix                                         |
| EXPORT_FORMATS                        | -ef / --export_formats                    | Defines the report export formats. Available formats: 'xlsx', 'csv', 'csv_zip', 'html' or 'all', where 'all' is a list of commonly used report formats: xlsx, csv and html. Extra formats can be specified explicitly, e.g. -ef all csv_zip. Default is 'all'                                                                                                                                           |                                                                  |
| FROM_STATE_FILE                       | -fsf / --from_state_file                  | Generates reports based on state file. If path is given - reads state from specified path. If is set to true - uses default state file path. Default is false                                                                                                                                                                                                                                           | true                                                             |
| GITIGNORE_MAPPING                     | -gm / --gitignore_mapping                 | Same as "ONLY_LAST_TEAM" parameter and is overridden if "ONLY_LAST_TEAM" is specified. Keeping for compatibility reasons for lucxbox users                                                                                                                                                                                                                                                              | true                                                             |
| HELP_PAGES_ROOT_DIR                   | -hprd / --help_pages_root_dir             | Root directory where help pages in HTML format are located. If specified, it creates custom configuration files where paths to help pages are set for all messages accordingly.                                                                                                                                                                                                                         |                                                                  |
| HELPER_CREATE_BASELINE                | -hcb / --helper_create_baseline           | If specified, a baseline will be created after an analysis run                                                                                                                                                                                                                                                                                                                                          |                                                                  |
| HELPER_REMOVE_FILE_LIST               | -hrfl / --helper_remove_file_list         | Give the absolute path or relative path (relative to project repo folder) of a text file OR an array, which contains list of files to be removed from the project                                                                                                                                                                                                                                       |                                                                  |
| HELPER_SUPPRESS_C_HEADER              | -hsc / --helper_suppress_c_header         | If set to a yes value all C headers .h will be ignored in the anaylsis                                                                                                                                                                                                                                                                                                                                  |                                                                  |
| HELPER_SUPPRESS_FILE_LIST_A           | -hsfa / helper_suppress_file_list_a       | Give the absolute path or relative path (relative to project repo folder) of a text file OR an array, which contains list of files to be excluded from the analysis                                                                                                                                                                                                                                     |                                                                  |
| HELPER_SUPPRESS_FILE_LIST_S           | -hsfs / --helper_suppress_file_list_s     | Give the absolute path or relative path (relative to project repo folder) of a text file OR an array, which contains list of files to be excluded from the sync                                                                                                                                                                                                                                         |                                                                  |
| FILTER_REPORT_OUTPUT_FILE             | -frof / --filter_report_output_file       | Write results to specified output file. Absolute or relative to repo root paths can be used                                                                                                                                                                                                                                                                                                             |                                                                  |
| IGNORE_VALIDATION                     | -iv / --ignore_validation                 | Bypasses QAC components validation mechanisms. False by default                                                                                                                                                                                                                                                                                                                                         |                                                                  |
| INPUT_CL_JSON                         | -icj / --input_cl_json                    | Path to json file to be patched                                                                                                                                                                                                                                                                                                                                                                         |                                                                  |
| JUSTIFICATION_MESSAGE_REGEXP          | -jmre/ --justification_message_regexp     | Regular expression(s) for suppressed Justification messages.                                                                                                                                                                                                                                                                                                                                            |                                                                  |
| LICENSE_SERVERS                       |                                           | List of license servers                                                                                                                                                                                                                                                                                                                                                                                 |                                                                  |
| LOCAL_BASELINE_PATH                   | -hsb / --helper_set_baseline              | Relative to project root or absolute. If specified, a baseline file will be used (files.sup), helper arg has priority and will override this: helper_set_baseline                                                                                                                                                                                                                                       | build/local_path/                                                |
| MAXIMUM_PARALLEL_WORKERS              | -mpw / --maximum_parallel_workers         | Number of CPUs to be used in analysis                                                                                                                                                                                                                                                                                                                                                                   | 4                                                                |
| METRICS_FILTER_LIST                   | -mfl / --metrics_filter_list              | List of metrics. If specified, then only provided metrics will be included in metrics report                                                                                                                                                                                                                                                                                                            | ["STPTH", "STPAR"]                                               |
| NCF_FILE                              |                                           | Path relative to project root or absolute to the NCF QAC configuration file or list of files. If several files are provided - contents of files will be merged into separate file. Merged file will be used in QAC project creation                                                                                                                                                                     | helix/ncf/helix_ccda_config_cpp_naming_1.0.ncf / ["helix/ncf/helix_ccda_config_cpp_naming_1.0.ncf", "helix/ncf/helix_ccda_config_cpp_naming_2.0.ncf"] |
| ONLY_LAST_TEAM                        | -olt / --only_last_team                   | Include only the last matched team in the teams report                                                                                                                                                                                                                                                                                                                                                  | true                                                             |
| *PROJECT_ROOT                         | -pr / --project_root                      | Path to project, relative from the location of the helper script                                                                                                                                                                                                                                                                                                                                        |                                                                  |
| *QAC_BIN_PATH                         | -qac / --qac_bin_path                     | Path to the directory where QAC is installed                                                                                                                                                                                                                                                                                                                                                            |                                                                  |
| QAC_CONFIG_PATH                       | -qaf / --qac_config_path                  | This parameter adds additional absolute or relative paths to PROJECT_ROOT to be searched for QAC configurations. The folders should contain the same structure as the one provided by the manufacturer - with the main folders "config" and "user_library". Usually should be set to the path to the sca_tools/cfg which contains the sca bundled configurations. Accepts single path or list of paths  | relative/path/to/sca_tools/cfg or C:/path/to/user/defined/config |
| QAC_CLEANUP_DIAGNOSTICS_OUTPUT        | -cdo / --cleanup_diagnostics_output       | By default defined as false. A boolean to remove QACLI diagnostics output XML files                                                                                                                                                                                                                                                                                                                     | false                                                            |
| QAC_DISABLE_OPTIMIZATION              | -do / --disable_optimization              | Disables QAC project optimization. Enabled by default                                                                                                                                                                                                                                                                                                                                                   | false                                                            |
| *QAC_PROJECT_PATH                     | -qap / --qac_project_path                 | Path relative to project root or absolute, without leading slash, this will also be the project name                                                                                                                                                                                                                                                                                                    | build/armclang_a53_helix                                         |
| QAC_THRESHOLD_WARNINGS_REPORT         | -twr / --threshold_warnings_report        | Path to threshold warnings report                                                                                                                                                                                                                                                                                                                                                                       |                                                                  |
| QAC_ANALYSIS_PATH_BLACKLIST           |                                           | List of files and folders to be excluded from analysis. Used in conjunction with QAC_MODULES                                                                                                                                                                                                                                                                                                            | ["build","dc_apl_test","ip_if","ip_mom","rc_fw"]                 |
| QAC_LOGGING_LEVEL                     | -qll / qac_logging_level                  | Set verbosity of the QAC output, can be one of ('NONE', 'ERROR', 'INFO', 'DEBUG', 'TRACE'). Default is 'ERROR'                                                                                                                                                                                                                                                                                          |                                                                  |
| QAC_MODULES                           |                                           | Modules are required to apply analysis filters. Only applies if analysis filters are used                                                                                                                                                                                                                                                                                                               | ["qacpp-4.4.0"]                                                  |
| QAC_SYNC_PATH_BLACKLIST               |                                           | List of files and folders to be removed from project synchronization                                                                                                                                                                                                                                                                                                                                    |                                                                  |
| QAC_SYNC_SETTINGS_INCLUDE_PATH        |                                           | List of sync settings used for e.g. -isystem in case of gcc/clang/qnx                                                                                                                                                                                                                                                                                                                                   | ["-isystem"]                                                     |
| QAVIEW_CSV                            | -qacsv / --qaview_csv                     | Path to qaview CSV export file                                                                                                                                                                                                                                                                                                                                                                          |                                                                  |
| QAV_USERNAME                          |                                           | QAVerify username. Used in conjunction with the QAV_PASSWORD. Must be provided as an environmental variable                                                                                                                                                                                                                                                                                             |                                                                  |
| QAV_PASSWORD                          |                                           | QAVerify password. Used in conjunction with the QAV_USERNAME. Must be provided as an environmental variable                                                                                                                                                                                                                                                                                             |                                                                  |
| QAV_PROJECT_NAME                      | -qpn / --qav_project_name                 | QAVerify project name                                                                                                                                                                                                                                                                                                                                                                                   |                                                                  |
| QAV_PROJECT_SNAPSHOT                  | -qps / --qav_project_snapshot             | QAVerify project snapshot name                                                                                                                                                                                                                                                                                                                                                                          |                                                                  |
| QAV_SERVER_URL                        | -qsu / --qav_server_url                   | QAVerify server URL                                                                                                                                                                                                                                                                                                                                                                                     |                                                                  |
| QAV_UPLOAD_SOURCE                     | -qus / --qav_upload_source                | QAVerify upload source directory                                                                                                                                                                                                                                                                                                                                                                        |                                                                  |
| SKIP_EXIT_ON_ANALYSIS_RETURN_CODES    | -see / skip_exit_on_analysis_return_codes | If set, the script does not exit after an analysis if its one of the specified return codes e.g. -see 3 9                                                                                                                                                                                                                                                                                               |                                                                  |
| SKIP_EXIT_ON_BUILD_RETURN_CODES       | -seb / skip_exit_on_build_return_codes    | If set, the script does not exit after a build when one of the specified return codes is a result e.g. -seb 0 2                                                                                                                                                                                                                                                                                         |                                                                  |
| *SYNC_TYPE                            |                                           | One of (JSON, BUILD_LOG, MONITOR)                                                                                                                                                                                                                                                                                                                                                                       | JSON                                                             |
| SYNC_BUILD_COMMAND                    | -sbc / --sync_build_command               | Build command that generates a log file, ideally a script, if this field is left empty, no build will be performed                                                                                                                                                                                                                                                                                      | SET DONTBUILD=true & tools\\jenkins\\build.bat                   |
| SYNC_BUILD_LOG_FILE                   | -sbf / --sync_build_log_file              | Either compile_commands.json or the default output of a build log                                                                                                                                                                                                                                                                                                                                       | build/a_target_dir/compile_commands.json                         |
| SYNC_TYPE_JSON_PATH_PATTERN_WHITELIST |                                           | File filter to apply as an inclusion mechanism (whitelist)                                                                                                                                                                                                                                                                                                                                              | .cpp$                                                            |
| *RCF_FILE                             |                                           | Path relative to project root or absolute to the RCF QAC configuration file or list of files. If several files are provided - contents of files will be merged into separate file. Merged file will be used in QAC projec creation                                                                                                                                                                      | helix/rcf/helix_ccda_config_cpp_1.4.rcf / ["helix/rcf/helix_ccda_config_cpp_1.4.rcf", "helix/rcf/helix2019.2_1.5.2_ccda_cpp.rcf"] |
| USE_PYTHON_BUILD_SHELL                | -pbs / --build_shell                      | If enabled command will be executed through the SHELL                                                                                                                                                                                                                                                                                                                                                   |                                                                  |
| USE_VSCODE_INTEGRATION                | -vsc / --vscode_integration               | If 'yes', then integrates output into VS-Code                                                                                                                                                                                                                                                                                                                                                           |                                                                  |
| USER_MESSAGES                         |                                           | Path relative to project root or absolute to the user messages configuration file or list of files. If several files are provided - contents of files will be merged into separate file. Merged file will be used in QAC project creation                                                                                                                                                               | helix/user_library/user_messages/messages.xml / ["helix/user_library/user_messages/messages_1.xml", "helix/user_library/user_messages/messages_2.xml"] |
| VCF_FILE                              |                                           | Path relative to project root or absolute to the RCF QAC configuration file                                                                                                                                                                                                                                                                                                                             | helix/acf/helix_ccda_config_git_1.0.xml                          |
| QACLI_POST_CREATE_COMMANDS            |                                           | List of commands to be executed after Helix QAC project creation                                                                                                                                                                                                                                                                                                                                        |                                                                  |
| WITH_ANALYSIS                         | -wa / --with_analysis                     | Generates analysis report. *Notice*: This parameter enables `WITH_STATE_FILE` parameter. Default is false                                                                                                                                                                                                                                                                                                                                                              | true                                                             |
| WITH_METRICS                          | -wm / --with_metrics                      | Generates metrics report. *Notice*: This parameter enables `WITH_STATE_FILE` parameter. Default is false                                                                                                                                                                                                                                                                                                                                                              | true                                                             |
| WITH_SUMMARY                          | -ws / --with_summary                      | Generates summary report. *Notice*: This parameter enables `WITH_STATE_FILE` parameter. Default is false                                                                                                                                                                                                                                                                                                                                                              | true                                                             |
| WITH_STATE_FILE                       | -wsf / --with_state_file                  | Generates state file. Default is false.                                                                                                                                                                                                                                                                                                                                                              | true                                                             |
| QACLI_VIEW_EXTRA_ARGS                 |                                           | List of extra arguments for qacli view subcommand                                                                                                                                                                                                                                                                                                                                                       |                                                                  |
| QAC_WITH_SUBDIAGNOSTICS               | -wsd / --with_subdiagnostics              | Generates report with light subdiagnostics included. Default is false                                                                                                                                                                                                                                                                                                                                   | true                                                             |
| QAC_WITH_FULL_SUBDIAGNOSTICS          | -wfsd / --with_full_subdiagnostics        | Generates report with full subdiagnostics included. Default is false                                                                                                                                                                                                                                                                                                                                    | true                                                             |

#### <a name="coverity-configuration-parameters">Coverity Configuration Parameters</a>

| Key                         | Command Line Argument           | Comment                                                                                                                                | Example                                                    |
| -                           | -                               | -                                                                                                                                      | -                                                          |
| BUILD_COMMAND               | -bc / --build_command           | Build command that runs full build, ideally a script. If `USE_COMPILE_COMMANDS_JSON` is specified the parameter is not used            | tools\\jenkins\\build.bat                                  |
| CODEOWNERS_FILE             | -cf / --codeowners_file         | Absolute path or relative to `PROJECT_ROOT` to the codeowners file                                                                     | C:/path/to/codeowners.txt                                  |
| *COVERITY_BIN_PATH          | -cbp / --coverity_bin_path      | Absolute path to the directory where Coverity binaries are                                                                             |                                                            |
| COVERITY_COMMIT_URL         |                                 | URL to the server with protocol and port                                                                                               | commit://abts5340.de.bosch.com:9090                        |
| COVERITY_COMMIT_DATAPORT    |                                 | Network TCP Port to be used while transferring data. *DEPRECATED*, keeping for compatibility reasons. Use `COVERITY_COMMIT_URL` instead| 9090                                                       |
| COVERITY_COMMIT_HOST        |                                 | Name of the server without protocol. *DEPRECATED*, keeping for compatibility reasons. Use `COVERITY_COMMIT_URL` instead                | abts5340.de.bosch.com                                      |
| COVERITY_COMMIT_STREAM      |                                 | Stream name to which to commit the defects                                                                                             | stream_name                                                |
| COVERITY_CONFIG_FILEPATH    | -ccf / --coverity_config_filepath | Path to covertiy configuration file. Can be absolute or relative to `PROJECT_ROOT`                                                   | path/to/coverity.conf                                      |
| COVERITY_RUN_DESKTOP_EXTRA_OPTIONS |                          | List of extra options to be passed to cov-run-desktop command                                                                          |                                                            |
| COV_ANALYZE_OPTION_LIST     |                                 | Optional coverity analysis commands according to [Coverity manual](https://abts55137.de.bosch.com:8443/doc/en/cov_command_ref.html)    |                                                            |
| COV_BUILD_OPTION_LIST       |                                 | Optional coverity build commands according to [Coverity manual](https://abts55137.de.bosch.com:8443/doc/en/cov_command_ref.html)       |                                                            |
| COV_EXPORT_WHITELIST        |                                 | Whitelist regexes that includes files to the analysis. Important: `COV_EXPORT_BLACKLIST` takes precedence over `COV_EXPORT_WHITELIST`  | *.c                                                        |
| COV_EXPORT_BLACKLIST        |                                 | Blacklist regexes that filters out files from the analysis. Important: `COV_EXPORT_BLACKLIST` takes precedence over `COV_EXPORT_WHITELIST` | *.cpp                                                  |
| COVERITY_AUTH_KEY_FILEPATH  | -akf / --auth_key_filepath      | Absolute path or relative to PROJECT_ROOT to an authentication key file, used for connecting to the Coverity Connect server            | /key/file                                                  |
| COVERITY_USERNAME           |                                 | Username provided to access server. Used in conjunction with the password. Must be provided as an environmental variable               |                                                            |
| COVERITY_PASSWORD           |                                 | Password provided to access server. Used in conjunction with the username. Must be provided as an environmental variable               |                                                            |
| COVERITY_WITH_NATIVE_HTML_REPORT | -wnhr / --with_native_html_report | Enables native Coverity html report generation                                                                                  |                                                            |
| *COVERITY_PROJECT_PATH      | -cpp / --coverity_project_path  | Specifies the project path relative to `PROJECT_ROOT`. Usually telling of the variant in usage                                         | msvc_coverity_2x.yz                                        |
| COMPILER_LIST               |                                 | List of compiler flags to be used for the analysis step                                                                                | ["--msvc"] for MSVC usage                                  |
| COMPILE_COMMANDS_BUILD_COMMAND | -ccbc / --compile_commands_build_command | The command that generates compile_commands.json. Effective only when `USE_COMPILE_COMMANDS_JSON` is set. Path to the generated compile_commands.json has to be provided in `COMPILE_COMMANDS_JSON` | C:/path/to/compile_commands_build_command.bat |
| COMPILE_COMMANDS_JSON       | -ccj / --compile_commands_json  | Path to compile_commands.json file. Effective only when `USE_COMPILE_COMMANDS_JSON` is set                                             | C:/path/to/compile_commands.json                           |
| DATASTORE_TARGET            | -dt / --datastore_target        | Target project to pull configurations from                                                                                             | msvc_coverity_2x.yz                                        |
| EXPORT_FORMATS              | -ef / --export_formats          | Defines the baseline export formats. Available formats: 'xlsx', 'csv', 'csv_zip', 'stdout', 'vscode' or 'all', where 'all' is a list of commonly used report formats: xlsx and csv. Default is 'all' |                                                            |
| GITIGNORE_MAPPING           | -gm / --gitignore_mapping       | Same as `ONLY_LAST_TEAM` parameter and is overridden if `ONLY_LAST_TEAM` is specified. Keeping for compatibility reasons for lucxbox users | true                                                       |
| INCLUDE_TRIAGE_HISTORY      | -ith / --include_triage_history | Include triage history into the report from Coverity View.                                                                             | true                                                       |
| INPUT_FILE_MATCHING_PATTERNS| -ifmp / --input_file_matching_patterns | Absolute path or relative to `PROJECT_ROOT` to a file which contains filter patterns of files to include in generated build script, one per line. In case `FILE_MATCHING_PATTERNS` is specified, list of patterns will be extended with patterns provided in `FILE_MATCHING_PATTERNS`                  | C:/path/to/file_matching_patterns.txt                |
| FILE_MATCHING_PATTERNS      | -fmp / --file_matching_patterns | Filter patterns of files to include in generated build script, separated with space. In case `INPUT_FILE_MATCHING_PATTERNS` is specified, list of patterns will be extended with patterns provided in file.                                                                  | [".*modules/core/src.*", ".*modules/lib.*"]                |
| FILTER_REPORT_OUTPUT_FILE   | -frof / --filter_report_output_file | Path to specified output file. Absolute or relative to `PROJECT_ROOT` paths can be used                                            |                                                            |
| MAXIMUM_PARALLEL_WORKERS    | -mpw / --maximum_parallel_workers   | Maximum number of parallel jobs to be executed in parallel workers                                         | 4                                               |
| ONLY_LAST_TEAM              | -olt / --only_last_team         | Include only the last matched team in the teams report                                                                                 | true                                                       |
| PREVIEW_REPORT_CSV          | -prcsv / --preview_report_csv   | Path to preview-report CSV export                                                                                                      |                                                            |
| *PROJECT_ROOT               | -pr / --project_root            | Path to project, relative from the location of the helper script                                                                       | /path/to/a/folder                                          |
| SKIP_EXIT_ON_ERROR          | -see / --skip_exit_on_error     | Ignore errors and continue execution if the return code is one of the space separated values                                           | 0 2 3                                                      |
| TO_STDOUT                   | -ts / --to_stdout               | Enables writing results to stdout. Otherwise, the results are overwrote to the file which is specified as filter report output file either from JSON configuration file, or from CLI |                                                            |
| TRANSLATION_UNITS_BLACKLIST |                                 | Optional translation units filter based on the Python Regex matching mechanism.                                                        |                                                            |
| TRIAGE_STORE                |                                 | Name of triage store                                                                                                                   |                                                            |
| USE_PYTHON_BUILD_SHELL      | -pbs / --build_shell            | Use python build shell for running the build command                                                                                   | true                                                       |
| USE_COMPILE_COMMANDS_JSON   | -uccj / --use_compile_commands_json | Use compile_commands.json compilation instead of `BUILD_COMMAND`                                                                     |                                                            |
| WEBAPI_PROJECT_NAME         |                                 | The name of the WEBAPI project to be used with the upload                                                                              | lorem_ipsum_project                                        |
| WEBAPI_VIEW_NAME            |                                 | The name of the WEBAPI view to be used                                                                                                 | lorem_ipsum_view                                           |
| WEBAPI_URL                  |                                 | The base URL of the server to connect to                                                                                               | https://abts5340.de.bosch.com:8443                         |
| WITH_CID                    | -wc / --with_cid                | Use to run export_analysis command. Generates cov-commit-defects preview report and adds "cid" information in project state             | true                                                       |

#### <a name="find-includes-configuration-parameters">Find Includes Configuration Parameters</a>


| Key                            | Command Line Argument                | Comment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Example                                      |
| ------------------------------ | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| CODE_DIRS_FILE                 | -cdf / --code_dirs_file              | Absolute path or relative path (relative to project repo folder) of a text file OR an array, which contains folders to be searched for find_includes                                                                                                                                                                                                                                                                                                                                               | C:/path/to/code_dirs.txt                     |
| BLACKLIST_PATTERN              | -bp / --blacklist_pattern            | Absolute path or relative path (relative to project repo folder) of a text file OR an array, which contains blacklist pattern                                                                                                                                                                                                                                                                                                                                                                      | C:/path/to/blacklist_pattern.txt             |
| FIND_INCLUDE_STRATEGY          | -fis / --find_include_strategy       | Defines how many c/cpp files to produce for a given header. Can be one of ('all', 'minimal'). If 'all', a list of all c/cpp which include the given h/hpp/inl files (directly or indirectly) are produced. If 'minimal', then at least one c/cpp file will be produced                                                                                                                                                                                                                             | "all"                                        |
| FIND_INCLUDES_GIT_DIFF_FILTER  | -gdf / --git_diff_filter             | Git diff filter used to identify changed files. It is 'rd' by default                                                                                                                                                                                                                                                                                                                                                                                                                              | "rd"                                         |
| FROM_LIST                      | -fl / --from_list                    | Absolute path or relative to PROJECT_ROOT to a file OR a list that contains list of source files desired for scan, to determine 'include' directive of a given headers. Every cpp file in the input list is also written to the output list, while for every hpp/inl file in the input list, either _all_ cpp files which (directly or indirectly) include that header file are written to the output list (option "all"), or _one_ such cpp file is written to the output list (option "minimal") | path/to/find_includes_source_files_list.txt  |
| FROM_STDIN                     | -fs / --from_stdin                   | List of source files desired for scan is read in from stdin                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                              |
| HEADER_EXTENSIONS              |                                      | List of header extensions to find includes from. By default is (".hpp", ".h", ".inl")                                                                                                                                                                                                                                                                                                                                                                                                              |                                              |
| MERGE_BASE                     | -mb / --merge_base                   | Branch the diff is made against                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | origin/develop                               |
| OUTPUT_FILE                    | -of / --output_file                  | Path to a file that contains list of source files desired for scan, to determine 'include' directive of a given headers. In further step this list is used in QAC analysis. If value is not defined, helper will use the value of 'ANALYZE_LIST' parameter                                                                                                                                                                                                                                         | path/to/sca_tools_file_list.txt              |
| *PROJECT_ROOT                  | -pr / --project_root                 | Path to project, relative from the location of the helper script                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                              |
| SOURCE_EXTENSIONS              |                                      | List of file extensions, to filter files that are considered for scan on 'include' directive of a header files given in input list for 'find_includes' helper target                                                                                                                                                                                                                                                                                                                               | ".cpp", ".c", ".inl"                         |
| SOURCE_OUTPUT_EXTENSIONS       |                                      | List of file extensions, to filter files that are kept in a 'find_includes' helper target result output                                                                                                                                                                                                                                                                                                                                                                                            | ".cpp", ".c"                                 |
| THIRDPARTY_PREFIXES            | -tp / --thirdparty_prefixes          | Absolute path to a file that contains a list with 3rdparty prefixes that will be excluded from the scan on includes or a list of prefixes                                                                                                                                                                                                                                                                                                                                                          | C:/path/to/exclude_prefixes.txt              |
| TO_STDOUT                      | -ts / --to_stdout                    | List of source files desired for scan plus all files which are dependend on these files, which also will be scanned. This list is written to stdout                                                                                                                                                                                                                                                                                                                                                |                                              |
| WITH_MAPPING_REPORT            | -wmr / --with_mapping_report         | Path to an XLSX report file. If specified, it changes find_includes behaviour to generate a mapping headers to compilation units report                                                                                                                                                                                                                                                                                                                                                            |                                              |


#### <a name="map-teams-configuration-parameters">Map Teams Configuration Parameters</a>
| Key                            | Command Line Argument                | Comment                                                                                                                                                                                        | Example                                      |
| ------------------------------ | ------------------------------------ | -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| -------------------------------------------- |
| *CODEOWNERS_FILE               | -cf / --codeowners_file              | Absolute path or relative to PROJECT_ROOT to the codeowners file                                                                                                                               | C:/path/to/codeowners.txt                    |
| FIELD_DELIMITER                | -fd / --field_delimiter              | Character used to separate fields. Can be one of (",", ";", ":", "\|"). Defauilt is ","                                                                                                        | ","                                          |
| GITIGNORE_MAPPING              | -gm / --gitignore_mapping            | Same as "ONLY_LAST_TEAM" parameter and is overridden if "ONLY_LAST_TEAM" is specified. Keeping for compatibility reasons for lucxbox users | true                                         |
| *INPUT_WARNINGS_REPORT         | -iwr / --input_warnings_report       | Absolute path or relative to PROJECT_ROOT to the input report file with warnings in CSV format. Any report we want to fit Team and Component information and map it by mapping column          | C:/path/to/warnings_report.csv               |
| MAPPING_COLUMN                 | -mc / --mapping_column               | Column name for mapping. Usually this is "File", "FilePath", etc. Default is "Filename"                                                                                                        | "Filename"                                   |
| ONLY_LAST_TEAM                 | -olt / --only_last_team              | Include only the last matched team in the teams report                                                                                 | true                                                       |
| PROJECT_ROOT                   | -pr  / --project_root                | Absolute path to a directory used to resolve all relative paths provided as configuration options to the subcommand                                                                            | C:/path/to/directory                         |
| *TEAMS_REPORT                  | -tr / --teams_report                 | Absolute path or relative to PROJECT_ROOT to the output CSV report file. Output format is based on dialect provided in the input file                                                          | true                                         |


#### <a name="compiler-warnings-configuration-parameters">Compiler Warnings Configuration Parameters</a>
| Key                               | Command Line Argument                       | Comment                                                                                                                                                                                                                                                                                    | Example                                      |
| --------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------- |
| BLACK_LIST                        | -bl / --black_list                          | Mention the black list files for which warnings are not be considered                                                                                                                                                                                                                      | some/path                                    |
| CHANGED_FILES                     | -ch / --changed_files                       | Files containing a list of changed files                                                                                                                                                                                                                                                   | ['file1', 'file2']                           |
| CODEOWNERS_FILE                   | -cf / --codeowners_file                     | Absolute path or relative to PROJECT_ROOT to the codeowners file. Accepts single path or list of paths                                                                                                                                                                                     | path/to/codeowners                           |
| *COMPILER                         | -c / --compiler                             | Compiler name. Possible values are 'clang', 'msvc' or 'greenhills'                                                                                                                                                                                                                         | msvc                                         |
| *COMPILER_LOG                     | -cl / --compiler_log                        | Path to compiler log file to parse the warnings from (globbing is allowed)                                                                                                                                                                                                                 | path/to/compiler_log                         |
| COMPILER_WARNINGS_MAPPING_COLUMN  | -mc / --mapping_column                      | Column name for mapping. Usually this is "File", "FilePath", etc. Default is "Filename"                                                                                                                                                                                                    | 'FilePath'                                   |
| COMPILER_WARNINGS_REPORT_BASENAME | -rb / --report_basename                     | Base name of compiler warnings report                                                                                                                                                                                                                                                      | basename                                     |
| COMPILER_WARNINGS_REPORT_DIR      | -rd / --report_dir                          | Absolute or relative to PROJECT_ROOT path where compiler warning reports are generated                                                                                                                                                                                                     | path/to/report/dir                           |
| EXPORT_FORMATS                    | -ef / --export_formats                      | Set export formats. Possible formats are 'xlsx', 'csv' or 'json'                                                                                                                                                                                                                           | 'xlsx'                                       |
| GITIGNORE_MAPPING                 | -gm / --gitignore_mapping                   | Same as "-olt / --only_last_team" argument and is overridden if "-olt / --only_last_team" is specified. Keeping for compatibility reasons for lucxbox users. "GITIGNORE_MAPPING" / -gm / --gitignore_mapping is deprecated. Please use "ONLY_LAST_TEAM" / -olt / --only_last_team instead  |                                              |
| JOBS                              | -j / --jobs                                 | Number of threads                                                                                                                                                                                                                                                                          | 4                                            |
| ONLY_LAST_TEAM                    | -olt / --only_last_team                     | Include only the last matched team in the teams report                                                                                                                                                                                                                                     |                                              |
| OUTPUT                            | -o / --output                               | Path to output file to log the warnings existing on the changed files                                                                                                                                                                                                                      | path/to/output.log                           |
| QUIET                             | -q / --quiet                                | Print only errors                                                                                                                                                                                                                                                                          |                                              |
| TARGET_DIRECTORY                  | -td / --target_directory                    | List of paths (separated by space) to include warning only from specified locations                                                                                                                                                                                                        | path/to/target/folder                        |
| THRESHOLD                         | -t / --threshold                            | Threshold of allowed overall warnings before script returns non-zero exit code                                                                                                                                                                                                             | 2                                            |
| THRESHOLD_FILE                    | -tf / --threshold_file                      | Threshold file which lists thresholds for each warning name. Threshold file is a json                                                                                                                                                                                                      | path/to/threshold.json                       |
| TYPES_DB                          | -tdb / --types_db                           | Compiler warning types database file (json)                                                                                                                                                                                                                                                | path/to/types_db.json                        |
| USE_RELATIVE_PATHS                | -rp / --use_relative_paths                  | Use relative file paths when mapping components                                                                                                                                                                                                                                            |                                              |


## <a name="qac-example-json">Example qac.json</a>

  _Example qac.json (filepaths are absolute in this case but could be relative to project_root (commandline defined)_
  ```json
{
    "QAC_CONFIG_PATH": "C:/path_to_proj/config",
    "RCF_FILE": "helix_ccda_config_cpp_1.6.rcf",
    "ACF_FILE": "helix_ccda_config_cpp_1.6.acf",
    "VCF_FILE": "helix_ccda_config_git_1.0.xml",

    "test_1_4": {
      "QAC_PROJECT_PATH": "C:/path_to_proj/helix_project",
      "SYNC_BUILD_LOG_FILE": "samples/bin_gcc/compile_commands.json",
      "SYNC_TYPE": "JSON",
      "SYNC_TYPE_JSON_PATH_PATTERN_WHITELIST": "\\.cpp$",
      "SYNC_BUILD_COMMAND": "powershell.exe scripts\\build.ps1 -compiler gcc",
      "ACF_FILE": "C:/path_to_proj/config/acf/helix_ccda_config_cpp_1.4.acf",
      "NCF_FILE": "C:/path_to_proj/config/ncf/helix_ccda_config_cpp_naming_1.0.ncf",
      "USER_MESSAGES": "messages.xml",
      "CUSTOM_HELP_PATH": "",
      "COMPILER_LIST": [
        "GNU_GCC-g++_5.3-x86_64-w64-mingw32-C++-c++11.cct"
      ],
      "ANALYZE_PARAMS": "--file-based-analysis --force-complete -I",
      "QAC_MODULES": ["qacpp-4.5.0"],
      "QAC_SYNC_PATH_BLACKLIST": [],
      "QAC_ANALYSIS_PATH_BLACKLIST": ["build","dc_apl_test","ip_if","ip_vmc","ip_mom","rc_fw"],
      "LOCAL_BASELINE_PATH": "",
      "FROM_LIST": "C:/path_to_proj/find_includes_source_files_list.txt",
      "OUTPUT_FILE": "C:/path_to_proj/sca_tools_file_list.txt",
      "FIND_INCLUDE_STRATEGY": "all",
      "SOURCE_FILE_EXTENSIONS": [".cpp", ".c", ".inl"],
      "SOURCE_FILE_OUTPUT_EXTENSIONS": [".cpp", ".c"],
      "HEADER_EXTENSIONS": [".hpp", ".h", ".inl"],
      "CODE_DIRS_FILE": "",
      "MERGE_BASE": "origin/develop",
      "THIRDPARTY_PREFIXES": "",
      "BLACKLIST_PATTERN": "",
      "UNIT_TEST_FILE_PATTERN": ".*_(test|unittest|cantata)_.*"
    }
}
```

_IF YOU THINK THERE IS A VALUE MISSING PLEASE CONTACT THE MAINTAINERS FIRST BEFORE CHANGING THE SCRIPT_.

### <a name="sca-tool-py">sca_tools.py</a>

Usage is explained in the script help output. Run python sca_tools.py.

It supports the following sub-commands:

* qac - interacts with QAC, supports following sub-commands:
  * create - creates QAC project
  * create_baseline - creates baseline with hashsum
  * analyze - analyzes QAC project
  * export_analysis - Generates project state based on analysis results. Additionally, exports reports based on state file,
  if any (or combination) of following arguments is provided: '--with_analysis', '--with_summary', '--with_metrics'
  * report - generates QAC analysis report
  * gui - opens project in QAC GUI
  * qavupload - uploads QAC project to QAView
  * s101gen - geterates s101 structure
  * state - generates project state report with metrics
  * export_state - exports state information
  * fix_cl_json - removes special characters from a given JSON file
  * filter_qaview - parses the export of QAC for which severity levels are contained in the export and then fail or pass the build on jenkins
  * export_analysis - generates project state based on analysis results
* coverity - interacts with Coverity, supports following sub-commands:
  * create - creates Coverity project
  * analyze - performs code analysis on a specified project using cov-analyze command
  * run_desktop - performs code analysis of all captured sources of a specified project using cov-run-desktop command
  * export - generates analysis result report
  * export_analysis - generates project state based on analysis results
  * upload - uploads analysis report and source data to the Coverity Connect database in a specified stream
  * preview_report - instead of sending files cross-references, and other assets to the Coverity Connect server, this option sends only the defect occurrences. The server returns a commit preview report, which is written in JSON format
  * webapi_export - exports specified view report from Coverity Connect. If '--include_triage_history' argument is provided, then triage history will be included into view report
  * check_buildlog - shows project build log
  * filter_report - parses the export of preview_report subcommand for which new triage classifications found
  and then fail or pass the build on jenkins
* find_includes - runs find_includes functionality
* map_teams - extends provided warnings report with teams and components information using codeowners file
* compiler_warnings - compiler warnings parser with multiple format export possibilities

There are available arguments in the helper below.

### <a name="arguments-general">General Arguments</a>

| Argument                              | Comment                                                                                                                                                 | Sources and Type     |
|---------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| -d / --debug                          | Enable debug mode.                                                                                                                                      | Arg, Optional        |

### <a name="arguments-common">Common arguments for all subcommands</a>

| Argument                 | Comment                                    | Sources and Type |
|--------------------------|--------------------------------------------|------------------|
| -dp / --datastore_path   | Path to configuration file                 | Arg, Optional   |
| -dt / --datastore_target | Target project to pull configurations from | Arg, Optional    |
| -pr / --project_root     | Path to project, relative from the location of the helper script | Arg, Optional  |

### SCA subcommands that support additional arguments

Some of the subcommands have additional arguments of their own and can be configured so.

#### <a name="arguments-qac">Common arguments for all *qac* subcommands</a>


| Argument                   | Comment                                                                                                                              | Sources and Type |
| -                          | -                                                                                                                                    | -                |
| -qac / --qac_bin_path      | Path to the directory where QAC is installed                                                                                         | Arg, Optional    |
| -qaf / --qac_config_path   | Absolute path or relative to PROJECT_ROOT to the QAC preferred configurations search path. Accepts single path or list of paths      | Arg, Optional    |
| -qap / --qac_project_path  | Path to a QAC project directory                                                                                                      | Arg, Optional    |
| -qll / --qac_logging_level | Set verbosity of the QAC output, can be one of ('NONE', 'ERROR', 'INFO', 'DEBUG', 'TRACE'). Default is 'ERROR'                       | Arg, Optional    |


#### *'create'* subcommand arguments

| Argument                                 | Comment                                                                                                                                                 | Sources and Type    |
| -                                        | -                                                                                                                                                       | -                   |
| -do / --disable_optimization             | Disables QAC project optimization. Enabled by default                                                                                                   | Arg, Optional       |
| -hprd / --help_pages_root_dir            | Root directory where help pages in HTML format are located. If specified, it creates custom configuration files where paths to help pages are set for all messages accordingly. | Arg, Optional |
| -hsb / --helper_set_baseline             | If specified, it will set an baseline when creating a new project from the baseline path                                                                | Arg, Optional       |
| -hsc / --helper_suppress_c_header        | If set to a yes value all C headers .h will be ignored in the anaylsis                                                                                  | Arg, Optional       |
| -hrfl / --helper_remove_file_list        | Give the absolute path or relative path (relative to project repo folder) of a text file, which contains list of files to be removed from the project   | Arg, File, Optional |
| -hsfa / --helper_suppress_file_list_a    | Give the absolute path or relative path (relative to project repo folder) of a text file, which contains list of files to be excluded from the analysis | Arg, File, Optional |
| -hsfs / --helper_suppress_file_list_s    | Give the absolute path or relative path (relative to project repo folder) of a text file, which contains list of files to be excluded from the sync     | Arg, File, Optional |
| -iv / --ignore_validation                | If provided will bypass QAC components validation mechanisms                                                                                            | Arg, Optional       |
| -pbs / --build_shell                     | Uses shell for running a build command                                                                                                                  | Arg, Optional       |
| -sbc / --sync_build_command              | Build command that generates a log file, ideally a script, if this field is left empty, no build will be performed                                      | Arg, Optional       |
| -sbf / --sync_build_log_file             | If specified, it uses the following json build log as input to create a QAC project. It will override the build log settings from the config file       | Arg, Optional       |
| -coc / --cleanup_on_create               | Defines wether the project will be cleansed on creation or not. False by default                                                                        | Arg, Optional       |
| -caac / --c_files_analyzed_as_c          | Enable analysis of C files as C instead of C++. By default the C files are analyzed according to the C++ configs                                        | Arg, Optional       |
| -seb / --skip_exit_on_build_return_codes | If set, the script does not exit after a build when one of the specified return codes is a result e.g. -seb 0 2                                         | Arg, Optional       |
| -mpw / --maximum_parallel_workers        | Maximum number of parallel jobs to be executed in parallel workers                                                                                      | Arg, Optional       |

#### *'analyze'* subcommand arguments

| Argument                                    | Comment                                                                                                                                                  | Sources and Type      |
| --------------------------------------      | -------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| -af / --analyze_file                        | Analyzes the given file                                                                                                                                  | Arg, Optional         |
| -al / --analyze_list                        | Path to a file that contains list of files to be analyzed. Can be absolute or relative to `PROJECT_ROOT`                                                 | Arg, Optional         |
| -hcb / --helper_create_baseline             | If specified, a baseline will be created after an analysis run                                                                                           | Arg, Optional         |
| -see / --skip_exit_on_analysis_return_codes | If set, the script does not exit after an analysis if its one of the specified return codes e.g. -see 3 9                                                | Arg, Optional         |
| -vsc / --vscode_integration                 | If 'yes', then integrates output into VS-Code                                                                                                            | Arg, Optional         |

#### *'export_analysis'* subcommand arguments
| Argument                              | Comment                                                                                                                                                                                                                                                                  | Sources and Type |
|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| -cf / --codeowners_file               | Absolute path or relative to PROJECT_ROOT to the codeowners file. Accepts single path or list of paths                                                                                                                                                                   | Arg, Optional    |
| -cdo / --cleanup_diagnostics_output   | A boolean to remove QACLI diagnostics output XML files                                                                                                                                                                                                                   | Arg, Optional    |
| -ef / --export_formats                | Defines the report export formats. Available formats: 'xlsx', 'csv', 'csv_zip', 'html' or 'all', where 'all' is a list of commonly used report formats: xlsx, csv and html. Extra formats can be specified explicitly, e.g. -ef all csv_zip. Default is 'all'            | Arg, Optional    |
| -fsf / --from_state_file              | An option/flag to generate reports based on state file. If path is given - reads state from specified path. If is set to true - uses default state file path                                                                                                             | Arg, Optional    |
| -gm / --gitignore_mapping             | Same as "-olt / --only_last_team" argument and is overridden if "-olt / --only_last_team" is specified. Keeping for compatibility reasons for lucxbox users                                                                                                              | Arg, Optional    |
| -mfl / --metrics_filter_list          | Metrics to be included in generated metrics report, e.g. "STPTH" "STPAR"                                                                                                                                                                                                 | Arg, Optional    |
| -olt / --only_last_team               | Include only the last matched team in the teams report                                                                                                                                                                                                                   | Arg, Optional    |
| -wa  / --with_analysis                | Generates analysis report. *Notice*: This option enables `with_state_file` option                                                                                                                                                                                        | Arg, Optional    |
| -wm  / --with_metrics                 | Generates metrics report. *Notice*: This option enables `with_state_file` option                                                                                                                                                                                         | Arg, Optional    |
| -ws  / --with_summary                 | Generates summary report. *Notice*: This option enables `with_state_file` option                                                                                                                                                                                         | Arg, Optional    |
| -wsd / --with_subdiagnostics          | Generates report with light subdiagnostics included                                                                                                                                                                                                                      | Arg, Optional    |
| -wsf  / --with_state_file             | Generates state file                                                                                                                                                                                                                                                     | Arg, Optional    |
| -wfsd / --with_full_subdiagnostics    | Generates report with full subdiagnostics included                                                                                                                                                                                                                       | Arg, Optional    |

#### *'qavupload'* subcommand arguments

| Argument                              | Comment                                                                                                                                                 | Sources and Type     |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| -qpn / --qav_project_name             | QAVerify project name                                                                                                                                   | Arg, Optional        |
| -qps / --qav_project_snapshot         | QAVerify project snapshot name                                                                                                                          | Arg, Optional        |
| -qsu / --qav_server_url               | QAVerify server URL                                                                                                                                     | Arg, Optional        |
| -qus / --qav_upload_source            | QAVerify upload source directory                                                                                                                        | Arg, Optional        |

#### *'state'* subcommand arguments

| Argument                              | Comment                                                                                                                                                                                                                                                                          | Sources and Type     |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| -cf / --codeowners_file               | Absolute path or relative to PROJECT_ROOT to the codeowners file. Accepts single path or list of paths                                                                                                                                                                           | Arg, Optional        |
| -cdo / --cleanup_diagnostics_output   | A boolean to remove QACLI diagnostics output XML files                                                                                                                                                                                                                           | Arg, Optional        |
| -ef / --export_formats                | Defines the report export formats. Available formats: 'xlsx', 'csv', 'csv_zip', 'html' or 'all', where 'all' is a list of commonly used report formats: xlsx, csv and html. Extra formats can be specified explicitly, e.g. -ef all csv_zip. Default is 'all'                    | Arg, Optional        |
| -gm / --gitignore_mapping             | Same as "-olt / --only_last_team" argument and is overridden if "-olt / --only_last_team" is specified. Keeping for compatibility reasons for lucxbox users                                                                                                                      | Arg, Optional        |
| -mfl / --metrics_filter_list          | Metrics to be included in generated metrics report, e.g. "STPTH" "STPAR"                                                                                                                                                                                                         | Arg, Optional        |
| -olt / --only_last_team               | Include only the last matched team in the teams report                                                                                                                                                                                                                           | Arg, Optional        |
| -wm  / --with_metrics                 | Generate metrics report                                                                                                                                                                                                                                                          | Arg, Optional        |
| -wsd / --with_subdiagnostics          | Generates report with light subdiagnostics included                                                                                                                                                                                                                              | Arg, Optional        |
| -wfsd / --with_full_subdiagnostics    | Generates report with full subdiagnostics included                                                                                                                                                                                                                               | Arg, Optional        |

#### *'export_state'* subcommand arguments

| Argument                              | Comment                                                                                                                                                                                                                                                                          | Sources and Type     |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| -cf / --codeowners_file               | Absolute path or relative to PROJECT_ROOT to the codeowners file. Accepts single path or list of paths                                                                                                                                                                           | Arg, Optional        |
| -ef / --export_formats                | Defines the report export formats. Available formats: 'xlsx', 'csv', 'csv_zip', 'html' or 'all', where 'all' is a list of commonly used report formats: xlsx, csv and html. Extra formats can be specified explicitly, e.g. -ef all csv_zip. Default is 'all'                    | Arg, Optional        |
| -gm / --gitignore_mapping             | Same as "-olt / --only_last_team" argument and is overridden if "-olt / --only_last_team" is specified. Keeping for compatibility reasons for lucxbox users                                                                                                                      | Arg, Optional        |
| -mfl / --metrics_filter_list          | Metrics to be included in generated metrics report, e.g. "STPTH" "STPAR"                                                                                                                                                                                                         | Arg, Optional        |
| -olt / --only_last_team               | Include only the last matched team in the teams report                                                                                                                                                                                                                           | Arg, Optional        |
| -wm  / --with_metrics                 | Generate metrics report                                                                                                                                                                                                                                                          | Arg, Optional        |

#### *'fix_cl_json'* subcommand arguments

| Argument                              | Comment                                                                                                                                                 | Sources and Type     |
|---------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| -icj / --input_cl_json                | Path to a JSON file that should be modified                                                                                                             | Arg, Mandatory       |

#### *'filter_qaview'* subcommand arguments

| Argument                                                      | Comment                                                                                                                                                                     | Sources and Type |
| -                                                             | -                                                                                                                                                                           | -                |
| -qacsv / --qaview_csv                                         | Path to qaview CSV export                                                                                                                                                   | Arg, Optional    |
| -i / --ignore_ids                                             | Error IDs that can be ignored (comma-separated values without whitespaces)                                                                                                  | Arg, Optional    |
| -jmre/ --justification_message_regexp                         | Regular expression(s) for suppressed Justification messages.                                                                                                                | Arg, Optional    |
| -f{level} / --severity_level_fail_threshold_for_level_{level} | Script will fail if warnings exceed the provided threshold (where {level} in 0..9)                                                                                          | Arg, Optional    |
| -frof / --filter_report_output_file                           | Write results to specified output file. Absolute or relative to repo root paths can be used                                                                                 | Arg, Optional    |
| -ts / --to_stdout                                             | Write results to stdout. Otherwise, the results are overwrote to the file which is specified as filter report output file either from JSON configuration file, or from CLI  | Arg, Optional    |
| -twr / --threshold_warnings_report                            | Path to threshold warnings report                                                                                                                                           | Arg, Optional    |

#### *'export_analysis'* subcommand arguments

| Argument                              | Comment                                                                                      | Sources and Type |
| -                                     | -                                                                                            | -                |
| -cdo / --cleanup_diagnostics_output   | A boolean to remove QACLI diagnostics output XML files                                       | Arg, Optional    |

#### <a name="arguments-coverity">Common arguments for all *coverity* subcommands</a>
| Argument                       | Comment                                                                                                                      | Sources and Type |
| -                              | -                                                                                                                            | -                |
| -cpp / --coverity_project_path | This value overrides the project path specified in json datastore                                                            | Arg, Optional    |
| -cbp / --coverity_bin_path     | Absolute path to the directory where Coverity binaries are                                                                   | Arg, Optional    |

#### *'create'* subcommand arguments

| Argument                                  | Comment                                                                                                                                         | Sources and Type |
| -                                         | -                                                                                                                                               | -                |
| -bc / --build_command                     | Build command that runs full build, ideally a script. If `USE_COMPILE_COMMANDS_JSON` is specified the parameter is not used                     | Arg, Optional    |
| -ccj / --compile_commands_json            | Path to compile_commands.json file. Effective only when `USE_COMPILE_COMMANDS_JSON` is set                                                      | Arg, Optional    |
| -fmp / --file_matching_patterns           | Filter patterns of files to include in filtered compile_commands.json file, separated with space. E.g.: ".*modules/core/src.*"                  | Arg, Optional    |
| -ifmp / --input_file_matching_patterns    | Absolute path or relative to `PROJECT_ROOT` to a file which contains filter patterns of files to include in filtered compile_commands.json file | Arg, Optional    |
| -pbs / --build_shell                      | Use python build shell for running the build command                                                                                            | Arg, Optional    |
| -see / --skip_exit_on_error               | Ignore errors and continue execution                                                                                                            | Arg, Optional    |
| -ccbc / --compile_commands_build_command  | The command that generates compile_commands.json                                                                                                | Arg, Optional    |
| -uccj / --use_compile_commands_json       | If provided will use compile_commands.json compilation instead of `BUILD_COMMAND`                                                               | Arg, Optional    |
| -mpw / --maximum_parallel_workers         | Maximum number of parallel jobs to be executed in parallel workers                                                                              | Arg, Optional    |

#### *'run_desktop'* subcommand arguments

| Argument                                  | Comment                                                                                                                                         | Sources and Type |
| -                                         | -                                                                                                                                               | -                |
| -akf / --auth_key_filepath                | Absolute path or relative to PROJECT_ROOT to an authentication key file, used for connecting to the Coverity Connect server                     | Arg, Optional    |
| -ccf / --coverity_config_filepath         | Path to covertiy configuration file. Can be absolute or relative to `PROJECT_ROOT`                                                              | Arg, Optional    |

#### *'export'* subcommand arguments
| Argument                           | Comment                                                                                                                                                                                                                                                                                         | Sources and Type |
|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| -cf / --codeowners_file            | Absolute path or relative to PROJECT_ROOT to the codeowners file. Accepts single path or list of paths                                                                                                                                                                                          | Arg, Optional    |
| -ef / --export_formats             | Defines the baseline export formats for format-errors and format-errors-filtered (if TRANSLATION_UNITS_BLACKLIST parameter is set) reports. Available formats: 'xlsx', 'csv', 'csv_zip', 'stdout', 'vscode' or 'all', where 'all' is a list of commonly used report formats: xlsx and csv       | Arg, Optional    |
| -gm / --gitignore_mapping          | Same as "-olt / --only_last_team" argument and is overridden if "-olt / --only_last_team" is specified. Keeping for compatibility reasons for lucxbox users                                                                                                                                     | Arg, Optional    |
| -olt / --only_last_team            | Include only the last matched team in the teams report                                                                                                                                                                                                                                          | Arg, Optional    |
| -wnhr / --with_native_html_report  | Enables native Coverity html report generation                                                                                                                                                                                                                                                  | Arg, Optional    |

#### *'export_analysis'* subcommand arguments
| Argument                        | Comment                                                                                      | Sources and Type |
|---------------------------------|----------------------------------------------------------------------------------------------|------------------|
| -wc / --with_cid                | Generates cov-commit-defects preview report and adds "cid" information in project state      | Arg, Optional    |

#### *'upload'* subcommand arguments
| Argument                        | Comment                                                                                                                                                                                                                                                                                     | Sources and Type |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| -akf / --auth_key_filepath      | Absolute path or relative to PROJECT_ROOT to an authentication key file, used for connecting to the Coverity Connect server                                                                                                                                                                 | Arg, Optional    |

#### *'preview_report'* subcommand arguments
| Argument                        | Comment                                                                                                                                                                                                                                                                                     | Sources and Type |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| -akf / --auth_key_filepath      | Absolute path or relative to PROJECT_ROOT to an authentication key file, used for connecting to the Coverity Connect server                                                                                                                                                                 | Arg, Optional    |
| -cf / --codeowners_file         | Absolute path or relative to PROJECT_ROOT to the codeowners file. Accepts single path or list of paths                                                                                                                                                                                      | Arg, Optional    |
| -ef / --export_formats          | Defines the baseline export formats for preview and preview-filtered (if TRANSLATION_UNITS_BLACKLIST parameter is set) reports. Available formats: 'xlsx', 'csv', 'csv_zip', 'stdout', 'vscode' or 'all', where 'all' is a list of commonly used report formats: xlsx and csv.              | Arg, Optional    |
| -gm / --gitignore_mapping       | Same as "-olt / --only_last_team" argument and is overridden if "-olt / --only_last_team" is specified. Keeping for compatibility reasons for lucxbox users                                                                                                                                 | Arg, Optional    |
| -olt / --only_last_team         | Include only the last matched team in the teams report                                                                                                                                                                                                                                      | Arg, Optional    |

#### *'webapi_export'* subcommand arguments
| Argument                        | Comment                                                                                                                                                                                  | Sources and Type |
|---------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| -ef / --export_formats          | Defines the baseline export formats. Available formats: 'xlsx', 'csv', 'csv_zip', 'stdout', 'vscode' or 'all', where 'all' is a list of commonly used report formats: xlsx and csv       | Arg, Optional    |
| -ith / --include_triage_history | Include triage history into the report from Coverity View                                                                                                                                | Arg, Optional    |

#### *'filter_report'* subcommand arguments

| Argument                                                      | Comment                                                                                                                                                                    | Sources and Type |
| -                                                             | -                                                                                                                                                                          | -                |
| -prcsv / --preview_report_csv                                 | Path to preview-report CSV export                                                                                                                                          | Arg, Optional    |
| -frof / --filter_report_output_file                           | Write results to specified output file. Absolute or relative to repo root paths can be used                                                                                | Arg, Optional    |
| -ts / --to_stdout                                             | Write results to stdout. Otherwise, the results are overwrote to the file which is specified as filter report output file either from JSON configuration file, or from CLI | Arg, Optional    |


### <a name="arguments-find-includes">Find-includes subcommand arguments</a>

| Argument                        | Comment                                                                                                                                                                                                                                                                | Sources and Type      |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                                               | --------------------- |
| -cdf / --code_dirs_file         | Absolute path to a file that contains a list with folders (relative to the repo root) that should be scanned on includes                                                                                                                                               | Arg, Optional         |
| -fis / --find_include_strategy  | Specify how many c/cpp files to produce for a given header. Can be one of ('all', 'minimal'). If 'all', a list of all c/cpp which include the given h/hpp/inl files (directly or indirectly) are produced. If 'minimal', then at least one c/cpp file will be produced | Arg, Optional         |
| -fl / --from_list               | Path to a file that contains list of source files desired for scan, to determine 'include' directive of a given headers                                                                                                                                                | Arg, Optional         |
| -fs / --from_stdin              | Read list of source files that are desired for scan on includes from stdin                                                                                                                                                                                             | Arg, Optional         |
| -gdf / --git_diff_filter        | Git diff filter used to identify changed files. It is 'rd' by default                                                                                                                                                                                                  | Arg, Optional         |
| -bp / --blacklist_pattern       | Absolute path to a file that contains only one line with a pattern for the file blacklist pattern                                                                                                                                                                      | Arg, Optional         |
| -mb / --merge_base              | Branch the diff is made against, default is 'origin/develop'                                                                                                                                                                                                           | Arg, Optional         |
| -of / --output_file             | Path to a file, in which list of source files, produced by 'find_includes' subcommand is written                                                                                                                                                                       | Arg, Optional         |
| -tp / --thirdparty_prefixes     | Absolute path to a file that contains a list with 3rdparty prefixes that will be excluded from the scan on includes                                                                                                                                                    | Arg, Optional         |
| -ts / --to_stdout               | Write result list of source files produced by 'find_includes' subcommand to stdout                                                                                                                                                                                     | Arg, Optional         |
| -wmr / --with_mapping_report    | Path to an XLSX report file. If specified, it changes find_includes behaviour to generate a mapping headers to compilation units report                                                                                                                                | Arg, Optional         |



### <a name="arguments-map-teams">Map-Teams subcommand arguments</a>

| Argument                           | Comment                                                                                                                          | Sources and Type |
| -                                  | -                                                                                                                                | -                |
| -iwr  / --input_warnings_report    | Absolute path or relative to PROJECT_ROOT to the input report file with warnings in CSV format                                   | Arg, Optional    |
| -cf / --codeowners_file            | Absolute path or relative to PROJECT_ROOT to the codeowners file. Accepts single path or list of paths                           | Arg, Optional    |
| -tr / --teams_report               | Absolute path or relative to PROJECT_ROOT to the output CSV report file                                                          | Arg, Optional    |
| -mc / --mapping_column             | Column name for mapping. Usually this is "File", "FilePath", etc. Default is "Filename"                                          | Arg, Optional    |
| -fd / --field_delimiter            | Character used to separate fields. Can be one of (",", ";", ":", "\|"). Defauilt is ","                                          | Arg, Optional    |
| -gm / --gitignore_mapping          | Same as "-olt / --only_last_team" argument. Keeping for compatibility reasons for lucxbox users                                  | Arg, Optional    |
| -olt / --only_last_team            | Include only the last matched team in the teams report                                                                           | Arg, Optional    |

### <a name="arguments-compiler-warnings">Compiler warnings subcommand arguments</a>

| Argument                                    | Comment                                                                                                                                                                                                                                                                                    | Sources and Type                             |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------- |
| -bl / --black_list                          | Mention the black list files for which warnings are not be considered                                                                                                                                                                                                                      | Arg, Optional                                |
| -ch / --changed_files                       | Files containing a list of changed files                                                                                                                                                                                                                                                   | Arg, Optional                                |
| -cf / --codeowners_file                     | Absolute path or relative to PROJECT_ROOT to the codeowners file. Accepts single path or list of paths                                                                                                                                                                                     | Arg, Optional                                |
| -c / --compiler                             | Compiler name. Possible values are 'clang', 'msvc' or 'greenhills'                                                                                                                                                                                                                         | Arg, Mandatory                               |
| -cl / --compiler_log                        | Path to compiler log file to parse the warnings from (globbing is allowed)                                                                                                                                                                                                                 | Arg, Mandatory                               |
| -mc / --mapping_column                      | Column name for mapping. Usually this is "File", "FilePath", etc. Default is "Filename"                                                                                                                                                                                                    | Arg, Optional                                |
| -rb / --report_basename                     | Base name of compiler warnings report                                                                                                                                                                                                                                                      | Arg, Optional                                |
| -rd / --report_dir                          | Absolute or relative to PROJECT_ROOT path where compiler warning reports are generated                                                                                                                                                                                                     | Arg, Optional                                |
| -ef / --export_formats                      | Set export formats. Possible formats are 'xlsx', 'csv' or 'json'                                                                                                                                                                                                                           | Arg, Optional                                |
| -gm / --gitignore_mapping                   | Same as "-olt / --only_last_team" argument and is overridden if "-olt / --only_last_team" is specified. Keeping for compatibility reasons for lucxbox users. "GITIGNORE_MAPPING" / -gm / --gitignore_mapping is deprecated. Please use "ONLY_LAST_TEAM" / -olt / --only_last_team instead  | Arg, Optional                                |
| -j / --jobs                                 | Number of threads                                                                                                                                                                                                                                                                          | Arg, Optional                                |
| -olt / --only_last_team                     | Include only the last matched team in the teams report                                                                                                                                                                                                                                     | Arg, Optional                                |
| -o / --output                               | Path to output file to log the warnings existing on the changed files                                                                                                                                                                                                                      | Arg, Optional                                |
| -q / --quiet                                | Print only errors                                                                                                                                                                                                                                                                          | Arg, Optional                                |
| -td / --target_directory                    | List of paths (separated by space) to include warning only from specified locations                                                                                                                                                                                                        | Arg, Optional                                |
| -t / --threshold                            | Threshold of allowed overall warnings before script returns non-zero exit code                                                                                                                                                                                                             | Arg, Optional                                |
| -tf / --threshold_file                      | Threshold file which lists thresholds for each warning name. Threshold file is a json                                                                                                                                                                                                      | Arg, Optional                                |
| -tdb / --types_db                           | Compiler warning types database file (json)                                                                                                                                                                                                                                                | Arg, Optional                                |
| -rp / --use_relative_paths                  | Use relative file paths when mapping components                                                                                                                                                                                                                                            | Arg, Optional                                |
### QAC BASELINE WORKFLOW

To properly use the script adhere to the following steps:
1. Create a prqa project with the helper and run an analysis with the arg to create a baseline.
2. Store/share baseline somewhere. I recommend to check it in with the other prqa script configuration.
3. Reference the location of the baseline in the json or pass it as argument when you create a NEW project that you want to analyse against a base line.
4. Run an analyse against a project configured with a baseline.


## <a name="build">How to build and test it</a>

No need to build. For requirements check the included [requirements.txt](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools/browse/requirements.txt).
To install the python requirements use on the [sca_tools](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools/browse) folder:

  > pip3 install -r requirements.txt

Be sure to check if the pip3 executable points to your python preferred interpreter.

To run the unit tests for this project simply run the following command on the [sca_tools](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools/browse) folder:

  > python -m unittest

To test if the script works you should once verify the created QAC/Coverity project in the GUI and check for the included files. For troubleshooting log at the analysis log files as provided by the script during execution.

## <a name="build-python-package">How to build the python package</a>

The build the package for the PyPI repositories, following commands need to be executed in the root folder.

  > python3 -m pip install --upgrade pip

Please note, that you should install the offical `build`-package with an explicit version. This is due to the fact, that the Bosch pypi mirror contains another package with the same name and a higher version number.
  > python3 -m pip install build==0.7.0

  > python3 -m build .

The subfolder `dist` now contains the `whl` and `tar.gz` files, which can be deployed to the PyPI repositories by CI with a technical user using e.g. `twine`. Do not forget to bump the version before deploying!

Once the package is deployed, the customers can then simply use the swq-sca-tools by installing it in their python environment, instead of using a submodule:

  > python3 -m pip install swq-sca-tools==VERSION

## <a name="contribute">How to contribute</a>

If you want to use this setup or contribute, please first contact the [Maintainers](#maintainers).


## <a name="licenses">Used 3rd party Licenses</a>

None


Software | License
------------------
[Apache Felix](http://felix.apache.org/) | [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0.txt)

## <a name="feedback">Feedback</a>

Get in contact with the [Maintainers](#maintainers), e.g. via email or via the [coding rules T&R project](https://rb-tracker.bosch.com/tracker/projects/CDF/summary).
