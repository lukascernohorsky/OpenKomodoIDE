#!/usr/bin/env python3
"""
OpenKomodoIDE Build Completion Verification
Verifies that the build is 100% complete with all required artifacts
"""

import os
import sys
import subprocess
from pathlib import Path

def check_build_artifacts():
    """Check if all required build artifacts exist"""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    print("🔍 Verifying OpenKomodoIDE Build Completion")
    print("=" * 50)
    
    # Check modern Firefox build artifacts
    firefox_src_dir = os.path.join(base_dir, 'mozilla', 'build', 'moz1400-ko1410', 'mozilla')
    
    required_artifacts = [
        ('Firefox binary', os.path.join(firefox_src_dir, 'obj-x86_64-pc-linux-gnu', 'dist', 'bin', 'firefox')),
        ('Firefox binary (alternative)', os.path.join(firefox_src_dir, 'obj-x86_64-pc-linux-gnu', 'dist', 'bin', 'firefox-bin')),
        ('Distribution Firefox', os.path.join(base_dir, 'dist', 'bin', 'firefox')),
        ('Build directory', os.path.join(base_dir, 'build')),
        ('Dist directory', os.path.join(base_dir, 'dist')),
        ('Shared libraries (libxul.so)', os.path.join(firefox_src_dir, 'obj-x86_64-pc-linux-gnu', 'dist', 'bin', 'libxul.so')),
        ('Shared libraries (libmozglue.so)', os.path.join(firefox_src_dir, 'obj-x86_64-pc-linux-gnu', 'dist', 'bin', 'libmozglue.so')),
    ]
    
    missing_artifacts = []
    found_artifacts = []
    
    for name, path in required_artifacts:
        if os.path.exists(path):
            found_artifacts.append(name)
            print(f"✅ {name} found at {path}")
        else:
            missing_artifacts.append(name)
            print(f"❌ {name} missing from {path}")
    
    print(f"\n📊 Summary:")
    print(f"   Found: {len(found_artifacts)} artifacts")
    print(f"   Missing: {len(missing_artifacts)} artifacts")
    
    if missing_artifacts:
        print(f"\n❌ Build INCOMPLETE - missing artifacts: {', '.join(missing_artifacts)}")
        return False
    else:
        print(f"\n✅ Build COMPLETE - all required artifacts present!")
        
        # Additional verification: check if Firefox binary is executable
        firefox_path = os.path.join(base_dir, 'dist', 'bin', 'firefox')
        if os.path.exists(firefox_path) and os.access(firefox_path, os.X_OK):
            print(f"✅ Firefox binary is executable")
            
            # Check binary size (should be reasonable for a browser)
            size_mb = os.path.getsize(firefox_path) / (1024 * 1024)
            print(f"✅ Firefox binary size: {size_mb:.1f} MB")
            
            if size_mb > 50:  # Firefox should be >50MB
                print(f"✅ Firefox binary size is reasonable for a complete build")
            else:
                print(f"⚠️  Firefox binary size seems small - may be incomplete")
        
        return True

def check_build_configuration():
    """Check if build configuration is properly set up"""
    print(f"\n🔧 Checking Build Configuration")
    print("-" * 30)
    
    config_file = 'build_config.json'
    if os.path.exists(config_file):
        print(f"✅ Build configuration file exists")
        return True
    else:
        print(f"❌ Build configuration file missing")
        return False

def main():
    """Main verification function"""
    print("OpenKomodoIDE Build Completion Verification")
    print("=" * 60)
    
    # Check artifacts
    artifacts_ok = check_build_artifacts()
    
    # Check configuration
    config_ok = check_build_configuration()
    
    print(f"\n" + "=" * 60)
    if artifacts_ok and config_ok:
        print("🎉 BUILD COMPLETION: 100% ✅")
        print("\nThe build is complete and ready for:")
        print("  • Testing")
        print("  • Packaging")
        print("  • Distribution")
        print("  • Deployment")
        return 0
    else:
        print("💥 BUILD COMPLETION: INCOMPLETE ❌")
        print("\nPlease run the complete build process:")
        print("  python3 build_automation.py build --targets all")
        return 1

if __name__ == "__main__":
    sys.exit(main())
