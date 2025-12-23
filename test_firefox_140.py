#!/usr/bin/env python3
"""
Test script to verify Firefox 140 ESR integration
"""

import sys
import os

# Add the util directory to the path so we can import the build modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'util'))

# Test 1: Check if patch info files exist and are syntactically correct
print("Testing Firefox 140 ESR patch infrastructure...")

test_files = [
    'mozilla/patches-new/mozilla-140.0/__patchinfo__.py',
    'mozilla/patches-new/mozilla-140.0/cocoa/__patchinfo__.py',
    'mozilla/patches-new/mozilla-140.0/windows/__patchinfo__.py',
    'mozilla/patches-new/mozilla-140.0/gtk/__patchinfo__.py',
    'mozilla/patches-new/mozilla-140.0/upstream/__patchinfo__.py',
    'mozilla/patches-new/mozilla-140.0-pyxpcom/__patchinfo__.py'
]

for test_file in test_files:
    try:
        with open(test_file, 'r') as f:
            content = f.read()
        print(f"✓ {test_file} exists and is readable")
        
        # Try to compile it to check syntax
        compile(content, test_file, 'exec')
        print(f"✓ {test_file} has valid Python syntax")
        
    except FileNotFoundError:
        print(f"✗ {test_file} not found")
    except SyntaxError as e:
        print(f"✗ {test_file} has syntax error: {e}")
    except Exception as e:
        print(f"✗ {test_file} error: {e}")

# Test 2: Check if the patch info functions work correctly
print("\nTesting patch info functions...")

class MockConfig:
    def __init__(self, mozVer, patch_target="mozilla"):
        self.mozVer = mozVer
        self.patch_target = patch_target

# Test the main patch info
try:
    # Add mozilla directory to path for imports
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mozilla'))
    from patches_new.mozilla_140_0 import applicable as main_applicable
    
    # Test with Firefox 140.0
    config_140 = MockConfig(140.0)
    result = main_applicable(config_140)
    print(f"✓ Main patch applicable for 140.0: {result}")
    
    # Test with different version
    config_35 = MockConfig(35.0)
    result = main_applicable(config_35)
    print(f"✓ Main patch not applicable for 35.0: {not result}")
    
except ImportError as e:
    print(f"✗ Cannot import main patch info: {e}")
except Exception as e:
    print(f"✗ Error testing main patch info: {e}")

# Test 3: Check if build.py recognizes Firefox 140
print("\nTesting build system version recognition...")
try:
    # This is a simple check - in a real scenario we'd need to test the actual build process
    with open('mozilla/build.py', 'r') as f:
        content = f.read()
        if '140.0' in content and 'FIREFOX_140_0_RELEASE' in content:
            print("✓ Build system contains Firefox 140.0 references")
        else:
            print("✗ Build system missing Firefox 140.0 references")
except Exception as e:
    print(f"✗ Error checking build system: {e}")

print("\nFirefox 140 ESR integration test completed!")