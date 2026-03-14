#!/bin/bash
# Docker entrypoint script for OpenKomodoIDE build environment

set -e

# Function to show help
show_help() {
    echo "OpenKomodoIDE Build Environment"
    echo "Usage: docker-entrypoint.sh [command]"
    echo ""
    echo "Commands:"
    echo "  build          - Run complete build process"
    echo "  configure      - Configure the build"
    echo "  test           - Run test suite"
    echo "  shell          - Start interactive shell"
    echo "  help           - Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  KOMODO_VERSION - Version to build (default: 12.0)"
    echo "  FIREFOX_VERSION - Firefox version (default: 140.0)"
    echo "  PLATFORM       - Target platform (auto-detected)"
    echo "  DEBUG          - Set to 1 for debug build"
    echo "  CLEAN          - Set to 1 to clean before build"
}

# Set default values
KOMODO_VERSION=${KOMODO_VERSION:-12.0}
FIREFOX_VERSION=${FIREFOX_VERSION:-140.0}
DEBUG=${DEBUG:-0}
CLEAN=${CLEAN:-0}
PLATFORM=${PLATFORM:-$(python3 -c "import platform; print(platform.system().lower())")}

# Detect platform more accurately
detect_platform() {
    local plat=$(python3 -c "import sys, platform; print(sys.platform)")
    local machine=$(python3 -c "import platform; print(platform.machine())")
    
    if [[ "$plat" == "linux" ]]; then
        if [[ "$machine" == "aarch64" || "$machine" == "arm64" ]]; then
            echo "linux-arm64"
        elif [[ -f "/etc/gentoo-release" ]]; then
            echo "gentoo"
        else
            echo "linux"
        fi
    elif [[ "$plat" == "freebsd"* ]]; then
        echo "freebsd"
    elif [[ "$plat" == "netbsd"* ]]; then
        echo "netbsd"
    elif [[ "$plat" == "openbsd"* ]]; then
        echo "openbsd"
    elif [[ "$plat" == "darwin" ]]; then
        echo "macos"
    elif [[ "$plat" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Set up environment
setup_environment() {
    echo "Setting up build environment..."
    
    # Detect platform
    PLATFORM=$(detect_platform)
    echo "Detected platform: $PLATFORM"
    
    # Set environment variables
    export PATH=/home/builduser/.local/bin:/usr/local/bin:/usr/bin:/bin
    export PYTHONPATH=/home/builduser/build
    export MOZCONFIG=/home/builduser/build/mozconfig
    export LD_LIBRARY_PATH=/home/builduser/build/lib
    export CCACHE_DIR=/home/builduser/.ccache
    export CCACHE_SLOPPINESS=file_macro,time_macros
    export CCACHE_MAXSIZE=10G
    export MAKEFLAGS="-j$(nproc)"
    export PLATFORM=$PLATFORM
    
    # Set build type
    if [[ "$DEBUG" == "1" ]]; then
        export BUILD_TYPE="debug"
        echo "Debug build enabled"
    else
        export BUILD_TYPE="release"
        echo "Release build enabled"
    fi
    
    echo "Environment ready"
}

# Run build automation command
run_build_automation() {
    local cmd="python3 /home/builduser/build/build_automation.py"
    
    # Add command line arguments
    cmd+=" --version $KOMODO_VERSION"
    cmd+=" --firefox $FIREFOX_VERSION"
    cmd+=" --platform $PLATFORM"
    
    if [[ "$DEBUG" == "1" ]]; then
        cmd+=" --debug"
    fi
    
    if [[ "$CLEAN" == "1" ]]; then
        cmd+=" --clean"
    fi
    
    # Add the specific command
    cmd+=" $1"
    
    echo "Running: $cmd"
    eval $cmd
}

# Main script logic
if [[ $# -gt 0 ]]; then
    case "$1" in
        build)
            setup_environment
            run_build_automation "complete"
            ;;
        configure)
            setup_environment
            run_build_automation "configure"
            ;;
        test)
            setup_environment
            run_build_automation "test"
            ;;
        shell)
            setup_environment
            echo "Starting interactive shell..."
            echo "Run 'build_automation.py --help' for build options"
            exec bash
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
else
    show_help
fi