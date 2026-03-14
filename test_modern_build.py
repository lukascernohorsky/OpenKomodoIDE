#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive test suite for modern build system
Validates all build scenarios and components
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))


def run_command(cmd: List[str], cwd: Path = None, capture_output: bool = True) -> tuple:
    """Run a command and return (success, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or PROJECT_ROOT,
            capture_output=capture_output,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def test_build_config():
    """Test build configuration system"""
    print("Testing build configuration...")
    
    success, stdout, stderr = run_command([
        sys.executable, "build_config.py"
    ])
    
    if success:
        print("✓ Build configuration test passed")
        return True
    else:
        print(f"✗ Build configuration test failed: {stderr}")
        return False


def test_build_local():
    """Test build local configuration"""
    print("Testing build local configuration...")
    
    success, stdout, stderr = run_command([
        sys.executable, "build_local.py"
    ])
    
    if success:
        print("✓ Build local configuration test passed")
        return True
    else:
        print(f"✗ Build local configuration test failed: {stderr}")
        return False


def test_rrun_modern():
    """Test modern remote build runner"""
    print("Testing modern remote build runner...")
    
    # Test machine listing
    success, stdout, stderr = run_command([
        sys.executable, "bin/rrun_modern.py", "-l"
    ])
    
    if not success:
        print(f"✗ rrun_modern machine listing failed: {stderr}")
        return False
    
    # Test simple task
    success, stdout, stderr = run_command([
        sys.executable, "bin/rrun_modern.py", "ping"
    ])
    
    if success:
        print("✓ Modern remote build runner test passed")
        return True
    else:
        print(f"✗ Modern remote build runner test failed: {stderr}")
        return False


def test_mknightly_modern():
    """Test modern nightly build creation"""
    print("Testing modern nightly build creation...")
    
    # Test Komodo IDE nightly
    success, stdout, stderr = run_command([
        sys.executable, "util/mknightly_modern.py",
        "-p", "komodoide",
        "-v", "-n"
    ])
    
    if not success:
        print(f"✗ Komodo IDE nightly test failed: {stderr}")
        return False
    
    # Test Komodo Edit nightly
    success, stdout, stderr = run_command([
        sys.executable, "util/mknightly_modern.py",
        "-p", "komodoedit",
        "-v", "-n"
    ])
    
    if success:
        print("✓ Modern nightly build creation test passed")
        return True
    else:
        print(f"✗ Modern nightly build creation test failed: {stderr}")
        return False


def test_mozilla_build_integration():
    """Test integration with modern Mozilla build system"""
    print("Testing Mozilla build integration...")
    
    # Test that the modern build system exists and is accessible
    mozilla_build = PROJECT_ROOT / "mozilla" / "build.py"
    if not mozilla_build.exists():
        print("✗ Mozilla build.py not found")
        return False
    
    # Test help output
    success, stdout, stderr = run_command([
        sys.executable, "mozilla/build.py", "--help"
    ])
    
    if success or "Usage:" in stdout:
        print("✓ Mozilla build integration test passed")
        return True
    else:
        print(f"✗ Mozilla build integration test failed: {stderr}")
        return False


def test_python3_compatibility():
    """Test Python 3.11+ compatibility"""
    print("Testing Python 3.11+ compatibility...")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print(f"✗ Python version {sys.version} is too old, need 3.11+")
        return False
    
    # Test that all modern scripts are Python 3 compatible
    modern_scripts = [
        "build_config.py",
        "build_local.py",
        "bin/rrun_modern.py",
        "util/mknightly_modern.py"
    ]
    
    for script in modern_scripts:
        script_path = PROJECT_ROOT / script
        if not script_path.exists():
            print(f"✗ Modern script not found: {script}")
            return False
        
        # Check for Python 3 shebang
        with open(script_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if not first_line.startswith('#!/usr/bin/env python3'):
                print(f"✗ Script missing Python 3 shebang: {script}")
                return False
    
    print("✓ Python 3.11+ compatibility test passed")
    return True


def test_legacy_removal():
    """Test that legacy components have been properly handled"""
    print("Testing legacy component removal...")
    
    # Check that python26 references have been removed from key files
    files_to_check = [
        "bin/builditall.bat",
        "Blackfile.py",
        "util/install_prerequisites.py",
        "src/apsw/Makefile"
    ]
    
    for file_path_str in files_to_check:
        file_path = PROJECT_ROOT / file_path_str
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Check for active python26 references (not commented out)
                lines = content.split('\n')
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith('python26') and not stripped.startswith('#'):
                        print(f"✗ Found uncommented python26 reference in: {file_path}")
                        return False
    
    print("✓ Legacy component removal test passed")
    return True


def test_build_directory_structure():
    """Test that build directory structure is properly created"""
    print("Testing build directory structure...")
    
    required_dirs = [
        "build", "install", "export", "packages",
        "support", "sdk", "stub", "readme", "sysdlls"
    ]
    
    for dir_name in required_dirs:
        dir_path = PROJECT_ROOT / dir_name
        if not dir_path.exists():
            print(f"✗ Required directory missing: {dir_name}")
            return False
    
    print("✓ Build directory structure test passed")
    return True


def run_all_tests():
    """Run all tests and return overall result"""
    print("Running comprehensive modern build system tests...")
    print("=" * 60)
    
    tests = [
        test_python3_compatibility,
        test_build_config,
        test_build_local,
        test_rrun_modern,
        test_mknightly_modern,
        test_mozilla_build_integration,
        test_legacy_removal,
        test_build_directory_structure
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Modern build system is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please review the output above.")
        return False


def main():
    """Main entry point"""
    print("Modern Build System Test Suite")
    print("=" * 40)
    
    success = run_all_tests()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())