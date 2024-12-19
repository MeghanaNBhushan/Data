# qacw

-----------------------

## General Information

These scritps require several prerequisites in order to work properly:
- The PRQA Framework is installed on the respective build machine.
- The environment variable "PRQA_HOME" is set to the installation root directory of the PRQA Framework. E.g. `D:\PRQA\PRQA-Framework-2.3.0`
- The executing user has the necessary licenses allocated, `QA Verify` and `QAC++`.
  If not, approach the [User Request Service](http://rb-urs.de.bosch.com/URSXFrontEnd/Sites/Home.cshtml). 
- The `map-team-warnings` function requires a 'components' file. Please refer to the example file in the test folder `test_components`
- Configuration files can be found in the [prqa_qaf repository](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/prqa_qaf/browse).

## Basic Usage

```
usage: qacw.py [-h] [-d] [-q] [--version] [-p PATH_PRQA] 
               {xml2excel,filereport,project} ...

A QAC+ wrapper script collection

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit
  -p PATH_PRQA, --qac-path PATH_PRQA
                        The path to the PRQA installation.

QAC Sub-Commands:
  {xml2excel,filereport,project}
    xml2excel           Converts a QAC+ XML Export to an Excel file
    filereport          Generates report listing files and their analysis
                        status
    project             Setup QAC Project
```

A QAC+ wrapper script collection

### optional arguments

```
-h, --help           show this help message and exit
-d, --debug          Print debug information
-q, --quiet          Print only errors
```

### positional arguments

```
xml2excel          Converts a QAC+ XML Export to an Excel file
filereport         Generates report listing files and their analysis
                   status
project            Setup QAC Project
```

## Subparsers

Available subparsers are `xml2excel`, `filereport` and `project`

### xml2excel

```
usage: qacw.py xml2excel [-h] -i INPUT -o OUTPUT
                         [-sl {1,2,3,4,5,6,7,8,9} [{1,2,3,4,5,6,7,8,9} ...]]
                         [-gc] [-l {list,matrix}]
```

#### optional arguments

```
-h, --help            show this help message and exit
-i INPUT, --input INPUT
                      XML file which contains a QACP analysis output
-o OUTPUT, --output OUTPUT
                      Path to the desired XLSX output file
-sl {1,2,3,4,5,6,7,8,9} [{1,2,3,4,5,6,7,8,9} ...], --severity-levels {1,2,3,4,
     5,6,7,8,9} [{1,2,3,4,5,6,7,8,9} ...]
                      Specify a subset of interested severity levels as a
                      space separated integer list
-gc, --guess-component
                      Whether to guess the component name of extracted files
                      or not. Default is False.
-l {list,matrix}, --layout {list,matrix}
                      Defines which excel sheet layout to use. Default is a
                      list of files/components where each line equals one
                      finding
```

### filereport

```
usage: qacw.py filereport [-h] -n PROJECT_NAME -o OUTPUT
```

#### optional arguments

```
-h, --help            show this help message and exit
-n PROJECT_NAME, --name PROJECT_NAME
                      Project name
-o OUTPUT, --output OUTPUT
                      Path where the report shall be stored in CSV format
```

### project

```
usage: qacw.py project [-h] -n PROJECT_NAME {create,report,upload-qav,upload-s101,map-team-warnings} ...
```

#### optional arguments

```
-h, --help                               show this help message and exit
-n PROJECT_NAME, --name PROJECT_NAME     Project name
```

#### QAC Project Sub-Commands

```
setup               Setup the QAC project. This command performs the
                    following tasks: - check the required licenses -
                    create the QAF project and set the source code root -
                    set file filters
analyze             Analyze the QAC project. This command performs the
                    following tasks: - check the required licenses - build
                    the software with build monitoring activated - do the
                    actual analysis
report              Generate QAC Report
upload-qav          Upload QAC Analysis to QAVerify
upload-s101         Upload QAC Analysis to S101
```

##### setup

```
usage: qacw.py project setup [-h] --acf ACF --cct CCT --rcf RCF [--vcf VCF]
                             [--user-messages USER_MESSAGES]
                             [-f [FILE_FILTERS [FILE_FILTERS ...]]]
```

###### optional parameters

```
-h, --help            show this help message and exit
--acf ACF             The path to the Analysis Configuration File (ACF).
--cct CCT             The path to the Compiler Compatibility Template (CCT).
                      The '--cct' argument may be specified more than once
                      in order to add support to a project for more than one
                      compiler.
--rcf RCF             The path to the Rule Configuration File (RCF).
--vcf VCF             The path to the Version Control Compatibility File (VCF)
--user-messages USER_MESSAGES
                      User messages configuration file
-f [FILE_FILTERS [FILE_FILTERS ...]], --file-filters [FILE_FILTERS [FILE_FILTERS ...]]
                      List of file filters to be applied to the analysis.
```

##### analyze

```
usage: qacw.py project analyze [-h] -b BUILD_COMMAND
```

###### optional arguments

```
-h, --help            show this help message and exit
-b BUILD_COMMAND, --build-cmd BUILD_COMMAND
                      Build Command
-c, --clean           Cleans all analysis data from the specified qaf-
                      project before performing analysis. In the case where
                      the 'cma-project' option is specified, all PRQA
                      Framework projects involved in the analysis will be
                      cleaned.
-m OUTPUT_FILE, --messages-output OUTPUT_FILE
                      Exports messages report in the format suitable for
                      SonarQube QAF plugin into specified file or folder
                      depending on the format.
-M OUTPUT_FORMAT, --messages-output-format OUTPUT_FORMAT
                      Sets the format of `--messages-output`. Possible values
                      are xml and txt (default).
-I, --inter-tu-dataflow
                      Perform Inter TU Dataflow analysis. This option is
                      only valid for QAC/QAC++. When enabled, the first pass
                      will be run with df::inter=0 and the second pass will
                      be run with the value of df::inter (previously set by
                      the user).
```

##### report

```
usage: qacw.py project report [-h]
                              [-r {CRR,HMR,MDR,RCR,SSR,SUR} [{CRR,HMR,MDR,RCR,SSR,SUR} ...]]
                              [-a ARCHIVE_TARGET_DIR]
```

###### optional arguments

```
-h, --help            show this help message and exit
-r {CRR,HMR,MDR,RCR,SSR,SUR} [{CRR,HMR,MDR,RCR,SSR,SUR} ...], --report-types 
   {CRR,HMR,MDR,RCR,SSR,SUR} [{CRR,HMR,MDR,RCR,SSR,SUR} ...]
                      A space separated integer list with the report types:
                          CRR - Code Review Report 
                          HMR - HIS Metrics Report 
                          MDR - Metrics Data Report 
                          RCR - Rule Compliance Report 
                          SSR - Severity Summary Report 
                          SUR - Suppressions Report
-a ARCHIVE_TARGET_DIR, --archive-target-dir ARCHIVE_TARGET_DIR
                      The path where the report shall be archived.
```

##### upload-qav

```
usage: qacw.py project upload-qav [-h] --stream STREAM --snapshot SNAPSHOT [--upload-source {ALL,NOT_IN_VCS,NONE}] --url URL -u USERNAME -p PASSWORD
```

###### optional arguments

```
-h, --help            show this help message and exit
--stream STREAM       The name of the QAVerify project
--snapshot SNAPSHOT   The name of the snapshot (e.g. the git commit hash)
--upload-source {ALL,NOT_IN_VCS,NONE}
                      Whether to upload the source code to QAVerify. Options
                      are 'ALL', 'NOT_IN_VCS', and 'NONE'. The default value is 'ALL'
--url URL             The url of the QAVerify server.
-u USERNAME, --username USERNAME    
                      The user to perform the upload.
-p PASSWORD, --password PASSWORD
                      The password to perform the upload
```

##### upload-s101

```
usage: qacw.py project upload-s101 [-h]
```

###### optional arguments

```
-h, --help  show this help message and exit
```

#### map-team-warnings

```
usage: qacw.py project map-team-warnings [-h] -c COMPONENTS_FILE -t TEAM_WARNINGS_FILE [-e EXCEPTION_WILDCARDS [EXCEPTION_WILDCARDS ...]] [-r REPORT_FILE]
```

###### optional arguments:

```
-h, --help            show this help message and exit
-c COMPONENTS_FILE, --components-file COMPONENTS_FILE
                      The path to the components file containing the mapping
                      components <-> team
-t TEAM_WARNINGS_FILE, --team-warnings-file TEAM_WARNINGS_FILE
                      Path and filename of the output report file. Output
                      format is based on the file extension provided in this
                      argument. For very large reports use csv as output
                      format as Excel has a maximum of 1.048.576 lines.
                      Possible file formats are 'xlsx' and 'csv'.
-s MIN_SEVERITY, --min-severity MIN_SEVERITY
                      Filter messages whose severity is less than the
                      supplied severity. Valid values are in the range 1-9.
                      0 and 1 are acceptable, but will display everything.
                      Values greater than 9 will filter everything.
-e EXCEPTION_WILDCARDS [EXCEPTION_WILDCARDS ...], --exception-wildcards EXCEPTION_WILDCARDS [EXCEPTION_WILDCARDS ...]
                      List of wildcard expressions in order to exclude files
                      from the analysis
-r REPORT_FILE, --report-file REPORT_FILE
                      The path to the intermediate report file containing
                      the warnings
```
