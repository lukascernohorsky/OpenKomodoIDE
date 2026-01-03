#!/usr/bin/env python3
"""
OpenKomodoIDE Build Test Script
Tests basic build functionality
"""

import os
import sys
import subprocess
import platform

def test_mach_available():
    """Test if Firefox mach build system is available"""
    print("Testing Firefox mach availability...")
    
    mach_path = os.path.join(os.getcwd(), 'firefox', 'mach')
    if not os.path.exists(mach_path):
        print(f"✗ Firefox mach not found at {mach_path}")
        return False
    
    print(f"✓ Firefox mach found at {mach_path}")
    
    # Test if mach is executable
    try:
        result = subprocess.run([mach_path, '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ Mach is executable and responds to --help")
            return True
        else:
            print(f"✗ Mach help failed with code {result.returncode}")
            print(f"stderr: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error testing mach: {e}")
        return False

def test_mozconfig():
    """Test if mozconfig file exists and is valid"""
    print("Testing mozconfig...")
    
    mozconfig_path = 'mozconfig'
    if not os.path.exists(mozconfig_path):
        print(f"✗ mozconfig not found at {mozconfig_path}")
        return False
    
    print(f"✓ mozconfig found")
    
    # Check if it contains basic required options
    with open(mozconfig_path, 'r') as f:
        content = f.read()
    
    required_options = ['ac_add_options', 'mk_add_options', 'MOZ_OBJDIR']
    for option in required_options:
        if option in content:
            print(f"✓ Found {option} in mozconfig")
        else:
            print(f"⚠ Missing {option} in mozconfig")
    
    return True

def test_build_environment():
    """Test if basic build environment is set up"""
    print("Testing build environment...")
    
    # Test required tools
    required_tools = ['python3', 'git', 'make']
    if platform.system() == 'Windows':
        required_tools.extend(['cl', 'link'])
    else:
        required_tools.extend(['gcc', 'g++'])
    
    missing_tools = []
    for tool in required_tools:
        try:
            result = subprocess.run([tool, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✓ {tool} available")
            else:
                missing_tools.append(tool)
        except Exception as e:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"✗ Missing tools: {', '.join(missing_tools)}")
        return False
    
    print("✓ All required tools available")
    return True

def test_firefox_source():
    """Test if Firefox source is properly integrated"""
    print("Testing Firefox source integration...")
    
    firefox_dir = 'firefox'
    if not os.path.exists(firefox_dir):
        print(f"✗ Firefox directory not found")
        return False
    
    # Check for key Firefox files
    key_files = [
        'configure',
        'mach',
        'moz.configure',
        'browser/app/moz.build'
    ]
    
    found_files = []
    for key_file in key_files:
        full_path = os.path.join(firefox_dir, key_file)
        if os.path.exists(full_path):
            found_files.append(key_file)
            print(f"✓ Found {key_file}")
        else:
            print(f"⚠ Missing {key_file}")
    
    if not found_files:
        print("✗ No key Firefox files found")
        return False
    
    print(f"✓ Found {len(found_files)} key Firefox files")
    return True

def main():
    """Run all build tests"""
    print("OpenKomodoIDE Build Test Suite")
    print("=" * 50)
    
    tests = [
        test_mach_available,
        test_mozconfig,
        test_build_environment,
        test_firefox_source
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print(f"\n{'=' * 50}")
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✓ All tests passed! Build environment is ready.")
        return 0
    else:
        print("✗ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())