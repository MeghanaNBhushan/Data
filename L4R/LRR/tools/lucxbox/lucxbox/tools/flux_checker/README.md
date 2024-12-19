flux_checker
============

## Basic Usage

```
usage: flux_checker.py [-h] [-d] [-q] [--version] [--fqm-version FQMVERSION]
                       [--fqm-dir FQMDIR | --fqm-exe FQMEXE]
                       {install,check} ...

Wrapper for FQM tool to check if all flux files have no errors and can be
opened in the flux GUI. Unless specified explicitly, the tool will look in all
subfolders for '.flux' files.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
  --version             show program's version number and exit
  --fqm-version FQMVERSION
                        Flux Quality Metrics version. Minimum 1.1. (e.g.
                        "1.1.0.19", required)
  --fqm-dir FQMDIR      Flux Quality Metrics directory (default: user TEMP
                        directory)
  --fqm-exe FQMEXE      Flux Quality Metrics executable

Flux checker sub-commands:
  {install,check}
    install             Install FQM from Artifactory.
    check               Check flux file(s).
```

## Subparsers

Available subparsers are `install` and `check`

### Install

```
usage: flux_checker.py install [-h] [--user USER] [--password PASSWORD]

optional arguments:
  -h, --help           show this help message and exit
  --user USER          User for accessing Artifactory (default: current user)
  --password PASSWORD  Password for accessing Artifactory (prompt if not
                       provided)
```

### Check

```
usage: flux_checker.py check [-h] [-j THREADS] [--whitelist WHITELIST]
                             [--flux-model FLUXMODEL]

optional arguments:
  -h, --help            show this help message and exit
  -j THREADS            Number of threads to use parallel (default is 1).
  --whitelist WHITELIST, -w WHITELIST
                        File containing a list of whitelisted files (one line
                        for each file).
  --flux-model FLUXMODEL
                        Flux model file (default: all .flux files in
                        subfolders)
```

### Example for a whitelist file:

```
.\cpj_jlr_fvc3\arch\cpj.flux
.\cpj_jlr_fvc3\arch_system\variants.flux
.\cpj_jlr_fvc3\arch_system\taskschemes\mempools_cpj.flux
.\cpj_jlr_fvc3\arch_system\taskschemes\mempools_dcv.flux
.\cpj_jlr_fvc3\arch_system\taskschemes\mempools_fv_cv.flux
.\cpj_jlr_fvc3\arch_system\taskschemes\mempools_fv_fct.flux
.\cpj_jlr_fvc3\arch_system\taskschemes\mempools_fv_hw.flux
.\cpj_jlr_fvc3\arch_system\taskschemes\mempools_fv_if.flux
.\cpj_jlr_fvc3\arch_system\taskschemes\mono\mempools.flux
.\cpj_jlr_fvc3\arch_system\taskschemes\stereo\mempools.flux
.\cpj_jlr_fvc3\arch_system\taskschemes\os_tasks_common.flux
```