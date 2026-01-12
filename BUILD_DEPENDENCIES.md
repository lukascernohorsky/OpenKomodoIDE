# OpenKomodoIDE Build Dependencies

This document lists all required dependencies for building OpenKomodoIDE with Firefox 140 ESR.

## System Requirements

### Basic Build Tools
- **Python 3.11+** (required for build system)
- **Git** (for source code management)
- **Make** (GNU Make 4.0+)
- **GCC/Clang** (C/C++ compiler)
- **G++/Clang++** (C++ compiler)
- **Zip/Tar** (for archive operations)

### Required Packages (Debian/Ubuntu)

```bash
# Basic build tools
sudo apt-get install build-essential python3 python3-pip git make gcc g++ zip tar

# Firefox build dependencies
sudo apt-get install autoconf2.13 yasm libgtk-3-dev libglib2.0-dev 
                     libdbus-glib-1-dev libxt-dev libx11-dev libxext-dev 
                     libxrender-dev libxcb1-dev libxcb-shm0-dev 
                     libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev

# WASM/WebAssembly support (critical for Firefox 140 ESR)
sudo apt-get install lld-19 wasi-libc clang-19 libclang-rt-19-dev-wasm32

# Additional development tools
sudo apt-get install cmake ninja-build pkg-config libssl-dev 
                     libffi-dev libxml2-dev libxslt1-dev

# Rust toolchain (required for Firefox build)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Node.js (required for some build tools)
sudo apt-get install nodejs npm

# Python virtual environment support
sudo apt-get install python3-venv python3-dev
```

## Firefox 140 ESR Specific Dependencies

### Critical WASM Dependencies
The following packages are **required** for Firefox 140 ESR build:

```bash
# LLVM 19 with WASM support (critical)
sudo apt-get install lld-19 clang-19 libclang-rt-19-dev-wasm32

# WASI libraries
sudo apt-get install wasi-libc
```

### WASM Runtime Libraries
If you encounter the error:
```
wasm-ld-19: error: cannot open /usr/lib/llvm-19/lib/clang/19/lib/wasm32-unknown-wasi/libclang_rt.builtins.a
```

Install the specific WASM runtime libraries:
```bash
sudo apt-get install libclang-rt-19-dev-wasm32
```

### Alternative: Disable WASM Sandboxing
If you cannot install WASM dependencies, you can build without WASM sandboxing:
```bash
./mach configure --without-wasm-sandboxed-libraries
```

## Build Configuration

### Recommended Configuration
```bash
# Configure with all features (requires WASM dependencies)
python3 build.py configure --jobs 2

# Or configure without WASM sandboxing (if dependencies missing)
cd mozilla/build/moz1400-ko1410/mozilla/
./mach configure --without-wasm-sandboxed-libraries
cd ../../../../

# Build with configurable job count (default: 2)
python3 build.py build --jobs 4  # Use 4 jobs instead of default 2
python3 build.py build          # Uses default 2 jobs
```

## Troubleshooting

### Missing WASM Libraries
**Error:**
```
wasm-ld-19: error: cannot open /usr/lib/llvm-19/lib/clang/19/lib/wasm32-unknown-wasi/libclang_rt.builtins.a
```

**Solution:**
```bash
# Install the missing WASM runtime libraries
sudo apt-get install libclang-rt-19-dev-wasm32

# Or build without WASM sandboxing
./mach configure --without-wasm-sandboxed-libraries
```

### Missing Build Tools
**Error:**
```
✗ Missing tools: wget, curl, gcc, g++, make, zip, tar
```

**Solution:**
```bash
sudo apt-get install build-essential wget curl gcc g++ make zip tar
```

### Python Virtual Environment Issues
**Error:**
```
✗ Python virtual environment creation failed
```

**Solution:**
```bash
sudo apt-get install python3-venv python3-dev
python3 -m pip install --upgrade pip virtualenv
```

## Platform-Specific Notes

### Ubuntu/Debian
```bash
# Install all build dependencies
sudo apt-get update
sudo apt-get install build-essential python3 python3-pip git make gcc g++ 
                     autoconf2.13 yasm libgtk-3-dev libglib2.0-dev 
                     libdbus-glib-1-dev libxt-dev libx11-dev libxext-dev 
                     libxrender-dev libxcb1-dev libxcb-shm0-dev 
                     libxcb-render0-dev libxcb-shape0-dev libxcb-xfixes0-dev
                     lld-19 wasi-libc clang-19 libclang-rt-19-dev-wasm32
                     cmake ninja-build pkg-config libssl-dev libffi-dev 
                     libxml2-dev libxslt1-dev nodejs npm python3-venv python3-dev
```

### Fedora/RHEL
```bash
sudo dnf install gcc gcc-c++ make python3 python3-pip git autoconf213 
              yasm gtk3-devel glib2-devel dbus-glib-devel 
              libXt-devel libX11-devel libXext-devel libXrender-devel 
              libxcb-devel lld clang cmake ninja-build pkgconfig 
              openssl-devel libffi-devel libxml2-devel libxslt-devel 
              nodejs npm python3-virtualenv
```

### macOS
```bash
# Install using Homebrew
brew install python@3.11 gcc make autoconf yasm gtk+ glib 
              dbus libxcb cmake ninja pkg-config openssl libffi 
              libxml2 libxslt node llvm@19 wasi-libc
```

## Verification

Check that all dependencies are installed:
```bash
# Check basic tools
gcc --version
g++ --version
make --version
python3 --version
node --version

# Check WASM tools
wasm-ld-19 --version
clang-19 --version

# Check Firefox build tools
./mach --help  # Should work from Firefox source directory
```

## Notes

- The build system uses exactly **2 jobs** as requested
- Path construction uses consistent version formatting (`moz1400-ko1410`)
- Firefox source is automatically downloaded if missing
- Configuration files are automatically generated
- Error messages are clear and actionable