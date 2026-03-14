#!/usr/bin/env python3
import re
import sys

def fix_print_statements(filename):
    """Fix Python 2 print statements to Python 3 syntax"""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Fix print statements with quotes
    content = re.sub(r'print "([^"]*)"', r'print("\1")', content)
    content = re.sub(r'print \'([^\']*)\'', r'print(\'\1\')', content)
    
    # Fix print statements with variables
    content = re.sub(r'print ([^#]*)', lambda m: f'print({m.group(1)})' if not m.group(1).strip().startswith('#') else m.group(0), content)
    
    with open(filename, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 fix_prints.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    print(f"Fixing print statements in {filename}...")
    fix_print_statements(filename)
    print("Done!")