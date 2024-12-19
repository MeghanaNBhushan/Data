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
#  Filename: changelog.md
# ----------------------------------------------------------------------------
-->

# Changelog for [SCA TOOLS PACKAGE](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse)

All notable changes to this project will be documented in this file.

For further questions about the project please refer to the [README](readme.md).
For project support information please check [README maintainers section](readme.md#maintainers).

[Click here to go to the sca_tools changelog](sca_tools/changelog.md).
[Click here to go to the CDF changelog](sca_tools/cfg/changelog.md).
[Click here the user_manual](doc/user_manual.md).

## [1.8.1] - 2022-02-25

### Changed

- \[[CDF-1334](https://rb-tracker.bosch.com/tracker/browse/CDF-1334)\] Fix for Coverity HIS metrics templates

*NOTE: This will probably be the last version of the sca_tools package, the new way of getting sca_tools is as a python package*

## [1.8.0] - 2022-02-04

### Changed

- \[[CDF-1149](https://rb-tracker.bosch.com/tracker/browse/CDF-1149)\] Updated CCTs for ARM_Compiler_6 R5 and R7
- \[[CDF-750](https://rb-tracker.bosch.com/tracker/browse/CDF-750)\]\[[CDF-1199](https://rb-tracker.bosch.com/tracker/browse/CDF-1199)\] Fixed CCTs for arm compiler, added missing cct files for C code arm_a53, r5, r7
- \[[CDF-885](https://rb-tracker.bosch.com/tracker/browse/CDF-885)\]\[[CDF-1249](https://rb-tracker.bosch.com/tracker/browse/CDF-1249)\] Updated CCTs with an environment variable GHS_HOME and scripts

### Added

- \[[CDF-1282](https://rb-tracker.bosch.com/tracker/browse/CDF-1282)\] Added coding ruleset 2.4, fixed incorrect spelling in user_messages, added missing Coverity versions for installation
- \[[PJDOIT-6306](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-6306)\] Added JQ installation

## [1.7.2] - 2021-10-21

### Changed

- \[[CDF-750](https://rb-tracker.bosch.com/tracker/browse/CDF-750)\] Updated ARM A53 cct configuration

## [1.7.1] - 2021-08-27

Nothing

## [1.7.0] - 2021-08-20

Nothing

## [1.6.2] - 2021-06-02

### Added

- \[[CDF-635](https://rb-tracker.bosch.com/tracker/browse/CDF-635)\] Add v0 of User Manual
- \[[CDF-897](https://rb-tracker.bosch.com/tracker/browse/CDF-897)\] QNX SDK 7.1 for C++17
- \[[CDF-912](https://rb-tracker.bosch.com/tracker/browse/CDF-912)\] GCC and G++ support for 8.4.0 on Linux for C++11
- \[[CDF-955](https://rb-tracker.bosch.com/tracker/browse/CDF-955)\] Clang 12 Linux for C++17
- \[[CDF-969](https://rb-tracker.bosch.com/tracker/browse/CDF-969)\] Support for new cortex m7 ghs arm compiler for C++14
- \[[CDF-976](https://rb-tracker.bosch.com/tracker/browse/CDF-976)\]\[[CDF-988](https://rb-tracker.bosch.com/tracker/browse/CDF-988)\] Bump C++ rules to 2.3 adding new RCF and ACF configurations. Supports Helix 2021.1 out of the box
- \[[CDF-973](https://rb-tracker.bosch.com/tracker/browse/CDF-973)\]\[[CDF-985](https://rb-tracker.bosch.com/tracker/browse/CDF-985)\] MSVC 14.16 (Visual Studio 2017) configuration files for C++17
- \[[CDF-991](https://rb-tracker.bosch.com/tracker/browse/CDF-991)\] Configuration files for TCV162 for C up to 9fp

### Changed

- \[[CDF-993](https://rb-tracker.bosch.com/tracker/browse/CDF-993)\] Fixes modelling of \_\_builtin\_ctz and \_builtin\_popcount for A53 (C++)

### Removed

- \[[CDF-988](https://rb-tracker.bosch.com/tracker/browse/CDF-988)\] CDF 2.2 release configurations in favor of 2.3

## [1.6.1] - 2021-04-16

### Added

Nothing

### Changed

Nothing

### Removed

Nothing

## [1.6.0] - 2021-04-09

### Added

- \[[CDF-814](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-814)\] Adds Helix QAC 2021.1 support with ACFs and TCC script
- \[[CDF-823](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-823)\] Added CMake TCC installation script
- \[[CDF-826](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-826)\] Added GIT TCC installation script
- \[[CDF-829](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-829)\] Allows merge of ACF Files. For an example, check [sca_mini_demo](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_mini_demo/browse)
- \[[CDF-834](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-834)\] Added MISRA 2008 configs

### Changed

- \[[CDF-771](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-771)\] Fixed macro preprocessing with the CL (MSVC) compiler in ACFs
- \[[CDF-782](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-782)\] Added python 3.9.1 TCC option but keeps 3.8.3 as default
- \[[CDF-796](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-796)\] Added HIS Metrics RCF configs
- \[[CDF-797](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-797)\]\[[CDF-913](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-913)\] Added support for Dataflow with QAC 2021.1 and fixes rule groups in RCF for both 2021.1 and 2020.2
- \[[CDF-872](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-872)\] Changes current docker deployment from "default" images to "snapshot" and adds qac and coverity only versions (smalr image sizes)
- \[[CDF-874](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-874)\]\[[CDF-877](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-877)\] Updated Helix QAC documentation to base 2021.1 and adds new RBC++ 2.2 documentations
- \[[CDF-915](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-915)\] Removed Code Guideline traceability from custom help texts

### Removed

- Support for Helix 2019.2 ACFs

## [1.5.0] - 2021-02-12

### Added

- \[[CDF-727](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-727)\] Rollouts RBC 20.0 configs
- \[[CDF-747](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-747)\]\[[CDF-752](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-752)\] Helix 2020.2 and Coverity 2020.12 support
- \[[CDF-749](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-749)\] Adds qac custom help texts based on existing BTC 1.5 available documentation
- \[[CDF-753](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-753)\] JQ TCC installation script and adds it to docker image deps
- \[[CDF-755](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-755)\] TCC_CACHE_PATH usage to tcc scripts

### Changed

- \[[CDF-777](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-777)\] Changes base image implementation to use the DTR available ones

### Removed

- \[[CDF-725](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-725)\]\[[CDF-726](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-726)\] Cleans up configurations

## [1.4.1] - 2020-12-01

### Added

- \[[CDF-718](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-718)\] Helix 2020.2 final version configs for TCC and Docker deployments
- \[[CDF-717](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-717)\] CDF 2.2 generated Coding Rules using CRF, the CDF Generator based on the Excel Spreadsheet version 371

### Changed

- \[[PJDOIT-3957](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3957)\] Fixes the components location for the generated docker image to be inside of the QAC installation in the "components" folder
- \[[CDF-617](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-617)\] Fixes a crash with armclang caused by the removal of the Stub folders from the A9, A53, R5 and R7

### Removed

Nothing

## [1.4.0] - 2020-10-23

### Added

- \[[CDF-679](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-679)\] Adds Helix 2020.2 Beta to the list of selectable TCC installations. This version should only be used for testing and beta feedback purposes
- \[[CDF-699](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-699)\] Adds a [release.md](doc/release.md) to present the current release instructions to the sca_tools and sca_tools_package

### Changed

- \[[CDF-690](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-690)\] Creates a TC1V162 GHS 201815 4fp based CCT on JLR's configuration
- \[[CDF-664](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-664)\] Adds missing ASCM+ and Linux paths to all ACFs

### Removed

- \[[CDF-690](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-690)\] Removes all previous RB 20.0 C CCT files

## [1.3.0] - 2020-09-25

### Added

- \[[CDF-623](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-623)\] Adds the existing configurations for CDF 2.0 pre3, C-Ruleset 20.0 and MISRA C BSW
- \[[PJDOIT-3674](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3674)\] Added Coverity to Docker image

### Changed

Nothing

### Removed

Nothing

## [1.2.1] - 2020-08-21

### Added

- \[[PJDOIT-3451](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3451)\] Adds the possibility of directly outputing filter_qaview to a file

### Changed

- \[[PJDOIT-3451](https://rb-tracker.bosch.com/tracker08/browse/PJDOIT-3451)\] Fixes filter_qaview crashes when severity levels are empty
- \[[CDF-631](https://sourcecode.socialcoding.bosch.com/plugins/servlet/jira-integration/issues/CDF-631)\] Fixes Open UI command in Linux
- \[[CDF-609](https://rb-tracker.bosch.com/tracker/browse/CDF-609)\] Adds 3.8.3 python TCC package

### Removed

- .gitignore for the sca_tools/cfg folder as projects can easily then overwrite it with their own configs

## [1.2.0] - 2020-08-07

### Added

- \[[CDF-629](https://rb-tracker.bosch.com/tracker/browse/CDF-629)\] CCT Generator 2020.08 as obtained from Perforce

### Changed

Nothing

### Removed

Nothing

## [1.2.0] - 2020-08-07

### Added

- \[[CDF-596](https://rb-tracker.bosch.com/tracker/browse/CDF-596)\] Configurations for CDF 1.6.1
- \[[CDF-614](https://rb-tracker.bosch.com/tracker/browse/CDF-614)\] Coverity TCC scripts for 2020.06 and previous versions

### Changed

- \[[CDF-605](https://rb-tracker.bosch.com/tracker/browse/CDF-605)\] Rollsback TCC python version to 3.6.5-14 after finding out that the previous version had not all required package versions.
- Fixes Integration Tests

### Removed

Nothing


### Added

### Changed
- Single Dockerfile changed to one for a technical user ([Dockerfile_tu.in](docker/Dockerfile_tu.in) based)
- And another Dockerfile for the root image ([Dockerfile.in](docker/Dockerfile.in) based)
- It is still possible to use the original root image with the parameters same as before

### Removed


## [1.1.0] - 2020-07-10

### Added

- Added sample Dockerfile
- Created new orga in DTR with the [prebuilt image](https://rb-dtr.de.bosch.com/repositories/swqa/sca_tools_package/)
- Added integration to [Jenkins CI](sca_tools/Jenkinsfile)
- Added config/project_name branches to track project specific history
- Added config/opencv for the [OpenCV Example](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/opencv_demo/browse)
- Added template bat and json files examples
- Added project folder on the root to be filled with project specific needs

### Changed

- TCC scripts to automatically append the latest version and to be able to get the installed TCC package
- Renames qac_tools to sca_tools
- Renamed repo to sca_tools_package
- Adapted integration tests and fixed them

### Removed

Nothing

## [1.0.0] - 2020-05-27

### Added

- qac_tools subfolder
- tcc_scripts subfolder to hold the TCC related scripts
- cfg folder inside of qac_tools/cfg


### Changed

Nothing

### Removed

Nothing
