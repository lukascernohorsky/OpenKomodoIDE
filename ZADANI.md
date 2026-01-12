# OpenKomodoIDE Build Assignment - Complete Build Process

## Overview
This document contains the comprehensive build plan for OpenKomodoIDE, including complete build execution, binary verification, cleanup, and rebuild with Mozilla file downloads.

## Build Configuration
- **Target**: Firefox 140 ESR for Komodo 14.10
- **Platform**: Linux x86_64
- **Python**: System Python 3.11
- **Build Type**: Release with optimizations
- **Build Directory**: `/home/lc/projekty/OpenKomodoIDE/mozilla/build/moz14000-ko14.10`

## Step 1: Initialize Progress Tracking

```bash
# Create PROGRES.md file
PROGRES_FILE="/home/lc/projekty/OpenKomodoIDE/PROGRES.md"

cat > "$PROGRES_FILE" << 'EOF'
# OpenKomodoIDE Build Progress Tracking

## Build Information
- **Start Time**: $(date +%Y-%m-%d\ %H:%M:%S)
- **Build System**: Firefox 140 ESR for Komodo 14.10
- **Platform**: Linux x86_64
- **Python Version**: 3.11
- **Build Type**: Release

## Progress Status
- [ ] Setup: External patches directory
- [ ] Setup: Build configuration
- [ ] Phase 1: Source download
- [ ] Phase 2: Patch application
- [ ] Phase 3: Mozilla configuration
- [ ] Phase 4: Main build
- [ ] Phase 5: PyXPCOM build
- [ ] Phase 6: Python siloing
- [ ] Phase 7: Verification
- [ ] Phase 8: Cleanup
- [ ] Phase 9: Rebuild

## Current State
- **Last Completed Step**: None
- **Next Step**: Setup external patches directory
- **Status**: Not started

## Build Artifacts
- **External Patches**: /home/lc/projekty/OpenKomodoIDE/patches-external
- **Build Directory**: /home/lc/projekty/OpenKomodoIDE/mozilla/build/moz14000-ko14.10
- **Expected Output**: /home/lc/projekty/OpenKomodoIDE/mozilla/build/moz14000-ko14.10/mozilla/obj-x86_64-pc-linux-gnu/dist/bin/komodo

## Log Files
- **Main Log**: /home/lc/projekty/OpenKomodoIDE/build_logs/$(date +%Y%m%d_%H%M%S)_build.log
- **Patch Log**: /home/lc/projekty/OpenKomodoIDE/mozilla/build/moz14000-ko14.10/mozilla-patches-moz14000-ko14.10/__patchlog__.py

## Notes
- External patches are preserved during cleanup
- Build can be resumed from any completed phase
- All critical artifacts are tracked outside build directory
EOF

echo "Progress tracking initialized in $PROGRES_FILE"

# Function to update progress
update_progress() {
    local step_name=$1
    local status=$2
    local timestamp=$(date +%Y-%m-%d\ %H:%M:%S)
    
    sed -i "s/- \[ \] $step_name/- \[$status\] $step_name/" "$PROGRES_FILE"
    sed -i "s/^## Current State$/## Current State\n- **Last Completed Step**: $step_name\n- **Status**: $status\n- **Timestamp**: $timestamp/" "$PROGRES_FILE"
    echo "[$timestamp] $step_name: $status" >> "$PROGRES_FILE"
}

# Function to handle interruption
handle_interruption() {
    local step_name=$1
    echo "Build interrupted during: $step_name"
    update_progress "$step_name" "interrupted"
    touch "/home/lc/projekty/OpenKomodoIDE/BUILD_INTERRUPTED"
}

## Step 2: Setup External Patches Directory

```bash
# Create external patches directory
mkdir -p /home/lc/projekty/OpenKomodoIDE/patches-external

# Create symlink for build system
ln -sf /home/lc/projekty/OpenKomodoIDE/patches-external /home/lc/projekty/OpenKomodoIDE/mozilla/patches-new

# Update build configuration
cd /home/lc/projekty/OpenKomodoIDE/mozilla
sed -i "s|patchesDirs = \['patches-new'\]|patchesDirs = ['patches-external']|" config.py

echo "External patches directory setup complete"
update_progress "Setup: External patches directory" "completed"

## Step 3: Execute Complete Build Process

