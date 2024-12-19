# Install Coverity

The installation of Synopsys is OS dependent and can include different steps and environmental variables for such. The follow-up sessions will cover the installation procedures per OS.

## Windows Installation

For the Windows installation the default delivery is done through [TCC](https://inside-docupedia.bosch.com/confluence/display/CCD/TCC+-+Tool+Collection+for+Collaboration). For TCC specific installation procedures please follow the instructions from its [user manual](https://inside-docupedia.bosch.com/confluence/display/CCD/TCC+manual).

### Installing the TCC Package

All TCC versions are available in the shared folder `\\abtv1000.de.bosch.com\ito\TCC\Tools\coverity`. A BAT script is delivered with sca_tools_package that allows user to select the TCC version they want to install. The script can be found [here](../scripts/tcc/_install_TCC_coverity.bat).

To run this script, simply run:

```
$ scripts/tcc/_install_TCC_coverity.bat
```

And you will be presented with a menu to select the version that will be installed. Alternatively, you can run:


```
$ scripts/tcc/_install_TCC_coverity.bat 0
```

to install the latest available version of the software.

## Linux Installation

For the Linux installation the default delivery is done via [DEB packages](#deb-packages)

### <a href="deb-packages">DEBIAN Packages (OSDX / Ubuntu / Debian)</a>

The existing DEB packages are available [here](https://rb-artifactory.bosch.com/artifactory/tcc-deb-local/tools-contrib/coverity/). If a new one is required, please get in touch with this project [maintainers](../readme.md).
