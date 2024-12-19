# QAC Configuration

* [About](#about)
* [Maintainers](#maintainers)
* [General information about QAC](#general)
* [Configuration](#configuration)
  * [QAC configuration](#qac_config)
  * [Minimal QAC configuration](#mini_config)
  * [Analysis configuration](#acf)
  * [Rules configuration](#rcf)
  * [Compiler Configuration Template](#cct)
  * [User Messages configuration](#user)
  * [Additional configuration](#additional)
* [How to contribute](#contribute)
* [Feedback](#feedback)


## <a name="about">About</a>

As part of SCA_TOOLS_PACKAGE the configuration for QAC static code analysis and help files are shipped here.


## <a name="maintainers">Maintainers</a>

  * [Ingo Jauch (CC-AD/ESW4)](https://connect.bosch.com/profiles/html/profileView.do?key=fccee294-fb86-40cf-8c78-6917f4a69e13)
  * [André Silva (CC-AD/ESW4)](https://connect.bosch.com/profiles/html/profileView.do?key=da1769d2-3f48-4549-962f-5b711cdc45c9)


## <a name="general">General information about QAC</a>

* The basic tool is installed using TCC: 

    > C:\TCC\tools\helix_qac\xxxx.y_WIN64

* The local QAC GUI can be called via 

    > C:\TCC\tools\helix_qac\xxxx.y_WIN64\common\bin\qagui.exe

* The plugins for MS Visual Studio / Eclipse can be installed from here

    > C:\TCC\tools\helix_qac\xxxx.y_WIN64\ide_plugins

## <a name="configuration">Configuration</a>

### <a name="qac_config">QAC configuration</a>
* The default configuration files are here:
    > C:\TCC\tools\helix_qac\xxxx.y_WIN64\config\

* QAC creates a user specific configuration folder under AppData\Local
    > C:\Users\<YOUR_NT_USERNAME>\AppData\Local\Perforce\<year>.<version>_WIN64
    
* It is possible to work with the default configuration shipped by QAC.
<br>
<br>


### <a name="mini_config">Minimal QAC configuration</a>
A minimal configuration consists of:

| Config File Name                      | Explanation                                                                                                                                                                                                     |
|---------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Analysis Configuration File (acf)     | Defines the components to be used for analysis depending on the language, e.g. qac for C, qacpp for C++ (Components and their purpose see below). In addition to this settings for each component can be given. |
| Rules Configuration File              | Defines coding standard rules and messages used to enforce these rules using messages.                                                                                                                          |
| Compiler Configuration Template (cct) | Defines compiler related settings (flags, include paths)                                                                                                                                                        |
| User Messages File                    | Defines Texts, severity levels and help links for each message.                                                                                                                                                 |
<br>

### <a name="acf">Analysis Configuration:</a>
- The _Analyser Config File (acf)_ holds the information which checker modules with what version shall be used (e.g. qacpp v 4.3.0), which compiler config shall be used, and some coding-rule specific settings (e.g. metric thresholds).
- Analysis configurations provided by QAC <br>
  can be found here: C:\TCC\Tools\helix_qac\<year>.<version>_WIN64\config\acf <br>
- Rules configurations provided by SCA_TOOLS_PACKAGE<br>
  can be found [here](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse/res/qac/cfg/config/rcf) <br>
- SCA_TOOLS_PACKAGE provides different kind of acf files:
  * acf files provided by C and CPP experts uses the following naming convention:
    > config/acf/helix<year><version>_<language>_<scope>_FILES_<coding_rules_version>_<internal_version>.acf 

    **Example:**<br>

    > helix2020.2_C_ALL_FILES_20.0_0373.acf <br>
    for Helix version 2020.2, for language C, scope "ALL" files, coding rule set version 2.0 and internal version 0373

  * acf files for dataflow have additional options to enable dataflow:
    ```
      <option argument="+" name="-enabledataflow"></option>
        <option argument="2048" name="-maxrecursivetemplatenestingdepth "></option>
        <!-- Uncomment for default timeouts (can sharply decrease runtime) -->
        <!-- <option argument="df::query_timeout=500" name="-prodoption "/> -->
        <!-- <option argument="df::function_timeout=10000" name="-prodoption "/> -->
        <option argument="df::inter=5" name="-prodoption "></option>
        <option argument="df::analyse_header_functions=intra" name="-prodoption "></option>
        <option argument="df::cma-" name="-prodoption "></option>
        <option argument="df::query_timeout_message+" name="-po "></option>
        <option argument="df::struct_last_array_member_size_1+" name="-po "></option>
    ```

    **Example:**<br>

    > helix_2020.2_dataflow_rule_groups.acf <br>
    for Helix version 2020.2

  * acf files supporting HIS metrics have additional metrics settings:
    ```
    <!-- code metric parameters -->
      <option argument="+" name="-ppmetrics"></option>
      <option argument="STCYC>20:6040" name="-threshold "></option>
      <option argument="STPTH>1000:6141" name="-threshold "></option>
      <option argument="STPAR>9:6042" name="-threshold "></option>
      <option argument="STMIF>4:6043" name="-threshold "></option>
      <option argument="STST3>100:6044" name="-threshold "></option>
      <option argument="STGTO>0:6045" name="-threshold "></option>
    ```
  * acf files supporting HIS metrics for early code checks have additional metrics settings:
    ```
    <!-- code metric parameters -->
    <option argument="+" name="-ppmetrics"></option>
    <option argument="STCYC>15:6140" name="-threshold "></option>
    <option argument="STPTH>800:6141" name="-threshold "></option>
    <option argument="STPAR>5:6142" name="-threshold "></option>
    <option argument="STMIF>2:6143" name="-threshold "></option>
    <option argument="STST3>80:6144" name="-threshold "></option>
    <option argument="STGTO>0:6145" name="-threshold "></option>
    ```
    Note: in the early code his metrics acf the treshold are much lower to enable the developers to handle issues before they get urgent.
    **Example:**<br>

    > enable_code_his_metrics.acf <br>
    > enable_early_code_his_metrics.acf <br>
    


- SCA_TOOLS_PACKAGE can merge a list of acf files, e.g. in order to use Cpp Language support and adding support for HIS metrics.

<br>
<br> 

### <a name="rcf">Rules Configuration:</a>
- The _Rule Config File (rcf)_ holds the information, which coding rules shall be checked by the tool.
- Rules configurations provided by QAC <br>
  can be found here: C:\TCC\Tools\helix_qac\<year>.<version>_WIN64\config\rcf <br>
- Rules configurations provided by SCA_TOOLS_PACKAGE<br>
  can be found [here](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse/res/qac/cfg/config/rcf) <br>
- SCA_TOOLS_PACKAGE provides different kind of rcf files:
  * rcf files provided by C and CPP experts uses the following naming convention:
    > config/rcf/helix<year><version>_<language>_<scope>_FILES_<coding_rules_version>_<internal_version>.rcf   

    **Example:**<br>

    > helix2020.2_C_ALL_FILES_20.0_0373.rcf <br>
    for Helix version 2020.2, for language C, scope "ALL" files, coding rule set version 2.0 and internal version 0373

  * rcf files for dataflow provide grouped collection of active dataflow checkers

    **Example:**<br>

    > helix_2020.2_dataflow_rule_groups.rcf <br>
    for Helix version 2020.2

  * rcf files supporting HIS metrics provide a grouping of HIS related checkers

    **Example:**<br>

    > enable_code_his_metrics.rcf <br>
    > enable_early_code_his_metrics.rcf <br>

- SCA_TOOLS_PACKAGE can merge a list of rcf files, e.g. in order to use C/C++ Language support and adding support for HIS metrics.
<br>
<br>

### <a name="cct">Compiler Configuration Template:</a>
- The _Compiler Configuration Template (cct)_ contains compiler related information like include paths and compiler flags.
- Compiler configurations provided by QAC <br>
  can be found here: C:\TCC\Tools\helix_qac\<year>.<version>_WIN64\config\cct

- SCA_TOOLS_PACKAGE provides additional compiler configurations [here](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse/res/qac/cfg/config/cct?at=refs%2Fheads%2Ffeature%2FCDF-940-improve-cfg-readme-in-sca_tools_package):

  | Compiler Type | Compiler Version | Target | OS  | CCT |
  | - | - | - | - | - |
  | ARM Compiler | 6.6.1 | ARMv7 Cortex-R5 | Win | ARM_Compiler_6_R5.cct |
  | ARM Compiler | 6.6.1 | ARMv7 Cortex-R7 | Win | ARM_Compiler_6_R7.cct |
  | ARM Compiler | 6.6.1 | ARMv8 Cortex-A53 | Win | ARM_Compiler_6_A53.cct |
  | GHS Compiler | 201715     | Tricore/Aurix | Win | GHS_201715_standalone_TC1V162_C++11.cct |
  | GHS Compiler | 201815 xfp | Tricore/Aurix | Win | GHS_201815_standalone_xfp_TC1V162_C++11.cct |
  | GHS Compiler | 201713     | RH850 | Win | GHS_201713_testversion1i_rh850_C++11.cct
  | GHS Compiler | 201815 xfp | RH850 | Win | GHS_201815_standalone_xfp_RH850_C++11.cct |
  | GCC Compiler | GNU G++ 7.4 | | Linux | GNU_GCC-g++_7.4.0-x86_64-linux-gnu-C++-c++11.cct |
  | GCC Compiler | GNU GCC 7.4 | | Linux | GNU_GCC-gcc_7.4.0-x86_64-linux-gnu-C-c11.cct |
  | GCC Compiler | QNX 7.0.0   | | Win | GNU_GCC-qcc_5.4.0-x86_64-pc-nto-qnx7.0.0-C++-c++1.cct |


- Generate own compiler configuration<br>
  The CCT Generator by QAC can be found in C:\TCC\Tools\helix_qac\<year>.<version>_WIN64\tools\cct_generator <br>
  **Example:** <br>
  [CCT Generator Manual for 2021.1](C:\TCC\Tools\helix_qac\2021.1_WIN64\tools\cct_generator\CCT_Generator_Manual.pdf)
<br>
<br>

### <a name="user">User Messages Configuration:</a>
- The _User Messages File_ holds the mapping of the code metrics setup to the displayed warning messages.
- Compiler configurations provided by QAC <br>
  can be found here: C:\TCC\Tools\helix_qac\<year>.<version>_WIN64\config\cct

- Compiler configurations provided by SCA_TOOLS_PACKAGE<br>
  can be found [here](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse/res/qac/cfg/user_library/user_messages) <br>
- SCA_TOOLS_PACKAGE provides different kind of user messages files:
  * user messages files provided by C and CPP experts uses the following naming convention:
    > config/user_library/user_messages/helix<year><version>_<language>_<scope>_FILES_<coding_rules_version>_<internal_version>_4helper.xml   

    **Example:**<br>

    > helix2020.2_C_ALL_FILES_20.0_0373_4helper.xml <br>
    for Helix version 2020.2, for language C, scope "ALL" files, coding rule set version 2.0 and internal version 0373

  * user messages files supporting HIS metrics provide all texts, help links and severities of HIS related checkers

    **Example:**<br>

    > enable_code_his_metrics.xml <br>
    > enable_early_code_his_metrics.xml <br>

- SCA_TOOLS_PACKAGE can merge a list of user messages files, e.g. in order to use C/C++ Language support and adding support for HIS metrics.
<br>
<br>

### <a name="additional">Additional configurations:</a>
- The _Name Config File (ncf)_ holds the configuration to check for the C++ naming rules.
- Name check configurations provided by SCA_TOOLS_PACKAGE<br>
  can be found [here](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse/res/qac/cfg/config/ncf) <br>

- The _Version Control Config File (vcf)_ holds the setup how to connect to the BIOS SocialCoding Bitbucket server via git.
- Version control configurations provided by SCA_TOOLS_PACKAGE<br>
  can be found [here](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse/res/qac/cfg/config/vcf) <br>


## <a name="contribute">How to contribute</a>

If you want to use this setup or contribute, please first contact the [Maintainers](#maintainers).

For contributing help files please do:
- Branch from current release branch.<br>
- **ACF**: Check in acf files to folder [config/acf](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse/res/qac/cfg/config/acf)<br>
- **RCF**: Check in rcf files to folder [config/rcf](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse/res/qac/cfg/config/rcf).<br>
- **User Messages**: Check in user messages files to folder [user_library/user_messages](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse/res/qac/cfg/user_library/user_messages).<br>
- Raise a pull request to maintainers.<br>

## <a name="feedback">Feedback</a>

Get in contact with the [Maintainers](#maintainers), e.g. via email or via the [coding rules T&R project](https://rb-tracker.bosch.com/tracker/projects/CDF/summary).

