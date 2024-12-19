# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 04_qac_full_compile_commands_anaylsis.feature
# ----------------------------------------------------------------------------

Feature: Full analysis using compile_commands json

  As a sca_tools_package tester
  I want to create a qac project for each config key (combination of qacversion, synctype and compiler)
  in order to test whether the files are correctly synced.

  Scenario Outline: create qac project with minimal set of files and no additional filtering.

    Given a clean qac project with defined configuration
    And a json config for <config_key>
      | key                                   | value                                                                       |
      | QAC_PROJECT_PATH                      | %(test_root)s/test/integration/bin/%(config_key)s_linux_compile_commands    |
      | SYNC_BUILD_COMMAND                    | bash -c "./cmake_build.sh variant1 "                                        |
      | SYNC_BUILD_LOG_FILE                   | %(project_root)s/build/variant1_gcc_linux/compile_commands.json             |
      | QAC_ANALYSIS_PATH_BLACKLIST           | build,test/integration                                                      |
      | CODEOWNERS_FILE                       | %(test_root)s/test/integration/generated_config/linux/codeowners.txt        |
      | THIRDPARTY_PREFIXES                   | vfc_,daddy_,vmc_                                                            |
    And the codeowners information
      | component              | team       |
      | **modules/core/src/al* | @test_team |
    Then create, analyze, create baseline and export a report for config <config_key> using compile_commands full project analysis

    @2020.1 @all
    Examples: Expected synced files per <config_key>
      | config_key                | expected_synced_files |
      | qac_gcc_json_helix2020.1  | 2                     |

    @2020.2 @all
    Examples: Expected synced files per <config_key>
      | config_key                | expected_synced_files |
      | qac_gcc_json_helix2020.2  | 2                     |

    @2021.1 @all
    Examples: Expected synced files per <config_key>
      | config_key                | expected_synced_files |
      | qac_gcc_json_helix2021.1  | 2                     |

    @2021.2 @all
    Examples: Expected synced files per <config_key>
      | config_key                | expected_synced_files |
      | qac_gcc_json_helix2021.2  | 2                     |

    @2021.3 @all
    Examples: Expected synced files per <config_key>
      | config_key                | expected_synced_files |
      | qac_gcc_json_helix2021.3  | 2                     |