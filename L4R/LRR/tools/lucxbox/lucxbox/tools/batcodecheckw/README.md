usage: batcodecheckw.py [-h] [--version] [-d] [-q] -o DIR
                        (-s FILE [FILE ...] | -l FILE [FILE ...])
                        [-tc TCC_SERVER_CONFIG | -tl TCC_LOCAL_CONFIG | -i INSTALL_PATH | -tv TCC_VAR]

Wrapper script for runnning BatCodeCheck

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  -o DIR, --output DIR  directory for reports
  -s FILE [FILE ...], --sources FILE [FILE ...]
                        source file(s) for analysis
  -l FILE [FILE ...], --list FILE [FILE ...]
                        text file(s) with one file path for analysis per line
  -tc TCC_SERVER_CONFIG, --tcc-server-config TCC_SERVER_CONFIG
                        Pass here name of TCC Server config -> e.g.
                        TCC_NRCS2_Windows_DevLatest
  -tl TCC_LOCAL_CONFIG, --tcc-local-config TCC_LOCAL_CONFIG
                        Pass here name of local TCC config
  -i INSTALL_PATH, --install-path INSTALL_PATH
                        Pass here the path to the BatCodeCheck executable
  -tv TCC_VAR, --tcc-var TCC_VAR
                        Pass here the TCC variable for BatCodeCheck, e.g.
                        'TCC_BATCODECHECK'