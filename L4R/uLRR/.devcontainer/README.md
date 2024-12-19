# AD Radar .devcontainer

## DevContainer: A-Core Application
This container is intended to guarantee a stable environment for the development and building of the a-core application both locally and in the cloud.


## DevContainer: AD Radar Sensor docs-as-code devcontainer
The VS Code DevContainer for docs-as-code in the context of Radar L4 Development is intended to provide the necessary tooling on top of VS Code to edit the desired artifacts in the most convenient way and to enable the local build of the documentation. 
The main build target is html, but off course also latexpdf build, needs build as well as a clean built. 

## Hints on configuration
### Docker container mount points
If no special settings are use, then VS Code installs a server into the container and connects to `WORKDIR` as specified in the _Dockerfile_ used to create the docker image. In our case we derive from a pre-defined docs-as-code [_Dockerfile_](https://github.boschdevcloud.com/docs-as-code/sphinx-needs-toolkit-docker).
For some reason they define the `WORKDIR` to be `sphinx-needs`.
In order to have the same folder structure within the container as we have it on disk (when cloning the repo) we mount to the devContainer by handing over the mount points. Additionally we mount also the `.git` folder because, the documentation build reads the git branch information via python commands (`documentation/conf.py`).

See `mounts` within the [docs-as-code/devcontainer.json (devContatiner configuration file)](docs-as-code/devcontainer.json)

> **NOTE**: Consider and synchronize the mount points also in the github workflows.

### Devcontainer settings / workspace settings
The [docs-as-code/devcontainer.json (devContatiner configuration file)](docs-as-code/devcontainer.json) contains settings for the installed extensions. See the `settings` section. 
However for some reason not all settings are taken over. Currently it seems the best to have the same settings in the [docs-as-code/devcontainer.json (devContatiner configuration file)](docs-as-code/devcontainer.json) and the [Workspace configuration file](../.vscode/settings.json).
