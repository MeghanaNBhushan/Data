# <a name="coverity-create-manual">Coverity Create Manual</a>

Click [here](readme.md) to go back to the manual.

 - [Coverity Create Manual](#coverity-create-manual)
  - [Project configuration](#project-configuration)
    - [Validate SCA Tools Configuration](#validate-sca-tools-configuration)
    - [SCA Tools initialization procedures](#sca-tools-initialization-procedures)
    - [Coverity Project creation and configuration](#coverity-project-creation-and-configuration)
    - [Validation of Coverity SCA Tools configuration](#validation-of-coverity-sca-tools-configuration)
    - [Coverity Project Creation](#coverity-project-creation)
    - [Populating Coverity project](#populating-coverity-project)
      - [Ordinary Flow](#ordinary-flow)
      - [Remove Files from Coverity Project](#remove-files-from-coverity-project)
      - [Advanced features for project populating](#advanced-features-for-project-populating)
        - [Build project](#build-project)
        - [JSON file processing](#json-file-processing)
          - [Work with MSVC CL specific command format](#work-with-msvc-cl-specific-command-format)
          - [JSON file filtering](#json-file-filtering)
      - [List translation units](#list-translation-units)

## <a name="project-configuration">Project configuration</a>

Coverity Project creation is triggered by `coverity create` command and controlled by configuration provided via command line parameters, environment variables, and JSON formatted configuration file.
Coverity Project creation in SCA Tools contains the following steps:

- Basic validation of configuration
- Creation of initial directory structure
- Generate configuration file for compile commands
- Preliminary steps for Coverity Project Populating(for `USE_COMPILE_COMMANDS_JSON` or `BUILD_COMMAND`)::
  - Generate or use existing `compile_commands.json` file used to populate Coverity project
  - Apply filtering to `compile_commands.json`
- Coverity Project Creation
- Project Populating
- List translation units

### <a name="validate-sca-tools-configuration">Validate SCA Tools Configuration</a>

Before running actual steps, SCA Tools validate configuration:

- Check if mandatory variables are specified
- Check if specified file and directory paths exist
- Basic validation of Coverity configuration:
  - Check if Coverity components specified in configuration file are available in Coverity installation
  - Check if interdependent parameters are specified

More details about validation mechanism implemented in SCA Tools are provided below in related sections.

### <a name="sca-tools-initialization-procedures">SCA Tools initialization procedures</a>

Parameters described in the section:

- `PROJECT_ROOT` - Path to the directory used by SCA Tools to resolve relative paths
- `COVERITY_PROJECT_PATH` - Path to a Coverity project directory
- `HELPER_LOGS_PATH` - Path to SCA Tools logs directory. Default value is `COVERITY_PROJECT_PATH/sca_tools/logs`

SCA Tools initialization procedures for Coverity Project creation are the following:

- Create initial directory tree under:
  - `COVERITY_PROJECT_PATH` - the directory for internal usage by Coverity
  - `HELPER_LOGS_PATH` - the directory to store logs and intermediate files for usage by SCA Tools

### <a name="coverity-project-creation-and-configuration">Coverity Project creation and configuration</a>

### <a name="validation-of-coverity-sca-tools-configuration">Validation of Coverity SCA Tools configuration</a>

If `COVERITY_PROJECT_PATH` is not specified SCA Tools fail.

### <a name="coverity-project-creation">Coverity Project Creation</a>

Parameters described in the section:

- `SKIP_EXIT_ON_ERROR` - Ignore errors and continue execution if the return code is one of the space separated values
- `MAXIMUM_PARALLEL_WORKERS` - Maximum number of parallel jobs to be executed in parallel workers. Defaults is 4 workers
- `COV_BUILD_OPTION_LIST` - Optional coverity build commands according to [Coverity manual](https://abts55137.de.bosch.com:8443/doc/en/cov_command_ref.html)

Coverity uses several parameters to create Coverity Projects. All the parameters can be configured via appropriate parameters in SCA Tools configuration file.
For some of the parameters advanced features like merging several files into one, validation are supported in SCA Tools. The features are described in separate sections.


### <a name="populating-coverity-project">Populating Coverity project</a>

The section describes available features in configuration of populating a Coverity project with files to analyze.

#### <a name="ordinary-flow">Ordinary Flow</a>

Parameters described in the section:
- `BUILD_COMMAND` - Build command that runs full build, ideally a script. If USE_COMPILE_COMMANDS_JSON is specified the parameter is not used
- `USE_COMPILE_COMMANDS_JSON` - Use compile_commands.json compilation instead of `COMPILE_COMMANDS_BUILD_COMMAND`
- `COMPILE_COMMANDS_BUILD_COMMAND` - The command that generates compile_commands.json. Effective only when `USE_COMPILE_COMMANDS_JSON` is set. Path to the generated compile_commands.json has to be provided in `COMPILE_COMMANDS_JSON`
- `COMPILE_COMMANDS_JSON` - Path to compile_commands.json file. Effective only when `USE_COMPILE_COMMANDS_JSON` is set

Coverity supports different ways of adding files to Coverity Projects. All of them are supported in SCA Tools and can be configured with `BUILD_COMMAND` or `USE_COMPILE_COMMANDS_JSON` parameters.

According to the build type specified for adding files to the project additional parameters are used:

`USE_COMPILE_COMMANDS_JSON` parameter dependencies:
- `COMPILE_COMMANDS_JSON` - mandatory, if is not specified SCA Tools `coverity create` command fail
- `COMPILE_COMMANDS_BUILD_COMMAND` - optional, if is not specified SCA Tools is used commands from `compile_commands.json`

Advanced usage of project build can be found in specific sections

#### <a name="remove-files-from-coverity-project">Remove Files from Coverity Project</a>

Parameters described in the section:

- `FILE_MATCHING_PATTERNS` - Filter patterns of files to include in generated build script, separated with space. In case INPUT_FILE_MATCHING_PATTERNS is specified, list of patterns will be extended with patterns provided in file.
- `INPUT_FILE_MATCHING_PATTERNS` - Absolute path or relative to `PROJECT_ROOT` to a file which contains filter patterns of files to include in generated build script, one per line. In case `FILE_MATCHING_PATTERNS` is specified, list of patterns will be extended with patterns provided in `FILE_MATCHING_PATTERNS`

If the parameter is specified then SCA Tools remove all the files provided from the created and populated Coverity Project.

#### <a name="advanced-features-for-project-populating">Advanced features for project populating</a>

SCA Tools have advanced feature for Coverity project populating by extra processing of `compile_commands.json` before passing it to Coverity.

- Run build command to generate `compile_commands.json`
- Extra processing of `compile_commands.json` before passing it to Coverity

##### <a name="build-project">Build project</a>

Parameters described in the section:

- `BUILD_COMMAND` - Build command that runs full build, ideally a script. If `USE_COMPILE_COMMANDS_JSON` is specified the parameter is not used
- `USE_COMPILE_COMMANDS_JSON` Use compile_commands.json compilation instead of `BUILD_COMMAND`
- `COMPILE_COMMANDS_JSON` - path to compile_commands.json file. Effective only when `USE_COMPILE_COMMANDS_JSON` is set
- `COMPILE_COMMANDS_BUILD_COMMAND` - The command that generates compile_commands.json. Effective only when `USE_COMPILE_COMMANDS_JSON` is set. Path to the generated compile_commands.json has to be provided in `COMPILE_COMMANDS_JSON`

SCA Tools can either accept already generated file or run command that will generate the files.
This is supported if `BUILD_COMMAND` or `USE_COMPILE_COMMANDS_JSON` is used.

To generate an artifact (compile_commands.json) automatically and then use it during `coverity create` it needs to define `BUILD_COMMAND` with an appropriate command and specify a path where the generated artifact can be found.

##### <a name="json-file-processing">JSON file processing</a>

The section applies only if `USE_COMPILE_COMMANDS_JSON` is set.

###### <a name="work-with-msvc-cl-specific-command-format">Work with MSVC CL specific command format</a>

Older versions of cmake generate `compile_commands.json` for MSVC CL compiler with specific symbols. Such JSON files have to be modified before using in Coverity.
There are no additional steps required. SCA Tools do this automatically when the symbols are found in JSON files.
It happens prior to any processing of `compile_commands.json` file.
SWQ SCA Tools store the processed JSON file in the same directory where the original file is located but with suffix `.fixed.json`.
For instance, if original file is `compile_commands.json` then resulting one is `compile_commands.json.fixed.json`

###### <a name="json-file-filtering">JSON file filtering</a>

Parameters described in the section:

- `INPUT_FILE_MATCHING_PATTERNS` - File filter to apply as an inclusion mechanism (whitelist)
- `FILE_MATCHING_PATTERNS` - Filter patterns of files to include in generated build script, separated with space.

The parameters listed above allow to make preliminary filtering of `compile_commands.json` before passing it to Coverity to populate the project. Any type of the mentioned filtering is enabled only if related parameter is defined.
If both parameters are defined then list of patterns will be extended with patterns provided in `INPUT_FILE_MATCHING_PATTERNS` and with `FILE_MATCHING_PATTERNS` parameter.

Once filtering is done the resulting file that is used to populate Coverity project is stored in `HELPER_LOGS_PATH/build/compile_commands.json` directory.

#### <a name="list-translation-units">List translation units</a>
Last step for `coverity create` command is to show translation units (TUs):
  - total number of TUs
  - number of failed TUs
  - number of successful TUs
  - percentage of successful TUs 