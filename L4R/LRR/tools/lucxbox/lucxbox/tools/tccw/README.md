# tccw - wrapper script for a 'docker-like' tcc usage

-----------------------

## Usage 

```
usage: tccw.py [options] -- [build command]

TCC wrapper script for a 'docker-like' tcc usage.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit
  -f CONFIG_FILE, --config-file CONFIG_FILE
                        TCC wrapper configuration file
  -c TCC_CONFIG, --tcc-config TCC_CONFIG
                        TCC xml configuration
  -cf TCC_CONFIG_FROM_FILE, --tcc-config-from-file TCC_CONFIG_FROM_FILE
                        Read TCC xml configuration from first line of specified file
  -l LOCAL_CONFIG, --local-config LOCAL_CONFIG
                        TCC xml configuration (local)
  -s, --no-install      Skips the availability check (and installation) of tools in the TCC configuration (overwrites the config file)
  --no-cache            Skips using tcc cache.
  --tries TRIES, -t TRIES
                        Number of retries for invoking TCC since TCC is not thread safe
  --extend-path EXTEND_PATH [EXTEND_PATH ...], -e EXTEND_PATH [EXTEND_PATH ...]
                        Extends the PATH with given paths based on TCC_ environment variables.
                        Example: Environment variable TCC_PYTHON3 -> --extend-path PYTHON3
                        Example2: Environment variable TCC_GIT -> --extend-path GIT/bin.
                        PATH will be extended on the front to assure that those entries are taken first!
  --env-export ENV_EXPORT, -x ENV_EXPORT
                        Exports all tcc variables into a seperate given file for further processing
                        This will exit the script afterwards. It will extend the given file with ".env" when not given.
                        It will also create a "sh.env" version of the file in the same directory
```

## tccw config file

The config file specified by `--config-file` can take following parameters:
* `TccXMLConfigPath`: Path to the config file of the TCC collection (e.g. `C:\TCC\Base\FVG3\Windows\TCC_FVG3_Windows_DevLatest.xml`)
* (OPTIONAL) `TccScriptPath`: Path to the TCC script (default is `C:\TCC\Base\InstallToolCollection\InstallToolCollection.ps1`)
* (OPTIONAL) `TccInvoker`: Programm to use as invoker for TCC script (default is `powershell.exe`)
* (OPTIONAL) `TccInstallXML`: Wether to always check and install/update the tool collection (default is `False`)


## Example with parameter

command:
```
$ python tools/tccw/tccw.py -c TCC_FVG3_Windows_DevLatest -- %TCC_ARMCOMPILER6%/bin/armclang.exe --version

2018-11-13 14:54:17 tcc_wrapper |INFO    | Calling TCC tools deploy for XML C:\TCC\Base\FVG3\Windows\TCC_FVG3_Windows_DevLatest.xml
2018-11-13 14:54:31 tcc_wrapper |INFO    | Calling command: ['%TCC_ARMCOMPILER6%/bin/armclang.exe', '--version']
Product: ARM Compiler 6.6.1 Long Term Maintenance
Component: ARM Compiler 6.6.1 Long Term Maintenance
Tool: armclang [5c782600]

Target: unspecified-arm-none-unspecified
```

## Example with config file

config.ini:

```
[TCC]
TccXMLConfigPath = C:\TCC\Base\FVG3\Windows\TCC_FVG3_Windows_DevLatest.xml
TccInstallXML = False
```

command:
```
$ python tools/tccw/tccw.py -f config.ini -- %TCC_ARMCOMPILER6%/bin/armclang.exe --version

2018-11-13 14:58:57 tcc_wrapper |INFO    | Calling command: ['%TCC_ARMCOMPILER6%/bin/armclang.exe', '--version']
Product: ARM Compiler 6.6.1 Long Term Maintenance
Component: ARM Compiler 6.6.1 Long Term Maintenance
Tool: armclang [5c782600]

Target: unspecified-arm-none-unspecified

```

# import tccw

tcc_wrapper can be imported to make use of tcc initialization routine in a python context.
The used function is called init_tcc().

## Usage
```
params: TccConfig cfg, Boolean no_install
- 'cfg' The TCC copnfiguration as object. (see example)
- 'no_install' provides an option to skip tcc installation routine, if you know the desired version is already installed.
```

## Example
```
from lucxbox.tools.tccw import tcc_config, tcc_wrapper

cfg = tcc_config.TccConfig()
cfg.set_by_value("TCC_FVG3_Windows_DevLatest")  # Create TccConfig from the desirec TCC version name.
exec_env = tcc_wrapper.init_tcc(cfg, False)
```

