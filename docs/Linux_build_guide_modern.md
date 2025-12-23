# Modern Linux Build Guide for OpenKomodoIDE

This guide provides instructions for building OpenKomodoIDE on modern Linux distributions (Ubuntu 22.04+, Fedora 36+, etc.) with Python 3 and Firefox 140 ESR support.

## Prerequisites

### Supported Distributions
- Ubuntu 22.04 LTS or later
- Fedora 36 or later
- Debian 11 or later
- Other modern distributions with recent packages

### Required Packages

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y \
    git \
    mercurial \
    subversion \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    autoconf2.13 \
    automake \
    libtool \
    pkg-config \
    curl \
    wget \
    unzip \
    zip \
    tar \
    gzip \
    bzip2 \
    xz-utils \
    patch \
    make \
    cmake \
    ninja-build \
    gcc \
    g++ \
    clang \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libffi-dev \
    liblzma-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libglib2.0-dev \
    libgtk-3-dev \
    libdbus-glib-1-dev \
    libgconf2-dev \
    libasound2-dev \
    libpulse-dev \
    libxt-dev \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libxrandr-dev \
    libxfixes-dev \
    libxi-dev \
    libxcb1-dev \
    libxcb-render0-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev \
    libxcb-randr0-dev \
    libxcb-shape0-dev \
    libxcb-keysyms1-dev \
    libxcb-icccm4-dev \
    libxcb-image0-dev \
    libxcb-util0-dev \
    libxkbcommon-dev \
    libxkbcommon-x11-dev \
    libwayland-dev \
    libegl1-mesa-dev \
    libgbm-dev \
    libdrm-dev \
    libgles2-mesa-dev \
    libvpx-dev \
    libopus-dev \
    libwebp-dev \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    libevent-dev \
    libnss3-dev \
    libnspr4-dev \
    libsqlite3-dev \
    libffi-dev \
    libpixman-1-dev \
    libharfbuzz-dev \
    libgraphite2-dev \
    libicu-dev \
    libhunspell-dev \
    libhyphen-dev \
    libstartup-notification0-dev \
    libsecret-1-dev \
    libjsoncpp-dev \
    libdbus-1-dev \
    libatk1.0-dev \
    libatk-bridge2.0-dev \
    libepoxy-dev \
    libgudev-1.0-dev \
    libcolord-dev \
    libgtk-3-dev \
    libgdk-pixbuf2.0-dev \
    libpango1.0-dev \
    libcairo2-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    libgstreamer-plugins-good1.0-dev \
    libgstreamer-plugins-ugly1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-pulseaudio
```

#### Fedora/RHEL
```bash
sudo dnf install -y \
    git \
    mercurial \
    subversion \
    @development-tools \
    python3 \
    python3-pip \
    python3-devel \
    autoconf213 \
    automake \
    libtool \
    pkgconfig \
    curl \
    wget \
    unzip \
    zip \
    tar \
    gzip \
    bzip2 \
    xz \
    patch \
    make \
    cmake \
    ninja-build \
    gcc \
    gcc-c++ \
    clang \
    openssl-devel \
    zlib-devel \
    bzip2-devel \
    readline-devel \
    sqlite-devel \
    ncurses-devel \
    libffi-devel \
    xz-devel \
    libxml2-devel \
    libxslt-devel \
    libjpeg-turbo-devel \
    libpng-devel \
    freetype-devel \
    glib2-devel \
    gtk3-devel \
    dbus-glib-devel \
    GConf2-devel \
    alsa-lib-devel \
    pulseaudio-libs-devel \
    libXt-devel \
    libX11-devel \
    libXext-devel \
    libXrender-devel \
    libXrandr-devel \
    libXfixes-devel \
    libXi-devel \
    libxcb-devel \
    libX11-xcb-devel \
    libxkbcommon-devel \
    libxkbcommon-x11-devel \
    wayland-devel \
    mesa-libEGL-devel \
    mesa-libgbm-devel \
    libdrm-devel \
    mesa-libGLES-devel \
    libvpx-devel \
    opus-devel \
    libwebp-devel \
    libavcodec-free-devel \
    libavformat-free-devel \
    libavutil-free-devel \
    libswscale-free-devel \
    libevent-devel \
    nss-devel \
    nspr-devel \
    sqlite-devel \
    libffi-devel \
    pixman-devel \
    harfbuzz-devel \
    graphite2-devel \
    libicu-devel \
    hunspell-devel \
    hyphen-devel \
    startup-notification-devel \
    libsecret-devel \
    jsoncpp-devel \
    dbus-devel \
    atk-devel \
    at-spi2-atk-devel \
    libepoxy-devel \
    libgudev-devel \
    colord-devel \
    gstreamer1-devel \
    gstreamer1-plugins-base-devel \
    gstreamer1-plugins-bad-free-devel \
    gstreamer1-plugins-good-devel \
    gstreamer1-plugins-ugly-free-devel \
    gstreamer1-plugin-libav \
    gstreamer1-tools
```

### Additional Requirements

#### Rust
Modern Firefox builds require Rust. Install it using:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env
```

