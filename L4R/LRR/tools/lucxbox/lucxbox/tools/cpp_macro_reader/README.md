
# cpp_macro_reader - script to parse sysconfig header file and print addresses
-----------------------

NOTE: Only tested for "+" and "-" operator.
Please see unittest for expected behavior and covered functionality.

## Usage 

```
usage: cpp_macro_reader.py [-h] -f FILE -c COMPILER [-l] [-o OUTPUT] [-d] [-q]
                           [--version]

This tool searches for macros and calculates the value with the given
compiler. It will return a list of key value pairs. Currently only macros
containing calculations like '+' and '-' are considered.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to sysconfig file
  -c COMPILER, --compiler COMPILER
                        Path to compiler
  -l, --list            List addresses
  -o OUTPUT, --output OUTPUT
                        Write addresses to csv file
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit

```
