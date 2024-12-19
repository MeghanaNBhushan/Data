# <a name="coverity-analyze-manual">Coverity Analyze Manual</a>

Click [here](readme.md) to go back to the manual.

- [Coverity Analyze Manual](#coverity-analyze-manual)
  - [Analyze Project](#analyze-project)
    - [Coverity Analysis procedure](#coverity-analysis-procedure)

## <a name="analyze-project">Analyze Project</a>

*NOTE: Prior to run analysis Coverity Project must be created with `coverity create` command. In case you are interested in delta project analysis see [Populating Coverity project](coverity_create.md#populating-coverity-project).*


Coverity analysis is performed by `coverity analyze` command.

SCA Tools save log file of the `coverity analyze` command to `HELPER_LOGS_PATH/sca_tools_coverity_analyze_{{datetime}}.log` file.

After Coverity Analysis command is executed SCA Tools checks its return code. In case it returns non-zero exit code SCA tools will return an error with proper message. Otherwise analysis will be finished.

### <a name="coverity-analysis-procedure">Coverity Analysis procedure</a>

Parameters described in the section:
- `TRANSLATION_UNITS_BLACKLIST` - list of translation units that will be excluded from Coverity Project

The analysis starts with translation units (TUs) filtering if `TRANSLATION_UNITS_BLACKLIST` in the following way:
- get list of patterns from `TRANSLATION_UNITS_BLACKLIST`
- for each of pattern it removes the file matched this pattern from project using `cov-manage-emit` tool
- in case `cov-manage-emit` returns exit codes other than 0 and 2 Analysis process will be stopped

The next step is collecting final list of translation units to perfrom analysis on:
- SCA Tools obtain the list from the `cov-manage-emit` tool (assumes it was already filtered using `TRANSLATION_UNITS_BLACKLIST`)
- for each of the "Translation unit:" line it calculates total number of TUs
- likely the calculation of total number of TUs it calculates failed number of TUs using counting the lines contain " (failure)" substring
- in case the total number of TUs equals zero SCA Tools will print the proper message and stop the analysis process
- as a result of operations performed on these steps the following data will be collected:
  - total number of TUs
  - number of failed TUs
  - number of successful TUs
  - percentage of successful TUs

For the next step SCA Tools will start the Coverity Project analysis from the list of TUs generated from the previous step.
