# retryw - because we fail

-----------------------

```
usage: retryw.py [options] -- [build command]

Wrapper to retry a command if it fails due to a known instability.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit
  -n NUM_RETRIES, --num-retries NUM_RETRIES
  -s STRINGS, --string STRINGS
                        If this string is found in the output a retry will be triggered. Can be given multiple times.
```