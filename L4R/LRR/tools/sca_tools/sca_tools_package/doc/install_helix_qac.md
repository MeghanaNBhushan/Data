# Install Helix QAC

The installation of Helix QAC is OS dependent and can include different steps and environmental variables for such. However it's license servers are unique. The follow-up sessions will cover the setup of the license server and the installation procedures per OS.

## License Setup

Request a license by requesting a service group access "CCFUNC_1711_176_ua" in [urs](https://rb-urs-n1.bosch.com/URSXFrontEnd/Sites/Home.cshtml?rid=QM2ITM5MTN2AjN).

After the URS access is approved, please wait until 48 hours until the group access is approved.

### Setup in Helix without sca_tools

In the Helix UI, be sure to configure the appropriate servers for the corresponding module versions.

| URL                                  | License | Comment                              |
| ------------------------------------ | ------- | ------------------------------------ |
| 5065@rb-lic-rlm-prqa-gl.de.bosch.com | C       | For C modules < 9.6 (< QAC 2019.1)   |
| 5065@rb-lic-rlm-prqa-cc.de.bosch.com | C++     | For C++ modules                      |
| 5065@rb-lic-rlm-prqa2.de.bosch.com   | C       | For C modules >= 9.7 (>= QAC 2019.1) |


### Setup in Helix with sca_tools

If you use the sca_tools no additional steps are necessary as per default the projects will be created with the appropriate licenses already configured.

## Windows Installation

For the Windows installation the default delivery is done through [TCC](https://inside-docupedia.bosch.com/confluence/display/CCD/TCC+-+Tool+Collection+for+Collaboration). For TCC specific installation procedures please follow the instructions from its [user manual](https://inside-docupedia.bosch.com/confluence/display/CCD/TCC+manual).

### Installing the TCC Package

All TCC versions are available in the shared folder `\\abtv1000.de.bosch.com\ito\TCC\Tools\helix_qac`. A BAT script is delivered with sca_tools_package that allows user to select the TCC version they want to install. The script can be found [here](../scripts/tcc/_install_TCC_qac.bat).

To run this script, simply run:

```
$ scripts/tcc/_install_TCC_qac.bat
```

And you will be presented with a menu to select the version that will be installed. Alternatively, you can run:


```
$ scripts/tcc/_install_TCC_qac.bat 0
```

To install the latest available version of the software.

## Linux Installation

For the Linux installation the default delivery is done via [DEB packages](#deb-packages)

### <a href="deb-packages">DEBIAN Packages (OSDX / Ubuntu / Debian)</a>

The existing DEB packages are available [here](https://rb-artifactory.bosch.com/artifactory/tcc-deb-local/tools/). If a new one is required, please get in touch with this project [maintainers](../readme.md).
