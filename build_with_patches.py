#!/usr/bin/env python3
"""
Enhanced Build System with Automatic Patch Application
Ensures all dependency fixes are applied before building
"""

import os
import subprocess
import sys

def apply_patches():
    """Apply all dependency patches"""
    patch_script = os.path.join(os.path.dirname(__file__), 'apply_patches.py')
    
    if os.path.exists(patch_script):
        print("🔧 Applying dependency patches...")
        result = subprocess.run([sys.executable, patch_script], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Patches applied successfully")
            return True
        else:
            print(f"❌ Patch application failed: {result.stderr}")
            return False
    else:
        print("ℹ No patch applier found, proceeding without patches")
        return True

def main():
    """Main build function with patch application"""
    # Apply patches first
    if not apply_patches():
        return 1
    
    # Then run the normal build
    build_script = os.path.join(os.path.dirname(__file__), 'build.py')
    
    # Pass all arguments to the original build script
    result = subprocess.run([sys.executable, build_script] + sys.argv[1:], capture_output=False)
    
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())
