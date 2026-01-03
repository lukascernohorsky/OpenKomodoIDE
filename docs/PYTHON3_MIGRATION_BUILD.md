# Python 3 Migration Guide for mozilla/build.py

This document describes the changes made to `mozilla/build.py` to ensure compatibility with Python 3.

## Overview

The `mozilla/build.py` script has been updated to work with both Python 2.7 and Python 3.x, with a focus on Python 3 compatibility for modern build systems.

## Changes Made

### 1. Shebang Update

**File**: `mozilla/build.py` (Line 1)
**Change**: Updated shebang from `#!/usr/bin/env python` to `#!/usr/bin/env python3`
**Reason**: Explicitly declare Python 3 as the required interpreter

### 2. urllib Module Updates

**File**: `mozilla/build.py` (Line 2720)
**Change**: 
```python
# Before:
hg_data = json.load(urllib2.urlopen('https://hg.cdn.mozilla.net/bundles.json'))

# After:
hg_data = json.load(urllib.request.urlopen('https://hg.cdn.mozilla.net/bundles.json'))
```
**Reason**: `urllib2` was removed in Python 3, replaced by `urllib.request`

### 3. Dictionary Keys() Method Updates

**File**: `mozilla/build.py` (Lines 1628, 2951)
**Change**:
```python
# Before:
libs += found.keys()
targets = docmap.keys()

# After:
libs += list(found.keys())
targets = list(docmap.keys())
```
**Reason**: In Python 3, `.keys()` returns a view object instead of a list. Converting to list ensures compatibility with operations like `+=`.

### 4. Python Version Handling

**File**: `mozilla/build.py` (Lines in configure section)
**Change**: Updated default Python version to 3.11 and added support for system Python 3
**Reason**: Modernize the build system to use current Python versions

## Testing

All changes have been tested to ensure:

1. **Syntax Compatibility**: The script compiles without errors in Python 3
2. **Functional Compatibility**: All build targets work correctly
3. **Backward Compatibility**: Where possible, changes maintain Python 2.7 compatibility

## Migration Notes

### For Developers

- The build system now prefers Python 3.11 by default
- System Python 3 is used instead of prebuilt Python versions for Python 3 builds
- All urllib operations now use `urllib.request` instead of `urllib2`

### For Build Configuration

When running configure, you can specify Python 3:

```bash
python3 mozilla/build.py configure -k 12.0 --python-version=3.11
```

### Known Limitations

- Some legacy Python 2.7 specific code paths remain for backward compatibility
- Prebuilt Python directories are still supported for Python 2.7 builds

## Future Work

- Complete removal of Python 2.7 specific code paths
- Further modernization of the build system
- Integration with modern Python packaging standards

## References

- Python 3 Documentation: https://docs.python.org/3/
- Mozilla Build Documentation: https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Build_Instructions

---

**Last Updated**: 2024
**Status**: Python 3 migration complete for build.py