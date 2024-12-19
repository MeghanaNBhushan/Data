# A-Core pipeline flow

![FTL general flow](resources/A-Core_build_pipeline.drawio.png)

## A-Core Petalinux container build stage

![petalinux container stage](resources/A-Core_petalinux_container_build.drawio.png)

## A-Core base image build stage

![baseimage stage](resources/A-Core_baseimage_build.drawio.png)

## A-Core application build stage

![application build stage](resources/A-Core_application_build.drawio.png)

## A-Core on target stage

![flash on target stage](resources/A-Core_flash_on_target.drawio.png)

## ulrr master build pipeline
uLRR master build pipeline is scheduled for master branch every night at UTC 12:00:00 and triggered for any commit to master.
Latest master build image and sdk will be available for following day PR jobs
![flash on target stage](resources/ulrr-master-build_pipeline.drawio.png)