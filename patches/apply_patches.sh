#!/bin/bash

# OpenKomodoIDE Build System Fixes - Patch Applicator
# This script applies all the build system fixes

echo "OpenKomodoIDE Build System Fixes - Patch Applicator"
echo "==================================================="
echo

# Check if we're in the right directory
if [ ! -f "build.py" ]; then
    echo "Error: This script must be run from the OpenKomodoIDE root directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Create patches directory if it doesn't exist
if [ ! -d "patches" ]; then
    echo "Error: patches directory not found"
    echo "Please ensure you have the patches directory with all patch files"
    exit 1
fi

# Apply each patch
echo "Applying patches..."
echo

for patch_file in patches/*.patch; do
    if [ -f "$patch_file" ]; then
        echo "Applying $(basename $patch_file)..."
        if patch -p1 < "$patch_file"; then
            echo "✓ $(basename $patch_file) applied successfully"
        else
            echo "✗ Failed to apply $(basename $patch_file)"
            echo "You may need to apply this patch manually"
            exit 1
        fi
        echo
    fi
done

echo "==================================================="
echo "All patches applied successfully!"
echo
echo "Verifying the fixes..."
echo

# Test that the fixes work
if python3 build.py status > /dev/null 2>&1; then
    echo "✓ build.py status command works"
else
    echo "✗ build.py status command failed"
    exit 1
fi

if python3 test_build.py > /dev/null 2>&1; then
    echo "✓ test_build.py passes"
else
    echo "✗ test_build.py failed"
    exit 1
fi

echo
echo "==================================================="
echo "Build system fixes completed successfully!"
echo
echo "You can now run:"
echo "  python3 build.py configure"
echo "  python3 build.py build"
echo "  python3 build.py status"
echo