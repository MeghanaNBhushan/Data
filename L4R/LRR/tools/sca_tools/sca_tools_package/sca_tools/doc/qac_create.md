# <a name="qac-create-manual">QAC Create Manual</a>

Click [here](readme.md) to go back to the manual.

- [QAC Create Manual](#qac-create-manual)
  - [Project configuration](#project-configuration)
    - [Validate SCA Tools Configuration](#validate-sca-tools-configuration)
    - [SCA Tools initialization procedures](#sca-tools-initialization-procedures)
    - [QAC Project creation and configuration](#qac-project-creation-and-configuration)
    - [Validation of QAC SCA Tools configuration](#validation-of-qac-sca-tools-configuration)
      - [QAC Project Creation](#qac-project-creation)
      - [Setting Baseline](#setting-baseline)
    - [Populating QAC project](#populating-qac-project)
      - [Ordinary Synchronization Flow](#ordinary-synchronization-flow)
      - [Apply QAC built-in synchronization settings](#apply-qac-built-in-synchronization-settings)
      - [Remove Files from QAC Project](#remove-files-from-qac-project)
      - [Advanced features for project populating](#advanced-features-for-project-populating)
        - [Build project](#build-project)
        - [JSON file processing](#json-file-processing)
          - [Work with MSVC CL specific command format](#work-with-msvc-cl-specific-command-format)
          - [JSON file filtering](#json-file-filtering)
        - [Build log file processing](#build-log-file-processing)
          - [Build log file filtering](#build-log-file-filtering)

## <a name="project-configuration">Project configuration</a>

QAC Project creation is triggered by `qac create` command and controlled by configuration provided via command line parameters, environment variables, and JSON formatted configuration file.
QAC Project creation in SCA Tools contains the following steps:

- Basic validation of configuration
- Creation of initial directory structure
- Preliminary steps for QAC Project Populating (for `JSON` or `BUILD_LOG` sync types only):
  - Generate `compile_commands.json` or `build log` files used to populate QAC project
  - Apply preliminary filtering to `compile_commands.json` or `build log`
- QAC Project Creation
- (Optional) Baseline configuration
- Project Populating
- (Optional) Remove compilation units from QAC Project

### <a name="validate-sca-tools-configuration">Validate SCA Tools Configuration</a>

Before running actual steps SCA Tools validate configuration:

- Check if mandatory variables are specified
- Check if specified file and directory paths exist
- Basic validation of QAC configuration:
  - Check if QAC components specified in configuration file are available in QAC installation
  - Check if interdependent parameters are specified

More details about validation mechanism implemented in SCA Tools are provided below in related sections.

### <a name="sca-tools-initialization-procedures">SCA Tools initialization procedures</a>

Parameters described in the section:

- `PROJECT_ROOT` - Path to the directory used by SCA Tools to resolve relative paths
- `QAC_PROJECT_PATH` - Path to a QAC project directory
- `HELPER_LOGS_PATH` - Path to SCA Tools logs directory. Default value is `QAC_PROJECT_PATH/sca_tools`
- `CLEANUP_ON_CREATE` - Re-creates QAC project directory

SCA Tools initialization procedures for QAC Project creation are the following:

- Remove `QAC_PROJECT_PATH` directory tree if parameter `CLEANUP_ON_CREATE` is specified
- Create initial directory tree under:
  - `QAC_PROJECT_PATH` - the directory for internal usage by Helix QAC
  - `HELPER_LOGS_PATH` - the directory to store logs and intermediate files for usage by SCA Tools

### <a name="qac-project-creation-and-configuration">QAC Project creation and configuration</a>

### <a name="validation-of-qac-sca-tools-configuration">Validation of QAC SCA Tools configuration</a>

If `QAC_ANALYSIS_PATH_BLACKLIST` is specified and `QAC_MODULES` is not, then SCA Tools fail.

If QAC Components specified in `QAC_MODULES` do not exist in `ACF_FILE` then SCA Tools fail.

Validates ACF, VCF, NCF, RCF, User messages and Custom help file paths


#### <a name="qac-project-creation">QAC Project Creation</a>

Parameters described in the section:

- `ACF_FILE` - (Mandatory) Path relative to project root or absolute to the ACF QAC configuration file
- `COMPILER_LIST` - List of CCT files corresponding to the individual used targets
- `NCF_FILE` - Path relative to project root or absolute to the NCF QAC configuration file or list of files. If several files are provided then contents of files will be merged into separate file. The merged file will be used in QAC project creation
- `RCF_FILE` - (Mandatory) Path relative to project root or absolute to the RCF QAC configuration file or list of files. If several files are provided then contents of files will be merged into separate file. Merged file will be used in QAC project creation
- `USER_MESSAGES` - Path relative to project root or absolute to the user messages configuration file or list of files. If several files are provided then contents of files will be merged into separate file. Merged file will be used in QAC project creation
- `VCF_FILE` - Path relative to project root or absolute to the VCF QAC configuration file

QAC uses several parameters to create QAC Projects. All the parameters can be configured via appropriate parameters in SCA Tools configuration file.
For some of the parameters advanced features like merging several files into one, validation, and setting up custom help pages are supported in SCA Tools. The features are described in separate sections.

#### <a name="setting-baseline">Setting Baseline</a>

Parameters described in the section:

- `LOCAL_BASELINE_PATH` - Relative to project root or absolute. If specified, a baseline file will be used (files.sup)

To configure and use a baseline for QAC analysis (e.g. to suppress already known warnings) the parameter above has to specified.
Refer to official QAC documentation for more details.

### <a name="populating-qac-project">Populating QAC project</a>

The section describes available features in configuration of populating a QAC project with files to analyze.

#### <a name="ordinary-synchronization-flow">Ordinary Synchronization Flow</a>

Parameters described in the section:

- `SYNC_TYPE` - Project synchronization type
- `SYNC_BUILD_COMMAND` - Shell command that either generates a build log file or `compile_commands.json`, or builds project sources
- `SYNC_BUILD_LOG_FILE` | `-sbf` / `--sync_build_log_file` - Path to either `compile_commands.json` or build log

QAC supports different ways of adding files to QAC Projects. All of them are supported in SCA Tools and can be configured via `SYNC_TYPE` parameter.

Valid values are:

- MONITOR
- JSON
- BUILD_LOG

According to the synchronization type specified for adding files to the project additional parameters are used:

- `SYNC_BUILD_COMMAND` - mandatory for `MONITOR` and optional for `JSON` and `BUILD_LOG`
- `SYNC_BUILD_LOG_FILE` - mandatory for `JSON` and `BUILD_LOG`

Advanced usage of project synchronization can be found in specific sections

#### <a name="apply-qac-built-in-synchronization-settings">Apply QAC built-in synchronization settings</a>

Parameters described in the section:

- `QAC_SYNC_SETTINGS_INCLUDE_PATH` - The symbols used to extract Include Paths

Currently SCA Tools support `INCLUDE_PATH` and `FILE_FILTER` QAC build-in synchronization settings.
It is possible to pass sync settings values via the following parameters:

- for `INCLUDE_PATH` via `QAC_SYNC_SETTINGS_INCLUDE_PATH`
- for `FILE_FILTER` via `QAC_SYNC_PATH_BLACKLIST`

For more details please refer to the official QAC documentation.

#### <a name="remove-files-from-qac-project">Remove Files from QAC Project</a>

Parameters described in the section:

- `HELPER_REMOVE_FILE_LIST` - Give the absolute path or relative path (relative to project repo folder) of a text file, which contains list of files to be removed from the project

If the parameter is specified then SCA Tools remove all the files provided from the created and populated QAC Project.

#### <a name="advanced-features-for-project-populating">Advanced features for project populating</a>

SCA Tools have advanced features for QAC project populating with `BUILD_LOG` or `JSON` sync types.
The features include:

- Run build command to generate `build.log` or `compile_commands.json`
- Extra processing of `compile_commands.json` before passing it to QAC
- Extra processing of `build.log` before passing it to QAC

##### <a name="build-project">Build project</a>

Parameters described in the section:

- `SYNC_TYPE` - Project synchronization type
- `SYNC_BUILD_COMMAND` - Build command that generates a log file, ideally a script
- `SYNC_BUILD_LOG_FILE` | `-sbf` / `--sync_build_log_file` - Path to either `compile_commands.json` or build log

SCA Tools can either accept already generated file or run command that will generate the files.
This is supported for `SYNC_TYPE` equals to `JSON` or `BUILD_LOG`.

To generate an artifact (either build log or compile_commands.json) automatically and then use it during `qac create` it needs to define `SYNC_BUILD_COMMAND` with an appropriate command and specify a path where the generated artifact can be found.

##### <a name="json-file-processing">JSON file processing</a>

The section applies to `SYNC_TYPE` equals to `JSON`.

###### <a name="work-with-msvc-cl-specific-command-format">Work with MSVC CL specific command format</a>

Older versions of cmake generate `compile_commands.json` for MSVC CL compiler with specific symbols. Such JSON files have to be modified before using in QAC.
There are no additional steps required. SCA Tools do this automatically when the symbols are found in JSON files.
It happens prior to any processing of `compile_commands.json` file.
SWQ SCA Tools store the processed JSON file in the same directory where the original file is located but with suffix `.fixed.json`.
For instance, if original file is `compile_commands.json` then resulting one is `compile_commands.json.fixed.json`

###### <a name="json-file-filtering">JSON file filtering</a>

Parameters described in the section:

- `SYNC_TYPE_JSON_PATH_PATTERN_WHITELIST` - File filter to apply as an inclusion mechanism (whitelist)
- `HELPER_SUPPRESS_FILE_LIST_S` - File filter to apply as an exclusion mechanism. Absolute path or relative (to project repo folder) path of a text file OR an array, which contains list of files to be excluded from the sync

The parameters listed above allow to make preliminary filtering of `compile_commands.json` before passing it to QAC to populate the project. Any type of the mentioned filtering is enabled only if related parameter is defined.
If both parameters are defined then the filtering is done in the following order:

- Inclusion. Result is in the same directory where the original file is located but with `.tmp` file extension. E.g. `compile_commands.json.tmp`
- Exclusion. Result is in the same directory in the same directory where the original file is located but with `.fil` file extension. E.g. `compile_commands.json.fil` or `compile_commands.json.tmp.fil` (if inclusion was executed before).

Once filtering is done the resulting file that is used to populate QAC project is stored in `HELPER_LOGS_PATH/build/compile_commands.json` directory.

##### <a name="build-log-file-processing">Build log file processing</a>

The section applies to `SYNC_TYPE` equals to `BUILD_LOG`.

###### <a name="build-log-file-filtering">Build log file filtering</a>

Parameters described in the section:

- `HELPER_SUPPRESS_FILE_LIST_S` - File filter to apply as an exclusion mechanism. Absolute path or relative (to project repo folder) path of a text file OR an array, which contains list of files to be excluded from the sync

Filtering is enabled only if `HELPER_SUPPRESS_FILE_LIST_S` parameter is defined.
Result is created in the same directory in the same directory where the original file is located but with `.fil` file extension. E.g. `build.log.fil`.

Once filtering is done the resulting file that is used to populate QAC project is stored in `HELPER_LOGS_PATH/build/build.log` directory.