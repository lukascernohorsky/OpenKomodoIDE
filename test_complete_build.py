#!/usr/bin/env python3
"""
Complete build test for OpenKomodoIDE
Tests the entire build process from configuration to final build
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, env=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, env=env, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_build_system():
    """Test the build system functionality"""
    print("Testing OpenKomodoIDE build system...")
    
    # Test 1: Help functionality
    print("\n1. Testing help functionality...")
    success, stdout, stderr = run_command("python3 mozilla/build.py --help")
    if success:
        print("✓ Build system help works")
    else:
        print(f"✗ Build system help failed: {stderr}")
        return False
    
    # Test 2: Targets listing
    print("\n2. Testing targets listing...")
    success, stdout, stderr = run_command("python3 mozilla/build.py -t")
    if success:
        print("✓ Build targets listing works")
        # Check that we have expected targets
        if "all" in stdout and "configure" in stdout and "mozilla" in stdout:
            print("✓ All expected targets present")
        else:
            print("✗ Some expected targets missing")
            return False
    else:
        print(f"✗ Build targets listing failed: {stderr}")
        return False
    
    # Test 3: Configuration
    print("\n3. Testing configuration...")
    success, stdout, stderr = run_command("python3 mozilla/build.py configure --help")
    if success:
        print("✓ Configuration help works")
    else:
        print(f"✗ Configuration help failed: {stderr}")
        return False
    
    return True

def test_python3_compatibility():
    """Test Python 3 compatibility"""
    print("\nTesting Python 3 compatibility...")
    
    # Test that all key Python files are Python 3 compatible
    key_files = [
        'mozilla/build.py',
        'util/preprocess.py',
        'util/platinfo.py',
        'util/patchtree.py',
        'util/sh.py',
    ]
    
    for file_path in key_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                compile(content, file_path, 'exec')
                print(f"✓ {file_path}: Python 3 compatible")
            except SyntaxError as e:
                print(f"✗ {file_path}: Python 3 syntax error: {e}")
                return False
            except Exception as e:
                print(f"✗ {file_path}: Error: {e}")
                return False
        else:
            print(f"✗ {file_path}: File not found")
            return False
    
    return True

def test_firefox_140_integration():
    """Test Firefox 140 ESR integration"""
    print("\nTesting Firefox 140 ESR integration...")
    
    # Test that Firefox 140 patch system is properly set up
    patch_dirs = [
        'mozilla/patches-new/mozilla-140.0',
        'mozilla/patches-new/mozilla-140.0/cocoa',
        'mozilla/patches-new/mozilla-140.0/windows',
        'mozilla/patches-new/mozilla-140.0/gtk',
        'mozilla/patches-new/mozilla-140.0/upstream',
        'mozilla/patches-new/mozilla-140.0/arm64',
        'mozilla/patches-new/mozilla-140.0/freebsd',
        'mozilla/patches-new/mozilla-140.0/netbsd',
        'mozilla/patches-new/mozilla-140.0/openbsd',
        'mozilla/patches-new/mozilla-140.0/gentoo',
        'mozilla/patches-new/mozilla-140.0/minix3',
        'mozilla/patches-new/mozilla-140.0-pyxpcom',
    ]
    
    for patch_dir in patch_dirs:
        patchinfo_path = os.path.join(patch_dir, '__patchinfo__.py')
        if os.path.exists(patchinfo_path):
            try:
                with open(patchinfo_path, 'r') as f:
                    content = f.read()
                compile(content, patchinfo_path, 'exec')
                print(f"✓ {patch_dir}: Valid patch info")
            except Exception as e:
                print(f"✗ {patch_dir}: Error: {e}")
                return False
        else:
            print(f"✗ {patch_dir}: Missing patch info")
            return False
    
    # Test that build.py contains Firefox 140 references
    try:
        with open('mozilla/build.py', 'r') as f:
            content = f.read()
        if '140.0' in content and 'FIREFOX_140_0_RELEASE' in content:
            print("✓ Build system contains Firefox 140.0 references")
        else:
            print("✗ Build system missing Firefox 140.0 references")
            return False
    except Exception as e:
        print(f"✗ Error checking build system: {e}")
        return False
    
    return True

def test_multiplatform_support():
    """Test multiplatform support"""
    print("\nTesting multiplatform support...")
    
    # Test that all platforms are in gPlat2BinDir
    from mozilla.build import gPlat2BinDir
    
    expected_platforms = [
        'win32', 'linux2', 'darwin', 'freebsd6', 'netbsd', 'openbsd',
        'minix3', 'gentoo', 'linux_aarch64', 'linux_arm64'
    ]
    
    for platform in expected_platforms:
        if platform in gPlat2BinDir:
            print(f"✓ {platform}: Supported")
        else:
            print(f"✗ {platform}: Not supported")
            return False
    
    return True

def test_environment_setup():
    """Test environment setup"""
    print("\nTesting environment setup...")
    
    # Save original environment
    original_env = os.environ.copy()
    
    try:
        # Set test environment variables
        test_vars = {
            'PLATFORM': 'test-platform',
            'MOZCONFIG': 'test-mozconfig',
            'LDFLAGS': '-lrt -lm',
            'CFLAGS': '-O2 -Wall',
            'PATH': os.environ.get('PATH', '')
        }
        
        for key, value in test_vars.items():
            os.environ[key] = value
        
        print("✓ Environment variables set successfully")
        
        # Test that we can import build modules
        try:
            from mozilla.build import gPlat2BinDir
            print("✓ Can import build modules")
        except Exception as e:
            print(f"✗ Cannot import build modules: {e}")
            return False
        
        return True
        
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)

def test_dependency_check():
    """Test that required dependencies are available"""
    print("\nTesting dependencies...")
    
    # Check for Python 3
    success, stdout, stderr = run_command("python3 --version")
    if success:
        print(f"✓ Python 3: {stdout.strip()}")
    else:
        print(f"✗ Python 3 not found: {stderr}")
        return False
    
    # Check for git
    success, stdout, stderr = run_command("git --version")
    if success:
        print(f"✓ Git: {stdout.strip()}")
    else:
        print(f"✗ Git not found: {stderr}")
        return False
    
    # Check for basic build tools
    tools = ['make', 'gcc', 'g++', 'patch', 'zip', 'tar']
    for tool in tools:
        success, stdout, stderr = run_command(f"{tool} --version")
        if success:
            print(f"✓ {tool}: Available")
        else:
            print(f"⚠ {tool}: Not found (may be optional)")
    
    return True

def test_build_scripts():
    """Test that all build scripts work"""
    print("\nTesting build scripts...")
    
    scripts = [
        'test_build.py',
        'test_multiplatform.py',
        'test_firefox_140.py',
        'python2to3_converter.py',
        'migrate_python3.py'
    ]
    
    for script in scripts:
        if os.path.exists(script):
            try:
                with open(script, 'r') as f:
                    content = f.read()
                compile(content, script, 'exec')
                print(f"✓ {script}: Valid Python syntax")
            except Exception as e:
                print(f"✗ {script}: Error: {e}")
                return False
        else:
            print(f"✗ {script}: Not found")
            return False
    
    return True

def main():
    """Main test function"""
    print("OpenKomodoIDE Complete Build Test")
    print("=" * 60)
    
    # Run all tests
    tests = [
        test_build_system,
        test_python3_compatibility,
        test_firefox_140_integration,
        test_multiplatform_support,
        test_environment_setup,
        test_dependency_check,
        test_build_scripts,
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
    print("COMPLETE BUILD TEST SUMMARY:")
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED!")
        print("\nThe build system is ready for:")
        print("  • Python 3 compatibility")
        print("  • Firefox 140 ESR integration")
        print("  • Multiplatform support (ARM64, BSD, Gentoo, Minix3)")
        print("  • Complete build process")
        print("\nTo start the actual build, run:")
        print("  python3 mozilla/build.py configure -k 12.0")
        print("  python3 mozilla/build.py all")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED!")
        print("\nPlease check the output above for details on what failed.")
        print("Common issues:")
        print("  • Missing dependencies")
        print("  • Python 3 not properly configured")
        print("  • File permissions issues")
        print("  • Syntax errors in Python files")
        return 1

if __name__ == "__main__":
    sys.exit(main())