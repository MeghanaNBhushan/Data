usage: cppcheckw.py [-h] [--version] [-s FILE|DIR [FILE|DIR ...]]
                    [-l FILE [FILE ...]] -o FILE [-c FILE] [-f txt|xml|html]
                    [-tc TCC_SERVER_CONFIG | -tl TCC_LOCAL_CONFIG | -i INSTALL_PATH]
                    [-tv TCC_VAR]

Script for running Cppcheck

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -s FILE|DIR [FILE|DIR ...], --sources FILE|DIR [FILE|DIR ...]
                        source file(s) or directories for analyze
  -l FILE [FILE ...], --lists FILE [FILE ...]
                        text file(s) with one file path for analysis per line
  -o FILE, --output FILE
                        file for report
  -c FILE, --config FILE
                        file with parameters for Cppcheck
  -f txt|xml|html, --format txt|xml|html
                        report output format
  -tc TCC_SERVER_CONFIG, --tcc-server-config TCC_SERVER_CONFIG
                        Pass here name of TCC Server config -> e.g.
                        TCC_NRCS2_Windows_DevLatest
  -tl TCC_LOCAL_CONFIG, --tcc-local-config TCC_LOCAL_CONFIG
                        Pass here name of local TCC config
  -i INSTALL_PATH, --install-path INSTALL_PATH
                        Path to the directory that contains the CppCheck
                        executable
  -tv TCC_VAR, --tcc-var TCC_VAR
                        Pass here the TCC variable for CppCheck, e.g.
                        'TCC_CPPCHECK'