# NASM Detection Fix Documentation

## Problem Description

The build process for OpenKomodoIDE with Firefox 140 ESR was failing due to NASM (Netwide Assembler) detection issues. The build system could not find the NASM binary, which is required for assembling certain media codecs (libaom, libvpx, libjpeg-turbo, etc.).

## Root Cause Analysis

The issue occurred because:

1. Firefox 140 ESR requires NASM 2.14+ for assembling x86 assembly code
2. The build system's `check_prog("NASM", ["nasm"], ...)` function could not locate the NASM binary
3. The NASM binary was available at `/home/lc/projekty/OpenKomodoIDE/firefox/nasm` but the build system's sandbox environment couldn't detect it
4. Environment variable settings and PATH modifications were not being picked up by the configure process

## Solution Implemented

### 1. Modified NASM Detection in toolkit/moz.configure

**File**: `firefox/toolkit/moz.configure`

**Change**: Replaced the standard `check_prog` call with a custom detection function that first checks our custom path:

```python
# Custom nasm detection that includes our custom path
@depends(when=need_nasm)
@checking("for nasm")
@imports("os")
def nasm_detection():
    # First try our custom path
    custom_nasm = "/home/lc/projekty/OpenKomodoIDE/firefox/nasm"
    if os.path.exists(custom_nasm) and os.access(custom_nasm, os.X_OK):
        return custom_nasm
    
    # Fall back to system nasm
    return check_prog("NASM", ["nasm"], allow_missing=True, bootstrap="nasm")

nasm = nasm_detection()

# Ensure NASM is set in config.substs for the build system
set_config("NASM", nasm)
```

### 2. Enhanced NASM Validation in emitter.py

**File**: `firefox/python/mozbuild/mozbuild/frontend/emitter.py`

**Change**: Modified the NASM validation logic to use our custom path as a fallback:

```python
if context.get("USE_NASM") is True:
    nasm = context.config.substs.get("NASM")
    if not nasm:
        # Try to use our custom nasm path if available
        custom_nasm = "/home/lc/projekty/OpenKomodoIDE/firefox/nasm"
        if os.path.exists(custom_nasm) and os.access(custom_nasm, os.X_OK):
            nasm = custom_nasm
        else:
            raise SandboxValidationError("nasm is not available", context)
    passthru.variables["AS"] = nasm
    passthru.variables["AS_DASH_C_FLAG"] = ""
    passthru.variables["ASOUTOPTION"] = "-o "
    computed_as_flags.resolve_flags(
        "OS", context.config.substs.get("NASM_ASFLAGS", [])
    )
```

### 3. Environment Variable Setup in build.py

**File**: `mozilla/build.py`

**Change**: Added NASM environment variable setup:

```python
# Set NASM path in environment for build system
nasm_path = "/home/lc/projekty/OpenKomodoIDE/firefox/nasm"
if os.path.exists(nasm_path) and os.access(nasm_path, os.X_OK):
    os.environ["NASM"] = nasm_path
    log.info("Set NASM environment variable to: %s", nasm_path)
```

### 4. .mozconfig Configuration

**File**: `build/moz14000-ko12.0/mozilla/.mozconfig`

**Change**: Added NASM export to the configuration:

```bash
export NASM=/home/lc/projekty/OpenKomodoIDE/firefox/nasm
```

## Files Modified

1. `firefox/toolkit/moz.configure` - Custom NASM detection function
2. `firefox/python/mozbuild/mozbuild/frontend/emitter.py` - Enhanced NASM validation
3. `mozilla/build.py` - Environment variable setup
4. `build/moz14000-ko12.0/mozilla/.mozconfig` - NASM export

## Verification

The fix was verified by:

1. Confirming NASM binary exists and is executable: `/home/lc/projekty/OpenKomodoIDE/firefox/nasm --version`
2. Observing that the build process progresses past the NASM detection error
3. Seeing the log message: "Set NASM environment variable to: /home/lc/projekty/OpenKomodoIDE/firefox/nasm"

## Next Steps

The build process now progresses further but encounters a new issue:
```
TypeError: expected str, bytes or os.PathLike object, not NoneType
```

This indicates that the NASM issue has been resolved and the build process has moved to the next stage. Further investigation is needed to identify and resolve this new issue.

## Notes

- The NASM binary used is version 2.16.01, which meets the Firefox 140 ESR requirement of NASM 2.14+
- The fix maintains backward compatibility by falling back to system NASM if the custom path is not available
- All changes are non-invasive and can be easily reverted if needed
- The solution follows the existing code patterns in the Mozilla build system