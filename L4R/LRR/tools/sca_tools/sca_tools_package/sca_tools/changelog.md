<!---
# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 	changelog.md
# ----------------------------------------------------------------------------
-->

# Changelog for [SCA TOOLS](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools/browse)

All notable changes to this project will be documented in this file.

For further questions about the project please refer to the [README](readme.md).
For project support information please check [README#maintainers](readme.md#maintainers).

## [1.8.X] - 2022-XX-XX

## [1.8.1] - 2022-02-25

#### Added

#### general

- \[[PJDOIT-6697](https://rb-tracker.bosch.com/tracker/browse/PJDOIT-6697)\] Added version option to cli

#### coverity

- \[[PJDOIT-6304](https://rb-tracker.bosch.com/tracker/browse/PJDOIT-6304)\] Added coverity run_desktop subcommand

#### Changed

#### general

- \[[CDF-1316](https://rb-tracker.bosch.com/tracker/browse/CDF-1316)\] Updated license

#### qac

- \[[PJDOIT-6695](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6695)\] Improved cleanup_on_create behavior, changed default value to False, fixed analyze_list behavior for 'BUILD_LOG' and 'MONITOR' sync types

## [1.8.0] - 2022-02-04

### Added

#### general

- \[[PJDOIT-6121](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6121)\] Added possibility to generate state file without git installed

#### qac

- \[[PJDOIT-6072](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6072)\] Added possibility to provide extra arguments to qacli view via `QACLI_VIEW_EXTRA_ARGS`
- \[[PJDOIT-6320](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6320)\] Added possibility to execute extra commands after qac project creation via `QACLI_POST_CREATE_COMMANDS`
- \[[PJDOIT-6589](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6589)\] Added deprecation message for `qac state` subcommand

### Changed

#### general

- \[[PJDOIT-6569](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6569)\] Cleaned up codebase
- \[[PJDOIT-6330](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6330)\] Fixed pip packages installation on Linux
- \[[PJDOIT-6228](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6228)\] Fixed datastore paths merging logic
- \[[PJDOIT-6131](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6131)\] Removed InDirectory class and improved files lookup

#### qac

- \[[CDF-1200](https://rb-tracker.bosch.com/tracker/browse/CDF-1200)\] Improved QAC Analyze exit code logging
- \[[PJDOIT-6306](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6306)\] Migrated QAC reporting functionality to pandas
- \[[PJDOIT-3772](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3772)\] Refactored QAC project creation functionality and improved logging

#### unify_reports

- \[[PJDOIT-6132](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6132)\] Improved processing of duplicated fields

## [1.7.2] - 2021-10-21

### Added

#### general

- \[[CDF-1166](https://rb-tracker.bosch.com/tracker/browse/CDF-1166)\] Added `swq.py` location to logs

#### qac

- \[[PJDOIT-5865](https://rb-tracker.bosch.com/tracker/browse/PJDOIT-5865)\] Added license violation header to filter_qaview report
- \[[PJDOIT-5868](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-5868)\] Added possibility to accept list in `QAC_CONFIG_PATH`

### Changed

#### general

- \[[PJDOIT-5834](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-5834)\] Replaced suds-jurko package with suds-py3 for SWQ module installation

#### qac

- \[[CDF-899](https://rb-tracker.bosch.com/tracker/browse/CDF-899)\] Made `project_root`'s drive letter case insensitive
- \[[CDF-1071](https://rb-tracker.bosch.com/tracker/browse/CDF-1071)\] Improved subdiagnostics output
- \[[PJDOIT-5898](https://rb-tracker.bosch.com/tracker/browse/PJDOIT-5898)\] Removed open-8-and-9 severities report generation
- \[[PJDOIT-5899](https://rb-tracker.bosch.com/tracker/browse/PJDOIT-5899)\] Improved `SCA Tools Subdiagnostics Origin` format (new format is \<filepath\>:\<line\>:\<column\>:\<producer\>:\<msgnum\>)
- \[[PJDOIT-5914](https://rb-tracker.bosch.com/tracker/browse/PJDOIT-5914)\] Fixed threshold warnings report file creation

#### coverity

- \[[PJDOIT-5771](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-5771),[PJDOIT-5987](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-5987)\] Improved Coverity authentication (`COVERITY_USERNAME` and `COVERITY_PASSWORD` are not mandatory anymore for `upload` and `preview_report` subcommands)


## [1.7.1] - 2021-08-27

### Changed

#### compiler_warnings

- \[[PJDOIT-5293](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-5293)\] Fixed greenhills compiler log parsing in `compiler_warnings`

## [1.7.0] - 2021-08-20

### Added

#### qac

- \[[CDF-1087](https://rb-tracker.bosch.com/tracker/browse/CDF-1087)\] Added parameter to disable QAC Project optimization
- \[[CDF-1104](https://rb-tracker.bosch.com/tracker/browse/CDF-1104)\] Added possibility to generate warnings exceeding report in filter_qaview
- \[[PJDOIT-5439](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-5439)\] Added parameter for diagnostics output cleanup
- \[[PJDOIT-5101](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-5101)\] Added hashsum verification mechanism for baseline

#### coverity

- \[[CDF-1105](https://rb-tracker.bosch.com/tracker/browse/CDF-1105)\] Added parameter to pass Coverity Auth Key File for authentication on Coverity Connect
- \[[PJDOIT-4997](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4997)\] Implemented support of JSON v8 in Coverity Reporting
- \[[PJDOIT-4772](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4772)\] Implemented support of generating reports in multiple formats for Coverity

#### find_includes

- \[[CDF-1103](https://rb-tracker.bosch.com/tracker/browse/CDF-1103)\] Added parameter to configure git diff filter

#### compiler_warnings

- \[[CDF-1133](https://rb-tracker.bosch.com/tracker/browse/CDF-1133)\] Added `compiler_warnings` command, which generates compiler warnings report based on compiler log

### Changed

#### general

None

#### qac

None

#### coverity

None

### Removed

None

## [1.6.2] - 2021-06-02

### Changed

#### general

None

#### qac

- \[[CDF-930](https://rb-tracker.bosch.com/tracker/browse/CDF-930)\]\[[CDF-979](https://rb-tracker.bosch.com/tracker/browse/CDF-979)\] Id, depth and filename fields were wrongly generated. Ensures that the filepath for the subdiagnostics are properly generated
- \[[PJDOIT-5088](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-5088)\] Added --with_subdiagnostics CLI option for qac state command to enable subdiagnostics information in generated reports
- \[[PJDOIT-5120](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-5120)\] Metrics are not exported by default. CLI option --with_metrics enables both their export and metrics report generation.

#### coverity

- \[[CDF-965](https://rb-tracker.bosch.com/tracker/browse/CDF-965)\] Webapi export report directory is now under coverity_project_path/sca_tools
#### qac

#### coverity

None

## [1.6.1] - 2021-04-16

### Changed

#### general

- \[[PJDOIT-4937](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4937)\] CLI options helper_set_baseline, build_shell, sonarqube, and vscode_integration did not work

#### qac

- \[[PJDOIT-4937](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4937)\] Resolve LOCAL_BASELINE_PATH absolute path when it is set relative to PROJECT_ROOT

#### coverity

- \[[PJDOIT-4937](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4937)\] Move coverity configuration directory outside of sca_tools
- \[[PJDOIT-4937](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4937)\] Disable IO redirection in compile_commands.json compiler and inherit settings from parent process

## [1.6.0] - 2021-04-09

### Added

#### general

- \[[CDF-733](https://rb-tracker.bosch.com/tracker/browse/CDF-733)\] Added unify_reports command to merge QAC reports for several build variants
- \[[PJDOIT-4947](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4947)\] Add limitation for parallel jobs

#### coverity

- \[[PJDOIT-4760](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4760)\] Add parallel compilation support of compile_commands.json to coverity create
- \[[PJDOIT-4800](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4800)\] Add stdout and vscode export formats for integration with VSCode

### Changed

#### general

- \[[CDF-746](https://rb-tracker.bosch.com/tracker/browse/CDF-746)\] SCA Tools have now python package structure
- \[[PJDOIT-4697](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4697)\], \[[PJDOIT-4783](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4783)\] Implement support for multiple datastores
- \[[PJDOIT-4710](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4710)\] SCA Tools reporting commands accept list of CODEOWNERS files

#### qac

- \[[CDF-767](https://rb-tracker.bosch.com/tracker/browse/CDF-767)\] SCA Tools generate all QAC artifacts in specific folder
- \[[CDF-793](https://rb-tracker.bosch.com/tracker/browse/CDF-793)\] Remove unnecessary mapped no in merged RCFs
- \[[CDF-816](https://rb-tracker.bosch.com/tracker/browse/CDF-816)\], \[[CDF-830](https://rb-tracker.bosch.com/tracker/browse/CDF-830)\] Add support for QAC subdiagnostics in SCA Tools reporting
- \[[CDF-829](https://rb-tracker.bosch.com/tracker/browse/CDF-829)\] Add support for list of ACF files
- \[[CDF-838](https://rb-tracker.bosch.com/tracker/browse/CDF-838)\] SYNC_BUILD_LOG_FILE is now mandatory only for qac create command
- \[[CDF-895](https://rb-tracker.bosch.com/tracker/browse/CDF-895)\] Deprecate qaview command
- \[[PJDOIT-4729](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4729)\] QAC Analyze command line options were renamed: analyse_list to analyze_list, analyse_file to analyze_file
- \[[PJDOIT-4891](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4891)\] QAC QA View fails on xlsx creation with non-ASCII symbols in suppression justifications
- \[[PJDOIT-4892](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4892)\] Support QAC suppression justifications in state export
- \[[PJDOIT-4962](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4962)\] Fix invocation of sync_build_command when sync type is MONITOR

#### coverity

- \[[CDF-768](https://rb-tracker.bosch.com/tracker/browse/CDF-768)\] SCA Tools generate all Coverity artifacts in specific folder
- \[[CDF-788](https://rb-tracker.bosch.com/tracker/browse/CDF-788)\], \[[CDF-799](https://rb-tracker.bosch.com/tracker/browse/CDF-799)\] Run coverity commands in PROJECT_ROOT
- \[[CDF-898](https://rb-tracker.bosch.com/tracker/browse/CDF-898)\] Newlines in code snippets break Coverity CSV reports

### Removed

- \[[PJDOIT-4760](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4760)\] Remove compile_commands command

## [1.5.0] - 2021-02-12

### Added

#### general

- \[[PJDOIT-4276](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4276)\] Improves commandline output on sca_tools call

#### qac

- \[[PJDOIT-4299](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4299)\] Support for legacy \_\_bosch_help\_\_ and \_\_qa_help\_\_ documentations from BTC 1.5
- \[[PJDOIT-4489](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4489)\]\[[PJDOIT-4318](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4318)\]\[[PJDOIT-4222](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4222)\] *rule_group* from *custom* folder gets automatically replaced on RCF help path attribute on id match. USER_MESSAGES help path attribute is likewise automatically replaced

### Changed

#### general

- \[[PJDOIT-4310](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4310)\]\[[PJDOIT-4044](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4044)\]\[[PJDOIT-4275](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4275)\] Stability improvements
- \[[PJDOIT-4145](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4145)\] Adds support for CSV_ZIP as an input format
- \[[PJDOIT-4545](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4545)\] Fixes bug with single valued environmental variables whose type is a list

#### qac

- \[[CDF-754](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-754)\] Ensures correct initialization order with --cleanup_on_create true
- \[[CDF-757](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-757)\] No longer exports report-metrics.html on state creation due to high storage usage
- \[[PJDOIT-4486](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4486)\] Ensures successful return on empty project creation and analysis
- \[[PJDOIT-4324](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4324)\] VCF is no longer a mandatory config file for the project setup

#### coverity

- \[[CDF-756](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-ticket_num)\]\[[PJDOIT-4418](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4418)\] Fixes crashes with compile_commands_json for coverity subcommand and improves messaging for build

#### map_teams

- \[[PJDOIT-4328](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4328)\] git_ignore_mapping is now an alias, the actual parameter is --only_last_team
- \[[PJDOIT-4357](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4357)\] Improves CODEOWNERS syntax
- \[[PJDOIT-4319](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4319)\] Performance speedup

### Removed

Nothing

## [1.4.1] - 2020-11-27

### Added

Nothing

### Changed

- \[[CDF-714](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-714)\] Adds the config folder from the QAC default package as the last search option for configs to solve potential missing config files issues
- \[[CDF-707](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-707)\] Solves the precedency of the git diff for the find_includes
- \[[PJDOIT-4021](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4021)\] Fixes Coverity crash while generating filtered CSV exports
- \[[PJDOIT-4033](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-4033)\] Fixes the path calculation in the glob call that would cause the scripts to wrongly not find existing components in a Unix environment

### Removed

Nothing

## [1.4.0] - 2020-10-23

### Added

- \[[CDF-670](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-670)\] Allows merging multiple NCFs into a single
- \[[CDF-671](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-671)\] Allows merging multiple RCFs into a single
- \[[CDF-672](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-672)\]\[[PJDOIT-3814](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3814)\]  Allows merging multiple user_messages.xml into a single
- \[[PJDOIT-3510](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3510)\] Debugging message for unset values and usage of defaults
- \[[PJDOIT-3763](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3763)\] Allows translation units blacklist to be applied to coverity reporting
- \[[PJDOIT-3913](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3913)\] Implements the possibility of filtering metrics as obtained from the HMR reporting. This allows users to specify HIS metrics to be uploaded to Splunk, for example

### Changed

- \[[CDF-639](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-639)\] qac, coverity and find_includes subcommands can run without providing a datastore target on the commandline
- \[[CDF-668](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-668)\] C files are analyzed back with C coding rules by default (previously it was as C++)
- \[[CDF-688](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-688)\] All dump messages the name of the return code alongisde with the number and no longer the env variables by default. The dump of env variables is only enabled in DEBUG
- \[[PJDOIT-3582](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3582)\] Improves compile_commands subcommand implementation
- \[[PJDOIT-3681](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3681)\] Adds state.json export to coverity
- \[[PJDOIT-3697](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3697)\] Add Splunk QAC Warnings Format
- \[[PJDOIT-3751](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3751)\] Adds --justification_message_regular_expression for bitmasks 1 to 5
- \[[PJDOIT-3816](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3816)\]\[[PJDOIT-3831](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3831)\] Refactorings and stability increases

### Removed


- \[[CDF-692](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-692)\] All default values from commandline parameters of the qac subcommand to make it possible to set the parameters on the config json and environmental variables too
- \[[CDF-693](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-693)\] The default values from commandline parameters of the coverity subcommand to make it possible to set the parameters on the config json and environmental variables too
- \[[CDF-693](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-693)\] Unused -cll parameter in coverity

## [1.3.0] - 2020-09-25

### Added

- \[[PJDOIT-3768](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3768)\] Adds support for shell scripts on compile_commands
- \[[PJDOIT-3782](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3782)\] Adds ACF and User Messages to Summary Report
- Adds export_analysis as a new command for exporting the qac analysis results
- Adds compile_commands new command that enables the delta analysis for Coverity

### Changed

- \[[CDF-555](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-555)\] Handles negative return codes when Helix QAC 2020+ misbehaves
- \[[CDF-639](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-639)\] qac, coverity and find_includes subcommands can run without providing a datastore target on the commandline
- \[[PJDOIT-3179](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3179)\] Improves git operations used in find_includes and their error handling
- \[[PJDOIT-3510](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3510)\] Script now prints a message in DEBUG mode to explicitly demonstrate that a value is not defined
- \[[PJDOIT-3584](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3584)\] Prints COV_USER and COV_PASSPHRASE overriding warning only when they already preexist
- \[[PJDOIT-3598](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3598)\] Logs out the unused / unparsed parameters from the configuration file
- \[[PJDOIT-3692](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3692)\] Implements map_teams subcommand to extract additional Git Information to modules. Migrated from lucxbox
- \[[PJDOIT-3740](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3740)\] Switches the internal implementation of the export mechanism to use XMLs instead of the standard output for reliability purposes
- \[[PJDOIT-3778](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3778)\] Fixes TU pattern parameter for Coverity on Linux machines
- \[[PJDOIT-3787](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3787)\] Fixes CL JSON patch script
- No longer removes the printing of security sensitive variables but instead substitute their values with '****' symbols

### Removed

- fix_ninja_json is now removed, now it is called fix_cl_json
- state_no_metrics as its functionality is now replaced with export_analysis

## [1.2.1] - 2020-08-21

### Added

- \[[PJDOIT-3451](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3451)\] Redirection possibility of outputing filter_qaview to a file

### Changed

- \[[PJDOIT-3451](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3451)\] Fixes filter_qaview crashes when severity levels are empty
- \[[CDF-631](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-631)\] Fixes Open UI command in Linux
- \[[CDF-632](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-632)\] Fixes inverted property set when QAC_SYNC_SETTINGS_INCLUDE_PATH is used
- \[[CDF-636](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-636)\] Ensures that COV_USER and COVERITY_PASSPHRASE matches COVERITY_USER AND COVERITY_PASSWORD if these two environmental variables are set
- \[[CDF-637](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-637)\] Avoids printing username and passwords for both QAC and COVERITY subcommands


### Removed

Nothing

## [1.2.0] - 2020-08-07

### Added

- \[[PJDOIT-2988](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-2988)\] Create a compile commands builder for splitting monolithic compile_commands.json files
- \[[PJDOIT-3248](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3248)\]\[[PJDOIT-3329](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3329)\] Unifies reports and provides a per severity level and supression summary
- \[[CDF-597](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-597)] Allows c files to be analyzed with c coding rules configuration
- \[[PJDOIT-3340](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3340)] Implements the mapping of header to source files -wmr find_includes parameter

### Changed

- \[[CDF-588](https://rb-tracker.bosch.com/tracker/browse/CDF-588)\] Removes environmental override for Coverity
- \[[PJDOIT-3227](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3227)\] Updates unit tests
- Tested out with coverity_mini_demo
- \[[CDF-614](https://rb-tracker.bosch.com/tracker/browse/CDF-614)\] Adds coverity json and env variables documentation

### Removed

Nothing

## [1.1.1] - 2020-07-17

### Added

Nothing

### Changed

- Adapts header and source suppression list to new input parsing mechanism
- Fixes bug with sync json whitelist parameter that would render it unusable
- Fixes optimization flag on PRQA versions
- Refactors check_qaview into filter_qaview subcommand.

### Removed

Nothing

## [1.1.0] - 2020-07-10

### Added

- ENV variable parsing for all possible FILE Configurations. Comprehensive list in [README](readme.md)
- Integrated [Coverity Helper](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/coverity_helper/browse) with sca_tools
- Linux Support
- Integration with DACORE

### Changed

- Renamed qac_tools to sca_tools
- Increased unit testing coverage
- Separated subcommands into: qac, coverity and find_includes (prior find_cpps)
- Changed the fix_json to fix_ninja_json as a subcommand from qac
- Moved check_qaview into several subcommands
- Common parameters are given directly to subcommands. E.g. -dp -dt -pr are given to qac subcommands as of now
- Improved manual description and documentations
- Consolidated all scripts into sca_tools root folder
- Added QAC_HELPER_LOGS_PATH to be able to customize where the logs will be generated
- Adds SKIP_EXIT_ON_BUILD_RETURN_CODES to customize the possible return codes from the build
- Makes it possible to either define txt files or a JSON array with the file contents for several parameters
- Fixes a PROJECT_ROOT QAC bug where the variable was given with project_root instead and QAC is case sensitive

### Removed

- fix_json subfolder
- check_qaview

## [1.0.0] - 2020-05-27

### Added

- Unit Tests for core features
- CI Integration
- Baseline documentation

### Changed

- Created a common folder for a code library
- Renamed prqa_helper to qac_tools

### Removed

- Common code functionality that was extracted
- TCC scripts


