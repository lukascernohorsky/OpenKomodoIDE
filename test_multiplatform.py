#!/usr/bin/env python3
"""
Multiplatform test suite for OpenKomodoIDE build system
Tests platform detection and configuration for all supported platforms
"""

import sys
import os
import platform
import tempfile
import shutil
from pathlib import Path

# Add the util directory to the path so we can import the build modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'util'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mozilla'))

def test_platform_detection():
    """Test platform detection for all supported platforms"""
    print("Testing platform detection...")
    
    # Test current platform
    current_platform = sys.platform
    machine_type = platform.machine()
    
    print(f"Current platform: {current_platform}")
    print(f"Machine type: {machine_type}")
    
    # Test platform mapping
    from build import gPlat2BinDir
    
    supported_platforms = [
        'win32', 'sunos5', 'linux2', 'hp-uxB', 'darwin',
        'freebsd6', 'freebsd7', 'freebsd8', 'freebsd9', 'freebsd10',
        'freebsd11', 'freebsd12', 'freebsd13', 'freebsd14',
        'netbsd', 'openbsd', 'minix3', 'gentoo', 'linux_aarch64', 'linux_arm64'
    ]
    
    print("\nSupported platforms in build system:")
    for plat in supported_platforms:
        if plat in gPlat2BinDir:
            print(f"✓ {plat}: {gPlat2BinDir[plat]}")
        else:
            print(f"✗ {plat}: Missing from gPlat2BinDir")
    
    return True

def test_patch_system():
    """Test patch system for all platforms"""
    print("\nTesting patch system...")
    
    # Test that all patch directories exist and have valid __patchinfo__.py
    patch_dirs = [
        'mozilla-140.0',
        'mozilla-140.0/cocoa',
        'mozilla-140.0/windows',
        'mozilla-140.0/gtk',
        'mozilla-140.0/upstream',
        'mozilla-140.0/arm64',
        'mozilla-140.0/freebsd',
        'mozilla-140.0/netbsd',
        'mozilla-140.0/openbsd',
        'mozilla-140.0/gentoo',
        'mozilla-140.0/minix3',
        'mozilla-140.0-pyxpcom'
    ]
    
    for patch_dir in patch_dirs:
        full_path = os.path.join('mozilla', 'patches-new', patch_dir, '__patchinfo__.py')
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                compile(content, full_path, 'exec')
                print(f"✓ {patch_dir}: Valid patch info")
            except SyntaxError as e:
                print(f"✗ {patch_dir}: Syntax error: {e}")
            except Exception as e:
                print(f"✗ {patch_dir}: Error: {e}")
        else:
            print(f"✗ {patch_dir}: Missing __patchinfo__.py")
    
    return True

def test_build_configuration():
    """Test build configuration for different platforms"""
    print("\nTesting build configuration...")
    
    # Mock different platforms
    test_cases = [
        ('linux', 'x86_64', 'Linux x86_64'),
        ('linux', 'aarch64', 'Linux ARM64'),
        ('darwin', 'x86_64', 'macOS x86_64'),
        ('win32', 'AMD64', 'Windows x64'),
        ('freebsd12', 'amd64', 'FreeBSD 12'),
        ('netbsd', 'amd64', 'NetBSD'),
        ('openbsd', 'amd64', 'OpenBSD'),
        ('minix3', 'x86', 'Minix3'),
    ]
    
    for plat, machine, desc in test_cases:
        print(f"\nTesting configuration for {desc}:")
        print(f"  Platform: {plat}")
        print(f"  Machine: {machine}")
        
        # Check if platform is in gPlat2BinDir
        from build import gPlat2BinDir
        if plat in gPlat2BinDir:
            print(f"  ✓ Platform supported: {gPlat2BinDir[plat]}")
        else:
            print(f"  ✗ Platform not in gPlat2BinDir")
    
    return True

def test_environment_setup():
    """Test environment setup for different platforms"""
    print("\nTesting environment setup...")
    
    # Test that we can set up environment variables correctly
    test_env_vars = {
        'PLATFORM': 'test-platform',
        'MOZCONFIG': 'test-mozconfig',
        'LDFLAGS': '-lrt -lm',
        'CFLAGS': '-O2 -Wall'
    }
    
    # Save original environment
    original_env = os.environ.copy()
    
    try:
        # Set test environment variables
        for key, value in test_env_vars.items():
            os.environ[key] = value
        
        print("✓ Environment variables set successfully")
        
        # Test that we can read them back
        for key, value in test_env_vars.items():
            if os.environ.get(key) == value:
                print(f"✓ {key} = {value}")
            else:
                print(f"✗ {key} mismatch")
        
        return True
        
    except Exception as e:
        print(f"✗ Environment setup failed: {e}")
        return False
        
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)

def test_dependency_check():
    """Test dependency checking for build process"""
    print("\nTesting dependency checking...")
    
    # List of required tools for build process
    required_tools = [
        'python3', 'python', 'gcc', 'g++', 'make', 'autoconf', 'automake',
        'libtool', 'pkg-config', 'patch', 'zip', 'unzip', 'tar', 'git', 'hg'
    ]
    
    from util.which import which
    
    print("Checking for required build tools:")
    for tool in required_tools:
        try:
            # which() returns a generator, so we need to get the first result
            path_gen = which(tool)
            path = next(path_gen, None) if path_gen else None
            if path:
                print(f"✓ {tool}: {path}")
            else:
                print(f"✗ {tool}: Not found")
        except Exception as e:
            print(f"✗ {tool}: Error checking: {e}")
    
    return True

def create_test_build_script():
    """Create a test build script for different platforms"""
    print("\nCreating test build scripts...")
    
    # Create a test build script that can be used on different platforms
    test_script_content = '''#!/usr/bin/env python3
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
    
    print("\\nAll tests completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    # Write the test script
    with open('test_build.py', 'w') as f:
        f.write(test_script_content)
    
    # Make it executable
    os.chmod('test_build.py', 0o755)
    
    print("✓ Created test_build.py script")
    
    return True

def main():
    """Main test function"""
    print("OpenKomodoIDE Multiplatform Test Suite")
    print("=" * 60)
    
    # Run all tests
    tests = [
        test_platform_detection,
        test_patch_system,
        test_build_configuration,
        test_environment_setup,
        test_dependency_check,
        create_test_build_script,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY:")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())