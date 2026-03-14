#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build script for Komodo with support for both Edit and IDE versions.
Usage:
    python build_komodo.py --build-type edit   # For Komodo Edit
    python build_komodo.py --build-type ide    # For Komodo IDE (default)
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from build_config import build_config


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Build Komodo Edit or IDE')
    parser.add_argument('--build-type', choices=['edit', 'ide'], default='ide',
                       help='Specify build type: edit or ide (default: ide)')
    parser.add_argument('--clean', action='store_true',
                       help='Clean build directory before building')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('--package', action='store_true',
                       help='Create installable package')
    return parser.parse_args()


def configure_build(build_type):
    """Configure the build based on type"""
    build_config.load_from_file()
    build_config.set_build_type(build_type)
    
    # Save the configuration
    build_config.save_to_file()
    
    print(f"Configured for {build_type} build")
    print(f"Product type: {build_config.productType}")


def clean_build():
    """Clean the build directory"""
    build_dir = PROJECT_ROOT / 'build'
    if build_dir.exists():
        print(f"Cleaning build directory: {build_dir}")
        for item in build_dir.iterdir():
            if item.is_dir():
                subprocess.run(['rm', '-rf', str(item)], check=True)
            else:
                item.unlink()
        print("Build directory cleaned")


def run_modern_build():
    """Run the modern build system"""
    # Use the modern build.py script
    cmd = [sys.executable, str(PROJECT_ROOT / 'build.py')]
    
    if build_config.verbose:
        print(f"Running modern build: {' '.join(cmd)}")
    
    result = subprocess.run(cmd)
    return result.returncode


def create_package():
    """Create installable package"""
    # Use the langpack task as a template for packaging
    cmd = [sys.executable, str(PROJECT_ROOT / 'Makefile.py'), 'langpack']
    
    if build_config.verbose:
        print(f"Creating package: {' '.join(cmd)}")
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main build function"""
    args = parse_arguments()
    
    # Configure build
    configure_build(args.build_type)
    
    # Clean if requested
    if args.clean:
        clean_build()
    
    # Run the modern build
    print(f"\nStarting {args.build_type} build with modern build system...")
    return_code = run_modern_build()
    
    if return_code != 0:
        print(f"Error: Build failed with return code {return_code}")
        sys.exit(return_code)
    
    # Create package if requested
    if args.package:
        print(f"\nCreating {args.build_type} package...")
        return_code = create_package()
        if return_code != 0:
            print(f"Error: Package creation failed with return code {return_code}")
            sys.exit(return_code)
        print(f"\n{args.build_type.capitalize()} package created successfully!")
    else:
        print(f"\n{args.build_type.capitalize()} build completed successfully!")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
