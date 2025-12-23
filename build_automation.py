#!/usr/bin/env python3
"""
OpenKomodoIDE Build Automation System
Automates the complete build process across multiple platforms
"""

import os
import sys
import subprocess
import platform
import shutil
import tempfile
import argparse
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class BuildAutomation:
    """Main build automation class"""
    
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.build_dir = os.path.join(self.base_dir, 'build')
        self.dist_dir = os.path.join(self.base_dir, 'dist')
        self.log_dir = os.path.join(self.base_dir, 'logs')
        self.config_file = os.path.join(self.base_dir, 'build_config.json')
        
        # Ensure directories exist
        os.makedirs(self.build_dir, exist_ok=True)
        os.makedirs(self.dist_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Default configuration
        self.config = {
            'platform': self.detect_platform(),
            'version': '12.0',
            'firefox_version': '140.0',
            'build_type': 'release',
            'jobs': max(1, os.cpu_count() - 2) if os.cpu_count() else 1,
            'enable_debug': False,
            'enable_symbols': True,
            'targets': ['all'],
            'clean_build': False,
            'verbose': False,
            'log_file': os.path.join(self.log_dir, f'build_{time.strftime("%Y%m%d_%H%M%S")}.log')
        }
        
        # Load existing config if available
        self.load_config()
    
    def detect_platform(self) -> str:
        """Detect the current platform"""
        plat = sys.platform
        machine = platform.machine()
        
        if plat.startswith("linux"):
            if machine in ("aarch64", "arm64"):
                return "linux-arm64"
            elif os.path.exists("/etc/gentoo-release"):
                return "gentoo"
            else:
                return "linux"
        elif plat.startswith("freebsd"):
            return "freebsd"
        elif plat.startswith("netbsd"):
            return "netbsd"
        elif plat.startswith("openbsd"):
            return "openbsd"
        elif plat.startswith("minix"):
            return "minix3"
        elif plat == "darwin":
            return "macos"
        elif plat == "win32":
            return "windows"
        else:
            return "unknown"
    
    def load_config(self):
        """Load build configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
                print(f"Loaded configuration from {self.config_file}")
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
    
    def save_config(self):
        """Save build configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"Saved configuration to {self.config_file}")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def run_command(self, cmd: str, cwd: Optional[str] = None, 
                   env: Optional[Dict] = None, capture_output: bool = True) -> Tuple[bool, str, str]:
        """Run a command and return the result"""
        try:
            result = subprocess.run(cmd, shell=True, cwd=cwd, env=env, 
                                  capture_output=capture_output, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def setup_environment(self) -> bool:
        """Set up the build environment"""
        print("Setting up build environment...")
        
        # Set environment variables
        env_vars = {
            'PATH': f"{os.path.join(self.base_dir, 'bin')}:{os.environ.get('PATH', '')}",
            'MOZCONFIG': os.path.join(self.base_dir, 'mozconfig'),
            'LD_LIBRARY_PATH': os.path.join(self.base_dir, 'lib'),
            'PLATFORM': self.config['platform'],
            'BUILD_TYPE': self.config['build_type'],
            'MAKEFLAGS': f"-j{self.config['jobs']}"
        }
        
        for key, value in env_vars.items():
            os.environ[key] = value
        
        print(f"Environment set up for {self.config['platform']}")
        return True
    
    def check_dependencies(self) -> bool:
        """Check that all required dependencies are available"""
        print("Checking dependencies...")
        
        required_tools = ['python3', 'git', 'make', 'gcc', 'g++', 'patch', 'zip', 'tar']
        missing_tools = []
        
        for tool in required_tools:
            success, _, _ = self.run_command(f"{tool} --version", capture_output=True)
            if not success:
                missing_tools.append(tool)
        
        if missing_tools:
            print(f"Missing tools: {', '.join(missing_tools)}")
            print("Please install missing dependencies and try again.")
            return False
        
        print("All required dependencies are available")
        return True
    
    def configure_build(self) -> bool:
        """Configure the build"""
        print("Configuring build...")
        
        # Build configure command
        cmd = f"python3 mozilla/build.py configure -k {self.config['version']}"
        
        if self.config['enable_debug']:
            cmd += " --enable-debug"
        
        if self.config['enable_symbols']:
            cmd += " --with-crashreport-symbols"
        
        # Add platform-specific options
        if self.config['platform'] == 'linux-arm64':
            cmd += " --target=aarch64-linux-gnu"
        elif self.config['platform'] in ['freebsd', 'netbsd', 'openbsd']:
            cmd += f" --target={self.config['platform']}"
        
        print(f"Running: {cmd}")
        
        success, stdout, stderr = self.run_command(cmd, cwd=self.base_dir)
        
        if success:
            print("✓ Build configuration successful")
            return True
        else:
            print(f"✗ Build configuration failed: {stderr}")
            return False
    
    def clean_build(self) -> bool:
        """Clean the build directory"""
        print("Cleaning build directory...")
        
        success, stdout, stderr = self.run_command("python3 mozilla/build.py clean", cwd=self.base_dir)
        
        if success:
            print("✓ Build directory cleaned")
            return True
        else:
            print(f"✗ Clean failed: {stderr}")
            return False
    
    def distclean_build(self) -> bool:
        """Completely clean the build"""
        print("Performing distclean...")
        
        success, stdout, stderr = self.run_command("python3 mozilla/build.py distclean", cwd=self.base_dir)
        
        if success:
            print("✓ Distclean successful")
            return True
        else:
            print(f"✗ Distclean failed: {stderr}")
            return False
    
    def build_targets(self) -> bool:
        """Build the specified targets"""
        print(f"Building targets: {', '.join(self.config['targets'])}")
        
        all_success = True
        
        for target in self.config['targets']:
            print(f"\nBuilding target: {target}")
            
            cmd = f"python3 mozilla/build.py {target}"
            print(f"Running: {cmd}")
            
            success, stdout, stderr = self.run_command(cmd, cwd=self.base_dir)
            
            if success:
                print(f"✓ Target {target} built successfully")
            else:
                print(f"✗ Target {target} failed: {stderr}")
                all_success = False
                if not self.config.get('continue_on_error', False):
                    break
        
        return all_success
    
    def create_packages(self) -> bool:
        """Create distribution packages"""
        print("Creating packages...")
        
        success, stdout, stderr = self.run_command("python3 mozilla/build.py packages", cwd=self.base_dir)
        
        if success:
            print("✓ Packages created successfully")
            return True
        else:
            print(f"✗ Package creation failed: {stderr}")
            return False
    
    def run_tests(self) -> bool:
        """Run the test suite"""
        print("Running tests...")
        
        test_scripts = [
            'test_build.py',
            'test_multiplatform.py',
            'test_firefox_140.py',
            'test_complete_build.py'
        ]
        
        all_success = True
        
        for test_script in test_scripts:
            if os.path.exists(test_script):
                print(f"\nRunning {test_script}...")
                success, stdout, stderr = self.run_command(f"python3 {test_script}", cwd=self.base_dir)
                
                if success:
                    print(f"✓ {test_script} passed")
                else:
                    print(f"✗ {test_script} failed")
                    all_success = False
            else:
                print(f"⚠ {test_script} not found")
        
        return all_success
    
    def complete_build(self) -> bool:
        """Perform a complete build from start to finish"""
        print("Starting complete build process...")
        print("=" * 60)
        
        # Set up environment
        if not self.setup_environment():
            return False
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Clean if requested
        if self.config['clean_build']:
            if not self.distclean_build():
                return False
        
        # Configure
        if not self.configure_build():
            return False
        
        # Build
        if not self.build_targets():
            return False
        
        # Create packages
        if not self.create_packages():
            return False
        
        # Run tests
        if not self.run_tests():
            print("⚠ Tests failed, but build completed")
        
        print("\n" + "=" * 60)
        print("✓ COMPLETE BUILD SUCCESSFUL!")
        print(f"\nBuild artifacts available in:")
        print(f"  Build directory: {self.build_dir}")
        print(f"  Distribution: {self.dist_dir}")
        print(f"  Logs: {self.log_dir}")
        
        return True
    
    def show_status(self):
        """Show current build status and configuration"""
        print("Current Build Configuration:")
        print("=" * 40)
        
        for key, value in self.config.items():
            print(f"  {key:20}: {value}")
        
        print("\nPlatform Information:")
        print(f"  System: {platform.system()}")
        print(f"  Release: {platform.release()}")
        print(f"  Machine: {platform.machine()}")
        print(f"  Python: {sys.version}")
        print(f"  CPU Cores: {os.cpu_count()}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='OpenKomodoIDE Build Automation System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 build_automation.py configure
  python3 build_automation.py build
  python3 build_automation.py complete
  python3 build_automation.py test
  python3 build_automation.py status
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
    
    # Create build automation instance
    builder = BuildAutomation()
    
    # Update configuration from command line arguments
    if args.version:
        builder.config['version'] = args.version
    if args.firefox:
        builder.config['firefox_version'] = args.firefox
    if args.platform:
        builder.config['platform'] = args.platform
    if args.debug:
        builder.config['enable_debug'] = True
        builder.config['build_type'] = 'debug'
    if args.symbols is not None:
        builder.config['enable_symbols'] = args.symbols
    if args.clean:
        builder.config['clean_build'] = True
    if args.targets:
        builder.config['targets'] = args.targets
    if args.jobs:
        builder.config['jobs'] = args.jobs
    if args.verbose:
        builder.config['verbose'] = True
    
    # Save updated configuration
    builder.save_config()
    
    # Execute the requested command
    if args.command == 'configure':
        if not builder.configure_build():
            sys.exit(1)
    elif args.command == 'build':
        if not builder.build_targets():
            sys.exit(1)
    elif args.command == 'complete':
        if not builder.complete_build():
            sys.exit(1)
    elif args.command == 'test':
        if not builder.run_tests():
            sys.exit(1)
    elif args.command == 'clean':
        if not builder.clean_build():
            sys.exit(1)
    elif args.command == 'distclean':
        if not builder.distclean_build():
            sys.exit(1)
    elif args.command == 'packages':
        if not builder.create_packages():
            sys.exit(1)
    elif args.command == 'status':
        builder.show_status()
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()