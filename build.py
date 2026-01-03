#!/usr/bin/env python3
"""
OpenKomodoIDE Main Build Script
Simple wrapper around the build automation system
"""

import os
import sys
import subprocess
import argparse

def run_build_automation(args):
    """Run the build automation system with given arguments"""
    cmd = [sys.executable, 'build_automation.py'] + args
    
    try:
        result = subprocess.run(cmd, cwd=os.getcwd())
        return result.returncode == 0
    except Exception as e:
        print(f"Error running build automation: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='OpenKomodoIDE Build System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 build.py configure
  python3 build.py build
  python3 build.py complete
  python3 build.py test
  python3 build.py status
        '''
    )
    
    parser.add_argument('command', nargs='?', default='status',
                       help='Command to run (configure, build, complete, test, status)')
    parser.add_argument('--version', default='12.0',
                       help='Komodo version to build')
    parser.add_argument('--firefox', default='140.0',
                       help='Firefox version to use')
    parser.add_argument('--platform', help='Target platform')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug build')
    parser.add_argument('--no-symbols', action='store_false', dest='symbols',
                       help='Disable crash report symbols')
    parser.add_argument('--clean', action='store_true',
                       help='Clean build before starting')
    parser.add_argument('--targets', nargs='+', default=['all'],
                       help='Specific targets to build')
    parser.add_argument('--jobs', type=int,
                       help='Number of parallel jobs')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Build argument list for build_automation.py
    build_args = [args.command]
    
    if args.version:
        build_args.extend(['--version', args.version])
    if args.firefox:
        build_args.extend(['--firefox', args.firefox])
    if args.platform:
        build_args.extend(['--platform', args.platform])
    if args.debug:
        build_args.append('--debug')
    if args.symbols is not None:
        if not args.symbols:
            build_args.append('--no-symbols')
    if args.clean:
        build_args.append('--clean')
    if args.targets:
        build_args.extend(['--targets'] + args.targets)
    if args.jobs:
        build_args.extend(['--jobs', str(args.jobs)])
    if args.verbose:
        build_args.append('--verbose')
    
    print(f"Running build automation: {' '.join(build_args)}")
    
    success = run_build_automation(build_args)
    
    if success:
        print("Build completed successfully!")
        return 0
    else:
        print("Build failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())