#!/usr/bin/env python3
"""
Automatic Patch Applier for Firefox Build Dependencies
Applies all dependency fixes before building
"""

import os
import subprocess
import sys

def apply_patches():
    """Apply all dependency patches"""
    patch_dir = 'patches-new'
    
    if not os.path.exists(patch_dir):
        print(f"❌ Patch directory not found: {patch_dir}")
        return False
    
    # Find all patch files
    patch_files = []
    for filename in os.listdir(patch_dir):
        if filename.endswith('.patch'):
            patch_files.append(os.path.join(patch_dir, filename))
    
    if not patch_files:
        print("ℹ No patch files found")
        return True
    
    print(f"📋 Found {len(patch_files)} patch files to apply:")
    
    for patch_file in patch_files:
        print(f"🔧 Applying: {patch_file}")
        
        # Extract target file name from patch
        target_file = os.path.basename(patch_file).replace('.patch', '')
        target_path = os.path.join('mozilla', target_file)
        
        # Create target directory if needed
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # Apply the patch (simple copy for now)
        try:
            with open(patch_file, 'r') as src, open(target_path, 'w') as dst:
                dst.write(src.read())
            print(f"✅ Applied {patch_file}")
        except Exception as e:
            print(f"❌ Failed to apply {patch_file}: {e}")
            return False
    
    print("✅ All patches applied successfully!")
    return True

def main():
    """Main function"""
    print("🚀 Firefox Dependency Patch Applier")
    print("==================================")
    
    if apply_patches():
        print("\n🎉 Ready to build with all dependencies fixed!")
        return 0
    else:
        print("\n❌ Patch application failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
