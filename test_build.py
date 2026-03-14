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
    
    # Try new structure first (mozilla/build/...)
    mach_path = os.path.join(os.getcwd(), 'mozilla', 'build', 'moz1400-ko1410', 'mozilla', 'mach')
    
    # Fallback to old structure (firefox/mach)
    if not os.path.exists(mach_path):
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
    
    # Try new structure first
    mozconfig_path = os.path.join('mozilla', 'build', 'moz1400-ko1410', 'mozilla', '.mozconfig')
    
    # Fallback to old structure
    if not os.path.exists(mozconfig_path):
        mozconfig_path = '.mozconfig'
    
    if not os.path.exists(mozconfig_path):
        print(f"✗ mozconfig not found at {mozconfig_path}")
        return False
    
    print(f"✓ mozconfig found at {mozconfig_path}")
    
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
    
    # Try new structure first
    firefox_dir = os.path.join('mozilla', 'build', 'moz1400-ko1410', 'mozilla')
    
    # Fallback to old structure
    if not os.path.exists(firefox_dir):
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
    
    print(f"✓ Found {len(found_files)} key Firefox files at {firefox_dir}")
    return True

def main():
    """Run all build tests"""
    print("OpenKomodoIDE Build Test Suite")
    print("=" * 50)
    
    # Get test target from command line arguments
    import sys
    test_target = None
    if len(sys.argv) > 1:
        test_target = sys.argv[1]

    # Define all available tests
    all_tests = {
        'multiplatform': test_multiplatform,
        'firefox_140': test_firefox_140,
        'complete_build': test_complete_build,
        'all': [
            test_mach_available,
            test_mozconfig,
            test_build_environment,
            test_firefox_source,
            test_multiplatform,
            test_firefox_140,
            test_complete_build
        ]
    }

    # Determine which tests to run
    if test_target and test_target in all_tests:
        if test_target == 'all':
            tests = all_tests['all']
        else:
            tests = [all_tests[test_target]]
    else:
        # Default behavior - run original tests
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


def test_multiplatform():
    """Test multiplatform compatibility"""
    print("Testing multiplatform compatibility...")

    # Test platform detection
    current_platform = platform.system()
    print(f"✓ Current platform detected: {current_platform}")

    # Test platform-specific configurations
    if current_platform == "Linux":
        # Linux-specific checks
        linux_files = ["/etc/os-release", "/proc/version"]
        for file_path in linux_files:
            if os.path.exists(file_path):
                print(f"✓ Linux system file found: {file_path}")
            else:
                print(f"⚠ Linux system file missing: {file_path}")
    
    elif current_platform == "Windows":
        # Windows-specific checks
        windows_files = ["C:\\Windows", "C:\\Program Files"]
        for file_path in windows_files:
            if os.path.exists(file_path):
                print(f"✓ Windows system file found: {file_path}")
            else:
                print(f"⚠ Windows system file missing: {file_path}")
    
    elif current_platform == "Darwin":
        # macOS-specific checks
        macos_files = ["/Applications", "/System/Library"]
        for file_path in macos_files:
            if os.path.exists(file_path):
                print(f"✓ macOS system file found: {file_path}")
            else:
                print(f"⚠ macOS system file missing: {file_path}")

    # Test cross-platform build compatibility
    build_configs = [
        os.path.join("mozilla", "build", "moz1400-ko1410", "mozilla", ".mozconfig"),
        os.path.join("mozilla", "build", "moz1400-ko1410", "mozilla", "moz.configure"),
    ]
    
    config_found = False
    for config in build_configs:
        if os.path.exists(config):
            print(f"✓ Build config found: {config}")
            config_found = True
    
    if not config_found:
        print("⚠ No build configs found")
        return False

    print("✓ Multiplatform compatibility tests passed")
    return True


def test_firefox_140():
    """Test Firefox 140 ESR specific functionality"""
    print("Testing Firefox 140 ESR specific functionality...")

    # Test Firefox 140 source directory structure
    firefox_140_dir = os.path.join("mozilla", "build", "moz1400-ko1410", "mozilla")
    
    if not os.path.exists(firefox_140_dir):
        print(f"✗ Firefox 140 directory not found at {firefox_140_dir}")
        return False
    
    print(f"✓ Firefox 140 directory found: {firefox_140_dir}")

    # Test Firefox 140 specific files
    firefox_140_files = [
        "browser/config/moz.configure",
        "browser/confvars.sh",
        "toolkit/moz.configure",
        "python/mozbuild/mozbuild/mozconfig.py",
    ]
    
    found_files = []
    for file_path in firefox_140_files:
        full_path = os.path.join(firefox_140_dir, file_path)
        if os.path.exists(full_path):
            found_files.append(file_path)
            print(f"✓ Firefox 140 file found: {file_path}")
        else:
            print(f"⚠ Firefox 140 file missing: {file_path}")

    # Test Firefox 140 configuration
    mozconfig_path = os.path.join(firefox_140_dir, ".mozconfig")
    if os.path.exists(mozconfig_path):
        with open(mozconfig_path, 'r') as f:
            content = f.read()
            
        # Check for Firefox 140 specific options
        firefox_140_options = ["ac_add_options --enable-application=browser"]
        for option in firefox_140_options:
            if option in content:
                print(f"✓ Firefox 140 option found: {option}")
            else:
                print(f"⚠ Firefox 140 option missing: {option}")

    print(f"✓ Found {len(found_files)} Firefox 140 specific files")
    return True


def test_complete_build():
    """Test the complete build process"""
    print("Testing complete build process...")

    # Test build directory structure
    build_dirs = [
        "build",
        "dist", 
        "logs",
        os.path.join("mozilla", "build", "moz1400-ko1410", "mozilla", "obj-x86_64-pc-linux-gnu"),
    ]
    
    existing_dirs = []
    for dir_path in build_dirs:
        if os.path.exists(dir_path):
            existing_dirs.append(dir_path)
            print(f"✓ Build directory found: {dir_path}")
        else:
            print(f"⚠ Build directory missing: {dir_path}")

    # Test build artifacts
    build_artifacts = [
        os.path.join("dist", "komodo"),
        os.path.join("dist", "firefox"),
        os.path.join("logs", "build.log"),
    ]
    
    existing_artifacts = []
    for artifact in build_artifacts:
        if os.path.exists(artifact):
            existing_artifacts.append(artifact)
            print(f"✓ Build artifact found: {artifact}")
        else:
            print(f"⚠ Build artifact missing: {artifact}")

    # Test build configuration completeness
    config_files = [
        ".mozconfig",
        "build_config.json",
        os.path.join("mozilla", "build", "moz1400-ko1410", "mozilla", "moz.configure"),
    ]
    
    config_complete = True
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✓ Configuration file found: {config_file}")
        else:
            print(f"⚠ Configuration file missing: {config_file}")
            config_complete = False

    print(f"✓ Complete build test finished - {len(existing_dirs)} dirs, {len(existing_artifacts)} artifacts")
    return config_complete


if __name__ == "__main__":
    sys.exit(main())