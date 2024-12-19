
#!/bin/bash

# This shell script facilitates Python cross-compilation for ARM architecture.
# It takes a single input, which is the source directory location within the cross-compilation folder.
# Ensure that the following environment variables are set before running the script:
# - CROSS: Specifies the cross-compilation toolchain or compiler for ARM.
# - INSTALL_MMIC_DIR: Specifies the installation directory for Python within the cross-compilation directory.
# - TARGET_DIR: Specifies the target directory where the compiled Python will be placed.

# Usage: ./mmic_cross_compile.sh source_directory

set -e

if [ $# -ne 1 ]; then
  echo "Usage: $0 <SOURCE_DIR>"
  exit 1
fi

SOURCE_DIR="$1"

# Extract the archive
cd "$SOURCE_DIR/"
tar -xvf Python3.9.5-glibc.tar.xz

# Configure glibc for cross-compilation
cd "$SOURCE_DIR/config/"
../glibc-2.31/configure --prefix=$INSTALL_MMIC_DIR --exec-prefix=$INSTALL_MMIC_DIR \
  --build=x86_64-linux-gnu --host=aarch64-linux-gnu \
  STRIP="/usr/bin/aarch64-linux-gnu-strip " \
  AR="/usr/bin/aarch64-linux-gnu-ar " \
  LD="/usr/bin/aarch64-linux-gnu-ld " \
  CC="/usr/bin/aarch64-linux-gnu-gcc" \
  CXX="/usr/bin/aarch64-linux-gnu-g++" \
  CFLAGS="-s -O3 -fexpensive-optimizations -frename-registers -fomit-frame-pointer " \
  CXXFLAGS="-s -O3 -fexpensive-optimizations -frename-registers -fomit-frame-pointer " \
  LDFLAGS="-Wl,--rpath=$TARGET_DIR/lib -Wl,--dynamic-linker=$TARGET_DIR/lib/ld-linux.so.3 -Wl,-O3 -Wl,--hash-style=gnu -Wl,--as-needed " \
  CPP="/usr/bin/aarch64-linux-gnu-gcc"
make -j 4
make install

# Configure Python dependencies for cross-compilation
cd "$SOURCE_DIR/Python-3.9.5"
./configure \
  --prefix=$INSTALL_MMIC_DIR \
  --exec-prefix=$INSTALL_MMIC_DIR \
  --host="${CROSS}" \
  --target=arm \
  --build=x86_64-linux-gnu \
  --disable-ipv6 \
  ac_cv_file__dev_ptmx=no \
  ac_cv_file__dev_ptc=no \
  --with-ensurepip=install \
  --enable-loadable-sqlite-extensions \
  --enable-optimizations \
  --enable-shared \
  CHOST="${CROSS}" \
  CC="${CROSS}"-gcc \
  CXX="${CROSS}"-g++ \
  AR="${CROSS}"-ar \
  LD="${CROSS}"-ld \
  RANLIB="${CROSS}"-ranlib \
  LDFLAGS="-Wl,--strip-all -Wl,-start-group -ldl -lpthread -lm -lrt -Wl,-end-group -Wl,--rpath=$TARGET_DIR/lib/ -Wl,--dynamic-linker=$TARGET_DIR/lib/ld-linux.so.3"
make -j 4
make install

# Remove the redundant python, glibc zip files
mkdir -p /opt/bosch/ulrr/cross-compilation/python/include/aarch64-linux-gnu
cp -r /opt/bosch/ulrr/cross-compilation/python/include/python3.9 /opt/bosch/ulrr/cross-compilation/python/include/aarch64-linux-gnu/
rm -r /opt/bosch/ulrr/cross-compilation/python/include/python3.9
rm -r /opt/bosch/ulrr/cross-compilation/source/Python3.9.5-glibc.tar.xz