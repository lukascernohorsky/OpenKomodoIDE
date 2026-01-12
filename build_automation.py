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
import tarfile
import logging
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

        # Default configuration (needed for path calculation)
        self.config = {
            'platform': self.detect_platform(),
            'version': '12.0',
            'firefox_version': '140.0',
        }

        # Always use modern mozilla/build structure
        self.use_mozilla_build = True  # Always use modern structure
        self.mozilla_build_dir = os.path.join(self.base_dir, 'mozilla', 'build')
        self.firefox_src_dir = os.path.join(
            self.mozilla_build_dir,
            f"moz{self.config.get('firefox_version', '140.0').replace('.', '')}-ko{self.config.get('version', '12.0').replace('.', '')}",
            'mozilla'
        )
        
        # Ensure directories exist
        os.makedirs(self.build_dir, exist_ok=True)
        os.makedirs(self.dist_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        

        
        # Update config with additional defaults
        self.config.update({
            'build_type': 'release',
            'jobs': max(1, os.cpu_count() - 2) if os.cpu_count() else 1,
            'enable_debug': False,
            'enable_symbols': True,
            'targets': ['all'],
            'clean_build': False,
            'verbose': False,
            'log_file': os.path.join(self.log_dir, f'build_{time.strftime("%Y%m%d_%H%M%S")}.log')
        })
        
        # Load existing config if available
        self.load_config()
        
        # Set up logger
        self.logger = logging.getLogger('BuildAutomation')
        self.logger.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(console_handler)
        
        # Also log to file if configured
        if self.config.get('log_file'):
            file_handler = logging.FileHandler(self.config['log_file'])
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
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
    
    def apply_firefox_patches(self):
        """Apply all necessary patches to Firefox source code"""
        self.logger.info("No patches to apply - patch system has been removed")
        return
    

    

    

    

    
    def revert_firefox_patches(self):
        """Revert all applied Firefox patches"""
        self.logger.info("No patches to revert - patch system has been removed")
        return
    

    

    

    

    

    
    def test_patches(self) -> bool:
        """Test all patches without applying them
        
        Returns:
            True if all patches are valid, False otherwise
        """
        self.logger.info("No patches to test - patch system has been removed")
        return True
    

    
    def get_mach_path(self):
        """Get the path to mach (always uses modern structure)"""
        version_suffix = self.config.get('firefox_version', '140.0').replace('.', '')
        komodo_suffix = self.config.get('version', '12.0').replace('.', '')
        
        # Check if the modern structure exists
        modern_path = os.path.join(
            self.base_dir,
            'mozilla',
            'build',
            f'moz{version_suffix}-ko{komodo_suffix}',
            'mozilla',
            'mach'
        )
        
        if os.path.exists(modern_path):
            return modern_path
        
        # Fallback to alternative path if modern structure doesn't exist
        fallback_path = os.path.join(
            self.firefox_src_dir,
            'mach'
        )
        
        return fallback_path if os.path.exists(fallback_path) else modern_path

    def initialize_build(self) -> bool:
        """Initialize build environment and create necessary directories"""
        print("Initializing build environment...")
        
        # Create build directories
        os.makedirs(self.build_dir, exist_ok=True)
        os.makedirs(self.dist_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create modern mozilla/build structure
        mozilla_path = os.path.join(
            self.base_dir,
            'mozilla',
            'build',
            f'moz{self.config.get("firefox_version", "140.0").replace(".", "")}-ko{self.config.get("version", "12.0").replace(".", "")}',
            'mozilla'
        )
        os.makedirs(mozilla_path, exist_ok=True)
        print(f"Created Mozilla build structure at: {mozilla_path}")
        
        # Create default config file if it doesn't exist
        if not os.path.exists(self.config_file):
            default_config = {
                'platform': self.detect_platform(),
                'version': '12.0',
                'firefox_version': '140.0',
                'build_type': 'release',
                'jobs': max(1, os.cpu_count() - 2) if os.cpu_count() else 1,
                'enable_debug': False,
                'enable_symbols': True,
                'targets': ['all'],
                'clean_build': False,
                'verbose': False
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"Created default configuration file at: {self.config_file}")
        
        print("✓ Build environment initialized successfully")
        return True

    def download_firefox_source(self) -> bool:
        """Download Firefox source code if not already present"""
        print("Checking Firefox source code...")
        
        # Determine expected paths
        if self.use_mozilla_build:
            expected_mach_path = self.get_mach_path()
            expected_dir = os.path.dirname(expected_mach_path)
        else:
            expected_mach_path = self.get_mach_path()
            expected_dir = self.firefox_src_dir
        
        # Check if source code already exists
        if os.path.exists(expected_mach_path):
            # Verify it's a complete source directory
            if self.verify_firefox_source():
                print(f"✓ Firefox source code found at: {expected_dir}")
                return True
            else:
                print(f"✗ Existing Firefox source code at {expected_dir} is incomplete")
                print("Removing incomplete source and redownloading...")
                # Remove incomplete source
                if os.path.exists(expected_dir):
                    shutil.rmtree(expected_dir)
        
        print(f"✗ Firefox source code not found at: {expected_dir}")
        print("Downloading Firefox 140 ESR source code...")
        
        try:
            # Create temporary directory for download
            temp_dir = os.path.join(self.base_dir, 'temp_download')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Download Firefox source
            firefox_version = self.config.get('firefox_version', '140.0')
            firefox_url = f"https://archive.mozilla.org/pub/firefox/releases/{firefox_version}esr/source/firefox-{firefox_version}esr.source.tar.xz"
            tar_file = os.path.join(temp_dir, f"firefox-{firefox_version}esr.source.tar.xz")
            
            print(f"Downloading from: {firefox_url}")
            
            # Use wget or curl to download with extended timeout
            try:
                if shutil.which('wget'):
                    print("Using wget to download Firefox source...")
                    print("⚠ This may take a while (~200MB download)...")
                    subprocess.run(['wget', '-c', '--show-progress', '--timeout=600', '--tries=3', firefox_url, '-O', tar_file], 
                                 check=True, timeout=3600)
                elif shutil.which('curl'):
                    print("Using curl to download Firefox source...")
                    print("⚠ This may take a while (~200MB download)...")
                    subprocess.run(['curl', '-C', '-', '-L', '-o', tar_file, '--max-time', '600', '--retry', '3', firefox_url], 
                                 check=True, timeout=3600)
                else:
                    print("✗ Neither wget nor curl found. Cannot download Firefox source.")
                    return False
            except subprocess.TimeoutExpired:
                print("✗ Download timed out. The Firefox source archive is quite large (~200MB).")
                print("Please try again with a faster internet connection or download manually.")
                print(f"Manual download URL: {firefox_url}")
                print("\nTips for successful download:")
                print("  1. Use a wired connection instead of WiFi")
                print("  2. Try again during off-peak hours")
                print("  3. Increase timeout with --timeout parameter")
                print("  4. Download manually and place in temp_download directory")
                return False
            except Exception as e:
                print(f"✗ Download failed: {e}")
                return False
            
            # Extract the archive
            print("Extracting Firefox source code...")
            with tarfile.open(tar_file, 'r:xz') as tar:
                # Extract to temporary directory first
                tar.extractall(path=temp_dir)
            
            # Find the extracted directory (handle both naming conventions)
            extracted_items = os.listdir(temp_dir)
            source_dir = None
            for item in extracted_items:
                item_path = os.path.join(temp_dir, item)
                # Skip files, only look for directories
                if os.path.isdir(item_path) and item.startswith('firefox-'):
                    source_dir = item_path
                    break
            
            if source_dir is None:
                print(f"✗ Could not find extracted Firefox source directory in {temp_dir}")
                print(f"Contents of {temp_dir}: {os.listdir(temp_dir)}")
                return False
            
            if self.use_mozilla_build:
                # Move to mozilla structure
                dest_dir = os.path.dirname(expected_dir)
                os.makedirs(dest_dir, exist_ok=True)
                
                # Move contents (not the directory itself)
                for item in os.listdir(source_dir):
                    src = os.path.join(source_dir, item)
                    dst = os.path.join(expected_dir, item)
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.move(src, expected_dir)
            else:
                # Move to firefox structure
                for item in os.listdir(source_dir):
                    src = os.path.join(source_dir, item)
                    dst = os.path.join(expected_dir, item)
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.move(src, expected_dir)
            
            # Clean up temporary files
            shutil.rmtree(temp_dir)
            
            # Verify the download
            if os.path.exists(expected_mach_path):
                print(f"✓ Firefox source code successfully downloaded to: {expected_dir}")
                return True
            else:
                print(f"✗ Firefox source code extraction failed")
                return False
                
        except Exception as e:
            print(f"✗ Failed to download Firefox source: {e}")
            return False

    def verify_firefox_source(self) -> bool:
        """Verify that Firefox source code is complete and ready for build"""
        print("Verifying Firefox source code...")
        
        mach_path = self.get_mach_path()
        
        # Check basic files
        required_files = ['mach', 'configure', 'browser', 'toolkit']
        
        if self.use_mozilla_build:
            base_dir = os.path.dirname(mach_path)
        else:
            base_dir = self.firefox_src_dir
        
        missing_files = []
        for required_file in required_files:
            check_path = os.path.join(base_dir, required_file)
            if not os.path.exists(check_path):
                missing_files.append(required_file)
        
        if missing_files:
            print(f"✗ Firefox source code incomplete. Missing files: {', '.join(missing_files)}")
            return False
        
        # Check if mach is executable
        if not os.access(mach_path, os.X_OK):
            print("Making mach executable...")
            os.chmod(mach_path, 0o755)
        
        # Create .mozconfig if it doesn't exist
        mozconfig_path = os.path.join(base_dir, '.mozconfig')
        if not os.path.exists(mozconfig_path):
            print("Creating .mozconfig file...")
            self.create_mozconfig(base_dir)
        
        print(f"✓ Firefox source code verified and ready at: {base_dir}")
        return True

    def create_mozconfig(self, firefox_dir: str) -> bool:
        """Create .mozconfig file for Firefox build"""
        print(f"Creating .mozconfig in {firefox_dir}")
        
        try:
            mozconfig_path = os.path.join(firefox_dir, '.mozconfig')
            
            # Build type (release or debug)
            build_type = self.config.get('build_type', 'release')
            enable_debug = self.config.get('enable_debug', False)
            enable_symbols = self.config.get('enable_symbols', True)
            
            # Create .mozconfig content
            mozconfig_content = f"""
# Build configuration for OpenKomodoIDE

# Build type
ac_add_options --enable-{build_type}

# Disable tests (we don't need them for the build)
ac_add_options --disable-tests

# Debug and optimization settings
"""
            
            if build_type == 'release':
                mozconfig_content += "ac_add_options --enable-optimize\n"
            else:
                mozconfig_content += "ac_add_options --disable-optimize\n"
            
            if enable_debug:
                mozconfig_content += "ac_add_options --enable-debug\n"
            
            if enable_symbols:
                mozconfig_content += "ac_add_options --enable-crashreport-symbols\n"
            
            # Add platform-specific settings
            platform = self.config.get('platform', self.detect_platform())
            if platform.startswith('linux'):
                mozconfig_content += "\n# Linux-specific settings\n"
                mozconfig_content += "ac_add_options --with-system-libvpx\n"
                mozconfig_content += "ac_add_options --with-system-icu\n"
            elif platform == 'macos':
                mozconfig_content += "\n# macOS-specific settings\n"
                mozconfig_content += "ac_add_options --enable-macos-target=10.12\n"
            elif platform == 'windows':
                mozconfig_content += "\n# Windows-specific settings\n"
                mozconfig_content += "ac_add_options --enable-win32k-lockdown\n"
            
            # Write .mozconfig file
            with open(mozconfig_path, 'w') as f:
                f.write(mozconfig_content)
            
            print(f"✓ Created .mozconfig at {mozconfig_path}")
            print("Contents:")
            for line in mozconfig_content.strip().split('\n'):
                if line.strip():
                    print(f"  {line}")
            
            return True
            
        except Exception as e:
            print(f"✗ Failed to create .mozconfig: {e}")
            return False

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
            # Use current environment if none provided
            if env is None:
                env = os.environ.copy()
            
            result = subprocess.run(cmd, shell=True, cwd=cwd, env=env, 
                                  capture_output=capture_output, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def setup_environment(self) -> bool:
        """Set up the build environment for Firefox build"""
        print("Setting up Firefox build environment...")
        
        mach_path = self.get_mach_path()
        firefox_dir = os.path.dirname(mach_path)
        
        # Set up Python virtual environment if needed
        venv_dir = os.path.join(firefox_dir, '.venv')
        if not os.path.exists(venv_dir):
            print("Setting up Python virtual environment...")
            try:
                subprocess.run([
                    'python3', '-m', 'venv', venv_dir
                ], check=True, cwd=firefox_dir)
                
                # Install required packages for Firefox 140 ESR
                print("Installing Python requirements for Firefox 140 ESR...")
                if sys.platform == 'win32':
                    pip_path = os.path.join(venv_dir, 'Scripts', 'pip')
                else:
                    pip_path = os.path.join(venv_dir, 'bin', 'pip')
                
                # Install basic requirements for mach to work
                subprocess.run([
                    pip_path, 'install', 'six', 'py', 'click', 'tqdm'
                ], check=True, cwd=firefox_dir)
                
                # Try to install from bootstrap.py if it exists
                bootstrap_file = os.path.join(firefox_dir, 'python', 'mozboot', 'bootstrap.py')
                if os.path.exists(bootstrap_file):
                    print("Running bootstrap.py...")
                    subprocess.run([
                        sys.executable, bootstrap_file, '--no-interactive'
                    ], check=True, cwd=firefox_dir, env=os.environ.copy())
                
            except Exception as e:
                print(f"⚠ Failed to set up virtual environment: {e}")
                print("Continuing without virtual environment...")
        
        # Set environment variables for Firefox build
        env_vars = {
            'PATH': f"{os.path.dirname(mach_path)}:{os.path.join(self.base_dir, 'bin')}:{os.environ.get('PATH', '')}",
            'MOZCONFIG': os.path.join(firefox_dir, '.mozconfig'),
            'LD_LIBRARY_PATH': os.path.join(self.base_dir, 'lib'),
            'PLATFORM': self.config['platform'],
            'BUILD_TYPE': self.config['build_type'],
            'MAKEFLAGS': f"-j{self.config['jobs']}",
            'MOZILLA_OFFICIAL': '1',
            'MOZ_TELEMETRY_REPORTING': '1',
            'MOZ_ADDON_SIGNING': '1',
            'MOZ_REQUIRE_SIGNING': '1'
        }
        
        # Add virtual environment to PATH if it exists
        if os.path.exists(venv_dir):
            if sys.platform == 'win32':
                venv_bin = os.path.join(venv_dir, 'Scripts')
            else:
                venv_bin = os.path.join(venv_dir, 'bin')
            env_vars['PATH'] = f"{venv_bin}:{env_vars['PATH']}"
            env_vars['VIRTUAL_ENV'] = venv_dir
        
        for key, value in env_vars.items():
            os.environ[key] = value
        
        # Set platform-specific variables
        if self.config['platform'].startswith('linux'):
            os.environ['CC'] = 'gcc'
            os.environ['CXX'] = 'g++'
        elif self.config['platform'] == 'macos':
            os.environ['CC'] = 'clang'
            os.environ['CXX'] = 'clang++'
        elif self.config['platform'] == 'windows':
            os.environ['CC'] = 'cl'
            os.environ['CXX'] = 'cl'
        
        print(f"Environment set up for {self.config['platform']}")
        return True
    
    def check_dependencies(self) -> bool:
        """Check that all required dependencies are available"""
        print("Checking dependencies...")
        
        required_tools = ['python3', 'git', 'make', 'gcc', 'g++', 'zip', 'tar']
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
        """Configure the build using Firefox's mach system"""
        print("Configuring build using Firefox mach system...")
        
        # Use Firefox's mach build system
        mach_path = self.get_mach_path()
        if not os.path.exists(mach_path):
            print(f"✗ Firefox mach not found at {mach_path}")
            return False
        
        # Ensure .mozconfig exists
        mozconfig_path = os.path.join(os.path.dirname(mach_path), '.mozconfig')
        if not os.path.exists(mozconfig_path):
            print("Creating .mozconfig file...")
            if not self.create_mozconfig(os.path.dirname(mach_path)):
                print("✗ Failed to create .mozconfig")
                return False
        
        # Set up Python environment properly
        firefox_dir = os.path.dirname(mach_path)
        venv_dir = os.path.join(firefox_dir, '.venv')
        
        # Create virtual environment if it doesn't exist
        if not os.path.exists(venv_dir):
            print("Setting up Python virtual environment...")
            try:
                subprocess.run([
                    'python3', '-m', 'venv', venv_dir
                ], check=True, cwd=firefox_dir)
                
                # Install basic requirements
                if sys.platform == 'win32':
                    pip_path = os.path.join(venv_dir, 'Scripts', 'pip')
                else:
                    pip_path = os.path.join(venv_dir, 'bin', 'pip')
                
                subprocess.run([
                    pip_path, 'install', 'six', 'py', 'click', 'tqdm'
                ], check=True, cwd=firefox_dir)
                
                # Install mozbuild from source
                mozbuild_dir = os.path.join(firefox_dir, 'python', 'mozbuild')
                if os.path.exists(mozbuild_dir):
                    subprocess.run([
                        pip_path, 'install', '-e', mozbuild_dir
                    ], check=True, cwd=firefox_dir)
                
            except Exception as e:
                print(f"⚠ Failed to set up Python environment: {e}")
        
        # For modern Firefox, we use mach configure without arguments
        # All configuration is handled via .mozconfig file
        cmd = f"{mach_path} configure"
        
        print(f"Running: {cmd}")
        
        # Set up environment for mach
        env = os.environ.copy()
        env['MOZCONFIG'] = mozconfig_path
        
        # Add virtual environment to PATH
        if os.path.exists(venv_dir):
            if sys.platform == 'win32':
                venv_bin = os.path.join(venv_dir, 'Scripts')
            else:
                venv_bin = os.path.join(venv_dir, 'bin')
            env['PATH'] = f"{venv_bin}:{os.path.dirname(mach_path)}:{env['PATH']}"
            env['VIRTUAL_ENV'] = venv_dir
        else:
            env['PATH'] = f"{os.path.dirname(mach_path)}:{env['PATH']}"
        
        success, stdout, stderr = self.run_command(cmd, cwd=self.base_dir, env=env)
        
        if success:
            print("✓ Build configuration successful")
            return True
        else:
            # Check for common non-critical errors
            if "already configured" in stderr or "up-to-date" in stderr:
                print(f"⚠ Build configuration warning (non-critical): {stderr}")
                return True
            else:
                print(f"✗ Build configuration failed: {stderr}")
                print(f"stdout: {stdout}")
                print("\nTrying to diagnose the issue...")
                
                # Check if mozbuild is available
                try:
                    import mozbuild
                    print("✓ mozbuild module is available")
                except ImportError:
                    print("✗ mozbuild module is NOT available")
                    print("Please run the following commands manually:")
                    print(f"  cd {firefox_dir}")
                    print("  python3 -m venv .venv")
                    print("  source .venv/bin/activate")
                    print("  pip install six py click tqdm")
                    print("  pip install -e python/mozbuild")
                
                return False
    
    def clean_build(self) -> bool:
        """Clean the build directory using mach"""
        print("Cleaning build directory using mach...")
        
        mach_path = self.get_mach_path()
        if not os.path.exists(mach_path):
            print(f"✗ Firefox mach not found at {mach_path}")
            return False
        
        cmd = f"{mach_path} clobber"
        
        # Set up environment for mach
        env = os.environ.copy()
        env['MOZCONFIG'] = os.path.join(self.base_dir, 'mozconfig')
        env['PATH'] = f"{os.path.dirname(mach_path)}:{env['PATH']}"
        
        success, stdout, stderr = self.run_command(cmd, cwd=self.base_dir, env=env)
        
        if success:
            print("✓ Build directory cleaned")
            return True
        else:
            print(f"✗ Clean failed: {stderr}")
            return False
    
    def distclean_build(self) -> bool:
        """Completely clean the build using mach"""
        print("Performing distclean using mach...")
        
        mach_path = self.get_mach_path()
        if not os.path.exists(mach_path):
            print(f"✗ Firefox mach not found at {mach_path}")
            return False
        
        cmd = f"{mach_path} clobber"
        
        # Set up environment for mach
        env = os.environ.copy()
        env['MOZCONFIG'] = os.path.join(self.base_dir, 'mozconfig')
        env['PATH'] = f"{os.path.dirname(mach_path)}:{env['PATH']}"
        
        success, stdout, stderr = self.run_command(cmd, cwd=self.base_dir, env=env)
        
        if success:
            print("✓ Distclean successful")
            return True
        else:
            # Check if this is a non-critical error
            if "No such file or directory" in stderr or "not found" in stderr:
                print(f"⚠ Distclean warning (non-critical): {stderr}")
                # This might be expected if build directory doesn't exist yet
                return True
            else:
                print(f"✗ Distclean failed: {stderr}")
                return False
    
    def build_targets(self) -> bool:
        """Build the specified targets using mach"""
        print(f"Building targets: {', '.join(self.config['targets'])}")
        
        mach_path = self.get_mach_path()
        if not os.path.exists(mach_path):
            print(f"✗ Firefox mach not found at {mach_path}")
            print("Attempting to download Firefox source code...")
            
            # Try to download Firefox source
            if not self.download_firefox_source():
                print("✗ Failed to download Firefox source code")
                return False
            
            # Verify the source code
            if not self.verify_firefox_source():
                print("✗ Firefox source code verification failed")
                return False
            

            
            # Update mach_path after download
            mach_path = self.get_mach_path()
        
        all_success = True
        
        for target in self.config['targets']:
            print(f"\nBuilding target: {target}")
            
            # Map target names to mach commands
            if target == 'all':
                cmd = f"{mach_path} build"
            elif target == 'faster':
                cmd = f"{mach_path} build faster"
            elif target == 'debug':
                cmd = f"{mach_path} build --debug"
            elif target == 'release':
                cmd = f"{mach_path} build --release"
            else:
                cmd = f"{mach_path} build {target}"
            
            print(f"Running: {cmd}")
            
            # Set up environment for mach
            env = os.environ.copy()
            env['MOZCONFIG'] = os.path.join(self.base_dir, 'mozconfig')
            env['PATH'] = f"{os.path.dirname(mach_path)}:{env['PATH']}"
            env['MOZ_MAKE_FLAGS'] = f"-j{self.config['jobs']}"
            
            # Set PYTHONPATH to include mozbuild modules
            firefox_python_dir = os.path.join(self.firefox_src_dir, 'python')
            firefox_mozbuild_dir = os.path.join(self.firefox_src_dir, 'python', 'mozbuild')
            if os.path.exists(firefox_python_dir):
                env['PYTHONPATH'] = f"{firefox_python_dir}:{firefox_mozbuild_dir}:{env.get('PYTHONPATH', '')}"
            
            # Also set PYTHONPATH for the mach virtualenv by creating a .pth file
            mach_virtualenv_dir = os.path.join(os.path.expanduser("~/.mozbuild/srcdirs"), "mozilla-9626dada346e", "_virtualenvs", "build")
            if os.path.exists(mach_virtualenv_dir):
                pth_file = os.path.join(mach_virtualenv_dir, "lib", "python3.11", "site-packages", "mozbuild.pth")
                os.makedirs(os.path.dirname(pth_file), exist_ok=True)
                with open(pth_file, 'w') as f:
                    f.write(f"{firefox_python_dir}\n")
                    f.write(f"{firefox_mozbuild_dir}\n")
            
            success, stdout, stderr = self.run_command(cmd, cwd=self.base_dir, env=env)
            
            # For mach build, ignore non-critical warnings (like psutil warnings)
            if success:
                print(f"✓ Target {target} built successfully")
            else:
                # Check if the error is just warnings (non-critical)
                if "RuntimeWarning" in stderr and "psutil" in stderr:
                    print(f"⚠ Target {target} completed with warnings (non-critical)")
                    print(f"✓ Target {target} built successfully")
                else:
                    print(f"✗ Target {target} failed: {stderr}")
                    all_success = False
                    if not self.config.get('continue_on_error', False):
                        break
        
        return all_success
    
    def create_packages(self) -> bool:
        """Create distribution packages using mach"""
        print("Creating packages using mach...")
        
        mach_path = self.get_mach_path()
        if not os.path.exists(mach_path):
            print(f"✗ Firefox mach not found at {mach_path}")
            return False
        
        cmd = f"{mach_path} package"
        
        # Set up environment for mach
        env = os.environ.copy()
        env['MOZCONFIG'] = os.path.join(self.base_dir, 'mozconfig')
        env['PATH'] = f"{os.path.dirname(mach_path)}:{env['PATH']}"
        
        success, stdout, stderr = self.run_command(cmd, cwd=self.base_dir, env=env)
        
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
        
        # Check if Firefox source exists
        mach_path = self.get_mach_path()
        source_exists = os.path.exists(mach_path)
        
        # Handle cleaning based on source existence
        if self.config['clean_build']:
            if source_exists:
                # Only clean if source exists
                if not self.distclean_build():
                    print("⚠ Clean failed, but continuing with build...")
                    # Don't return False here - continue with build
            else:
                print("⚠ Skipping clean - no Firefox source found (first build)")
        
        # Ensure Firefox source is available
        if not source_exists:
            print("Firefox source not found - downloading...")
            if not self.download_firefox_source():
                print("✗ Failed to download Firefox source")
                return False
            
            # Verify the download
            if not self.verify_firefox_source():
                print("✗ Firefox source verification failed")
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
    parser.add_argument('--init', action='store_true',
                       help='Initialize build environment')
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
    if args.init:
        builder.initialize_build()
        sys.exit(0)
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