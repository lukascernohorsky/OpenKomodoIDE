# OpenKomodoIDE Build Guide for Debian

This guide provides step-by-step instructions for building OpenKomodoIDE on Debian-based systems (Debian, Ubuntu, etc.).

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installing Dependencies](#installing-dependencies)
3. [Build Process](#build-process)
4. [Troubleshooting](#troubleshooting)
5. [Cross-Platform Builds](#cross-platform-builds)
6. [ARM64 Support](#arm64-support)

## System Requirements

### Supported Debian Versions

- Debian 10 (Buster)
- Debian 11 (Bullseye) 
- Debian 12 (Bookworm)
- Ubuntu 20.04 LTS and later

### Minimum Hardware Requirements

- **CPU**: 4-core processor (8+ cores recommended)
- **RAM**: 8GB (16GB+ recommended)
- **Disk Space**: 50GB+ free space
- **Swap**: 4GB+ recommended

### ARM64 Requirements

- **CPU**: ARMv8-A 64-bit processor
- **RAM**: 8GB+ recommended
- **Disk Space**: 50GB+ free space

## Installing Dependencies

### Basic Build Tools

```bash
sudo apt update
sudo apt upgrade -y

# Install basic build tools
sudo apt install -y build-essential git python3 python3-dev 
    python3-pip python3-venv libssl-dev libffi-dev zlib1g-dev 
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm 
    libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev 
    liblzma-dev libxml2-dev libxslt1-dev
```

### Python 3 Setup

```bash
# Ensure Python 3 is the default
sudo apt install -y python-is-python3

# Install additional Python tools
sudo apt install -y python3-setuptools python3-wheel python3-distutils

# Install pip if not present
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip setuptools wheel
```

### Mozilla Build Dependencies

```bash
# Install Mozilla build dependencies
sudo apt install -y autoconf2.71 yasm libgtk-3-dev libdbus-glib-1-dev 
    libasound2-dev libcurl4-openssl-dev libiw-dev libxt-dev 
    mesa-common-dev libgl1-mesa-dev libglu1-mesa-dev libx11-xcb-dev 
    libxcb-shm0-dev libxcb-render0-dev libxcb-render-util0-dev 
    libxcb-xkb-dev libxcb-icccm4-dev libxcb-image0-dev 
    libxcb-keysyms1-dev libxcb-randr0-dev libxcb-shape0-dev 
    libxcb-sync-dev libxcb-xfixes0-dev libxcb-xinerama0-dev 
    libxcb-dri3-dev libxcb-util-dev libxkbcommon-dev 
    libxkbcommon-x11-dev libpango1.0-dev libgdk-pixbuf2.0-dev
```

### Additional Tools

```bash
# Install additional required tools
sudo apt install -y zip unzip tar gzip bzip2 xz-utils file 
    patch diffutils make automake libtool pkg-config 
    cmake ninja-build ccache

# Install version control systems
sudo apt install -y git subversion
```

### ARM64 Specific Dependencies

```bash
# For ARM64 systems, install additional dependencies
sudo apt install -y gcc-aarch64-linux-gnu g++-aarch64-linux-gnu 
    binutils-aarch64-linux-gnu libc6-dev-arm64-cross
```

## Build Process

### Using Git Instead of Mercurial

By default, the build system uses Mercurial to download Firefox source code. You can configure it to use Git instead:

```bash
# Set environment variables to use Git
export MOZ_SOURCE_REPO=https://github.com/mozilla-firefox/firefox.git
export MOZ_SOURCE_STAMP=firefox-140.7.0esr
```

This will download the source code from GitHub instead of Mercurial repositories.

### Step 1: Clone the Repository

```bash
# Clone the OpenKomodoIDE repository
git clone https://github.com/your-repo/OpenKomodoIDE.git
cd OpenKomodoIDE
```

### Step 2: Set Up Environment

```bash
# Set up environment variables
export PATH=$PATH:$PWD/bin

export MOZCONFIG=$PWD/mozconfig
export LD_LIBRARY_PATH=$PWD/lib:$LD_LIBRARY_PATH

export PLATFORM=linux  # or linux-arm64 for ARM64 systems
```

### Step 3: Configure the Build

```bash
# Configure the build for Komodo 12 with Firefox 140 ESR
python3 mozilla/build.py configure -k 12.0 --with-crashreport-symbols
```

### Step 4: Build the Project

```bash
# Start the build process
python3 mozilla/build.py all
```

### Step 5: Build Specific Components

```bash
# Build just the Mozilla part
python3 mozilla/build.py mozilla

# Build PyXPCOM
python3 mozilla/build.py pyxpcom

# Create packages
python3 mozilla/build.py packages
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: Python 3 not found

**Solution**: Ensure Python 3 is installed and set as default

```bash
sudo apt install -y python-is-python3
python3 --version
```

#### Issue: Missing build dependencies

**Solution**: Install missing packages using apt

```bash
sudo apt install -y <missing-package>
```

#### Issue: Permission denied

**Solution**: Ensure proper permissions

```bash
chmod +x mozilla/build.py
chmod -R +x bin/
```

#### Issue: Out of memory

**Solution**: Increase swap space or use a machine with more RAM

```bash
# Create additional swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Cross-Platform Builds

### Building for ARM64 on x86_64

```bash
# Install cross-compilation tools
sudo apt install -y gcc-aarch64-linux-gnu g++-aarch64-linux-gnu

# Configure for ARM64
python3 mozilla/build.py configure -k 12.0 --target=aarch64-linux-gnu

# Build for ARM64
python3 mozilla/build.py all
```

### Building for Other Platforms

```bash
# For FreeBSD
python3 mozilla/build.py configure -k 12.0 --target=freebsd

# For NetBSD
python3 mozilla/build.py configure -k 12.0 --target=netbsd

# For OpenBSD
python3 mozilla/build.py configure -k 12.0 --target=openbsd
```

## ARM64 Support

### Building on ARM64 Systems

```bash
# Install ARM64-specific dependencies
sudo apt install -y gcc-aarch64-linux-gnu g++-aarch64-linux-gnu

# Set platform
export PLATFORM=linux-arm64

# Configure and build
python3 mozilla/build.py configure -k 12.0
python3 mozilla/build.py all
```

### ARM64-Specific Configuration

```bash
# ARM64-specific environment variables
export CFLAGS="-march=armv8-a -mtune=generic"
export CXXFLAGS="-march=armv8-a -mtune=generic"
export LDFLAGS="-Wl,--no-undefined"

# For better performance on ARM64
export MOZ_OPTIMIZE_FLAGS="-O3 -march=armv8-a+crc+simd"
```

## Build Options

### Common Configuration Options

```bash
# Development build
python3 mozilla/build.py configure -k 12.10

# Release build with symbols
python3 mozilla/build.py configure -k 12.0 --with-crashreport-symbols

# Debug build
python3 mozilla/build.py configure -k 12.0 --enable-debug
```

### Environment Variables

```bash
# Parallel build (use all cores)
export MAKEFLAGS="-j$(nproc)"

# Use ccache for faster rebuilds
export CCACHE_DIR=$PWD/.ccache
export CCACHE_SLOPPINESS="file_macro,time_macros"

# Disable telemetry
export MOZ_TELEMETRY_REPORTING=0
```

## Testing the Build

### Running Tests

```bash
# Run basic tests
python3 test_build.py

# Run multiplatform tests
python3 test_multiplatform.py

# Run Firefox 140 ESR integration tests
python3 test_firefox_140.py
```

### Verifying the Build

```bash
# Check build artifacts
ls -la build/
ls -la dist/

# Check binary
file komodo
ldd komodo
```

## Cleaning Up

```bash
# Clean build
python3 mozilla/build.py clean

# Distclean (remove everything)
python3 mozilla/build.py distclean

# Remove temporary files
rm -rf .tmp .cache .ccache
```

## Advanced Configuration

### Custom Mozilla Configuration

Create a `mozconfig` file with custom options:

```bash
# Enable additional features
ac_add_options --enable-application=komodo
ac_add_options --enable-extensions=default
ac_add_options --enable-system-ffi
ac_add_options --enable-system-pixman

# Optimization flags
ac_add_options --enable-optimize="-O3"
ac_add_options --enable-linker=lld

# Debugging options
ac_add_options --enable-debug-symbols
ac_add_options --disable-install-strip
```

### Cross-Compilation Setup

For cross-compilation, create a custom toolchain file:

```bash
# ARM64 toolchain example
cat > arm64-toolchain.cmake << EOF
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
EOF
```

## Performance Optimization

### Build Cache

```bash
# Set up ccache
export CCACHE_DIR=$PWD/.ccache
export CCACHE_SLOPPINESS="file_macro,time_macros"
export CCACHE_MAXSIZE="10G"

# Enable sccache (faster than ccache)
export RCCACHE_DIR=$PWD/.sccache
export RCCACHE_MAX_SIZE="10G"
```

### Parallel Builds

```bash
# Use all available cores
export MAKEFLAGS="-j$(nproc)"

# For systems with limited memory, use fewer jobs
export MAKEFLAGS="-j$(($(nproc) - 2))"
```

## Documentation

### Build Documentation

```bash
# Generate documentation
python3 docs/generate_docs.py

# Build HTML documentation
python3 docs/build_html.py
```

### API Documentation

```bash
# Generate API documentation
python3 docs/generate_api_docs.py

# Build Sphinx documentation
cd docs
make html
```

## Contributing

### Reporting Issues

When reporting build issues, please include:

1. Debian version (`cat /etc/debian_version`)
2. CPU architecture (`uname -m`)
3. Python version (`python3 --version`)
4. GCC version (`gcc --version`)
5. Exact error message
6. Build log (if available)

### Submitting Patches

```bash
# Create a feature branch
git checkout -b feature/your-feature

# Make your changes and commit
git commit -m "Add your feature"

# Push to your fork
git push origin feature/your-feature

# Create a pull request
```

## License

This build guide is provided under the same license as OpenKomodoIDE.

## Support

For additional support:

- Check the [OpenKomodoIDE Wiki](https://github.com/your-repo/OpenKomodoIDE/wiki)
- Join our [Discord server](https://discord.gg/your-invite)
- Open an issue on [GitHub](https://github.com/your-repo/OpenKomodoIDE/issues)

## Appendix

### Useful Commands

```bash
# Check system information
uname -a
cat /etc/debian_version
lsb_release -a

# Monitor build process
htop
top
free -h
df -h

# Check build logs
tail -f build.log
journalctl -f
```

### Build Environment Variables

```bash
# Common environment variables
MOZCONFIG=path/to/mozconfig
LD_LIBRARY_PATH=path/to/libs
PATH=path/to/tools:$PATH
CC=gcc
CXX=g++
CFLAGS="-O2 -Wall"
CXXFLAGS="-O2 -Wall"
LDFLAGS="-Wl,--no-undefined"
```

This guide provides comprehensive instructions for building OpenKomodoIDE on Debian-based systems, including ARM64 support and cross-platform builds.