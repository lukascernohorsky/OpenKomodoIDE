# Python 2 to Python 3 Compatibility Fixes for OpenKomodoIDE

This document summarizes all the Python 2 vs 3 compatibility issues that were fixed to enable the build system to run under Python 3.

## Files Modified

### 1. `mozilla/build.py`

#### Issue 1: `str.translate()` method
**Problem**: Python 2's `str.translate(None, "0123456789")` syntax is not supported in Python 3.

**Fix**: Replaced with `str.translate(str.maketrans('', '', '0123456789'))`

**Lines changed**: 2137, 2234

**Before**:
```python
elif git_rev.translate(None, "0123456789") == "":
```

**After**:
```python
elif git_rev.translate(str.maketrans('', '', '0123456789')) == "":
```

#### Issue 2: Missing Linux platform mapping
**Problem**: Python 3 returns `'linux'` for `sys.platform`, but the script only had `'linux2'` mapping.

**Fix**: Added `'linux': os.path.abspath('bin-linux-x86')` to `gPlat2BinDir`

**Lines changed**: 185

**Before**:
```python
gPlat2BinDir = {
    'win32': os.path.abspath('bin-win32'),
    'sunos5': os.path.abspath('bin-solaris-sun'),
    'linux2': os.path.abspath('bin-linux-x86'),
    # ...
}
```

**After**:
```python
gPlat2BinDir = {
    'win32': os.path.abspath('bin-win32'),
    'sunos5': os.path.abspath('bin-solaris-sun'),
    'linux2': os.path.abspath('bin-linux-x86'),
    'linux': os.path.abspath('bin-linux-x86'),
    # ...
}
```

### 2. `util/sh.py`

#### Issue: `string.find()` function
**Problem**: Python 2's `string.find()` function was removed in Python 3. Use string method `str.find()` instead.

**Fix**: Replaced `string.find(src, '*')` with `src.find('*')`

**Lines changed**: 98-100

**Before**:
```python
if string.find(src, '*') != -1 or \
   string.find(src, '?') != -1 or \
   string.find(src, '[') != -1:
```

**After**:
```python
if src.find('*') != -1 or \
   src.find('?') != -1 or \
   src.find('[') != -1:
```

### 3. `util/patchtree.py`

#### Issue 1: `basestring` type
**Problem**: Python 2's `basestring` type was removed in Python 3. Use `str` instead.

**Fix**: Replaced `isinstance(patch, basestring)` with `isinstance(patch, str)`

**Lines changed**: 248, 263, 446

**Before**:
```python
if isinstance(patch, basestring):
    patch = patch.splitlines()
```

**After**:
```python
if isinstance(patch, str):
    patch = patch.splitlines()
```

#### Issue 2: Subprocess stdin encoding
**Problem**: In Python 3, subprocess stdin expects bytes, not strings.

**Fix**: Added encoding of string to bytes before writing to stdin

**Lines changed**: 177-179, 187-189

**Before**:
```python
if stdin is not None:
    p.stdin.write(stdin)
```

**After**:
```python
if stdin is not None:
    if isinstance(stdin, str):
        stdin = stdin.encode('utf-8')
    p.stdin.write(stdin)
```

#### Issue 3: Subprocess stdout decoding
**Problem**: In Python 3, subprocess stdout returns bytes, but `sys.stdout.write()` expects strings.

**Fix**: Added decoding of bytes to string before writing to stdout

**Lines changed**: 584-586

**Before**:
```python
sys.stdout.write(stdout)
```

**After**:
```python
if isinstance(stdout, bytes):
    stdout = stdout.decode('utf-8', errors='replace')
sys.stdout.write(stdout)
```

### 4. `config.py` (temporary workaround)

#### Issue: Patches directory path
**Problem**: The build script expects patches in current directory, but they're in `mozilla/patches-new`.

**Fix**: Created symbolic link `ln -s mozilla/patches-new patches-new`

**Alternative**: Could modify build script to use relative path, but symbolic link is simpler.

## Testing

The fixes have been tested and verified to resolve the following issues:

1. ✅ Configuration parsing works
2. ✅ Platform detection works on Linux
3. ✅ Patches directory is found
4. ✅ Patch application starts (fails due to missing source files, not Python compatibility)

## Remaining Issues

The build process now fails at the patching stage because:
1. Git repository was cloned but not checked out (network timeout issues)
2. Source files are missing, so patches cannot be applied

These are build infrastructure issues, not Python 2 vs 3 compatibility issues.

## Recommendations

1. **For developers**: Use Python 3.6+ for building OpenKomodoIDE
2. **For network issues**: Consider using pre-built source tarballs or local mirrors
3. **For large repositories**: Use shallow clones or specific branches to reduce download size

## Verification

All modified files have been verified to:
1. Compile without syntax errors: `python3 -m py_compile <file>`
2. Pass basic functionality tests
3. Maintain backward compatibility where possible

The build system can now progress significantly further under Python 3 than before these fixes.