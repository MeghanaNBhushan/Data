# team_mapping

-----------------------
## Use-case
- You can fit the COMPONENTS and team information into any report contains the file path or specified mapping column.
- Example test_report.csv file could be found in the `./test/` folder.

## General requirements:
 - Please follow the steps described in the installation section of main library [documentation](../../../README.md).
 - It requires a 'components' file implemented according with GitHub CODEOWNERS [style](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/about-code-owners).
 - Example 'components' file could be found in the `/lib/test/` folder.
 - Rule for enabled gitignore specification in teams mapping next rule is used: **within one level of precedence, the last matching pattern decides the outcome**

## Usage
teams_mapping.py [-h] [-d] [-q] [--version] -r REPORT -c COMPONENTS -t
                        TEAMS_REPORT [-m MAPPING_COLUMN] [-l {,,;,:,|}] [-g]

```
usage: teams_mapping.py [-h] [-d] [-q] [--version] -r REPORT -c COMPONENTS -t
                        TEAMS_REPORT [-m MAPPING_COLUMN] [-l {,,;,:,|}] [-g]

Map input csv warnings report with COMPONENTS file.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit
  -r REPORT, --report REPORT
                        The path to the input report file with warnings in csv
                        format. Any report we want to fit Team and Component
                        information and map it by mapping-column
  -c COMPONENTS, --components COMPONENTS
                        The path to the COMPONENTS file
  -t TEAMS_REPORT, --teams-report TEAMS_REPORT
                        The output csv report filepath and filename. Output
                        format is based on the input file dialect provided.
  -m MAPPING_COLUMN, --mapping-column MAPPING_COLUMN
                        Column name for mapping. Usually this is "File",
                        "FilePath", etc.
  -l {,,;,:,|}, --delimiter {,,;,:,|}
                        A one-character string used to separate fields.
  -g, --gitignore-mapping
                        Switch to enable of team mapping that implements gitignore specification - within one level of
                        precedence, the last matching pattern decides the outcome
```
