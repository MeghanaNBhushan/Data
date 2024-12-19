# LUCxBox - A collection of common used tools and scripts in CC

[![Build Status](http://abtv55100.de.bosch.com:8081/jenkins/DACx/buildStatus/icon?job=LUCX/lucxbox/develop)](http://abtv55100.de.bosch.com:8081/jenkins/DACx/job/LUCX/job/lucxbox/job/develop)

-----------------------

1. [About](#about)
2. [Installation](#install)
3. [How to use it](#use)
4. [Development](#develop)
5. [Maintainers](#maintainers)
6. [Contributors](#contributors)
7. [License](#license)

-----------------------

This README tries to give a brief introduction and motivation of the LUCx tools repository. Further information can be found in following documents:

* [Getting Started with LUCxBox](docs/GettingStartedWithLUCxBox.md) - covers how to integrate LUCxBox in your project.
* [How to contribute](docs/HowToContribute.md) - introduction to the development process to contribute.
* [LUCxBox CodeStyle](docs/CodeStyle.md) - CodeStyle you should adhere to while contributing.

-----------------------

## <a name="about">About</a>

The motivation for LUCxBox was to benefit from reusing scripts and tools across different project.

The main goals for this framework can be summarized with the following points:

* Reuse of code
* Share tools across projects by making them reusable
* Offer an environment to easily test scripts
* Compatible with Unix and Windows environments
* Running stable scripts for Python 3.5 and higher

-----------------------

## <a name="install">Installation</a>

### <a name="install-pip">Virtual environment (recommended)</a>

The recommended way to use the LUCxBox library and its tools is to install it into a Python virtual environment for proper dependency isolation. On Windows with a standard Python 3.5 installation this works as follows:
```bash
# Create a virtual environment with the name 'venv'.
python -m venv venv

# Activate the virtual environment.
# Amongst other things, pip will install tools to .\venv\Lib\site-packages.
.\venv\Scripts\activate

# Install LUCxBox 2.0.0 along with its dependencies.
# Adjust the given git tag for other released versions.
pip install "git+ssh://git@sourcecode.socialcoding.bosch.com:7999/LUCX/lucxbox.git@2.0.0#egg=lucxbox"
```

This will install the LUCxBox library and provide its tools as executables in the `venv\Scripts` directory.

Comments
- This installation process is possible since LUCxBox version `1.16.0` which at the same time is the last version which supports Python 2.7.
- In LUCxBox version `2.0.0` direct support of Python 2.7 was dropped, since it will not be officially maintained from January 1, 2020. Python 3.5 or higher is required.
- On Debian derivatives like OSD, either the `python3-venv` or `python3-virtualenv` package needs to be installed to create virtual environments.
- On these systems, you need to run `source ./venv/bin/activate` instead to activate the virtual environment.
- For more details, see [venv](https://docs.python.org/3/library/venv.html) (standard library module) or [virtualenv](https://virtualenv.pypa.io/en/latest/) (external library).

### <a name="artifactory">Artifactory configuration</a>

To properly download dependencies without configuring a proxy, set the `PIP_INDEX_URL` environment variable to use the Artifactory PyPI remote
```
https://<username>:<password>@rb-artifactory.bosch.com/artifactory/api/pypi/python-remote/simple
```
or appropriately use pip's `--index-url` command line parameter. Alternatively, the configuration can be stored in a
configuration file, see [Artifactory documentation](https://www.jfrog.com/confluence/display/RTF/PyPI+Repositories)
or [PIP user guide](https://pip.pypa.io/en/stable/user_guide/#config-file). 

The password to use is either the standard NT user's password or its encrypted version which may be copied from one's user profile page after logging into Artifactory.

### <a name="install-tcc-tool">TCC tool</a>

A [TCC](https://inside-docupedia.bosch.com/confluence/x/GY_wHQ) tool was created which provides the LUCxBox tools as standalone executables. To use these in your project, the tool
- must be added to your TCC tool collection ([details](https://inside-docupedia.bosch.com/confluence/x/WA-EI)) -- tool name: `lucxbox`, version: `2.0.0_WIN64`
- installed on the local machine

```powershell
C:\TCC\Base\InstallToolCollection\InstallToolCollection.ps1 -XMLFile <ToolCollectionXMLFile> -InstallTools lucxbox -GenerateToolPathBat "$(Get-Location)\tools.bat"
```

This installs the configured version of LUCxBox and creates a `tools.bat` file which defines an environment variable `TCCPATH_lucxbox`. This variable points to the version-specific installation directory of the TCC tool and will usually be `C:\TCC\Tools\lucxbox\2.0.0_WIN64`.

### <a name="install-tcc-python">TCC Python with LUCxBox</a>

A Python 3.7.4 installation with a pre-installed LUCxBox library including all dependencies exists in [TCC](https://inside-docupedia.bosch.com/confluence/x/GY_wHQ). To use it in your project, the tool
- must be added to your TCC tool collection ([details](https://inside-docupedia.bosch.com/confluence/x/WA-EI)) -- tool name: `python3`, version: `3.7.4_WIN64`
- installed on the local machine

```powershell
C:\TCC\Base\InstallToolCollection\InstallToolCollection.ps1 -XMLFile <ToolCollectionXMLFile> -InstallTools python3 -GenerateToolPathBat "$(Get-Location)\tools.bat"
```

### <a name="install-git-checkout">Git checkout</a>

It is also possible to checkout the LUCxBox repository or add this repository as a submodule and access the scripts directly.

```powershell
cd <some-directory>

# System Dependencies, necessary on a fresh OSD5 installation 
# to get wheel builds working. If you happen to see the following 
# error message then you are holding missing dependencies for
# wheel building:
#
# error: invalid command 'bdist_wheel'

sudo apt-get install gcc libpq-dev fonts-noto -y
sudo apt-get install python-dev  python-pip -y
sudo apt-get install python3-tk python3-dev python3-pip python3-venv python3-wheel

# Checkout
git checkout ssh://git@sourcecode.socialcoding.bosch.com:7999/lucx/lucxbox.git

cd lucxbox

# Create a virtual environment with the name 'venv'.
python -m venv venv

# Activate the virtual environment.
.\venv\Scripts\activate

# Install tested specific versions of dependencies 
# (especially on OSD5 you may want to upgrade pip and wheel prior to proceeding)
pip install --upgrade pip wheel
pip install -r .\requirements.txt
```

For installing the respective dependencies, you may need to configure pip to use Artifactory ([instructions](#artifactory)).

-----------------------

## <a name="use">How to use it</a>

Most of the following steps are written for Windows users. On Linux, everything is very similar if `venv/Scripts` is replaced by `venv/bin`. TCC is however not yet available on Linux.

### <a name="use-venv">Virtual environment (recommended)</a>

After installing LUCxBox into a virtual environment ([instructions](#install-pip)), the LUCxBox tools are available as executables in `venv\Scripts` and you may run them after activating the virtual environment:
```powershell
# Activate the virtual environment.
# Amongst other things, this puts venv\Scripts on PATH.
.\venv\Scripts\activate

# Tools are now available.
qacw.exe --help
```

You may also run the executables directly without activating the virtual environment. The virtual environment's Python executable is hard-wired during the `pip install` step.
```powershell
.\venv\Scripts\qacw.exe --help
```

### <a name="use-tcc-tool">TCC tool</a>

To use the standalone LUCxBox tools provided via the TCC tool ([installation instructions](#install-tcc-tool)), execute the environment setting script and access the LUCxBox tool as follows

```cmd
.\tools.bat
%TCCPATH_lucxbox%\qacw.exe --help
```

Of course, the specific path can also be used directly, but using the environment variable approach makes the script version independent and therefore easier to maintain.

In general, this approach is recommended in the following cases:
- if you would like to use a simple approach and not deal with Python virtual environments
- if your project still uses Python 2.7 and you fear version conflicts. Please consider upgrading to a Python 3 version. Python 2.7 will not be maintained past 2020 ([details](https://pythonclock.org/)).

### <a name="install-git-checkout">Git checkout</a>

To use LUCxBox tools from a checked out repository, it is important to tell the Python interpreter where to find the library and tools. This must be done by adding the checkout path used earlier ([instructions](#install-git-checkout)) to the `PYTHONPATH` environment variable. Then, the tool's script may be executed as follows:

```powershell
# Add checkout path to PYTHONPATH
$env:PYTHONPATH = "<some-directory>\lucxbox"

# Execute script (requires explicit path)
python <some-directory>\lucxbox\tools\qacw\qacw.py --help

# Alternative: execute as module which will be found using PYTHONPATH
python -m lucxbox.tools.qacw.qacw --help
```

This is the quick-fix for the following error message, when the LUCxBox library cannot be found:
```
Traceback (most recent call last):
  File "lucxbox/tools/qacw/qacw.py", line 9, in <module>
    from lucxbox.lib import lucxargs, lucxlog
ImportError: No module named lucxbox.lib
```

The transition to the virtual environment based approach should however be considered ([instructions](#use-venv)).

## <a name="develop">Development</a>

### <a name="develop-install">Installation</a>

Follow the installation instructions outlined above in the [git checkout](#install-git-checkout) section.

### <a name="develop-test">Development</a>

The `lucxbox_steps.py` is the main entry point script for several development steps. To show all available options, run
```
python lucxbox_steps.py --help
```

The most important of these are the ones for testing, which use [unittest](https://docs.python.org/3.5/library/unittest.html) and [pytest](https://pytest.org/en/latest/), and linting [pylint](https://pylint.readthedocs.io/en/latest/).

```powershell
# Run unittest/pytest
python lucxbox_steps.py --test

# Alternative: use pytest directly
py.test

# Run pylint
python lucxbox_steps.py --lint

# Run unittest/pytest and pylint
python lucxbox_steps.py --all
```

-----------------------

## <a name="release">Release Process</a>

Every new feature needs to pass a review by one of the maintainers. There's a weekly meeting for "merge" sessions to bring all features to the develop branch. After this sessions the CHANGELOG will be updated and a new release tag is created.

The release tag naming follows the [Semantic Versioning](https://semver.org/). Given a version number MAJOR.MINOR.PATCH, we increment the:

- MAJOR version when there are incompatible API changes (e.g. parameter changes to any script),
- MINOR version when functionality was added in a backwards-compatible manner, and
- PATCH version when backwards-compatible bug fixes have been made.

-----------------------

## <a name="maintainers">Maintainers</a>

Main maintainers right now are:

* Engeroff Michael (ITKG/ENG32.5)
* Schleemilch Sebastian (CC-DA/ESI4)

-----------------------

## <a name="contributors">Contributors</a>

No contributors yet. Do you want to contribute? Just create a branch, get things done and create a pull-request back to the `develop` branch.
We are happy about every contributor who is interested in providing new features and we will review your proposals as soon as we can!

-----------------------

## <a name="license">License</a>

>       Copyright (c) 2018 Robert Bosch GmbH and its subsidiaries.
>       This program and the accompanying materials are made available under
>       the terms of the Bosch Internal Open Source License v4
>       which accompanies this distribution, and is available at
>       http://bios.intranet.bosch.com/bioslv4.txt
