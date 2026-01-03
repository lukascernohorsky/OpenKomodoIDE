# OpenKomodoIDE Developer Guide - Firefox 140 ESR Patches

This guide provides comprehensive information for developers working with OpenKomodoIDE Firefox 140 ESR patches.

## Table of Contents

1. [Introduction](#introduction)
2. [Patch Architecture](#patch-architecture)
3. [Development Workflow](#development-workflow)
4. [Patch Creation Guide](#patch-creation-guide)
5. [Testing and Validation](#testing-and-validation)
6. [Debugging](#debugging)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Introduction

This guide covers the development and maintenance of Firefox 140 ESR patches for OpenKomodoIDE. The patch system enables Komodo to work with modern Firefox versions while maintaining compatibility with existing functionality.

## Patch Architecture

### Patch Organization

```
mozilla/patches-new/mozilla-140.0/
├── __patchinfo__.py          # Patch management (core)
├── README.md                 # Documentation
├── upstream/                 # Core functionality patches
├── gtk/                      # Linux-specific patches
├── cocoa/                    # macOS-specific patches
├── windows/                  # Windows-specific patches
└── arm64/                    # ARM64 architecture patches
```

### Patch Types

1. **Core Patches**: Essential functionality (always applied)
2. **Platform Patches**: OS-specific integrations (platform-dependent)
3. **Architecture Patches**: CPU-specific optimizations (architecture-dependent)

### Patch Management System

The `__patchinfo__.py` file contains:

```python
def applicable(config):
    """Determine if patches apply to this configuration"""
    return config.mozVer == 140.0 and config.patch_target == "mozilla"

def patch_args(config):
    """Return patch command arguments"""
    return ['-p1']

def get_patches(config):
    """Return list of patches for current configuration"""
    patches = [
        # Core patches
        'upstream/komodo_integration.patch',
        'upstream/pyxpcom_integration.patch',
        'upstream/webextensions_integration.patch',
    ]
    
    # Platform-specific patches
    if config.platform.startswith('linux'):
        patches.append('gtk/gtk_integration.patch')
    elif config.platform == 'darwin':
        patches.append('cocoa/cocoa_integration.patch')
    elif config.platform == 'win32':
        patches.append('windows/windows_integration.patch')
    
    # Architecture-specific patches
    if config.arch == 'arm64':
        patches.append('arm64/arm64_optimization.patch')
    
    return patches
```

## Development Workflow

### 1. Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/ActiveState/OpenKomodoIDE.git
cd OpenKomodoIDE

# Install dependencies
pip3 install -r requirements.txt

# Set up build environment
./setup-build-environment.sh
```

### 2. Creating New Patches

```bash
# Create a new patch file
cd mozilla/patches-new/mozilla-140.0/
mkdir -p new_feature
touch new_feature/new_feature.patch

# Edit the patch file with your changes
# Use unified diff format
```

### 3. Testing Patches

```bash
# Run structure validation
python3 test_patch_format.py

# Run integration tests
python3 test_patch_integration.py

# Test patch selection
python3 test_get_patches.py
```

### 4. Applying Patches

```bash
# Apply patches through build system
python3 build.py patch

# Or apply manually
for patch in $(python3 get_patches_for_platform.py); do
    patch -p1 --dry-run < "$patch"  # Test first
    patch -p1 < "$patch"            # Apply
 done
```

## Patch Creation Guide

### Unified Diff Format

All patches must use the standard unified diff format:

```diff
--- original_file.cpp.orig	2024-01-01 00:00:00.000000000 +0000
+++ original_file.cpp	2024-01-01 00:00:00.000000000 +0000
@@ -25,6 +25,10 @@
 #include "existing_header.h"
 
+#ifdef MOZ_KOMODO
+#include "komodo/NewFeature.h"
+#endif
+
 #include "another_header.h"
```

### Creating Patches from Source

```bash
# Make your changes to the source files
# Then create a patch
cd /path/to/firefox/source
diff -u original_file.cpp modified_file.cpp > /path/to/patch.patch
```

### Patch File Structure

```patch
--- original_file.ext.orig	YYYY-MM-DD HH:MM:SS.MICROSECONDS +TIMEZONE
+++ original_file.ext	YYYY-MM-DD HH:MM:SS.MICROSECONDS +TIMEZONE
@@ -line,count +line,count @@
- removed line
+ added line
  unchanged line
```

### Best Practices for Patch Creation

1. **One Feature per Patch**: Keep patches focused on single features
2. **Clear Descriptions**: Add comments explaining the purpose
3. **Minimal Changes**: Only modify what's necessary
4. **Consistent Style**: Follow existing code style
5. **Proper Flags**: Use appropriate #ifdef MOZ_KOMODO guards

## Testing and Validation

### Automated Testing

#### Structure Validation

```bash
python3 simple_patch_test.py
```

Tests:
- Valid header format (---)
- Valid target format (+++)
- Presence of diff chunks (@@)
- Valid diff line prefixes (+, -, , \\)

#### Integration Testing

```bash
python3 test_patch_integration.py
```

Tests:
- Patch file readability
- Python syntax validation
- Function existence (get_patches)

#### Platform Testing

```bash
python3 test_get_patches.py
```

Tests:
- Linux platform patch selection
- macOS platform patch selection
- Windows platform patch selection
- ARM64 architecture detection

### Manual Testing

```bash
# Test patch application
patch -p1 --dry-run < patchfile.patch

# Check for conflicts
patch -p1 --dry-run -v < patchfile.patch

# Apply with fuzz if needed
patch -p1 --fuzz=3 < patchfile.patch
```

### Validation Checklist

- [ ] Patch has correct unified diff format
- [ ] All modified files exist in target Firefox version
- [ ] Patch applies without conflicts (or with acceptable fuzz)
- [ ] Build system recognizes the patch
- [ ] Configuration flags are properly set
- [ ] No syntax errors in modified code
- [ ] Integration with existing functionality works

## Debugging

### Common Patch Issues

#### 1. Patch Format Errors

**Symptom**: `patch: **** malformed patch at line X`

**Solution**:
```bash
# Check line X in the patch file
# Ensure proper diff format
# Use diff -u to generate correct format
```

#### 2. File Not Found

**Symptom**: `can't find file to patch`

**Solution**:
```bash
# Verify file path in patch matches Firefox source
# Check -p (strip) level
# Ensure you're in correct directory
```

#### 3. Fuzz Issues

**Symptom**: `patch: **** Only garbage was found in the patch input.`

**Solution**:
```bash
# Try with fuzz factor
patch -p1 --fuzz=3 < patch.patch

# Or manually edit the patch to match current source
```

#### 4. Rejected Hunks

**Symptom**: `Hunk #X FAILED`

**Solution**:
```bash
# Check what changed in the target file
# Update the patch to match current source
# Or apply manually and resolve conflicts
```

### Debugging Tools

```bash
# Check patch syntax
patch --dry-run -v < patch.patch

# See what would be changed
patch --dry-run --verbose < patch.patch

# Apply with detailed output
patch -v < patch.patch

# Check applied patches
grep -r "MOZ_KOMODO" .
```

## Best Practices

### Patch Organization

1. **Logical Grouping**: Group related changes together
2. **Platform Separation**: Keep platform-specific code separate
3. **Clear Naming**: Use descriptive patch names
4. **Consistent Structure**: Follow existing patch organization

### Code Integration

1. **Feature Flags**: Use MOZ_KOMODO guards appropriately
2. **Minimal Impact**: Avoid unnecessary changes to core Firefox
3. **Backward Compatibility**: Maintain compatibility where possible
4. **Error Handling**: Add proper error handling for Komodo features

### Documentation

1. **Inline Comments**: Explain complex changes in patches
2. **Header Information**: Include purpose and status in patch files
3. **README Updates**: Keep documentation current
4. **Change Logs**: Document significant changes

### Version Control

1. **Commit Messages**: Use clear, descriptive commit messages
2. **Atomic Commits**: One feature per commit
3. **Branch Strategy**: Use feature branches for development
4. **Tag Releases**: Tag stable patch versions

## Troubleshooting

### Build System Issues

**Problem**: Patches not being applied during build

**Solutions**:
1. Check `patchesDirs` configuration in build.py
2. Verify `__patchinfo__.py` syntax
3. Ensure `applicable()` returns True for your configuration
4. Check build logs for patch application errors

### Configuration Problems

**Problem**: MOZ_KOMODO flags not being set

**Solutions**:
1. Verify `--enable-komodo` is passed to configure
2. Check moz.configure for proper flag handling
3. Ensure confvars.sh is properly modified
4. Verify build system includes Komodo sources

### Runtime Issues

**Problem**: Komodo features not working after patching

**Solutions**:
1. Check that patches were actually applied
2. Verify configuration flags in build
3. Ensure all required patches are applied
4. Check for missing dependencies or libraries

### Cross-Platform Issues

**Problem**: Patches work on one platform but not others

**Solutions**:
1. Verify platform-specific patches are applied
2. Check for platform-specific code paths
3. Ensure architecture-specific patches are included
4. Test on all target platforms

## Advanced Topics

### Creating Complex Patches

For patches that modify multiple files:

```bash
# Create a comprehensive patch
diff -urN original_source/ modified_source/ > comprehensive.patch

# Split into logical patches
csplit comprehensive.patch '/^--- /' '{*}'
```

### Patch Conflict Resolution

```bash
# When patches conflict
patch -p1 < patch1.patch
# Manually resolve conflicts
patch -p1 < patch2.patch

# Or use 3-way merge tools
merge original modified patch
```

### Custom Patch Application

```python
# Custom patch application logic
def apply_patches_custom():
    import subprocess
    import os
    
    patches_dir = "mozilla/patches-new/mozilla-140.0"
    
    # Get patches for current platform
    patches = get_patches_for_current_platform()
    
    # Apply with custom logic
    for patch in patches:
        patch_path = os.path.join(patches_dir, patch)
        
        # Pre-application checks
        if not pre_apply_check(patch_path):
            continue
        
        # Apply patch
        result = subprocess.run([
            'patch', '-p1', '--fuzz=2', 
            '--input', patch_path
        ], capture_output=True, text=True)
        
        # Post-application verification
        if result.returncode != 0:
            handle_patch_failure(patch, result)
        else:
            log_successful_patch(patch)
```

## Resources

### Documentation

- [Firefox 140 ESR Release Notes](https://www.mozilla.org/en-US/firefox/140.0/releasenotes/)
- [Mozilla Build System Documentation](https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Build_Instructions)
- [Unified Diff Format Specification](https://www.gnu.org/software/diffutils/manual/html_node/Unified-Format.html)

### Tools

- [GNU Patch](https://www.gnu.org/software/patch/)
- [Diffutils](https://www.gnu.org/software/diffutils/)
- [Mercurial](https://www.mercurial-scm.org/) (for Mozilla source)

### Community

- [Komodo IDE Forums](http://community.komodoide.com/)
- [Mozilla Developer Network](https://developer.mozilla.org/)
- [GitHub Issues](https://github.com/ActiveState/OpenKomodoIDE/issues)

---

**Last Updated**: 2025-12-25
**Version**: 1.0
**Status**: Complete and ready for development use