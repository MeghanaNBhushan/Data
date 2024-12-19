# SCA Tools Package

- [SCA Tools Package](#sca-tools-package)
	- [<a name="about">About</a>](#about)
	- [<a name="maintainers">Maintainers</a>](#maintainers)
	- [<a name="license">License</a>](#license)
	- [<a name="use">Common Use Cases</a>](#use)
	- [<a name="build">How to build and test it</a>](#how-to-build-and-test-it)
	- [<a name="contribute">How to contribute</a>](#how-to-contribute)
	- [<a name="licenses">Used 3rd party Licenses</a>](#used-3rd-party-licenses)
	- [<a name="feedback">Feedback</a>](#feedback)

## <a name="about">About</a>

This project holds the packaging for the [sca_tools](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools/browse).

This project is part of the [TOOLS Highway Initiative](https://inside-docupedia.bosch.com/confluence/display/CCD/Static+Code+Analysis#StaticCodeAnalysis-roadmap).

It adds the following additional contents on top of sca_tools:

1. [sca_tools resource files](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse/sca_tools/res) obtained from the [prqa qaf](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/prqa_qaf/browse) repository, based on the [Coding Rule Database and Framework](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/cdf/browse).
3. [TCC scripts](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse/scripts/tcc) for dependency installation with the homonymous tool.

For general sca_tools usage please check the [SCA Tools documentation](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools/browse/doc).

Check the following link for the [CHANGELOG](changelog.md).

## <a name="maintainers">Maintainers</a>

  * [Software Quality Team](mailto:CC-ADPJ-DoitSoftwareQualityTeam@bcn.bosch.com)
  * [Pro XC DOIT Software Quality Team](mailto:CC-ADPJ-DoitSoftwareQualityTeam@bcn.bosch.com)
  * [PJ-DOIT Software Quality Competency Cluster](https://inside-docupedia.bosch.com/confluence/display/CCD/PJ-DOIT+Software+Quality+Competency+Cluster)


## <a name="license">License</a>

> Copyright (c) 2022 Robert Bosch GmbH. All rights reserved.

## <a name="use">Common Use Cases</a>

SCA Tools Package is commonly used as a deployment bundle, that holds the relevant SCA Tools release with all necessary resources
(CCT files, RCF files,  etc.) needed for project configuration/analysis. It also comes with the SWQ software installation scripts.

Check the [SCA mini demo](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_mini_demo/browse) for a real-life like application setup. The corresponding sca_tools_package configuration is on the [config/mini_demo](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/sca_tools_package/browse?at=refs%2Fheads%2Fconfig%2Fmini_demo) branch.

## <a name="build">How to build and test it</a>

No build steps are necessary.
To test this project consider looking at the [qac qualification](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/helix_qualification/browse).
For integration tests see [here](sca_tools/test/integration/readme.md)

## <a name="contribute">How to contribute</a>

Get in contact with [the maintainers](#maintainers).

## <a name="licenses">Used 3rd party Licenses</a>

| License                         |
| ------------------------------- |
| [MIT](https://mit-license.org/) |

## <a name="feedback">Feedback</a>

Get in contact with the [Maintainers](#maintainers), e.g. via email or via the [coding rules T&R project](https://rb-tracker.bosch.com/tracker/projects/CDF/summary).
