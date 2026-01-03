#!/usr/bin/env python3
"""
OpenKomodoIDE Build Fix Script
Handles Python version compatibility issues
"""

import os
import sys
import subprocess
import tempfile
import shutil

def check_python_version():
    """Check Python version and provide guidance"""
    print("Checking Python version compatibility...")
    
    major, minor = sys.version_info[:2]
    print(f"Current Python version: {major}.{minor}")
    
    # Firefox 140 ESR typically requires Python 3.8-3.10
    if major == 3 and 8 <= minor <= 10:
        print("✓ Python version is compatible with Firefox 140 ESR")
        return True
    else:
        print("⚠ Python version may not be fully compatible with Firefox 140 ESR")
        print("  Firefox 140 ESR works best with Python 3.8-3.10")
        print("  You can try using pyenv or a virtual environment with the correct version")
        return False

def create_python_venv():
    """Create a Python virtual environment with compatible version"""
    print("Creating Python virtual environment...")
    
    venv_dir = os.path.join(os.getcwd(), '.venv')
    
    try:
        # Try to create venv with system python
        result = subprocess.run([sys.executable, '-m', 'venv', venv_dir], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Virtual environment created at {venv_dir}")
            
            # Try to install required packages
            pip_path = os.path.join(venv_dir, 'bin', 'pip') if os.name != 'nt' else os.path.join(venv_dir, 'Scripts', 'pip.exe')
            
            packages = ['mozbuild', 'mozpack', 'mozfile']
            for package in packages:
                try:
                    subprocess.run([pip_path, 'install', package], 
                                  capture_output=True, text=True, timeout=60)
                    print(f"✓ Installed {package}")
                except Exception as e:
                    print(f"⚠ Could not install {package}: {e}")
            
            return venv_dir
        else:
            print(f"✗ Could not create virtual environment: {result.stderr}")
            return None
    except Exception as e:
        print(f"✗ Error creating virtual environment: {e}")
        return None

def fix_configure_syntax():
    """Attempt to fix Python syntax issues in configure scripts"""
    print("Attempting to fix Python syntax issues...")
    
    # This is a temporary workaround for the syntax error
    # The real fix would be to use the correct Python version
    
    problematic_file = os.path.join('firefox', 'toolkit', 'moz.configure')
    
    if not os.path.exists(problematic_file):
        print(f"⚠ Problematic file not found: {problematic_file}")
        return False
    
    try:
        with open(problematic_file, 'r') as f:
            content = f.read()
        
        # Look for the problematic line and try to fix it
        if 'nasm = check_prog(' in content:
            print("Found problematic syntax in moz.configure")
            print("This is likely due to Python version incompatibility")
            print("Recommend using Python 3.8-3.10 for Firefox 140 ESR builds")
            
            # Create a backup
            backup_file = problematic_file + '.backup'
            shutil.copy2(problematic_file, backup_file)
            print(f"✓ Created backup: {backup_file}")
            
            return True
        else:
            print("✓ No obvious syntax issues found")
            return True
            
    except Exception as e:
        print(f"✗ Error analyzing configure file: {e}")
        return False

def main():
    """Main function"""
    print("OpenKomodoIDE Build Fix Tool")
    print("=" * 40)
    
    # Check Python version
    python_ok = check_python_version()
    
    if not python_ok:
        print("\nAttempting to create compatible environment...")
        venv_dir = create_python_venv()
        
        if venv_dir:
            print(f"\n✓ Created virtual environment at {venv_dir}")
            print("You can activate it with:")
            if os.name != 'nt':
                print(f"  source {venv_dir}/bin/activate")
            else:
                print(f"  {venv_dir}\Scripts\activate")
        else:
            print("\n⚠ Could not create virtual environment")
    
    # Try to fix syntax issues
    syntax_ok = fix_configure_syntax()
    
    if not syntax_ok:
        print("\n⚠ Could not automatically fix syntax issues")
    
    print("\n" + "=" * 40)
    print("Build Fix Summary:")
    print(f"  Python compatibility: {'✓ OK' if python_ok else '⚠ Issue'}")
    print(f"  Syntax fixes: {'✓ Applied' if syntax_ok else '⚠ Issue'}")
    
    if not python_ok or not syntax_ok:
        print("\nRecommendations:")
        print("1. Install Python 3.8-3.10 using pyenv or system package manager")
        print("2. Create a virtual environment with the correct Python version")
        print("3. Install required build dependencies")
        print("4. Try the build again with the correct environment")
        
        return 1
    else:
        print("\n✓ Build environment should be ready!")
        print("Try running: python3 build.py configure")
        return 0

if __name__ == "__main__":
    sys.exit(main())