#!/bin/bash

# Docker entrypoint script for OpenKomodoIDE build environment

set -e

# Print welcome message
echo "=========================================="
echo "OpenKomodoIDE Modern Build Environment"
echo "=========================================="
echo "Python: $(python3 --version)"
echo "Node.js: $(node --version 2>/dev/null || echo "Not installed")"
echo "Rust: $(rustc --version 2>/dev/null || echo "Not installed")"
echo "=========================================="
echo ""

# Set up environment variables if not already set
export PYTHON=${PYTHON:-python3}
export MOZCONFIG=${MOZCONFIG:-/root/mozconfig}
export MOZ_OBJDIR=${MOZ_OBJDIR:-/root/mozilla-objdir}

# Add build tools to PATH
export PATH="/root/build/util/black:/root/.cargo/bin:$PATH"

# Handle different commands
case "$1" in
    "build-mozilla")
        echo "Building Mozilla with Firefox 140 ESR..."
        cd /root/build/mozilla
        python3 build.py configure -k 14.10 --moz-src=14000:FIREFOX_140_0_RELEASE
        python3 build.py distclean all
        ;;
    
    "build-komodo")
        echo "Building Komodo..."
        cd /root/build
        bk configure -V 14.10.0-devel
        bk build
        ;;
    
    "build-all")
        echo "Building Mozilla and Komodo..."
        cd /root/build/mozilla
        python3 build.py configure -k 14.10 --moz-src=14000:FIREFOX_140_0_RELEASE
        python3 build.py distclean all
        
        cd /root/build
        bk configure -V 14.10.0-devel
        bk build
        ;;
    
    "run")
        echo "Running Komodo..."
        cd /root/build
        bk run
        ;;
    
    "shell")
        echo "Starting interactive shell..."
        exec bash
        ;;
    
    "help"|"--help"|-h)
        echo "Available commands:"
        echo "  build-mozilla    - Build Mozilla with Firefox 140 ESR"
        echo "  build-komodo     - Build Komodo IDE"
        echo "  build-all        - Build both Mozilla and Komodo"
        echo "  run              - Run Komodo IDE"
        echo "  shell            - Start interactive shell"
        echo "  help             - Show this help message"
        ;;
    
    *)
        echo "Unknown command: $1"
        echo "Use 'help' to see available commands"
        exec "$@"
        ;;
esac