# AOS project build script
This script provides to project's pipelines, an easy way to handle the application software.

## How to use it
Depending on the intended action, provide the respective flag (for some of those flags, additional information is required)

The list of actions available:
   -h          display this help and exit
   -c          clean conan workspace
   -i          install conan recepy
   -b          build of AOS project
   -a          archive (generated debian package)
   -f          deploy fpga bit file into the rootfs
   -m          deploy mmic libraries into the rootfs
   -w          suppress the cmake compiler warnings

   -e MIDDLEWAREINSTANCE middleware instance (tec0204_linux/te0950_linux/te0950_neutrino/car_pc/testing)
   -d DEBIANPCKGPATH     deploy aos runnable into the rootfs 
   -r ROOTFSPATH         path to rootfs (to where the deploy will be done)
   -u XMLTESTREPORTPATH  run unit-test (path to where the test report will be stored)
   -x BUILDTYPE          build type (debug/release)
   -t TARGETTYPE         architecture target (x86-64/armv8)
   -s AOSVERSION         AOS middleware version

### Examples of usage
 1. Install conan recepy (e.g. for tec0204_linux)
    - ```./build_script.sh -i -x <debug|release> -t <armv8|x86-64> -e tec0204_linux```

 2. Build AOS project
    - ```./build_script.sh -b -x <debug|release> -t <armv8|x86-64> -e tec0204_linux```

 3. Run unit-test
    - ```./build_script.sh -u <Path-to-folder-where-test-report-will-be-saved> -t <armv8|x86-64>```

 4. Archive debian package (generate debian package)
    - ```./build_script.sh -a -x <debug|release> -t <armv8|x86-64> -e tec0204_linux```

 5. Deploy AOS runnable into baseimage
    - ```./build_script.sh -d <path-to-deb-pckg> -o <path-to-ext4-rootfs-file>```

 6. Deploy FPGA bit file into baseimage
    - ```./build_script.sh -f -o <path-to-ext4-rootfs-file>```
