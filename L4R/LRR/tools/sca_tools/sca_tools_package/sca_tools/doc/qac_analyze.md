# <a name="qac-analyze-manual">QAC Analyze Manual</a>

Click [here](readme.md) to go back to the manual.

 - [QAC Analyze Manual](#qac-analyze-manual)
  - [Analyze Project](#analyze-project)
    - [QAC Analysis procedure](#qac-analysis-procedure)
      - [Analyze only one file](#analyze-only-one-file)
      - [Analyze list of files](#analyze-list-of-files)
        - [Analyze only files included into QAC project from provided list](#analyze-only-files-included-into-qac-project-from-provided-list)
      - [Analyze all files from QAC Project](#analyze-all-files-from-qac-project)
    - [Ignore Failures in QAC Analysis](#ignore-failures-in-qac-analysis)
    - [Create Baseline](#create-baseline)
    - [VS Code Integration](#vs-code-integration)

## <a name="analyze-project">Analyze Project</a>

*NOTE: Prior to run analysis QAC Project must be created with `qac create` command. *

QAC analysis is performed by `qac analyze` command.
SCA Tools start analysis with cleaning up the `app/logs` directory under QAC user data location.

The following ways to run QAC analysis are supported:

- single file
- list of files (specified in a file)
- whole QAC project

SCA Tools save log file of QAC Analysis to `HELPER_LOGS_PATH/analysis/analyze_output_{{timestamp}}.log` file.
Once Analysis is finished the log file is checked for errors. If any of QAC components returns non-zero exit code appropriate log line is to be written to failures log files. It can be found at `HELPER_LOGS_PATH/analysis/analyze_failures_{{timestamp}}.log`

If there are any failures in the logs SCA Tools do the following:

- back up all log files generated by QAC to `HELPER_LOGS_PATH/analysis/`
- fail with an appropriate error message (to change this behavior please refer to "Ignore failures in QAC analysis" section).

There are few extra features available for `qac analyze` command:

- Ignore failures in QAC analysis
- Baseline creation
- Print found warnings to stdout for integration with VS Code

### <a name="qac-analysis-procedure">QAC Analysis procedure</a>

Parameters described in the section:

- `ANALYZE_FILE` - Analyzes the given file
- `ANALYZE_LIST` - Path to a file that contains list of files to be analyzed. Can be absolute or relative to `PROJECT_ROOT`

More details are provided in specific sections below.

#### <a name="analyze-only-one-file">Analyze only one file</a>

If it needs to run analysis only for one file,  the `ANALYZE_FILE` parameter has to be defined with the path to the file for analysis.
SCA Tools pass the value directly to QAC.

#### <a name="analyze-list-of-files">Analyze list of files</a>

To run analysis on a list of files the following steps are to be performed:

- Put file paths to analyze one per line to the file
- Provide path to the file as `ANALYZE_LIST`

If `ANALYZE_LIST` is specified and target file exists SCA Tools run analysis for all files metnioned in the list.
If the file does not exist then SCA Tools fail with the appropriate error message.

##### <a name="analyze-only-files-included-into-qac-project-from-provided-list">Analyze only files included into QAC project from provided list</a>

QAC fails when a file to be analyzed does not exist in QAC project.
To prevent such situations SCA Tools filter list of files to be analyzed and excludes non-existing files from the list before passing it to QAC.
Resulting file is stored at `HELPER_LOGS_PATH/analysis/analyze_list.txt`

This functionality works with `SYNC_TYPE` equals to `JSON` only.

#### <a name="analyze-all-files-from-qac-project">Analyze all files from QAC Project</a>

SCA Tools trigger QAC analysis for all files from QAC project if neither `ANALYZE_LIST` nor `ANALYZE_FILE` are defined.

### <a name="ignore-failures-in-qac-analysis">Ignore Failures in QAC Analysis</a>

Parameters described in the section:

- `SKIP_EXIT_ON_ANALYSIS_RETURN_CODES` - List of return codes to be ignored in QAC Analysis log

If the parameter is defined then SCA Tools ignore failures in QAC Analysis log with all return codes set as parameter's value.

### <a name="create-baseline">Create Baseline</a>

Parameters described in the section:

- `HELPER_CREATE_BASELINE` - The parameter enables baseline creation after analysis

If the parameter is specified then SCA Tools trigger baseline creation once QAC analysis is finished.
Resulting path for the baseline file is `QAC_PROJECT_PATH/prqa/configs/Initial/output/files.sup`.

More information about baseline and its usage can be found in the official QAC documentation.

### <a name="vs-code-integration">VS Code Integration</a>

Parameters described in the section:

- `USE_VSCODE_INTEGRATION` - The parameter turns on printing of found warnings to stdout for VS Code integration.

If the parameter is specified then SCA Tools generate QAC analysis report in specific format and print it to stdout so that VS Code can consume it and use to display warnings in code editor.# QAC Analyze Manual