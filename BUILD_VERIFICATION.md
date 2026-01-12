# Build Verification Guide

This document explains how to verify that the OpenKomodoIDE build process completed successfully.

## Success Indicators

### Configuration Phase

**Successful Configuration:**
```bash
python3 build.py configure --jobs 2
# Expected output: "✓ Build configuration successful"
```

**Verification:**
- Check for `.mozconfig` file in Firefox source directory
- Check for `config.status` file
- No error messages in output

### Build Phase

**Successful Build:**
```bash
python3 build.py build --jobs 2
# Expected: Clean completion with binary outputs
```

**Verification:**
- Check for binary files in `obj-*` directories
- Check for final build artifacts
- Look for "✓ Build successful" messages

## Verification Methods

### 1. Check Build Logs

```bash
# View the latest build log
cat logs/build_*.log | grep -E "(✓|✗|ERROR|SUCCESS)"

# Check for successful completion
if grep -q "✓ Build successful" logs/build_*.log; then
    echo "Build completed successfully!"
else
    echo "Build may have issues"
fi
```

### 2. Check Binary Outputs

```bash
# Check for expected binary files
BUILD_DIR="mozilla/build/moz1400-ko1410/mozilla"

if [ -f "$BUILD_DIR/obj-*/dist/bin/firefox" ]; then
    echo "✓ Firefox binary found"
else
    echo "✗ Firefox binary missing"
fi

if [ -f "$BUILD_DIR/obj-*/dist/bin/xul" ]; then
    echo "✓ XUL binary found"
else
    echo "✗ XUL binary missing"
fi
```

### 3. Check Configuration Files

```bash
# Verify configuration was generated
CONFIG_DIR="mozilla/build/moz1400-ko1410/mozilla"

if [ -f "$CONFIG_DIR/.mozconfig" ]; then
    echo "✓ Configuration file exists"
else
    echo "✗ Configuration file missing"
fi

if [ -f "$CONFIG_DIR/config.status" ]; then
    echo "✓ Config status file exists"
else
    echo "✗ Config status file missing"
fi
```

### 4. Check Build Artifacts

```bash
# Check for build artifacts
BUILD_DIR="mozilla/build/moz1400-ko1410/mozilla"

if [ -d "$BUILD_DIR/obj-*" ]; then
    echo "✓ Build directory exists"
    # Count files in build directory
    find "$BUILD_DIR/obj-*" -type f | wc -l
else
    echo "✗ Build directory missing"
fi
```

## Common Success Patterns

### Successful Configuration
```
✓ Build configuration successful
```

### Successful Build
```
✓ Build successful
```

### Successful Package Creation
```
✓ Packages created successfully
```

## Common Failure Patterns

### Configuration Failures
```
✗ Build configuration failed:
```

### Build Failures
```
✗ Target ... failed:
```

### Missing Dependencies
```
✗ Missing tools: ...
```

## Automated Verification Script

Create a verification script:

```bash
#!/bin/bash
# build_verify.sh - Automated build verification

set -e

echo "=== OpenKomodoIDE Build Verification ==="
echo

# 1. Check configuration files
echo "1. Checking configuration files..."
CONFIG_DIR="mozilla/build/moz1400-ko1410/mozilla"

if [ -f "$CONFIG_DIR/.mozconfig" ]; then
    echo "✓ .mozconfig exists"
else
    echo "✗ .mozconfig missing"
    exit 1
fi

if [ -f "$CONFIG_DIR/config.status" ]; then
    echo "✓ config.status exists"
else
    echo "✗ config.status missing"
    exit 1
fi

# 2. Check build directory
echo "2. Checking build directory..."
if [ -d "$CONFIG_DIR/obj-*" ]; then
    echo "✓ Build directory exists"
    BUILD_FILES=$(find "$CONFIG_DIR/obj-*" -type f | wc -l)
    echo "  Found $BUILD_FILES files in build directory"
else
    echo "✗ Build directory missing"
    exit 1
fi

# 3. Check binary outputs
echo "3. Checking binary outputs..."
BINARY_FOUND=false

if [ -f "$CONFIG_DIR/obj-*/dist/bin/firefox" ]; then
    echo "✓ Firefox binary found"
    BINARY_FOUND=true
fi

if [ -f "$CONFIG_DIR/obj-*/dist/bin/xul" ]; then
    echo "✓ XUL binary found"
    BINARY_FOUND=true
fi

if [ "$BINARY_FOUND" = false ]; then
    echo "✗ No expected binaries found"
    exit 1
fi

# 4. Check recent build log
echo "4. Checking build logs..."
LATEST_LOG=$(ls -t logs/build_*.log 2>/dev/null | head -1)

if [ -n "$LATEST_LOG" ]; then
    if grep -q "✓ Build successful" "$LATEST_LOG"; then
        echo "✓ Build success message found in logs"
    else
        echo "⚠ No explicit success message found"
    fi
    
    if grep -q "✗\|ERROR" "$LATEST_LOG"; then
        echo "⚠ Warnings or errors found in logs"
    fi
else
    echo "⚠ No build log found"
fi

echo
echo "=== Verification Complete ==="
echo "✅ All checks passed - Build appears successful!"
```

Save this as `build_verify.sh` and run:
```bash
chmod +x build_verify.sh
./build_verify.sh
```

## Manual Verification Steps

### 1. Check Exit Codes
```bash
python3 build.py configure --jobs 2
echo "Exit code: $?"  # 0 = success, non-zero = failure
```

### 2. Check Process Completion
```bash
# Run build in background and check status
python3 build.py build --jobs 2 &
BUILD_PID=$!
wait $BUILD_PID
echo "Build completed with exit code: $?"
```

### 3. Check File Timestamps
```bash
# Check if build artifacts were recently created
find mozilla/build/moz1400-ko1410/mozilla/obj-* -type f -newermt "1 hour ago" | wc -l
```

## Troubleshooting

### Build Fails Immediately
- Check system dependencies
- Verify Python version (3.11+)
- Check disk space

### Build Fails During Configuration
- Check `.mozconfig` syntax
- Verify all build tools installed
- Check file permissions

### Build Fails During Compilation
- Check compiler versions
- Verify system libraries
- Check memory availability

## Success Criteria

A build is considered successful when:
1. ✅ Configuration completes without errors
2. ✅ All system checks pass
3. ✅ Binary files are generated
4. ✅ Exit code is 0
5. ✅ No critical error messages in logs

## Next Steps

After successful build:
1. Run verification script
2. Check binary functionality
3. Create distribution packages
4. Run tests (if available)

```bash
# After successful build
python3 build.py package --jobs 2
python3 build.py check-binaries
```

## Documentation

For complete build documentation, see:
- [BUILD_DEPENDENCIES.md](BUILD_DEPENDENCIES.md) - All required dependencies
- [README.md](README.md) - Getting started guide
- [DOCKER_README.md](DOCKER_README.md) - Docker build instructions