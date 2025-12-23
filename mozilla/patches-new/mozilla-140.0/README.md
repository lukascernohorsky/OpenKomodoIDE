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

## Resources

- [Firefox 140 ESR Release Notes](https://www.mozilla.org/en-US/firefox/140.0/releasenotes/)
- [Firefox 140 Developer Documentation](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/140)
- [WebExtensions API Reference](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions)

## Current State

- ✅ Directory structure created
- ✅ Patch info files created for all platforms
- ✅ Version mapping updated in build system
- ❌ Actual patches need to be ported/created
- ❌ Testing infrastructure needs to be updated
- ❌ Documentation needs to be completed