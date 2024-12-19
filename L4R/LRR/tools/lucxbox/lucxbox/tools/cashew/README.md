# cashew

-----------------------

```
usage: cashew.py [options] -- [build command]

### Description: ###
This script is intended to wrap build commands to change the CLACHE_PATH and CCACHE_DIR variable.
This is needed if the build produces different variants or runs in different jenkins
workspaces since compiler cache tools have bad hit rates when using the same cache for different builds.
Therefore we are calculating a hash from the build command string and the workspace
to produce a unique cache identifier for certain build variation.

optional arguments:
  -h, --help            show this help message and exit
  --path PATH, -p PATH  If this parameter is set the tool will use this path as root dir instead of CLACHE_PATH and CCACHE_DIR. Optional parameter.
  --clcache CLCACHE     Path to clcache exe.
  --ccache CCACHE       Path to ccache exe.
  --ccachelog           Enable log generation for ccache.
  --ccachedepend        Enable depend mode for ccache (necessary for GHS compiler).
  --clcache-object-timeout OBJECT_TIMEOUT, -cot OBJECT_TIMEOUT
                        Sets the environment variable 'CLCACHE_OBJECT_CACHE_TIMEOUT_MS' to the given value. Increases stability. Default value is 10000 (ms).
  --size SIZE, -M SIZE  Change default size (in GB).
  --stats, -s           Clear the statistics at the beginning of a run and print them at the end.
  --compress, -c        Use ccache compression
  --root ROOT, -r ROOT  Root of the repository.
  --skip-object-path-length-check
                        Skip the check for max path length of object files (max. 255 character). The background is that ccache is a mingw based tool. Internally ccache escapes '\' which reduces the possible file path. If you disable this check you will run into 'FileNotFoundError'.
  --basedir BASEDIR     clcache: Has effect only when direct mode is on. Set this to path to root  directory of your project. (ccache: no effect)
  --hardlink            clcache: If this variable is set, cached object files won't be copied to their final location. Instead, hard links pointing to the cached object files will be created. (ccache: no effect)
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit
```


##### Details for '--skip-object-path-length-check'
If you just disable the check you will run into 'FileNotFoundError'.
Background is that ccache is not written for Windows and compiled with mingw, so it escapes internally '\'.
This means ccache cannot handle full 255 char long paths.
To warn the user of ccache we added the check.
This means you need to reduce you build folder path length.
