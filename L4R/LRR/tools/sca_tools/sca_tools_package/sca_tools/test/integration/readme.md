# SCA Tools Package

- [SCA Tools Package](#sca-tools-package)
  - [<a name="about">About</a>](#about)
  - [<a name="maintainers">Maintainers</a>](#maintainers)
  - [<a name="license">License</a>](#license)
  - [<a name="use">How to use it</a>](#how-to-use-it)
  - [<a name="build">How to build and test it</a>](#how-to-build-and-test-it)
  - [<a name="contribute">How to contribute</a>](#how-to-contribute)
  - [<a name="licenses">Used 3rd party Licenses</a>](#used-3rd-party-licenses)
  - [<a name="feedback">Feedback</a>](#feedback)

## <a name="about">About</a>

This package provides integration tests for SCA Tools Package. They are implemented as behave tests.
For installation see [here](https://pypi.org/project/behave/)
For using behave see [here](https://jenisys.github.io/behave.example/)

For QAC as well as for Coverity the following features exist:
- config: creates configurations for the given tools versions
- create: creates the project, builds the code base if necessary
- analyze: analyzes the project
- report: create reports for the given export formats

All QAC features except the create-feature are independent from the project under test.
All Coverity features except the create/report-feature are independent from the project under test.
Note: This is a chance for improvement to make the create feature independent as well.

## <a name="maintainers">Maintainers</a>

* [Pro XC DOIT Software Quality Team](mailto:CC-ADPJ-DoitSoftwareQualityTeam@bcn.bosch.com)

## <a name="license">License</a>

>	Copyright (c) 2022 Robert Bosch GmbH. All rights reserved.

## <a name="use">How to use it</a>

For running the behave tests please clone the demo project [OpenCV](https://sourcecode.socialcoding.bosch.com/projects/CDF/repos/opencv_demo/browse) latest branch.
Provide the root folder of OpenCV as your --project_root parameter, see examples below.
Start Behave tests from a command line.
Make sure you called set_env.bat before.

You can start all QAC behave tests like this:
python test/integration/run_behave_tests.py qac --project_root D:/PRQA/opencv_20202

You can start tests for all features like this:
python test/integration/run_behave_tests.py qac --project_root D:/PRQA/opencv_20202 --features all

You can start tests for single features like this:
python test/integration/run_behave_tests.py qac --project_root D:/PRQA/opencv_20202 --features create
Note: If you start a certain feature all features required as preconditions are executed as well.

You can start tests for single features without running the prerequisite features like this:
python test/integration/run_behave_tests.py qac --project_root D:/PRQA/opencv_20202 --features create --minimal

You can start tests for a single tools version like this:
python test/integration/run_behave_tests.py qac --project_root D:/PRQA/opencv_20202 --version 2019.2

To get a very verbose output starting with -v like this:
python test/integration/run_behave_tests.py -v qac --project_root D:/PRQA/opencv_20202

Note: You can combine all options mentioned above.

## <a name="build">How to build and test it</a>




## <a name="contribute">How to contribute</a>

Get in contact with [the maintainers](#maintainers).


## <a name="licenses">Used 3rd party Licenses</a>

| License |
| --- |
| [MIT](https://mit-license.org/) |

## <a name="feedback">Feedback</a>

Get in contact with the [Maintainers](#maintainers), e.g. via email or via the [coding rules T&R project](https://rb-tracker.bosch.com/tracker/projects/CDF/summary).
