# <a name="coverity-run-dekstop-manual">Coverity Run Desktop Manual</a>

Click [here](readme.md) to go back to the manual.

- [Coverity Run Desktop Manual](#coverity-run-desktop-manual)
  - [Analyze Project](#analyze-project)
    - [Coverity Run Desktop procedure](#coverity-run-desktop-procedure)

## <a name="analyze-project">Analyze Project</a>

*NOTE: Prior to run analysis Coverity Project must be created with `coverity create` command. In case you are interested in delta project analysis see [Populating Coverity project](coverity_create.md#populating-coverity-project).*

Coverity analysis can be aslo performed by `coverity run_desktop` command. This approach communicates directly with Coverity Connect instance and relies on the results of a previous analysis.

*NOTE: Unlike analysis performed by `coverity analyze`, desktop analysis is not guaranteed to produce exactly the same results. Many checkers report close to the same results. But some checkers are disabled because they only work well with full analysis, therefore do not assume that a defect that does not show up in desktop analysis was actually fixed.*

SCA Tools save log file of the `coverity run_desktop` command to `HELPER_LOGS_PATH/sca_tools_coverity_run_desktop_{{datetime}}.log` file.

After Coverity Run Desktop command is executed, SCA Tools checks its return code. In case non-zero return codes, SCA tools return an error with proper message.

### <a name="coverity-run-desktop-procedure">Coverity Run Desktop procedure</a>

Parameters described in the section:
- `TRANSLATION_UNITS_BLACKLIST` - List of translation units that will be excluded from Coverity Project
- `COVERITY_CONFIG_FILEPATH` - Path to coverity configuration file
- `AUTH_KEY_FILEPATH` - Path to authentication key
- `COVERITY_USERNAME` - Username provided to access Coverity Connect server. Used in conjunction with the password. Must be provided as an environment variable
- `COVERITY_PASSWORD` - Password provided to access Coverity Connect server. Used in conjunction with the username. Must be provided as an environment variable
- `COVERITY_COMMIT_URL` - Use this option to specify the information needed to connect to a Coverity Connect server
- `COVERITY_COMMIT_HOST` -  Name of the server without protocol. DEPRECATED, keeping for compatibility reasons. Use `COVERITY_COMMIT_URL` instead
- `COVERITY_COMMIT_DATAPORT` - Network TCP Port to be used while obtaining data. DEPRECATED, keeping for compatibility reasons. Use `COVERITY_COMMIT_URL` instead
- `COVERITY_COMMIT_STREAM` - Stream name in Coverity Connect platform
- `COVERITY_RUN_DESKTOP_EXTRA_OPTIONS` - List of extra options to be passed to cov-run-desktop command

The analysis starts with translation units (TUs) filtering if `TRANSLATION_UNITS_BLACKLIST` in the following way:
- get list of patterns from `TRANSLATION_UNITS_BLACKLIST`
- for each of pattern it removes the file matched this pattern from project using `cov-manage-emit` tool
- in case `cov-manage-emit` returns exit codes other than 0 and 2 Analysis process will be stopped

The next step is generating connection options to be passed into cov-run-desktop command:
- connection can be established using `COVERITY_COMMIT_URL` or `COVERITY_COMMIT_HOST` in conjunction with `COVERITY_COMMIT_DATAPORT`
- `COVERITY_COMMIT_STREAM` must be specified
- authentication can be performed using `AUTH_KEY_FILEPATH` or `COVERITY_USERNAME` in conjunction with `COVERITY_PASSWORD`
- in case `AUTH_KEY_FILEPATH` is specified, cov-run-desktop command will be extended with proper options to use it as an authentication method
- in case `COVERITY_USERNAME` and `COVERITY_PASSWORD` are specified, `COV_USER` and `COVERITY_PASSPHRASE` environment variables will be overriden respectively during sca_tools execution (native coverity configuration)
- if no authentication or connection methods are provided, sca_tools will exit with proper error message

The final step invokes cov-run-desktop to analyze sources captured during `coverity create`. It includes following actions:
- in case `COVERITY_CONFIG_FILEPATH` is defined the provided configuration will be used
- in case `COVERITY_RUN_DESKTOP_EXTRA_OPTIONS` is defined, cov-run-desktop command will be extended with these arguments
- selects translation units to analyze
- downloads analysis summaries from Coverity Connect
- analyzes selected translation units
- retrieves triage data for analysis results
- filters locally found issues
- outputs returned analysis data in JSON format
