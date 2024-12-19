# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 03_coverity_delta_analysis.feature
# ----------------------------------------------------------------------------

Feature: Delta analysis

  As a sca_tools_package tester
  I want to create a report for a given Coverity project for each config key (combination of coverity version, compiler)
  using delta analysis in order to test whether the reports are created in all format and with expected content.

  Scenario Outline: Report is created
    Given a clean coverity project
    And a json config for <config_key>
      | key                                 | value                                                                              |
      | COMPILE_COMMANDS_BUILD_COMMAND      | bash -c "%(project_root)s/cmake_build.sh variant1"                                 |
      | COVERITY_PROJECT_PATH               | %(test_root)s/test/integration/bin//%(config_key)s_linux_delta                     |
      | EXPORT_FORMATS                      | csv                                                                                |
      | COMPILE_COMMANDS_JSON               | %(project_root)s/build/variant1_gcc_linux/compile_commands.json                    |
    Then create, analyze and export a report for config <config_key> using delta project analysis

    @2021.12 @all
    Examples: Create delta reports for 2021.12 version
      | config_key                    |
      | coverity_gcc_coverity2021.12  |

    @2021.06 @all
    Examples: Create delta reports for 2021.06 version
      | config_key                    |
      | coverity_gcc_coverity2021.06  |

    @2020.12 @all
    Examples: Create delta reports for 2020.12 version
      | config_key                    |
      | coverity_gcc_coverity2020.12  |

    @2020.09 @all
    Examples: Create delta reports for 2020.09 version
      | config_key                    |
      | coverity_gcc_coverity2020.09  |

    @2020.06 @all
     Examples: Create delta reports for 2020.06 version
       | config_key                   |
       | coverity_gcc_coverity2020.06 |
