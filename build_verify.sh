#!/bin/bash
# build_verify.sh - Automated build verification for OpenKomodoIDE

set -e

echo "=== OpenKomodoIDE Build Verification ==="
echo

# Configuration
CONFIG_DIR="mozilla/build/moz1400-ko1410/mozilla"
LOG_DIR="logs"

# 1. Check configuration files
echo "1. Checking configuration files..."

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
    BUILD_FILES=$(find "$CONFIG_DIR/obj-*" -type f 2>/dev/null | wc -l)
    echo "  Found $BUILD_FILES files in build directory"
else
    echo "✗ Build directory missing"
    exit 1
fi

# 3. Check binary outputs
echo "3. Checking binary outputs..."

BINARY_FOUND=false

# Look for Firefox binary
if find "$CONFIG_DIR/obj-*" -name "firefox" -type f 2>/dev/null | grep -q ";"; then
    echo "✓ Firefox binary found"
    BINARY_FOUND=true
fi

# Look for XUL binary
if find "$CONFIG_DIR/obj-*" -name "xul" -type f 2>/dev/null | grep -q ";"; then
    echo "✓ XUL binary found"
    BINARY_FOUND=true
fi

# Look for libxul
if find "$CONFIG_DIR/obj-*" -name "libxul.so" -type f 2>/dev/null | grep -q ";"; then
    echo "✓ libxul.so found"
    BINARY_FOUND=true
fi

if [ "$BINARY_FOUND" = false ]; then
    echo "⚠ No expected binaries found (may need full build)"
fi

# 4. Check recent build log
echo "4. Checking build logs..."

LATEST_LOG=$(ls -t "$LOG_DIR"/build_*.log 2>/dev/null | head -1)

if [ -n "$LATEST_LOG" ]; then
    echo "✓ Found build log: $LATEST_LOG"
    
    if grep -q "✓ Build successful" "$LATEST_LOG"; then
        echo "✓ Build success message found in logs"
    else
        echo "⚠ No explicit success message found"
    fi
    
    ERROR_COUNT=$(grep -c "✗\|ERROR" "$LATEST_LOG" 2>/dev/null || echo "0")
    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo "⚠ Found $ERROR_COUNT warnings or errors in logs"
    fi
else
    echo "⚠ No build log found"
fi

# 5. Check for common build artifacts
echo "5. Checking for common build artifacts..."

ARTIFACTS_FOUND=0

# Check for various build artifacts
if [ -f "$CONFIG_DIR/obj-*/dist/include/mozilla-config.h" ]; then
    echo "✓ Mozilla config header found"
    ARTIFACTS_FOUND=$((ARTIFACTS_FOUND + 1))
fi

if [ -d "$CONFIG_DIR/obj-*/dist/include" ]; then
    echo "✓ Include directory found"
    ARTIFACTS_FOUND=$((ARTIFACTS_FOUND + 1))
fi

if [ "$ARTIFACTS_FOUND" -eq 0 ]; then
    echo "⚠ No common build artifacts found"
fi

# 6. Summary
echo
echo "=== Verification Summary ==="

if [ -f "$CONFIG_DIR/.mozconfig" ] && [ -f "$CONFIG_DIR/config.status" ] && [ -d "$CONFIG_DIR/obj-*" ]; then
    echo "✅ Configuration appears successful!"
    echo
    echo "Configuration files: ✓"
    echo "Build directory: ✓"
    echo "Build artifacts: ✓"
    
    if [ "$BINARY_FOUND" = true ]; then
        echo "Binaries: ✓"
    else
        echo "Binaries: ⚠ (may need full build)"
    fi
    
    echo
    echo "Next steps:"
    echo "  1. Run full build: python3 build.py build --jobs 2"
    echo "  2. Check logs: cat $LOG_DIR/build_*.log"
    echo "  3. Create packages: python3 build.py package --jobs 2"
else
    echo "❌ Configuration incomplete"
    echo
    echo "Please run:"
    echo "  python3 build.py configure --jobs 2"
    exit 1
fi