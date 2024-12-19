# <a name="qac-reporting-manual">QAC Filter Qaview Manual</a>

Click [here](readme.md) to go back to the manual.

- [QAC Filter Qaview Manual](#qac-reporting-manual)
  - [Overview](#overview)
  - [Supported Features](#supported-features)
    - [Parameters Overview](#parameters-overview)

## <a name="overview">Overview</a>

QAC Filter Qaview is a SCA Tools feature that is mostly used as a Pull Request Gate in CI automation.
It parses the exported `qacli-view` CSV report for severity levels, compares to a given threshold number for specific severity level
and then fails or passes the build on CI.

As result `qac filter_qaview` generates two reports:

1. Report with total and active warnings per severity
2. Threshold exceeded warnings report

## <a name="supported-features">Supported Features</a>

SCA Tools have the following command to run Filter Qaview functionality:

- `qac filter_qaview`

### <a name="parameters-overview">Parameters Overview</a>

Parameters described in the section:

- `FILTER_REPORT_OUTPUT_FILE` - Path to a filtered report output file.
Absolute or relative to project root paths can be used

- `IGNORE_IDS` - List of error IDs that can be ignored

- `JUSTIFICATION_MESSAGE_REGEXP` - Regular expression(s) for suppressed Justification messages

- `SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_0` - `SEVERITY_LEVEL_FAIL_THRESHOLD_FOR_LEVEL_9` -
Threshold number of admissible warnings for specific severity level. If the number of warnings for the level
exceeds the specified number - SCA Tools will exit with error

- `THRESHOLD_WARNINGS_REPORT` - Path to threshold exceeding warnings report in HTML format

- `TO_STDOUT` - A boolean to write results to stdout. Otherwise, the results are written to the file which is specified via `FILTER_REPORT_OUTPUT_FILE` parameter

- `QAVIEW_CSV` - Path to qacli-view CSV report file
