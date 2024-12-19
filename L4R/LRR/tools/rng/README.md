<!---

	Copyright (c) 2009, 2018 Robert Bosch GmbH and its subsidiaries.
	This program and the accompanying materials are made available under
	the terms of the Bosch Internal Open Source License v4
	which accompanies this distribution, and is available at
	http://bios.intranet.bosch.com/bioslv4.txt

-->

# Release Note Generator (RnG)  <!-- omit in toc -->

[![License: BIOSL v4](http://bios.intranet.bosch.com/bioslv4-badge.svg)](#license)

Toolchain to semi-automate the release note creation and release process based on python/asciidoc. The tool support the different stages of the release note creation, signing and publishing process.

* Stage "Draft": generates an a draft version of an asciidoc file which contains data such as QAC, Coverity, Compiler statiscits, Overview of new features, known problems, release specific links,...The draft document can be manually edited. 
* Stage "Final": generates a PDF and HTML of the release not
* Stage "Workon": creates a workon RBGA based no PDF `(in development)`
* Stage "Publish": publish the release and release note e.g. in MS Teams, copy to customer folder, ... `(in development)`


![Overview](./doc/rng_overview.png)

**Processing Chain**

![Processing chain](./doc/processing_chain.png)


## Table of Contents  <!-- omit in toc -->

- [Getting Started as a User](#getting-started-user)
- [Getting Started as a Developer](#getting-started-dev)
- [Building and Testing](#building-and-testing)
- [Contribution Guidelines](#contribution-guidelines)
- [Configure Git and correct EOL handling](#configure-Git-and-correct-EOL-handling)
- [Feedback](#feedback)
- [About](#about)
  - [Maintainers](#maintainers)
  - [Contributors](#contributors)
  - [3rd Party Licenses](#3rd-party-licenses)
  - [Used Encryption](#used-encryption)
  - [License](#license)

## Getting Started as User <a name="getting-started-user"></a>
In order to edit content and run the RnG the following tolls needs to be installed and setup.

* **python**
* **Asciidoc**
* **git (+ SourceTree)** (optional, in case adoc file shall be stored in git)

### Install python
Install **Anaconda Python** via [IT SERVICE PORTAL](https://rb-servicecatalog.apps.intranet.bosch.com/RequestCenter/website/Grunt/application/home.html?route=home)

Set python related environmentvariable according to your Anaconda3 installation directory (_here C:\Anaconda3_):

* `Path`: C:\Anaconda3; C:\Anaconda3\Library\bin
* `PYTHON_INCLUDE`: C:\Anaconda3\include
* `PYTHON_LIB`: C:\Anaconda3\libs\python37.lib (_python37.lib depends on your python version ..._)

> **NOTE**: You do not need Admin rights in order to set the environmentvariable!

### Install AsciidocTools
Install **AsciidocTools** by a clone of additional bitbucket repository.
This AsciidocTools repository contains the Asciidoc tools collection for Windows.

TODO: Get fork  of AsciidocTools into rng repo

> 1.) Clone this repository (ssh://git@sourcecode.socialcoding.bosch.com:7999/gades/asciidoctools.git) into `C:/AsciidocTools` 
> 
> **2.) Change master branch to AD-Radar-Sensor branch**
> 
> 3.) Execute `C:/AsciidocTools/setEnvironmentVariables.bat`

More information see bitbucket repository: https://sourcecode.socialcoding.bosch.com/projects/GADES/repos/asciidoctools/browse

> **NOTE**: Currently used PDF genration in the project requires an update of the AsciidocTools (_update of Asciidoctor PDF verison_). So, use the feature branch AD-Radar-Sensor inside the project.

## Getting Started as Developer <a name="getting-started-dev"></a>

### IDE (proposal)
Visual Studio Code available via [IT SERVICE PORTAL](https://rb-servicecatalog.apps.intranet.bosch.com/RequestCenter/website/Grunt/application/home.html?route=home)

### Visual Studio Code (Extensions)
The following visual studio code extension may help you as an author. 

#### AsciiDoc
An extension that provides live preview, syntax highlighting and snippets for the AsciiDoc format using Asciidoctor flavor into VS Code.

> Further information see online documentation: https://docs.asciidoctor.org/asciidoc/latest/

#### Python
ms-python.python

### Linting
It is mandotory to use: pylint

### Auto Formatting
It is mandotory to use:  black

## Building and Testing <a name="building-and-testing"></a>

TBD

## Folder Structure

```
┣ logs/
```
* `logs`: stores log files for different log levels  

```
┣ logs/
```
* `docs`: documentation folder  

```
┣ rn_TestProject/
┣ rn_TestProject/adoc/
┣ rn_TestProject/adoc_input/
┣ rn_TestProject/build_data/
┣ rn_TestProject/cfg/
┣ rn_TestProject/export/
┣ rn_TestProject/output/
```

* `adoc`: contains the adoc base file (based on XC-DA System Release Note Template V2.15 (20.10.2020) ). Compiled adoc file from various input sources is generated here
* `adoc_input`: asciidoc text snippets are located here which are compiled into overall adoc via template engine
* `build_data`: contains test data for QAC, coverity, compiler warnings which is typcally located in build folder
* `cfg`: contains config for build folder structure, jira export, workon config, ...
* `export`: contains exported data e.g. from jira
* `output`: final release note pdf /html is located here

```
┣ src/
┣ src/compiler
┣ src/converter
┣ src/creator
┣ src/exporter
┣ src/signer
```
* `src\`: contains  python / powershell scripts. main python module rng.py calling all subfunctions is located here
* `src\<subfunctions>`: contains the individual subfunctions to generated draft version, export of jira data, ..


## Configuration <a name="configuration"></a>

Following conifguration files are available

/rn_TestProject/rng_cfg.json : contains the main path info of the project directory

/rn_TestProject/cfg/build_dir_cfg.json configuration of layout of the build directory used for converting raw data into to ascii doc text snippets

/rn_TestProject/cfg/jira_export_cfg.json
Contains the jql queries used in powershell script to export 
* Customer Features
* Internal Features
* Customer Open Problems
* Internal Open Problems
* Customer Fixed Problems
* Internal Fixed Problems

/rn_TestProject/cfg/workon/workon_cfg.json
Contains the json workon config which is used in workon REST api to create draft of workon.

/rn_TestProject/adoc/asciidoc_cfg.json
Contains the adoc file specific variants (e.g. internal, customer). This is used to determine the number of release note variants which are generated in the *Final* stage

## How to run the tool

*Option 1:*
Call one of the batch files in /src after you have configured your project specific config see [Configuration](#configuration)

*Option 2:*
Call rng.py directly. Use rng.py -h to get additional help for mandatory and optional arguments


## Roadmap / Feature Requests

Roadmap/open tasks are tracked in [TODO.md](./TODO.md)

New Feautures can be requested there.

## Contribution Guidelines <a name="contribution-guidelines"></a>

Use this section to describe or link to documentation which explaining how users can make contributions to the contents of this repository. Consider adopting the [BIOS way of facilitating contributions](http://bos.ch/ygF).

TBD

## Configure Git and correct EOL handling <a name="configure-Git-and-correct-EOL-handling"></a>
Here you can find the references for [Dealing with line endings](https://help.github.com/articles/dealing-with-line-endings/ "Wiki page from Social Coding"). 

Every time you press return on your keyboard you're actually inserting an invisible character called a line ending. Historically, different operating systems have handled line endings differently.
When you view changes in a file, Git handles line endings in its own way. Since you're collaborating on projects with Git and GitHub, Git might produce unexpected results if, for example, you're working on a Windows machine, and your collaborator has made a change in OS X.

To avoid problems in your diffs, you can configure Git to properly handle line endings. If you are storing the .gitattributes file directly inside of your repository, than you can asure that all EOL are manged by git correctly as defined.


## Feedback <a name="feedback"></a>

Consider using this section to describe how you would like other developers
to get in contact with you or provide feedback.

jochen.held@de.bosch.com

## About <a name="about"></a>

### Maintainers <a name="maintainers"></a>

List the maintainers of this repository here. Consider linking to their Bosch Connect profile pages. Mention or link to their email as a minimum.

Jochen Held jochen.held@de.bosch.com

### Contributors <a name="contributors"></a>

Consider listing contributors in this section to give explicit credit. You could also ask contributors to add themselves in this file on their own.

### 3rd Party Licenses <a name="3rd-party-licenses"></a>

You must mention all 3rd party licenses (e.g. OSS) licenses used by your
project here. Example:

| Name | License | Type |
|------|---------|------|
| [AsciidocFX](https://asciidocfx.com/) |  [Apache 2.0 License](https://github.com/asciidocfx/AsciidocFX/blob/master/LICENSE) | exe | 
| [Asciidoctor](https://asciidoctor.org/) | [MIT License](https://github.com/asciidoctor/asciidoctor/blob/master/LICENSE) | exe |
| [git](https://github.com/git/git) | [LGPL-2.1](https://github.com/git/git/blob/master/LGPL-2.1) | exe

### Used Encryption <a name="used-encryption"></a>

Declaration of the usage of any encryption (see BIOS Repository Policy §4.a).

The source code in this repository (releasenotegenerator) does not use any encryption.

### License <a name="license"></a>

[![License: BIOSL v4](http://bios.intranet.bosch.com/bioslv4-badge.svg)](#license)

> Copyright (c) 2009, 2018 Robert Bosch GmbH and its subsidiaries.
> This program and the accompanying materials are made available under
> the terms of the Bosch Internal Open Source License v4
> which accompanies this distribution, and is available at
> http://bios.intranet.bosch.com/bioslv4.txt

<!---

	Copyright (c) 2009, 2018 Robert Bosch GmbH and its subsidiaries.
	This program and the accompanying materials are made available under
	the terms of the Bosch Internal Open Source License v4
	which accompanies this distribution, and is available at
	http://bios.intranet.bosch.com/bioslv4.txt

-->
