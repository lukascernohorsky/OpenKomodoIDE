#!/usr/bin/env python3
"""
Test build script for OpenKomodoIDE
Can be used to test build process on different platforms
"""

import os
import sys
import platform
import subprocess

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_build_system():
    """Test the build system"""
    print("Testing OpenKomodoIDE build system...")
    
    # Test basic build.py functionality
    success, stdout, stderr = run_command("python3 mozilla/build.py --help")
    if success:
        print("✓ Build system help works")
    else:
        print(f"✗ Build system help failed: {stderr}")
        return False
    
    # Test targets listing
    success, stdout, stderr = run_command("python3 mozilla/build.py -t")
    if success:
        print("✓ Build targets listing works")
    else:
        print(f"✗ Build targets listing failed: {stderr}")
        return False
    
    return True

def detect_platform():
    """Detect current platform"""
    plat = sys.platform
    machine = platform.machine()
    
    print(f"Detected platform: {plat}")
    print(f"Machine architecture: {machine}")
    
    # Determine platform type
    if plat.startswith("linux"):
        if machine in ("aarch64", "arm64"):
            return "linux-arm64"
        elif os.path.exists("/etc/gentoo-release"):
            return "gentoo"
        else:
            return "linux"
    elif plat.startswith("freebsd"):
        return "freebsd"
    elif plat.startswith("netbsd"):
        return "netbsd"
    elif plat.startswith("openbsd"):
        return "openbsd"
    elif plat.startswith("minix"):
        return "minix3"
    elif plat == "darwin":
        return "macos"
    elif plat == "win32":
        return "windows"
    else:
        return "unknown"

def main():
    """Main test function"""
    print("OpenKomodoIDE Multiplatform Build Test")
    print("=" * 50)
    
    # Detect platform
    current_platform = detect_platform()
    print(f"Current platform: {current_platform}")
    
    # Test build system
    if not test_build_system():
        print("Build system test failed!")
        return 1
    
    print("\nAll tests completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
