# Firefox 140 ESR Patches for Komodo

This directory contains patches for Firefox 140 ESR (Extended Support Release) to make it compatible with Komodo IDE.

## Status

This is a work in progress. The following needs to be done:

### 1. Platform-Specific Patches
- **Cocoa (macOS)**: Need to port patches from Firefox 35 to work with modern macOS APIs
- **Windows**: Need to update Windows-specific patches for modern Windows versions
- **GTK (Linux)**: Need to update GTK patches for modern GTK versions

### 2. Core Functionality Patches
- **PyXPCOM Integration**: Update Python-XPCOM bridge for modern Firefox
- **Plugin System**: Modernize plugin loading and compatibility
- **Debugging Support**: Update debugging protocols and interfaces
- **XUL/JS Compatibility**: Ensure XUL and JavaScript compatibility layers work

### 3. API Changes
Firefox 140 ESR has significant API changes from Firefox 35:
- **WebExtensions**: Replace legacy add-on APIs with WebExtensions
- **XUL Deprecation**: Handle deprecated XUL elements and replace with modern alternatives
- **Security Changes**: Update for modern web security requirements
- **Performance APIs**: Update performance monitoring and profiling

### 4. Build System Updates
- Update build configuration for modern Firefox build system
- Handle new compiler requirements and toolchain updates
- Update dependency management for modern libraries

## Migration Strategy

1. **Incremental Porting**: Start with core functionality and gradually add platform-specific features
2. **Feature Flags**: Maintain backward compatibility during transition
3. **Testing**: Comprehensive testing of each component before integration
4. **Documentation**: Document all changes and API differences

## Patch Application Guide

### Using the Build System

The recommended way to apply patches is through the build system:

```bash
# Configure the build with Komodo support
python3 build.py configure -k 14.10 --moz-src=14000:FIREFOX_140_0_RELEASE --enable-komodo

# Apply patches automatically
python3 build.py patch
```

### Manual Patch Application

For manual patch application:

```bash
# Navigate to Firefox source directory
cd /path/to/firefox/source

# Apply patches based on your platform
python3 -c "
from patchinfo import get_patches
from types import SimpleNamespace

# Configure for your platform
config = SimpleNamespace()
config.platform = 'linux'  # or 'darwin', 'win32'
config.arch = 'x86_64'    # or 'arm64'

# Get list of patches to apply
patches = get_patches(config)
for patch in patches:
    print(f'Appling {patch}...')
    # patch -p1 < /path/to/patches/{patch}
"
```

### Platform-Specific Patches

| Platform | Patches Applied |
|----------|-----------------|
| Linux (x86_64) | 4 patches |
| Linux (ARM64) | 5 patches |
| macOS (x86_64) | 4 patches |
| macOS (ARM64) | 5 patches |
| Windows | 4 patches |

### Patch Verification

To verify patches were applied correctly:

```bash
# Check for Komodo configuration
grep -r "MOZ_KOMODO" browser/confvars.sh

# Check for Komodo integration in source
grep -r "KomodoIntegration" browser/app/

# Check build configuration
grep -r "MOZ_KOMODO" toolkit/moz.configure
```

## Resources

- [Firefox 140 ESR Release Notes](https://www.mozilla.org/en-US/firefox/140.0/releasenotes/)
- [Firefox 140 Developer Documentation](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/140)
- [WebExtensions API Reference](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions)

## Current State

- ✅ Directory structure created
- ✅ Patch info files created for all platforms
- ✅ Version mapping updated in build system
- ✅ Core integration patches created:
  - `komodo_integration.patch` - Main Komodo integration
  - `pyxpcom_integration.patch` - PyXPCOM support for Firefox 140 ESR
  - `webextensions_integration.patch` - WebExtensions integration
- ✅ Platform-specific patches created:
  - `gtk/gtk_integration.patch` - Linux GTK integration
  - `cocoa/cocoa_integration.patch` - macOS Cocoa integration
  - `windows/windows_integration.patch` - Windows integration
  - `arm64/arm64_optimization.patch` - ARM64 optimizations
- ❌ Testing infrastructure needs to be updated
- ❌ Documentation needs to be completed
- ⚠️  Patches need testing and validation