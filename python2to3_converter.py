#!/usr/bin/env python3
"""
Custom Python 2 to Python 3 converter for OpenKomodoIDE
Focuses on specific conversion patterns needed for this project
"""

import os
import re
import sys
from pathlib import Path

def convert_file(file_path):
    """Convert a single Python file from Python 2 to Python 3"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Convert print statements
        # print "hello" -> print("hello")
        content = re.sub(r'print\s+(["\'])(.*?)\1', r'print(\1\2\1)', content)
        # print 'hello' -> print('hello')
        content = re.sub(r'print\s+(["\'])(.*?)\1', r'print(\1\2\1)', content)
        # print variable -> print(variable)
        content = re.sub(r'print\s+([a-zA-Z_][a-zA-Z0-9_]*\b)', r'print(\1)', content)
        # print variable, -> print(variable)
        content = re.sub(r'print\s+([a-zA-Z_][a-zA-Z0-9_]*\b),', r'print(\1)', content)
        
        # 2. Convert exception syntax
        # except Exception, e: -> except Exception as e:
        content = re.sub(r'except\s+([\w\.]+),\s*([a-zA-Z_][a-zA-Z0-9_]*)', r'except \1 as \2', content)
        
        # 3. Convert xrange to range
        content = re.sub(r'\bxrange\b', 'range', content)
        
        # 4. Convert dict methods
        content = re.sub(r'\.has_key\(', '.keys()', content)
        content = re.sub(r'\.iteritems\(', '.items()', content)
        content = re.sub(r'\.iterkeys\(', '.keys()', content)
        content = re.sub(r'\.itervalues\(', '.values()', content)
        
        # 5. Convert string methods
        content = re.sub(r'\.decode\(', '.encode()', content)  # This is simplified
        
        # 6. Convert import statements
        content = re.sub(r'from\s+urllib2\s+import\s+', 'from urllib.request import ', content)
        content = re.sub(r'from\s+urlparse\s+import\s+', 'from urllib.parse import ', content)
        
        # 7. Convert raw_input to input
        content = re.sub(r'\braw_input\(', 'input(', content)
        
        # 8. Convert unicode literals
        content = re.sub(r'\bunicode\(', 'str(', content)
        
        # 9. Convert long to int
        content = re.sub(r'\blong\b', 'int', content)
        
        # 10. Convert exec statement
        content = re.sub(r'\bexec\s+([^#]*)', r'exec(\1)', content)
        
        # Only write back if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error converting {file_path}: {e}")
        return False

def find_python_files(directory):
    """Find all Python files in the given directory"""
    python_files = []
    
    for root, dirs, files in os.walk(directory):
        # Skip some directories
        if any(skip_dir in root for skip_dir in ['.git', '__pycache__', 'node_modules', '.hg', '.svn', 'build', 'dist']):
            continue
            
        for file in files:
            if file.endswith('.py') and not file.startswith('.'):
                python_files.append(os.path.join(root, file))
    
    return python_files

def main():
    print("Starting custom Python 2 to Python 3 conversion...")
    
    # Start with critical directories for build system
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
            
            if convert_file(file_path):
                converted_files += 1
                print("✓")
            else:
                failed_files += 1
                print("✗")
    
    print(f"\nConversion complete!")
    print(f"Total files processed: {total_files}")
    print(f"Files with changes: {converted_files}")
    print(f"Files without changes: {failed_files}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())