# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: 01_qac_create_config.feature
# ----------------------------------------------------------------------------
Feature: CONFIG

  As a sca_tools_package tester
  I want to create json configurations for all supported qac versions
  combined with the sync types
  and combined with different compilers
  in order to test other features of sca_tools_package.

  @all @2020.1 @2020.2 @2021.1 @2021.2 @2021.3
  Scenario: Generates configuration for combinations of qac versions with synctypes with different compilers with minimal base configuration options

    Given those helix versions and specifications
      | qac_version | coding_rules_version | component_version | rcf_file          |
      | helix2020.1 | 2.2_0373             | qacpp-4.6.0       | default-en_US.rcf |
      | helix2020.2 | 2.2_0373             | qacpp-4.7.0       | default-en_US.rcf |
      | helix2021.1 | 2.2_0373             | qacpp-4.8.0       | default-en_US.rcf |
      | helix2021.2 | 2.3_0373             | qacpp-5.0.0       | default-en_US.rcf |
      | helix2021.3 | 2.4                  | qacpp-5.1.0       | default-en_US.rcf |
    And these synctypes
      | key     | synctype |
      | json    | JSON     |
      | monitor | MONITOR  |
    And these options for config generation
      | key             | value                                                                               |
      | PROJECT_ROOT    | %(project_root)s                                                                    |
      | QAC_BIN_PATH    | /opt/Perforce/Helix-QAC-%(qac_version_min)s/common/bin                              |
      | QAC_CONFIG_PATH | tools/sca/ip_sca_tools_package/res/qac/cfg                                          |
      | ANALYZE_PARAMS  | --file-based-analysis --force-complete --inter-tu-dataflow --show-timings --retry 2 |
      | ACF_FILE        | default.acf                                                                         |
      | VCF_FILE        | prqavcs.xml                                                                         |
      | QAC_MODULES     | [%(qacpp_version)s]                                                                 |
      | USER_MESSAGES   | helix2021.2_CPP_2.4_component_path.xml                                              |
    Then configurations are generated for those compilers
      | qac_version | compiler | cct                                                                                                   |
      | helix2020.1 | gcc      | [GNU_GCC-gcc_8.3-x86_64-generic-linux-C-c11.cct,GNU_GCC-g++_8.3-x86_64-generic-linux-C++-c++11.cct]   |
      | helix2020.2 | gcc      | [GNU_GCC-gcc_8.3-x86_64-generic-linux-C-c11.cct,GNU_GCC-g++_8.3-x86_64-generic-linux-C++-c++11.cct]   |
      | helix2021.1 | gcc      | [GNU_GCC-gcc_8.3-x86_64-generic-linux-C-c11.cct,GNU_GCC-g++_8.3-x86_64-generic-linux-C++-c++11.cct]   |
      | helix2021.2 | gcc      | [GNU_GCC-gcc_8.3-x86_64-generic-linux-C-c11.cct,GNU_GCC-g++_8.3-x86_64-generic-linux-C++-c++11.cct]   |
      | helix2021.3 | gcc      | [GNU_GCC-gcc_8.3-x86_64-generic-linux-C-c11.cct,GNU_GCC-g++_8.3-x86_64-generic-linux-C++-c++11.cct]   |
