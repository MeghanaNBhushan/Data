# Build Tool

## Description
The build_tool is a command-line utility designed to streamline the build process for the ad-radar-sensor a-core apllication SW.

## Features
- Handles A-Core SW: Business logic and AOS project
  - Conan dependencies installation
  - SW Build
  - Unit-test execution
  - Packaging (debian and conan)

Similar to pre-exist build_script, it supports the deploy of artefacts (fpga bit file, mmic libraries, aos project build) into a debian base image

## Usage
To build the ad-radar-sensor project using the build_tool, follow these steps:

1. Open a terminal. As the tool is sourced when the dev-container is created, the same shall be accessible from any point
2. To see the commmands available: 
    ```
    ir2-build-tool --help
    ```
3. Config tool
    ```
    # example 1 - Change target type for BL from armv8 to x86-86
    ir2-build-tool config bl --target-type x86-64
    
    # example 2 - Suppress compiler warning on BL
    ir2-build-tool config bl --suppress-warnings true
    
    # example 3 - Enable back the compiler warnings on BL
    ir2-build-tool config bl --suppress-warnings false
    ```
4. Software build
    ```
    # example 1 - Build business logic
    ir2-build-tool install bl
    ir2-build-tool build bl
    
    # example 2 - Build aos
    ir2-build-tool install aos
    ir2-build-tool build aos
    ```
5. Packaging
    ```
    # example 1 - Build a conan package for business logic
    ir2-build-tool package bl --package-type conan -> available soon

    # example 2 - Build a deb package for AOS project
    ir2-build-tool package aos --package-type deb
    ```
6. Unit-test
    ```
    # example 1 - Trigger unit tests from AOS application
    ir2-build-tool unit-test aos --base-image-file path-to-base-image/rootfs_tec0204_bullseye_final_arm64_latest.ext4.gz

    # example 2 - Trigger unit tests from BL 
    ir2-build-tool unit-test bl
    ```

For a detailed view: https://inside-docupedia.bosch.com/confluence/display/ATD/Handbook

## Configuration
The build_tool can be customized by modifying the configuration file located at `/workspaces/ad-radar-sensor/tools/build_tool`. Here, you can specify build options, and configure other settings according to your needs.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please contact C3 Team.
