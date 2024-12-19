# <a name="qac-export-analysis-manual">QAC Export Analysis Manual</a>

Click [here](readme.md) to go back to the manual.

- [QAC Export Analysis Manual](#qac-export-analysis-manual)
  - [Supported Features](#supported-features)
    - [Parameters Overview](#parameters-overview)
    - [Mapping Teams](#mapping-teams)

## <a name="supported-features">Supported Features</a>

SCA Tools have the following command to generate QAC Analysis Reports:

- `qac export_analysis`

QAC analysis reports generation in general is based on `qacli.exe view export` command (native QAC command).
The command exports analysis details in XML files, which are used by SCA Tools to create single state.json
(so called "project state" file) with aggregated analysis information.
Therefore, `qac export_analysis` command involves two phases under the hood:

1. Generates / reads QAC project state file
2. Runs actual report generation based on state file

Additionally, mapping functionality based on GitHub CODEOWNERS files is available.

### <a name="parameters-overview">Parameters Overview</a>

Parameters described in the section:

- `QAC_CLEANUP_DIAGNOSTICS_OUTPUT` - A boolean to remove QACLI diagnostics output XML files. Default value is *False*.

QACLI diagnostics output XML files are natively created by Helix QAC when running `qac export_analysis`
and contain analysis result data. These files are used to generate QAC project state file

If set to *True* - all QACLI diagnostics output XML files are removed from 'diagnostics_output' directory

*NOTE: Is effective only in combination with `QAC_WITH_STATE_FILE` parameter*

- `EXPORT_FORMATS` - Defines the report export formats. Available formats: 'xlsx', 'csv', 'csv_zip', 'html' or 'all', where 'all' is a list of commonly used report formats: xlsx, csv and html. Default value is 'all'

Report generating commands can generate reports in multiple formats in one run.
List of generated reports includes:

- info - information about configuration of QAC project (`ACF_FILE`, `RCF_FILE`, etc.), QAC Version, `PROJECT_ROOT`, baseline.
- summary - statistic data based on warning severity, suppression type, producer component and message id, rule text
- view - detailed information about all found QAC warnings

The reports can be generated separately (e.g. HTML, CSV) or in one file (e.g. Excel sheets, ZIP archive with multiple CSV files)

- `QAC_FROM_STATE_FILE` - Generates reports based on state file. This parameter acts as boolean flag and also accepts path to the state file.

- Default value is *False*
- When set to *True* - reads QAC project state file from default SCA Tools export directory
- When specific path to file is given - reads the file from provided path. Accepted file formats:
  - JSON file
  - ZIP file with JSON within

*NOTE: If used in combination with `QAC_WITH_STATE_FILE` - `QAC_FROM_STATE_FILE` parameter takes precedence*

- `METRICS_FILTER_LIST` - List of metrics to be included in generated metrics report.

*NOTE: Is effective only in combination with `QAC_WITH_METRICS` parameter*

- `QAC_WITH_ANALYSIS` - Generates analysis report with detailed information about all found QAC warnings

*NOTE: Setting `QAC_WITH_ANALYSIS` parameter enables QAC project state file generation,
when `QAC_WITH_STATE_FILE` and `QAC_FROM_STATE_FILE` parameters are not set*

- `QAC_WITH_METRICS` - Generates metrics report

*NOTE: Setting `QAC_WITH_METRICS` parameter enables QAC project state file generation,
when `QAC_WITH_STATE_FILE` and `QAC_FROM_STATE_FILE` parameters are not set*

- `QAC_WITH_SUMMARY` - Generates summary report with statistic data based on warning severity,
suppression type, producer component and message id, rule text

*NOTE: Setting `QAC_WITH_SUMMARY` parameter enables QAC project state file generation,
when `QAC_WITH_STATE_FILE` and `QAC_FROM_STATE_FILE` parameters are not set*

- `QAC_WITH_STATE_FILE` - A boolean parameter that enables generation of QAC project state file.
Default value is *False*.

*NOTE: Setting any of `QAC_WITH_ANALYSIS`, `QAC_WITH_METRICS`, `QAC_WITH_SUMMARY` parameter enables
QAC project state file generation, when `QAC_WITH_STATE_FILE` and `QAC_FROM_STATE_FILE` parameters are not set*

- `QAC_WITH_SUBDIAGNOSTICS` - Generates report with light subdiagnostics included (only origins will be present in analysis report).
Default is *False*

When `QAC_WITH_SUBDIAGNOSTICS` parameter is set - analysis report is extended with `SCA Tools Subdiagnostics ID` and `SCA Tools Subdiagnostics Origin` columns.
See `SCA Tools Subdiagnostics ID` and `SCA Tools Subdiagnostics Origin` values explained in example below:

|SCA Tools Subdiagnostics ID|SCA Tools Subdiagnostics Origin|
|-|-|
|1_8_2_1|src\app\variant1_app.cpp:33:5:qacpp-5.0.0:1585|

`SCA Tools Subdiagnostics ID`:
- `1` - Index of analyzed file
- `8` - Index of warning in file
- `2` - Index of subdiagnostic in warning `8`
- `1` - Index of nested subdiagnostic in subdiagnostic `2`

`SCA Tools Subdiagnostics Origin`:
- `src\app\variant1_app.cpp` - Source file the warning belongs too
- `33` - Line in source file
- `5` - Column in line
- `qacpp-5.0.0` - Component that produced the warning
- `1585` - Warning ID

*NOTE: If both `QAC_WITH_SUBDIAGNOSTICS` and `QAC_WITH_FULL_SUBDIAGNOSTICS` parameters are set -
`QAC_WITH_FULL_SUBDIAGNOSTICS` takes precedence*

- `QAC_WITH_FULL_SUBDIAGNOSTICS` - Generates report with full subdiagnostics included in analysis report.
Default is *False*

When `QAC_WITH_FULL_SUBDIAGNOSTICS` parameter is set - analysis report is extended with `SCA Tools Subdiagnostics ID` and `SCA Tools Subdiagnostics Depth` columns.
All subfinding for each warning is written to the report as separate row. It is possible that each warning can have multiple subfindings and subfindings themselves
can have nested subfindigs. `SCA Tools Subdiagnostics Depth` column indicates the nesting depth of subfinding and the `SCA Tools Subdiagnostics ID` includes information
about parent warning the subfinding belongs too. See `SCA Tools Subdiagnostics ID` value explained in example above


### <a name="mapping-teams">Mapping Teams</a>

Parameters described in the section:

- `CODEOWNERS_FILE` - Absolute path or relative to `PROJECT_ROOT` to the codeowners file
- `ONLY_LAST_TEAM` - Include only the last matched team in the teams report

SCA Tools support team mapping for files where warnings are found based on GitHub Codeowners files.
The feature is enabled automatically once `CODEOWNERS_FILE` is defined. It creates 2 additional columns - "Team" (with list of teams) and "Components.
If `ONLY_LAST_TEAM` is specified then only teams from the latest match are returned. 