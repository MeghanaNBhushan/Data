# dauerlaufw

-----------------------

```
usage: dauerlaufw.py [options] -- [build command]

Wrapper script for testing the robustness of another tool. Just pass a build command and run it over night and you get a statistic of the robustness of the tool. Output will be saved if an error occures.

optional arguments:
  -h, --help   show this help message and exit
  -n MAX_RUNS  Max numbers of runs.
  -d, --debug  Print debug information
  -q, --quiet  Print only errors
  --version    show program's version number and exit
```