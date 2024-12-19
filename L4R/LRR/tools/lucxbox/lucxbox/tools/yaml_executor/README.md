# yaml_executor for local build  execution

This script will parse a given .yaml file in the same way the jenkins does.
For this a according lucxbau.jar need to be provided.
After parsing the command steps define in the yaml will be executed in the same order as defined in the .yaml.

-----------------------

## Usage 

```
usage: yaml_executor.py [-h] -y YAML -l LUCXLIB [--lucx-dir LUCX_DIR] -r
                        ROOT_DIR [-o OUTPUT] [-c] [--log-dir LOG_DIR]
                        [--pwd [PWD [PWD ...]]] [--ssh [SSH [SSH ...]]]
                        [--credentials CREDENTIALS] [--encoding ENCODING]
                        [-p [PARAMETER [PARAMETER ...]]]
                        [-i [INCLUDE [INCLUDE ...]]] [-d] [-q]

optional arguments:
  -h, --help            show this help message and exit
  -y YAML, --yaml YAML  the root yaml file
  -l LUCXLIB, --lucxlib LUCXLIB
                        path to lucxbau.jar
  --lucx-dir LUCX_DIR   path to lucx execution directory, usually repository
                        root
  -r ROOT_DIR, --root-dir ROOT_DIR
                        path to com mand execution directory, usually
                        repository root
  -o OUTPUT, --output OUTPUT
                        output directory
  -c, --continuous-output
                        print continuous output
  --log-dir LOG_DIR     logs output directory
  --pwd [PWD [PWD ...]]
                        Specify a password credential of the form
                        user:password or id:user:password
  --ssh [SSH [SSH ...]]
                        Specify a private SSH key credential of the form
                        id:user:ssh-key-path
  --credentials CREDENTIALS
                        Specify a path to a file with the credentials. A line
                        represents a credential of the form
                        type:credential_data
  --encoding ENCODING   Specify a default encoding for the commands output.
  -p [PARAMETER [PARAMETER ...]], --parameter [PARAMETER [PARAMETER ...]]
                        Specify parameters used for .yaml processing
  -i [INCLUDE [INCLUDE ...]], --include [INCLUDE [INCLUDE ...]]
                        Specify include directories used for .yaml processing
  -d, --debug           Print debug information
  -q, --quiet           Print only errors
```



### yaml input file

This is the root yaml, which also defines the entry point for the jenkins job.
This file will be preparsed by the given lucxbau.jar

### lucxlib

A lucxbau.jar must be provided, which version is according to the lucx version used for the project.
This lucxbau.jar is used for preprocessing of the .yaml files.

### root directory

The path to the repositories root has to be provided.

### Output dir

This is where the preprocessed yaml files will be stored.

### Log dir

In this directory a log file is created for each step that is ebing executed. Meaning for each cmd step define in the .yaml file.


## Example with parameter

%python_exe% %script_dir%..\lucxbox\lucxbox\tools\yaml_executor\yaml_executor.py --yaml %yaml_file% --lucx %lucx_dir%\lucxbau.jar --root-dir %REPO_ROOT_DIR% --output %lucx_dir%\preprocessed --log-dir %script_dir%logs


## Supported Syntax

Due to the excessive use of the Jenkins API and Jenkins plugins, the yaml executor is not able to implement the
complete LUCx functionality.

The following lists describe the supported functionality. Unsupported calls are ignored.

### Nodes

All nodes are executed on the local machine ignoring the specified labels.

The executor recognizes the following additional properties:

* `executionOrder`
* `name`
* `runIfAllEnvsSet`
* `runIfEnvIsSet`
* `skip`
* `skipIfAllEnvsSet`
* `skipIfEnvIsSet`

### Stages

Stages support the following properties:

* `executionOrder`
* `name`
* `runIfAllEnvsSet`
* `runIfEnvIsSet`
* `skip`
* `skipIfAllEnvsSet`
* `skipIfEnvIsSet`

### Steps

The yaml executor understands the following properties for all steps listed in the table below:

* `executionOrder`
* `name`
* `runIfAllEnvsSet`
* `runIfEnvIsSet`
* `skip`
* `skipIfAllEnvsSet`
* `skipIfEnvIsSet`


| Step                            | Additionally supported properties                 |
|---------------------------------|---------------------------------------------------|
| cmd                             | fromPath                                          |
| Artifactory.getArtifact         | force, localPath, remotePath, repository (properties.artifactory.repository), url (properties.artifactory.url) |
| Artifactory.getBuild            | buildName, buildNumber, force, localPath, url (properties.artifactory.url) |
| Util.copyFiles                  | destination, flat, includes, source               |
| Util.failOnFilesMissing         | files, fromPath                                   |
| Workspace.setEnvVar             | name, value                                       |


### Credentials

Credentials are supported inside `cmd` as well as for some calls like `Artifactory.getArtifact`.

To set a credential either pass it as an argument to the yaml executor or enter it at execution time.
The argument parser provides the `--pwd` and `--ssh` options to specify single credentials of the form
`id:username:password/ssh file`. The `id` can be omitted for `--pwd` to set the default credential (LUCXPASSWORD).

In case this is unwanted - i.e. because the exeucted command is protocolized - you can also pass a file containing
credentials via `--credentials`.
Each line in this file represents a credential (empty lines or lines starting with # are ignored).
A credential is encoded as `kind:id:data` where `data` is credential specific (i.e. `username:password` for passwords).

Currently possible kinds are shown below. Unknown kinds are ignored.

* `pwd` - password credential
* `ssh` - SSH private key credential
