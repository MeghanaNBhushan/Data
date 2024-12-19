# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 01_coverity_create_config.feature
# ----------------------------------------------------------------------------
Feature: Create coverity configuration

  As a sca_tools_package tester
  I want to create configurations for all supported coverity versions
  and combined with different compilers
  in order to test other features of sca_tools_package.

  @all @2020.06 @2020.09 @2020.12 @2021.06 @2021.12
  Scenario: Generate configuration for combinations of coverity versions with different compilers with minimal base configuration options

    Given those coverity versions
      | coverity_version |
      | coverity2020.06  |
      | coverity2020.09  |
      | coverity2020.12  |
      | coverity2021.06  |
      | coverity2021.12  |
    And these options for config generation
      | key                         | value                                                       |
      | COVERITY_BIN_PATH           | C:/TCC/Tools/coverity/%(coverity_version_min)s_WIN64/bin    |
      | COV_BUILD_OPTION_LIST       | [--instrument,--disable-ms-pch]                             |
      | COV_ANALYZE_OPTION_LIST     | [--enable-parse-warnings,--enable PARSE_ERROR]              |
      | TRANSLATION_UNITS_BLACKLIST | [C:/Program.*,C:/TCC/.*]                                    |
      | COVERITY_COMMIT_HOST        | abts5340.de.bosch.com                                       |
      | COVERITY_COMMIT_DATAPORT    | 9090                                                        |
      | COVERITY_COMMIT_STREAM      | opencv_demo_msvc                                            |
    And the codeowners information
      | component              | team       |
      | **src\demo\*           | @test_team |
    Then configurations are generated for those compilers
      | key  | value  |
      | msvc | --msvc |
