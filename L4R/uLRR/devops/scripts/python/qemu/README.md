# QEMU Fusion

QEMU Fusion is a Python tool for managing a QEMU environment.

## Usage

You can use the `qemu_fusion.py` script to install artifacts, install Debian packages, and run unit tests. Here are some examples:

```bash
python devops/scripts/python/qemu/qemu_fusion.py install-artifact --artifact /workspaces/ad-radar-sensor/commands.txt --destination-path /usr/bin/ --rootfs-filepath /workspaces/ad-radar-sensor/te0950rootfs/rootfs_te0950_bullseye_arm64_latest.ext4

python devops/scripts/python/qemu/qemu_fusion.py install-deb --deb-package /workspaces/ad-radar-sensor/artifacts/ulrr-0-0-1-ubuntu2004-armv8-gcc8-debug.deb --rootfs-filepath /workspaces/ad-radar-sensor/te0950rootfs/rootfs_te0950_bullseye_arm64_latest.ext4

mkdir /workspaces/ad-radar-sensor/test_reports/
python devops/scripts/python/qemu/qemu_fusion.py run-unit-test --test-report-path /workspaces/ad-radar-sensor/test_reports/ --rootfs-filepath /workspaces/ad-radar-sensor/te0950rootfs/rootfs_te0950_bullseye_arm64_latest.ext4
```

## Reference

rootfs_te0950_bullseye_arm64_latest.ext4 was taken using [this instructions](./../../../../software/os/debian/conan/base_image/README.md)