#### Node.js
Some build tools require Node.js:
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Fedora/RHEL
sudo dnf install -y nodejs
```

#### Python Dependencies
```bash
pip3 install --upgrade pip setuptools wheel
pip3 install mercurial six
```

## Build Process

### 1. Configure Mozilla Build

```bash
cd mozilla
python3 build.py configure -k 14.10 --moz-src=14000:FIREFOX_140_0_RELEASE
```

**Options:**
- `-k 14.10`: Komodo version (14.10 for development builds)
- `--moz-src=14000:FIREFOX_140_0_RELEASE`: Use Firefox 140 ESR
- `--with-crashreport-symbols`: Include crash reporting symbols
- `--debug`: Build with debug symbols
- `--release`: Build release version (default)

### 2. Build Mozilla

```bash
python3 build.py distclean all
```

This will:
1. Download Firefox 140 ESR source code
2. Apply Komodo-specific patches
3. Configure the build
4. Compile Mozilla with Komodo extensions

### 3. Build Komodo

```bash
cd ..
export PATH=$(pwd)/util/black:$PATH
bk configure -V 14.10.0-devel
bk build
```

### 4. Run Komodo

```bash
bk run
```

## Troubleshooting

### Common Issues

#### Python 2 vs Python 3
Ensure you're using Python 3 for all build commands. The build system has been updated to support Python 3.

#### Missing Dependencies
If you encounter missing library errors, install the corresponding development packages.

#### Build Failures
- Check `mozilla/build.log` for detailed error information
- Try `python3 build.py distclean` and rebuild
- Ensure you have enough disk space (20GB+ recommended)

#### Firefox 140 ESR Specific Issues
- **WebExtensions**: Legacy add-on APIs have been replaced
- **XUL Changes**: Some XUL elements may need updates
- **Security**: Modern security requirements may need adjustments

## Modern Build System Features

### Environment Variables
- `MOZCONFIG`: Path to Mozilla configuration file
- `MOZ_OBJDIR`: Mozilla object directory
- `PYTHON`: Python interpreter to use (should be python3)
- `CC`/`CXX`: Compiler selection

### Build Optimization
```bash
# Use multiple cores for faster builds
export MAKEFLAGS="-j$(nproc)"

# Use ccache for faster recompilation
export USE_CCACHE=1
```

### Cross-Platform Builds
The modern build system supports cross-compilation:
```bash
# For 32-bit builds on 64-bit systems
python3 build.py configure --target=i686-pc-linux-gnu
```

## Migration from Legacy Builds

### Key Changes
1. **Python 3**: All build scripts now use Python 3
2. **Firefox 140 ESR**: Updated from Firefox 35
3. **Modern Toolchain**: Uses recent compilers and build tools
4. **Container Support**: Ready for Docker/Kubernetes builds

### Backward Compatibility
The build system maintains compatibility with:
- Legacy build configurations
- Existing patch infrastructure
- Komodo extension system

## Advanced Configuration

### Custom Mozilla Configuration
Create a `.mozconfig` file:
```bash
# Enable additional features
ac_add_options --enable-application=komodo
ac_add_options --enable-extensions=default
ac_add_options --enable-debug

# Optimization flags
ac_add_options --enable-optimize="-O2"
ac_add_options --enable-strip

# Disable unnecessary components
ac_add_options --disable-tests
ac_add_options --disable-updater
```

### Build Profiles
```bash
# Development build (faster, less optimization)
python3 build.py configure -k 14.10 --debug

# Production build (optimized, stripped)
python3 build.py configure -k 14.0 --release --with-crashreport-symbols
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Komodo CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
    - uses: actions/checkout@v3
    
    - name: Install dependencies
      run: sudo apt-get update && sudo apt-get install -y build-essential python3 autoconf2.13
    
    - name: Build Mozilla
      run: |
        cd mozilla
        python3 build.py configure -k 14.10 --moz-src=14000:FIREFOX_140_0_RELEASE
        python3 build.py distclean all
    
    - name: Build Komodo
      run: |
        export PATH=$(pwd)/util/black:$PATH
        bk configure -V 14.10.0-devel
        bk build
```

## Support

For build issues, check:
- [Komodo Build Documentation](docs/BUILD.txt)
- [Firefox Build Documentation](https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Build_Instructions)
- [GitHub Issues](https://github.com/ActiveState/OpenKomodoIDE/issues)

## Appendix: Legacy vs Modern Build Comparison

| Feature | Legacy (Firefox 35) | Modern (Firefox 140 ESR) |
|---------|---------------------|--------------------------|
| Python | 2.7 | 3.8+ |
| Firefox | 35.0 | 140.0 ESR |
| Build System | Make | Make + Cargo (Rust) |
| Toolchain | GCC 4.x | GCC 10+ / Clang 12+ |
| Platform Support | Older distros | Ubuntu 22.04+, Fedora 36+ |
| Security | Legacy APIs | Modern security standards |
| Performance | Basic | Optimized with Rust components |

This guide provides a comprehensive approach to building OpenKomodoIDE on modern systems while maintaining compatibility with the existing codebase and build infrastructure.