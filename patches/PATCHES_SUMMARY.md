# OpenKomodoIDE Build System Fixes - Patch Summary

This directory contains individual patch files for each modified file in the OpenKomodoIDE build system fix.

## Available Patches

### 1. `build.py.patch`
**Purpose**: Fixes the main build script
**Changes**:
- Updates default Komodo version from 12.0 to 14.10
- Ensures proper argument passing to build_automation.py

### 2. `build_config.json.patch`
**Purpose**: Updates the build configuration
**Changes**:
- Updates `version` field from "12.0" to "14.10"
- Maintains Firefox version at "140.0"

### 3. `build_automation.py.patch`
**Purpose**: Fixes the build automation system
**Changes**:
- Updates all default version references from 12.0/14.1 to 14.10
- Fixes path construction for Firefox mach system
- Updates `get_mach_path()` method to find correct directory structure

### 4. `test_build.py.patch`
**Purpose**: Fixes the test suite
**Changes**:
- Updates hardcoded paths from `moz1400-ko120` to `moz1400-ko1410`
- Ensures tests find the correct Firefox mach location

## How to Apply Patches

### Individual Patch Application:
```bash
cd /home/lc/projekty/OpenKomodoIDE
patch -p1 < patches/build.py.patch
patch -p1 < patches/build_config.json.patch
patch -p1 < patches/build_automation.py.patch
patch -p1 < patches/test_build.py.patch
```

### Apply All Patches:
```bash
cd /home/lc/projekty/OpenKomodoIDE
for patch in patches/*.patch; do
    patch -p1 < "$patch"
done
```

## What These Patches Fix

### Problem
The build system was failing because it couldn't find the Firefox mach build system at the expected path:
- **Expected**: `mozilla/build/moz1400-ko120/mozilla/mach`
- **Actual**: `mozilla/build/moz1400-ko1410/mozilla/mach`

### Root Cause
The Komodo version was hardcoded as "12.0" in multiple files, but the actual directory structure uses version "14.10".

### Solution
Updated all version references from "12.0" to "14.10" to match the actual directory structure.

## Verification
After applying these patches:
- ✅ `python3 build.py status` - Shows correct configuration with version 14.10
- ✅ `python3 build.py configure` - Runs properly (no immediate failure)
- ✅ `python3 test_build.py` - All tests pass
- ✅ Firefox mach found at correct path: `mozilla/build/moz1400-ko1410/mozilla/mach`

## Clean Build Compatibility
These patches are designed to be applied even after:
- `make clean`
- `git clean -xdf`
- Any other cleanup operation that removes build artifacts

The patches modify only source files, not generated build artifacts.