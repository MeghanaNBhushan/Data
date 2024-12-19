# Update bitbucket summary table

-----------------------
### 1. Description
Script searches and updates the summary table in the Bitbucket comment. If the comment that contains the table is not found, creates a new comment.
The table is always grouped by build variant.

* Each script call updates single entry in the table.
* Implementation of the markdown in Bitbucket cannot contain multiline strings in the tables. This script simulates new lines with additional rows.

Some details on the comment update algorithm can be found on the flow diagram [here](https://inside-docupedia.bosch.com/confluence/x/8ai2X#Toolingforcreatingbaselineforcompiler/linkerwarnings-flow_diagram).


### 2. Usage
Values for the table can be provided with command-line parameters (inline usage) or JSON file (file usage). Schema for the summary JSON file is described in compiler_delta_check/schemas/summary_table.json.
```
usage: update_bitbucket_summary.py [-h] [-d] [-q] [--version] {inline,file} ...

optional arguments:
  -h, --help     show this help message and exit
  -d, --debug    Print debug information
  -q, --quiet    Print only errors
  --version      show program's version number and exit

Source:
  {inline,file}
    inline       Update Bitbucket summary report with inline parameters
    file         Update Bitbucket summary report using summary JSON file
```

#### inline mode usage
```
usage: update_bitbucket_summary.py inline [-h] --prid PRID --build-number BUILD_NUMBER
       --build-variant BUILD_VARIANT --tool TOOL --result RESULT [--details DETAILS [DETAILS ...]]
       [-c COMPONENTS [COMPONENTS ...]] [--comment COMMENT] -u USER -p PASSWORD
       [-bu BITBUCKET_URL] -br BITBUCKET_REPO -bp BITBUCKET_PROJECT [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --prid PRID           Pull request ID
  --build-number BUILD_NUMBER
                        Build number
  --build-variant BUILD_VARIANT
                        Build variant
  --tool TOOL           Reporting tool name
  --result RESULT       Result of tool execution
  --details DETAILS [DETAILS ...]
                        Detail field of summary table. Usually link to full report
  -c COMPONENTS [COMPONENTS ...], --components COMPONENTS [COMPONENTS ...]
                        List of components
  --comment COMMENT     Additional commets to display
  -u USER, --user USER  System user username
  -p PASSWORD, --password PASSWORD
                        System user password
  -bu BITBUCKET_URL, --bitbucket-url BITBUCKET_URL
                        Bitbucket URL
  -br BITBUCKET_REPO, --bitbucket-repo BITBUCKET_REPO
                        Bitbucket repo name
  -bp BITBUCKET_PROJECT, --bitbucket-project BITBUCKET_PROJECT
                        Bitbucket project name
  --debug               Enable debugging mode
```

#### file mode usage
```
usage: update_bitbucket_summary.py file [-h] --summary-json SUMMARY_JSON -u USER
       -p PASSWORD [-bu BITBUCKET_URL] -br BITBUCKET_REPO -bp BITBUCKET_PROJECT [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --summary-json SUMMARY_JSON
                        JSON file name of summary
  -u USER, --user USER  System user username
  -p PASSWORD, --password PASSWORD
                        System user password
  -bu BITBUCKET_URL, --bitbucket-url BITBUCKET_URL
                        Bitbucket URL
  -br BITBUCKET_REPO, --bitbucket-repo BITBUCKET_REPO
                        Bitbucket repo name
  -bp BITBUCKET_PROJECT, --bitbucket-project BITBUCKET_PROJECT
                        Bitbucket project name
  --debug               Enable debugging mode
```

### 3. Requirements for script execution
Python version: Python >=3.6