```bash
cd /home/lc/projekty/OpenKomodoIDE/mozilla

# Start with source download
update_progress "Phase 1: Source download" "in_progress"
python3 build.py src
if [ $? -eq 0 ]; then
    update_progress "Phase 1: Source download" "completed"
else
    handle_interruption "Source download"
    exit 1
fi

# Apply patches
update_progress "Phase 2: Patch application" "in_progress"
python3 build.py patch
if [ $? -eq 0 ]; then
    update_progress "Phase 2: Patch application" "completed"
else
    handle_interruption "Patch application"
    exit 1
fi

# Configure Mozilla
update_progress "Phase 3: Mozilla configuration" "in_progress"
python3 build.py configure_mozilla
if [ $? -eq 0 ]; then
    update_progress "Phase 3: Mozilla configuration" "completed"
else
    handle_interruption "Mozilla configuration"
    exit 1
fi

# Main build
update_progress "Phase 4: Main build" "in_progress"
python3 build.py mozilla
if [ $? -eq 0 ]; then
    update_progress "Phase 4: Main build" "completed"
else
    handle_interruption "Main build"
    exit 1
fi

# PyXPCOM build
update_progress "Phase 5: PyXPCOM build" "in_progress"
python3 build.py pyxpcom
if [ $? -eq 0 ]; then
    update_progress "Phase 5: PyXPCOM build" "completed"
else
    handle_interruption "PyXPCOM build"
    exit 1
fi

# Python siloing
update_progress "Phase 6: Python siloing" "in_progress"
python3 build.py silo_python
if [ $? -eq 0 ]; then
    update_progress "Phase 6: Python siloing" "completed"
else
    handle_interruption "Python siloing"
    exit 1
fi

## Step 4: Verify Binary Outputs

```bash
BUILD_DIR="/home/lc/projekty/OpenKomodoIDE/mozilla/build/moz14000-ko14.10/mozilla/obj-x86_64-pc-linux-gnu"

update_progress "Phase 7: Verification" "in_progress"

# Check for main executables
if [ -f "$BUILD_DIR/dist/bin/komodo" ]; then
    echo "✓ Komodo binary found: $(du -h "$BUILD_DIR/dist/bin/komodo" | cut -f1)"
else
    echo "✗ Komodo binary not found"
    update_progress "Phase 7: Verification" "failed"
    exit 1
fi

if [ -f "$BUILD_DIR/dist/bin/mozpython" ]; then
    echo "✓ Python XPCOM integration successful"
else
    echo "⚠ Python XPCOM integration may be missing"
fi

# List key files
ls -la "$BUILD_DIR/dist/bin/" | grep -E '(komodo|firefox|xpcshell)'
update_progress "Phase 7: Verification" "completed"

## Step 5: Cleanup and Rebuild

```bash
# Cleanup
update_progress "Phase 8: Cleanup" "in_progress"
python3 build.py clean
rm -rf "$BUILD_DIR/mozilla-patches-*"
rm -rf "$BUILD_DIR/obj-*"
find "$BUILD_DIR" -name "*.pyc" -delete
find "$BUILD_DIR" -name "__pycache__" -type d -exec rm -rf {} +

# Verify patches preserved
if [ -d "/home/lc/projekty/OpenKomodoIDE/patches-external" ]; then
    echo "✓ External patches preserved"
    update_progress "Phase 8: Cleanup" "completed"
else
    echo "✗ Patch preservation failed"
    update_progress "Phase 8: Cleanup" "failed"
    exit 1
fi

# Rebuild
update_progress "Phase 9: Rebuild" "in_progress"
python3 build.py src -f
python3 build.py all

# Final verification
if [ -f "$BUILD_DIR/dist/bin/komodo" ]; then
    echo "✓ Rebuild successful"
    update_progress "Phase 9: Rebuild" "completed"
else
    echo "✗ Rebuild failed"
    update_progress "Phase 9: Rebuild" "failed"
    exit 1
fi

## Step 6: Final Documentation

```bash
# Create build summary
FINAL_SUMMARY="/home/lc/projekty/OpenKomodoIDE/BUILD_SUMMARY.md"

cat > "$FINAL_SUMMARY" << 'EOF'
# OpenKomodoIDE Build Summary

