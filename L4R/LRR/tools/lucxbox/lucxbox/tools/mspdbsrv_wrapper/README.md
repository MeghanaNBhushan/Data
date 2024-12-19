# mspdbsrv_wrapper

-----------------------

usage: mspdbsrv_wrapper.py [options] -- [build command]

Wrapper for MSBuild based jenkins jobs. Details why this is needed can be found here:
http://blog.peter-b.co.uk/2017/02/stop-mspdbsrv-from-breaking-ci-build.html

optional arguments:

-h, --help            show this help message and exit

-v {10,14}, --msv_version {10,14}
                        MSVC version

-d, --debug           Print debug information

-q, --quiet           Print only errors

--version             show program's version number and exit