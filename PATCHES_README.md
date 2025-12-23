# Firefox 140 ESR Patches for OpenKomodoIDE

This document describes the patch system for Firefox 140 ESR integration with OpenKomodoIDE.

## Table of Contents

1. [Patch System Overview](#patch-system-overview)
2. [Patch Structure](#patch-structure)
3. [Creating New Patches](#creating-new-patches)
4. [Patch Categories](#patch-categories)
5. [Platform-Specific Patches](#platform-specific-patches)
6. [Testing Patches](#testing-patches)
7. [Patch Maintenance](#patch-maintenance)

## Patch System Overview

The patch system allows OpenKomodoIDE to integrate with Firefox 140 ESR by applying modifications to the Mozilla source code. Patches are organized by:

- **Version**: Firefox 140.0 ESR
- **Platform**: Windows, macOS (Cocoa), Linux (GTK), ARM64, BSD variants
- **Component**: Core, PyXPCOM, UI, Debugging, etc.

## Patch Structure

```
mozilla/patches-new/mozilla-140.0/
├── __patchinfo__.py          # Main patch info for Firefox 140.0
├── upstream/                 # Upstream Mozilla patches
│   ├── __patchinfo__.py
│   └── *.patch
├── windows/                  # Windows-specific patches
│   ├── __patchinfo__.py
│   └── *.patch
├── cocoa/                    # macOS-specific patches
│   ├── __patchinfo__.py
│   └── *.patch
├── gtk/                      # Linux GTK patches
│   ├── __patchinfo__.py
│   └── *.patch
├── arm64/                    # ARM64-specific patches
│   ├── __patchinfo__.py
│   └── *.patch
├── freebsd/                  # FreeBSD patches
│   ├── __patchinfo__.py
│   └── *.patch
├── netbsd/                   # NetBSD patches
│   ├── __patchinfo__.py
│   └── *.patch
├── openbsd/                  # OpenBSD patches
│   ├── __patchinfo__.py
│   └── *.patch
├── gentoo/                   # Gentoo patches
│   ├── __patchinfo__.py
│   └── *.patch
└── minix3/                   # Minix3 patches
    ├── __patchinfo__.py
    └── *.patch
```

## Creating New Patches

### Step 1: Identify the Change

Determine what needs to be modified in Firefox 140 ESR:

```bash
# Find the relevant source files
find mozilla-source -name "*.cpp" -o -name "*.h" -o -name "*.js" | grep -i "your_feature"
```

### Step 2: Create the Patch

Use `git diff` to create a patch:

```bash
# Make your changes to the source files
# Then create a patch
cd mozilla-source
git diff > ../mozilla/patches-new/mozilla-140.0/upstream/your_feature.patch
```

### Step 3: Add Patch Information

Edit the appropriate `__patchinfo__.py` file:

```python
def applicable(config):
    return (config.mozVer == 140.0 and 
            config.patch_target == "mozilla" and 
            # Add any platform-specific conditions here
            True)

def patch_args(config):
    return ['-p1']
```

### Step 4: Test the Patch

```bash
# Apply the patch manually for testing
cd mozilla-source
patch -p1 < ../mozilla/patches-new/mozilla-140.0/upstream/your_feature.patch

# Test the build
python3 ../mozilla/build.py mozilla
```

## Patch Categories

### 1. Upstream Patches

Patches that apply to all platforms:

- **Core Integration**: Komodo core integration with Firefox
- **API Compatibility**: Ensure API compatibility between versions
- **Debugging Support**: Debugging protocol enhancements
- **Security**: Security-related modifications

### 2. Platform-Specific Patches

Patches that apply to specific platforms:

- **Windows**: Windows API integration, registry access
- **Cocoa**: macOS-specific UI and API integration
- **GTK**: Linux GTK integration
- **ARM64**: ARM64-specific optimizations and fixes
- **BSD**: BSD compatibility layers

### 3. Component-Specific Patches

- **PyXPCOM**: Python-XPCOM bridge modifications
- **XUL**: XUL runner and UI modifications
- **WebExtensions**: WebExtensions API enhancements
- **Networking**: Network stack modifications

## Platform-Specific Patches

### Windows Patches

Common Windows-specific modifications:

- Registry access for Komodo settings
- Windows-specific file system integration
- COM object integration
- Windows event handling

### Cocoa (macOS) Patches

macOS-specific modifications:

- Native menu integration
- macOS accessibility features
- Sandboxing and security
- Native file dialogs

### GTK (Linux) Patches

Linux GTK-specific modifications:

- GTK theme integration
- Wayland/X11 compatibility
- Linux accessibility features
- Native file dialogs

### ARM64 Patches

ARM64-specific optimizations:

- CPU-specific optimizations
- Memory alignment fixes
- ARM64 assembly optimizations
- Performance tuning

### BSD Patches

BSD compatibility patches:

- BSD-specific system calls
- BSD threading model
- BSD networking stack
- BSD file system integration

## Testing Patches

### Unit Testing

```bash
# Run unit tests for patched components
python3 test_patches.py --platform linux --firefox 140.0
```

### Integration Testing

```bash
# Test the complete build with patches
python3 build_automation.py complete
```

### Regression Testing

```bash
# Run regression tests
python3 test_regression.py --firefox 140.0
```

## Patch Maintenance

### Updating Patches

When Firefox 140 ESR is updated:

1. Check for upstream changes that affect your patches
2. Update patch files to work with new source
3. Test all patches thoroughly
4. Update documentation

### Adding New Platform Support

To add support for a new platform:

1. Create a new directory under `mozilla-140.0/`
2. Add a `__patchinfo__.py` file
3. Create platform-specific patches
4. Update the build system to recognize the new platform
5. Test the new platform support

### Deprecating Patches

When patches are no longer needed:

1. Mark them as deprecated in the patch info
2. Add comments explaining why they're deprecated
3. Keep them for one release cycle
4. Remove in the next major version

## Example Patch Files

### Example 1: Simple API Patch

```diff
--- a/browser/components/nsBrowserGlue.js
+++ b/browser/components/nsBrowserGlue.js
@@ -123,6 +123,10 @@
   
   // Komodo integration
   if (AppConstants.MOZ_KOMODO) {
+    // Firefox 140 ESR specific
+    Services.obs.addObserver(this, "komodo-ready");
+    this._komodoInit();
   }
   
   // Original code continues...
```

### Example 2: Platform-Specific Patch

```diff
--- a/widget/cocoa/nsNativeThemeCocoa.mm
+++ b/widget/cocoa/nsNativeThemeCocoa.mm
@@ -456,7 +456,11 @@
   
   // Komodo macOS integration
   if (IsKomodoEnabled()) {
+    // Firefox 140 ESR macOS specific
+    if (@available(macOS 12.0, *)) {
+      return DrawModernWidget(aWidgetType, aFrame, aContext, aRect, aState);
+    }
     return DrawLegacyWidget(aWidgetType, aFrame, aContext, aRect, aState);
   }
   
   // Original code...
```

## Patch Best Practices

1. **Keep patches minimal**: Only change what's necessary
2. **Document changes**: Add comments explaining why changes were made
3. **Test thoroughly**: Each patch should be tested in isolation
4. **Follow upstream**: Try to follow Mozilla's coding standards
5. **Update regularly**: Keep patches compatible with upstream changes
6. **Organize logically**: Group related patches together

## Patch Review Process

1. **Code Review**: All patches must be reviewed before inclusion
2. **Testing**: Patches must pass all tests
3. **Documentation**: Patches must be documented
4. **Sign-off**: Patches must be signed off by a maintainer

## Resources

- [Mozilla Patch Guidelines](https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/How_to_Submit_a_Patch)
- [Firefox 140 ESR Documentation](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/140)
- [Komodo Patch System Documentation](https://github.com/your-repo/OpenKomodoIDE/wiki/Patch-System)

## Current Status

### Completed Patches

- [ ] Core integration patches
- [ ] PyXPCOM bridge patches
- [ ] Windows-specific patches
- [ ] macOS (Cocoa) patches
- [ ] Linux (GTK) patches
- [ ] ARM64 patches
- [ ] BSD patches
- [ ] Debugging support patches
- [ ] WebExtensions patches

### Patch Statistics

- **Total patches needed**: ~150
- **Patches completed**: 0 (infrastructure ready)
- **Patches in progress**: 0
- **Patches to port from Firefox 35**: ~100
- **New patches for Firefox 140**: ~50

## Migration Strategy

### Phase 1: Infrastructure (COMPLETED)

- [x] Create patch directory structure
- [x] Set up patch info files
- [x] Integrate with build system
- [x] Create test framework

### Phase 2: Core Patches (IN PROGRESS)

- [ ] Port core integration patches from Firefox 35
- [ ] Update for Firefox 140 ESR API changes
- [ ] Test core functionality

### Phase 3: Platform Patches

- [ ] Port Windows patches
- [ ] Port macOS patches
- [ ] Port Linux patches
- [ ] Create ARM64 patches
- [ ] Create BSD patches

### Phase 4: Component Patches

- [ ] PyXPCOM integration
- [ ] Debugging support
- [ ] WebExtensions
- [ ] UI integration

### Phase 5: Testing and Optimization

- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance optimization
- [ ] Documentation

## Contributing

To contribute patches:

1. Fork the repository
2. Create a feature branch
3. Add your patches
4. Update documentation
5. Submit a pull request

## License

All patches are provided under the same license as OpenKomodoIDE.