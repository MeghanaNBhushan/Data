# Repository Miner Reader

Writes out a txt file that contains suggestions about files that can be co-modified based on association analysis of the previous merge commit history association rules derived by Repository Miner.

## Argparse help
usage: repository_miner_reader.py [-h] --branch BRANCH
                                  --association-rules-file
                                  ASSOCIATION_RULES_FILE --output-path
                                  OUTPUT_PATH [--stats-path STATS_PATH] [-d]
                                  [-q] [--version]

## Description
RepositoryMiner is a tool that automates the software repository mining process and analyzes merge commit history for a given branch (
see https://sourcecode01.de.bosch.com/projects/NRCSGEN2/repos/repository_miner/). For this purpose, a Jenkins pipeline is configured to perform the mining on
a weekly basis for selected repositories (see https://rb-jmaas.de.bosch.com/NRCS2/job/maintenance/job/Monitoring/job/repository_miner/). One of the mining results
is a txt file containing association rules describing dependencies between files in a software repository for a given branch. The Repository Miner Reader is a tool
that compares modifications in the branch you are currently on with the association rules derived for the target branch to which your branch should be merged. The
result of this comparison is a txt file containing a comment that shall be posted to Bitbucket. This is meant as a recommender system that shall support pull request
owners in the development of error-free code.

## Usage
In order to benefit from the recommender system, consider the following steps:

1. Configure the Jenkins pipeline so that your repository is mined on a weekly basis. Association rules are saved by default to
\\bosch.com\dfsrb\DfsDE\DIV\CS\DE_CS$\Tech\IT-Engineering\repository_miner\{REPOSITORY}\{BRANCH}_association_rules_lucx.json where {REPOSITORY} is the name of the
repository and {BRANCH} is the name of the target branch.

2. Define a new stage as part of your PR build pipeline.

3. In the new stage, call ```python /path/to/this/repo/repository_miner_reader.py -b BRANCH -f ASSOCIATIONS_RULES_FILE -o OUTPUT_PATH -s STATS_PATH```. This call will print the absolute
path of the txt file that was written out. This file contains the recommendations as a text.

4. Post the content of the written out file for example as a comment in repository hosting services (like Bitbucket) in order to make pull request owners aware of files
that they might also need to modify in their pull reuqest.

Required arguments:
  --branch BRANCH, -b BRANCH                                                      association rules derived for the given branch will be compared with modifications in the branch you are currently on
  --association-rules-file ASSOCIATIONS_RULES_FILE, -f ASSOCIATIONS_RULES_FILE    path of the txt file containing association rules
  --output-path OUTPUT_PATH,-o OUTPUT_PATH                                        path where the comment file shall be stored
  --stats-path STATS_PATH, -s STATS_PATH                                          statistics will be written out here   -b BRANCH, --branch BRANCH                                          association rules for the given branch will be compared with modifications done in the branch you are currently on
  ---association-rules-file ASSOCIATION_RULES_FILE, -f ASSOCIATION_RULES_FILE     absolute path of the txt file containing association rules
  --output-path OUTPUT_PATH, -o OUTPUT_PATH                                       path where the output txt file shall be stored
  -s STATS_PATH, --stats-path STATS_PATH                                          folder path where statistics shall be stored and tracked by management (use \\bosch.com\dfsrb\DfsDE\DIV\CS\DE_CS$\Tech\IT-Engineering\repository_miner\{REPOSITORY})


optional arguments:
  -h, --help            show this help message and exit' not in README.md
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit

## Authors
Angel Iliev (XC-DA/EPS1) <fixed-term.angelivanov.iliev@bosch.com>
Jens Kramer (XC-DA/EPS1) <Jens.Kramer@de.bosch.com>