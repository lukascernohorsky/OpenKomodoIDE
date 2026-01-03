# OpenKomodoIDE Build System

This document describes how to build OpenKomodoIDE from source.

## Prerequisites

### Required Tools
- **Python 3.7+** - Required for build automation
- **Git** - For source control operations
- **GCC/G++** (Linux/macOS) or **Visual Studio** (Windows) - C/C++ compiler
- **Make** - Build tool
- **Node.js 14+** - For JavaScript components
- **npm 6+** - Node package manager

### Platform-Specific Requirements

#### Linux
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip git make gcc g++ libgtk-3-dev libffi-dev libsqlite3-dev libicu-dev
```

#### macOS
```bash
brew install python3 git make gcc
```

#### Windows
- Install Visual Studio with C++ development tools
- Install Git for Windows
- Install Python 3 from python.org

## Build Process

### Quick Start

1. **Configure the build:**
   ```bash
   python3 build.py configure
   ```

2. **Build the project:**
   ```bash
   python3 build.py build
   ```

3. **Complete build (configure + build + package):**
   ```bash
   python3 build.py complete
   ```

### Build Options

| Command | Description |
|---------|-------------|
| `python3 build.py configure` | Configure the build environment |
| `python3 build.py build` | Build the project |
| `python3 build.py complete` | Full build process (configure + build + package) |
| `python3 build.py clean` | Clean build artifacts |
| `python3 build.py test` | Run build tests |
| `python3 build.py status` | Show build configuration status |

### Advanced Options

```bash
# Debug build
python3 build.py build --debug

# Specific targets
python3 build.py build --targets faster

# Clean build
python3 build.py build --clean

# Custom version
python3 build.py build --version 12.1 --firefox 140.1

# Parallel jobs
python3 build.py build --jobs 8
```

## Build Configuration

The build system uses `build_config.json` for configuration. You can edit this file directly or override settings via command line arguments.

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `platform` | Auto-detected | Target platform (linux, macos, windows) |
| `version` | 12.0 | Komodo version |
| `firefox_version` | 140.0 | Firefox ESR version |
| `build_type` | release | Build type (release/debug) |
| `jobs` | CPU cores - 2 | Number of parallel build jobs |
| `enable_debug` | false | Enable debug symbols |
| `enable_symbols` | true | Enable crash report symbols |
| `targets` | ['all'] | Build targets |
| `clean_build` | false | Clean before build |
| `verbose` | false | Verbose output |

## Mozilla Build Configuration

The `mozconfig` file contains Firefox-specific build options. Key options include:

- **Application branding and versioning**
- **Platform-specific build targets**
- **Feature enables/disables**
- **Optimization settings**
- **Debug/release configuration**

## Build Artifacts

After a successful build, artifacts are located in:

- `build/` - Build directory
- `dist/` - Distribution packages
- `logs/` - Build logs

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Ensure all required tools are installed
2. **Permission issues**: Run with appropriate permissions
3. **Firefox mach not found**: Verify Firefox source is properly integrated
4. **Build configuration errors**: Check `mozconfig` for syntax errors

### Debugging

```bash
# Verbose build
python3 build.py build --verbose

# Check build status
python3 build.py status

# Run tests
python3 test_build.py
```

## Development Builds

For development, you can use faster build options:

```bash
# Faster build (skips some optimizations)
python3 build.py build --targets faster

# Debug build with symbols
python3 build.py build --debug --symbols
```

## Cross-Platform Builds

The build system supports cross-platform builds:

```bash
# Build for Linux ARM64
python3 build.py build --platform linux-arm64

# Build for macOS
python3 build.py build --platform macos

# Build for Windows
python3 build.py build --platform windows
```

## Continuous Integration

For CI environments, use the complete build command:

```bash
python3 build.py complete --clean --verbose
```

This will perform a clean build with verbose output and create distribution packages.

## Support

For build-related issues, please open an issue on the GitHub repository with:
- Your operating system and version
- Build configuration details
- Error messages and logs
- Steps to reproduce the issue