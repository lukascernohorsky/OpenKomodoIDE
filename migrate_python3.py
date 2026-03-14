#!/usr/bin/env python3
"""
Script to automate Python 2 to Python 3 conversion for OpenKomodoIDE
"""

import os
import subprocess
import sys
from pathlib import Path

def find_python_files(directory):
    """Find all Python files in the given directory"""
    python_files = []
    
    for root, dirs, files in os.walk(directory):
        # Skip some directories that might contain generated files or third-party code
        if any(skip_dir in root for skip_dir in ['.git', '__pycache__', 'node_modules', '.hg', '.svn', 'build', 'dist']):
            continue
            
        for file in files:
            if file.endswith('.py') and not file.startswith('.'):
                python_files.append(os.path.join(root, file))
    
    return python_files

def run_2to3_conversion(file_path, backup=True):
    """Run 2to3 conversion on a single file"""
    try:
        cmd = ['/usr/bin/2to3', '--write', '--no-diffs']
        if backup:
            cmd.append('--backup')
        cmd.append(file_path)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"2to3 failed for {file_path}: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error converting {file_path}: {e}")
        return False

def main():
    print("Starting Python 2 to Python 3 conversion...")
    
    # Directories to process - start with critical ones for build system
    directories = [
        'util',
        'mozilla',
        'bin'
    ]
    
    total_files = 0
    converted_files = 0
    failed_files = 0
    
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist, skipping...")
            continue
            
        print(f"Processing directory: {directory}")
        python_files = find_python_files(directory)
        
        for file_path in python_files:
            total_files += 1
            print(f"Converting {file_path}...", end=" ")
            
            if run_2to3_conversion(file_path):
                converted_files += 1
                print("✓")
            else:
                failed_files += 1
                print("✗")
    
    print(f"\nConversion complete!")
    print(f"Total files processed: {total_files}")
    print(f"Successfully converted: {converted_files}")
    print(f"Failed conversions: {failed_files}")
    
    if failed_files > 0:
        print("\nSome files failed to convert. Check the output above for details.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())