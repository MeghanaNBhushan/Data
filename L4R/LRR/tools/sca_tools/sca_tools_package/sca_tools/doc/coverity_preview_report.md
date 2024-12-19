# <a name="coverity-preview-report-manual">Coverity Preview Report Manual</a>

Click [here](readme.md) to go back to the manual.

- [Coverity Preview Report Manual](#coverity-preview-report-manual)
  - [Preview Report](#preview-report)
    - [Common Parameters Overview](#common-parameters-overview)
    - [Filtering](#filtering)
    - [Mapping Teams](#mapping-teams)

## <a name="preview-report">Preview Report</a>

*NOTE: Prior to generate Preview report Coverity Project must be analyzed with `coverity analyze` command.*
Coverity preview report is generated by `coverity preview_report` command.
Instead of sending files cross-references, and other assets to the Coverity Connect server, this option sends only the defect occurrences. The server returns a commit preview report, which is written in JSON format wich is then converted into one of supported formats - 'xlsx', 'csv', 'vscode' supported format or just printed to STDOUT.

SCA Tools supports filtering of preview report based on `TRANSLATION_UNITS_BLACKLIST`.
Additionally, mapping functionality based on GitHub CODEOWNERS files is available.

SCA Tools exports preview report to `COVERITY_PROJECT_PATH/sca_tools/export/preview_report.xlsx`

SCA Tools exports filtered preview report to `COVERITY_PROJECT_PATH/sca_tools/export/preview-report-filtered.xlsx`

SCA Tools save log file of the `coverity preview_report` command to `HELPER_LOGS_PATH/sca_tools_coverity_preview_report_{{datetime}}.log` file.

### <a name="common-parameters-overview">Common Parameters Overview</a>

Parameters described in the section:

- `COVERITY_USERNAME` - Username provided to access Coverity Connect server. Used in conjunction with the password. Must be provided as an environment variable
- `COVERITY_PASSWORD` - Password provided to access Coverity Connect server. Used in conjunction with the username. Must be provided as an environment variable
- `COVERITY_COMMIT_URL` - Use this option to specify the information needed to connect to a Coverity Connect server
- `COVERITY_COMMIT_HOST` - Name of the server without protocol. DEPRECATED, keeping for compatibility reasons. Use `COVERITY_COMMIT_URL` instead
- `COVERITY_COMMIT_DATAPORT` - Network TCP Port to be used while transferring data. DEPRECATED, keeping for compatibility reasons. Use `COVERITY_COMMIT_URL` instead
- `COVERITY_COMMIT_STREAM` - Stream name to which to commit the defects
- `EXPORT_FORMAT` - Defines the report export format. Available formats: 'xlsx', 'csv', 'csv_zip', 'stdout', 'vscode' or 'all', where 'all' is a list of commonly used report formats: xlsx and csv. Default format is 'all'

### <a name="filtering">Filtering</a>

Parameters described in the section:

- `TRANSLATION_UNITS_BLACKLIST` - list of translation units that will be excluded from Coverity Project

In case if `TRANSLATION_UNITS_BLACKLIST` is specified - SCA Tools will generate both full and filtered preview reports.
Filtered report excludes warnings on files that are matching expressions in `TRANSLATION_UNITS_BLACKLIST`.

### <a name="mapping-teams">Mapping Teams</a>

Parameters described in the section:

- `CODEOWNERS_FILE` - Absolute path or relative to `PROJECT_ROOT` to the codeowners file
- `ONLY_LAST_TEAM` - Include only the last matched team in the teams report

SCA Tools support team mapping for files where warnings are found based on GitHub Codeowners files.
The feature is enabled automatically once `CODEOWNERS_FILE` is defined. It creates 2 additional columns - "Team" (with list of teams) and "Components.
If `ONLY_LAST_TEAM` is specified then only teams from the latest match are returned.
Team mapping is applied on both - full and filtered preview reports.