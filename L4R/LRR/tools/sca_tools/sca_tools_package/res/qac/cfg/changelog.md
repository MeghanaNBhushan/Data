<!--- 
# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2020 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
# Filename: 	changelog.md
# Author(s): 	Andre Silva (CC-AD/ESW4)
# ----------------------------------------------------------------------------

-->
# Changelog for [CDF QAF](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/prqa_qaf/browse)

All notable changes to this project will be documented in this file.

For further questions about the project please refer to the [README](readme.md).
For project support information please check [MAINTAINERS](readme.md#maintainers).

## [1.6.1] - 2020-07-29

### Added

- This changelog
- Support for QNX Compiler
- TCC package / config for Helix 2020.1
- Tailoring option for tool checkers qacpp-4941 / CERTC.DCL39-C Definite: Passing a padded structure from a trusted boundary to another domain
- qacpp-4.5.0-0403: "No matching functions" false positive
- qacpp-4.6.0-3018: "Unexpected value" warning for numbers within range


### Changed

- NEON level 9 qacpp warning: missing vld2q model
- Helix wrong tool mappings 
- Line-break issues in the CDF xml database
- qacpp-4.5.0-0621: Critical Parsing error, parser failures for ARMClang ccts do not work with Helix2020.1 any more: result are parse errors with the functional stub

### Removed

Nothing

## [1.6.0] - 2020-05-18

### Added

- Default version is now Helix QAC 2020.1
- PRQA 4066: braces for case statements [QAC-38391] 
- PRQA 3842: in wrong rule? [QCT-38398, QCT-38400] 

### Changed

- Improved file tree performance problems
- Solves path calculation on ARM_Compiler_6_A53.py and R7 file

### Removed

Nothing