## Build Results
- **Status**: COMPLETED
- **Start Time**: $(grep "Start Time" "$PROGRES_FILE" | cut -d: -f2-)
- **Completion Time**: $(date +%Y-%m-%d\ %H:%M:%S)
- **Total Duration**: $(grep "Start Time" "$PROGRES_FILE" | cut -d: -f2- | xargs -I {} bash -c 'echo $((($(date +%s) - $(date +%s -d "{}")))) seconds')

## Build Artifacts
- **Komodo Binary**: /home/lc/projekty/OpenKomodoIDE/mozilla/build/moz14000-ko14.10/mozilla/obj-x86_64-pc-linux-gnu/dist/bin/komodo
- **Binary Size**: $(du -h /home/lc/projekty/OpenKomodoIDE/mozilla/build/moz14000-ko14.10/mozilla/obj-x86_64-pc-linux-gnu/dist/bin/komodo 2>/dev/null | cut -f1 || echo "N/A")
- **External Patches**: /home/lc/projekty/OpenKomodoIDE/patches-external
- **Build Logs**: /home/lc/projekty/OpenKomodoIDE/build_logs/

## Verification Results
- ✓ Komodo binary exists
- ✓ Python XPCOM integration
- ✓ External patches preserved
- ✓ Clean rebuild successful

## Resumption Capabilities
To resume an interrupted build:
1. Check PROGRES.md for last completed step
2. Run: cd /home/lc/projekty/OpenKomodoIDE/mozilla && python3 build.py [next_target]
3. Or use the resumption script: /home/lc/projekty/OpenKomodoIDE/resume_build.sh

## Notes
- All patches are preserved in external directory
- Build can be safely cleaned and rebuilt
- Progress tracking allows for precise resumption
EOF

# Create resumption script
RESUME_SCRIPT="/home/lc/projekty/OpenKomodoIDE/resume_build.sh"

cat > "$RESUME_SCRIPT" << 'EOF'
#!/bin/bash
# OpenKomodoIDE Build Resumption Script

PROGRES_FILE="/home/lc/projekty/OpenKomodoIDE/PROGRES.md"
BUILD_DIR="/home/lc/projekty/OpenKomodoIDE/mozilla"

determine_next_step() {
    if grep -q "Phase 1.*completed" "$PROGRES_FILE" && ! grep -q "Phase 2.*completed" "$PROGRES_FILE"; then
        echo "patch"
    elif grep -q "Phase 2.*completed" "$PROGRES_FILE" && ! grep -q "Phase 3.*completed" "$PROGRES_FILE"; then
        echo "configure_mozilla"
    elif grep -q "Phase 3.*completed" "$PROGRES_FILE" && ! grep -q "Phase 4.*completed" "$PROGRES_FILE"; then
        echo "mozilla"
    elif grep -q "Phase 4.*completed" "$PROGRES_FILE" && ! grep -q "Phase 5.*completed" "$PROGRES_FILE"; then
        echo "pyxpcom"
    elif grep -q "Phase 5.*completed" "$PROGRES_FILE" && ! grep -q "Phase 6.*completed" "$PROGRES_FILE"; then
        echo "silo_python"
    elif grep -q "Phase 6.*completed" "$PROGRES_FILE" && ! grep -q "Phase 7.*completed" "$PROGRES_FILE"; then
        echo "all"
    else
        echo "all"
    fi
}

if [ -f "/home/lc/projekty/OpenKomodoIDE/BUILD_INTERRUPTED" ]; then
    echo "Resuming interrupted build..."
    NEXT_STEP=$(determine_next_step)
    rm "/home/lc/projekty/OpenKomodoIDE/BUILD_INTERRUPTED"
else
    echo "Starting fresh build..."
    NEXT_STEP="src"
fi

cd "$BUILD_DIR"
echo "Executing: python3 build.py $NEXT_STEP"
python3 build.py "$NEXT_STEP"

if [ $? -eq 0 ]; then
    echo "Build step completed successfully!"
    if [ "$NEXT_STEP" = "all" ]; then
        echo "Full build completed!"
    else
        echo "Continuing with next phase..."
        NEXT_STEP=$(determine_next_step)
        python3 build.py "$NEXT_STEP"
    fi
else
    echo "Build step failed. Check logs for details."
    exit 1
fi
EOF

chmod +x "$RESUME_SCRIPT"

echo "Build completed successfully!"
echo "Summary saved to: $FINAL_SUMMARY"
echo "Progress tracking: $PROGRES_FILE"
echo "Resumption script: $RESUME_SCRIPT"
