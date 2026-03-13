#!/usr/bin/env python3
"""
OpenKomodoIDE Complete Build System
Standalone build script with full build capabilities
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


class BuildSystem:
    """Complete build system for OpenKomodoIDE"""
    
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.build_dir = os.path.join(self.base_dir, 'build')
        self.dist_dir = os.path.join(self.base_dir, 'dist')
        self.log_dir = os.path.join(self.base_dir, 'logs')
        self.config_file = os.path.join(self.base_dir, 'build_config.json')

        # Default configuration
        self.config = {
            'platform': self.detect_platform(),
            'version': '14.10',
            'firefox_version': '140.0',
            'build_type': 'release',
            'jobs': 2,  # Default to 2 jobs, but can be overridden by parameter
            'enable_debug': False,
            'enable_symbols': True,
            'targets': ['all'],
            'clean_build': False,
            'verbose': False,
            'log_file': os.path.join(self.log_dir, f'build_{time.strftime("%Y%m%d_%H%M%S")}.log')
        }

        # Initialize directories
        os.makedirs(self.build_dir, exist_ok=True)
        os.makedirs(self.dist_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)

        # Set up logger
        self.setup_logger()
        
        # Load existing config if available
        self.load_config()
        
        # Set up paths
        self.setup_paths()
    
    def setup_paths(self):
        """Set up all necessary paths"""
        # Modern mozilla/build structure
        self.use_mozilla_build = True
        self.mozilla_build_dir = os.path.join(self.base_dir, 'mozilla', 'build')
        version_suffix = self.config.get('firefox_version', '140.0').replace('.', '')
        komodo_suffix = self.config.get('version', '12.0').replace('.', '')
        
        self.firefox_src_dir = os.path.join(
            self.mozilla_build_dir,
            f"moz{version_suffix}-ko{komodo_suffix}",
            'mozilla'
        )
    
    def setup_logger(self):
        """Set up logging system"""
        self.logger = logging.getLogger('BuildSystem')
        self.logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        
        # File handler
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
    
    def load_config(self):
        """Load build configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
                self.logger.info(f"Loaded configuration from {self.config_file}")
        except Exception as e:
            self.logger.warning(f"Could not load config: {e}")
    
    def save_config(self):
        """Save build configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            self.logger.info(f"Saved configuration to {self.config_file}")
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def update_config_from_args(self, args):
        """Update configuration from command line arguments"""
        if hasattr(args, 'version') and args.version:
            self.config['version'] = args.version
        if hasattr(args, 'firefox') and args.firefox:
            self.config['firefox_version'] = args.firefox
        if hasattr(args, 'platform') and args.platform:
            self.config['platform'] = args.platform
        if hasattr(args, 'debug') and args.debug:
            self.config['enable_debug'] = True
            self.config['build_type'] = 'debug'
        if hasattr(args, 'symbols') and args.symbols is not None:
            self.config['enable_symbols'] = args.symbols
        if hasattr(args, 'clean') and args.clean:
            self.config['clean_build'] = True
        if hasattr(args, 'targets') and args.targets:
            self.config['targets'] = args.targets
        if hasattr(args, 'jobs') and args.jobs:
            self.config['jobs'] = args.jobs
        if hasattr(args, 'verbose') and args.verbose:
            self.config['verbose'] = True
        if hasattr(args, 'test') and args.test:
            self.config['run_tests'] = True
        
        # Update paths after config change
        self.setup_paths()
        self.save_config()
    
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
    
    def get_mach_path(self):
        """Get the path to mach with consistent version formatting"""
        # Remove dots from both versions for consistency
        firefox_version_clean = self.config.get('firefox_version', '140.0').replace('.', '')
        komodo_version_clean = self.config.get('version', '14.10').replace('.', '')
        
        # Modern path structure
        modern_path = os.path.join(
            self.base_dir,
            'mozilla',
            'build',
            f'moz{firefox_version_clean}-ko{komodo_version_clean}',
            'mozilla',
            'mach'
        )
        
        # Fallback paths
        fallback_paths = [
            os.path.join(self.base_dir, 'firefox', 'mach'),
            os.path.join(self.base_dir, 'mozilla', 'mach')
        ]
        
        # Check if modern path exists
        if os.path.exists(modern_path):
            return modern_path
        
        # Check fallback paths
        for path in fallback_paths:
            if os.path.exists(path):
                return path
        
        # Return modern path even if it doesn't exist (for error reporting)
        return modern_path
    
    def get_firefox_build_dir(self):
        """Get the Firefox build directory"""
        mach_path = self.get_mach_path()
        if os.path.exists(mach_path):
            return os.path.dirname(mach_path)
        return self.firefox_src_dir
    
    def setup_environment(self) -> bool:
        """Set up the build environment"""
        self.logger.info("Setting up build environment...")
        
        # Set environment variables
        env_vars = {
            'PATH': f"{os.path.join(self.base_dir, 'bin')}:{os.environ.get('PATH', '')}",
            'LD_LIBRARY_PATH': os.path.join(self.base_dir, 'lib'),
            'PLATFORM': self.config['platform'],
            'BUILD_TYPE': self.config['build_type'],
            'MAKEFLAGS': f"-j{self.config['jobs']}",
            'MOZILLA_OFFICIAL': '1',
            'MOZ_TELEMETRY_REPORTING': '1',
            'MOZ_ADDON_SIGNING': '1',
            'MOZ_REQUIRE_SIGNING': '1'
        }
        
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
        
        self.logger.info(f"Environment set up for {self.config['platform']}")
        return True
    
    def check_dependencies(self) -> bool:
        """Check that all required dependencies are available"""
        self.logger.info("Checking dependencies...")
        
        required_tools = ['python3', 'git', 'make', 'gcc', 'g++', 'zip', 'tar']
        missing_tools = []
        
        for tool in required_tools:
            success, _, _ = self.run_command(f"{tool} --version", capture_output=True)
            if not success:
                missing_tools.append(tool)
        
        if missing_tools:
            self.logger.error(f"Missing tools: {', '.join(missing_tools)}")
            return False
        
        self.logger.info("All required dependencies are available")
        return True
    
    def download_firefox_source(self) -> bool:
        """Download Firefox source code if not already present"""
        self.logger.info("Checking Firefox source code...")
        
        mach_path = self.get_mach_path()
        expected_dir = os.path.dirname(mach_path)
        
        # Check if force download is requested
        if self.config.get('force_download', False):
            self.logger.info("✓ Force download requested - will download fresh source code")
            # Remove existing source if it exists
            if os.path.exists(expected_dir):
                self.logger.info(f"Removing existing source at {expected_dir}...")
                try:
                    shutil.rmtree(expected_dir)
                    self.logger.info("✓ Successfully removed existing source")
                except Exception as e:
                    self.logger.error(f"✗ Could not remove existing source: {e}")
                    return False
            return self._download_firefox_source_fresh()
        
        # Check if source code already exists
        if os.path.exists(mach_path):
            if self.verify_firefox_source():
                self.logger.info(f"✓ Firefox source code found at: {expected_dir}")
                return True
            else:
                self.logger.error(f"✗ Existing Firefox source code at {expected_dir} is incomplete")
                self.logger.info("Removing incomplete source and redownloading...")
                # Remove incomplete source
                if os.path.exists(expected_dir):
                    shutil.rmtree(expected_dir)
        
        self.logger.info(f"✗ Firefox source code not found at: {expected_dir}")
        self.logger.info("Downloading Firefox 140 ESR source code...")
        
        try:
            # Create temporary directory for download
            temp_dir = os.path.join(self.base_dir, 'temp_download')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Download Firefox source
            firefox_version = self.config.get('firefox_version', '140.0')
            firefox_url = f"https://archive.mozilla.org/pub/firefox/releases/{firefox_version}esr/source/firefox-{firefox_version}esr.source.tar.xz"
            tar_file = os.path.join(temp_dir, f"firefox-{firefox_version}esr.source.tar.xz")
            
            self.logger.info(f"Downloading from: {firefox_url}")
            self.logger.info("⚠ This may take a while (~200MB download)...")
            
            # Use wget or curl to download with extended timeout
            try:
                if shutil.which('wget'):
                    self.logger.info("Using wget to download Firefox source...")
                    subprocess.run(['wget', '-c', '--show-progress', '--timeout=600', '--tries=3', firefox_url, '-O', tar_file], 
                                 check=True, timeout=3600)
                elif shutil.which('curl'):
                    self.logger.info("Using curl to download Firefox source...")
                    subprocess.run(['curl', '-C', '-', '-L', '-o', tar_file, '--max-time', '600', '--retry', '3', firefox_url], 
                                 check=True, timeout=3600)
                else:
                    self.logger.error("✗ Neither wget nor curl found. Cannot download Firefox source.")
                    self.logger.error("Please install wget or curl and try again.")
                    return False
            except subprocess.TimeoutExpired:
                self.logger.error("✗ Download timed out. The Firefox source archive is quite large (~200MB).")
                self.logger.error("Please try again with a faster internet connection or download manually.")
                self.logger.error(f"Manual download URL: {firefox_url}")
                self.logger.error(f"Expected download location: {tar_file}")
                return False
            except Exception as e:
                self.logger.error(f"✗ Download failed: {e}")
                return False
            
            # Verify download file exists and has reasonable size
            if not os.path.exists(tar_file):
                self.logger.error(f"✗ Download failed: File {tar_file} was not created")
                return False
            
            file_size = os.path.getsize(tar_file)
            if file_size < 1000000:  # Less than 1MB is likely incomplete
                self.logger.error(f"✗ Download failed: File size {file_size} bytes is too small")
                return False
            
            self.logger.info(f"✓ Download completed: {file_size} bytes")
            
            # Extract the archive
            self.logger.info("Extracting Firefox source code...")
            try:
                with tarfile.open(tar_file, 'r:xz') as tar:
                    # Extract to temporary directory first
                    tar.extractall(path=temp_dir)
            except Exception as e:
                self.logger.error(f"✗ Extraction failed: {e}")
                self.logger.error("This might be due to incomplete download or corrupted archive")
                return False
            
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
                self.logger.error(f"✗ Could not find extracted Firefox source directory in {temp_dir}")
                self.logger.error(f"Contents of {temp_dir}: {os.listdir(temp_dir)}")
                return False
            
            self.logger.info(f"Found extracted source directory: {source_dir}")
            
            # Prepare destination directory
            dest_dir = os.path.dirname(expected_dir)
            os.makedirs(dest_dir, exist_ok=True)
            
            # Clean up existing destination directory if it exists
            if os.path.exists(expected_dir):
                self.logger.info(f"Cleaning up existing directory: {expected_dir}")
                try:
                    # Remove the entire directory and recreate it
                    shutil.rmtree(expected_dir)
                    os.makedirs(expected_dir, exist_ok=True)
                    self.logger.info(f"✓ Successfully cleaned and recreated {expected_dir}")
                except Exception as e:
                    self.logger.error(f"✗ Failed to clean directory {expected_dir}: {e}")
                    self.logger.info("Falling back to individual file cleanup...")
                    # Fallback to individual file cleanup
                    for item in os.listdir(expected_dir):
                        item_path = os.path.join(expected_dir, item)
                        try:
                            if os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                            else:
                                os.remove(item_path)
                        except Exception as e:
                            self.logger.warning(f"⚠ Warning: Could not remove {item_path}: {e}")
            
            # Move contents to expected location
            self.logger.info(f"Moving source code to: {expected_dir}")
            
            # Ensure target directory exists and is empty
            if os.path.exists(expected_dir):
                self.logger.info(f"Cleaning existing directory: {expected_dir}")
                try:
                    shutil.rmtree(expected_dir)
                except Exception as e:
                    self.logger.error(f"✗ Could not clean directory {expected_dir}: {e}")
                    return False
            
            os.makedirs(expected_dir, exist_ok=True)
            
            for item in os.listdir(source_dir):
                src = os.path.join(source_dir, item)
                dst = os.path.join(expected_dir, item)
                try:
                    if os.path.exists(dst):
                        self.logger.info(f"Removing existing: {dst}")
                        if os.path.isdir(dst):
                            shutil.rmtree(dst)
                        else:
                            os.remove(dst)
                    shutil.move(src, expected_dir)
                except Exception as e:
                    self.logger.error(f"✗ Failed to move {src} to {dst}: {e}")
                    return False
            
            # Clean up temporary files
            self.logger.info("Cleaning up temporary files...")
            shutil.rmtree(temp_dir)
            
            # Verify the download
            if os.path.exists(mach_path):
                self.logger.info(f"✓ Firefox source code successfully downloaded to: {expected_dir}")
                return True
            else:
                self.logger.error(f"✗ Firefox source code extraction failed - mach not found at {mach_path}")
                self.logger.error(f"Contents of {expected_dir}: {os.listdir(expected_dir) if os.path.exists(expected_dir) else 'Directory does not exist'}")
                return False
                
        except Exception as e:
            self.logger.error(f"✗ Failed to download Firefox source: {e}")
            self.logger.error("Please check your internet connection and try again")
            return False
    
    def verify_firefox_source(self) -> bool:
        """Verify that Firefox source code is complete and ready for build"""
        self.logger.info("Verifying Firefox source code...")
        
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
            self.logger.error(f"✗ Firefox source code incomplete. Missing files: {', '.join(missing_files)}")
            return False
        
        # Check if mach is executable
        if not os.access(mach_path, os.X_OK):
            self.logger.info("Making mach executable...")
            os.chmod(mach_path, 0o755)
        
        # Create .mozconfig if it doesn't exist
        mozconfig_path = os.path.join(base_dir, '.mozconfig')
        if not os.path.exists(mozconfig_path):
            self.logger.info("Creating .mozconfig file...")
            self.create_mozconfig(base_dir)
        
        self.logger.info(f"✓ Firefox source code verified and ready at: {base_dir}")
        return True
    
    def _download_firefox_source_fresh(self) -> bool:
        """Download fresh Firefox source code (used when force_download is set)"""
        self.logger.info("Downloading fresh Firefox source code...")
        # Reset the force_download flag
        self.config['force_download'] = False
        self.save_config()
        return self.download_firefox_source()
    
    def create_mozconfig(self, firefox_dir: str) -> bool:
        """Create .mozconfig file for Firefox build"""
        self.logger.info(f"Creating .mozconfig in {firefox_dir}")
        
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
            
            # Note: --enable-crashreport-symbols is not supported in Firefox 140 ESR
            # if enable_symbols:
            #     mozconfig_content += "ac_add_options --enable-crashreport-symbols\n"
            
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
            
            self.logger.info(f"✓ Created .mozconfig at {mozconfig_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Failed to create .mozconfig: {e}")
            return False
    
    def configure_build(self) -> bool:
        """Configure the build using Firefox's mach system"""
        self.logger.info("Configuring build using Firefox mach system...")
        
        # Use Firefox's mach build system
        mach_path = self.get_mach_path()
        if not os.path.exists(mach_path):
            self.logger.error(f"✗ Firefox mach not found at {mach_path}")
            
            # Check if this is expected (force_download was set)
            if self.config.get('force_download', False):
                self.logger.info("✓ Source not found as expected (force_download was set)")
            else:
                self.logger.info("✗ Source not found unexpectedly")
            
            # Try to download Firefox source
            self.logger.info("Attempting to download Firefox source code...")
            if not self.download_firefox_source():
                self.logger.error("✗ Failed to download Firefox source code")
                return False
            
            # Update mach_path after download
            mach_path = self.get_mach_path()
            if not os.path.exists(mach_path):
                self.logger.error(f"✗ Firefox mach still not found at {mach_path} after download")
                
                # Last resort: Try to find mach in any location
                self.logger.info("Attempting to find mach in alternative locations...")
                alternative_paths = [
                    os.path.join(self.base_dir, 'mozilla', 'build', 'moz1400-ko1410', 'mozilla', 'mach'),
                    os.path.join(self.base_dir, 'mozilla', 'build', 'moz14000-ko14.10', 'mozilla', 'mach'),
                    os.path.join(self.base_dir, 'build', 'moz1400-ko1410', 'mozilla', 'mach'),
                ]
                
                for alt_path in alternative_paths:
                    if os.path.exists(alt_path):
                        self.logger.info(f"✓ Found mach at alternative location: {alt_path}")
                        mach_path = alt_path
                        break
                
                if not os.path.exists(mach_path):
                    self.logger.error("✗ Could not find mach in any location")
                    return False
        
        # Ensure .mozconfig exists
        mozconfig_path = os.path.join(os.path.dirname(mach_path), '.mozconfig')
        if not os.path.exists(mozconfig_path):
            self.logger.info("Creating .mozconfig file...")
            if not self.create_mozconfig(os.path.dirname(mach_path)):
                self.logger.error("✗ Failed to create .mozconfig")
                return False
        
        # For modern Firefox, we use mach configure without arguments
        # All configuration is handled via .mozconfig file
        cmd = f"{mach_path} configure"
        
        self.logger.info(f"Running: {cmd}")
        
        # Set up environment for mach
        env = os.environ.copy()
        env['MOZCONFIG'] = mozconfig_path
        env['MOZ_MAKE_FLAGS'] = f"-j{self.config['jobs']}"  # Use 2 jobs for configuration
        
        success, stdout, stderr = self.run_command(cmd, cwd=self.base_dir, env=env)
        
        if success:
            self.logger.info("✓ Build configuration successful")
            return True
        else:
            # Check for common non-critical errors
            if "already configured" in stderr or "up-to-date" in stderr:
                self.logger.warning(f"⚠ Build configuration warning (non-critical): {stderr}")
                return True
            else:
                self.logger.error(f"✗ Build configuration failed: {stderr}")
                self.logger.error(f"stdout: {stdout}")
                self.logger.error("Please check the configuration and try again")
                return False
    
    def clean_build(self) -> bool:
        """Clean the build directory using mach"""
        self.logger.info("Cleaning build directory using mach...")
        
        mach_path = self.get_mach_path()
        if not os.path.exists(mach_path):
            self.logger.error(f"✗ Firefox mach not found at {mach_path}")
            return False
        
        cmd = f"{mach_path} clobber"
        
        # Set up environment for mach
        env = os.environ.copy()
        env['MOZCONFIG'] = os.path.join(self.base_dir, 'mozconfig')
        env['PATH'] = f"{os.path.dirname(mach_path)}:{env['PATH']}"
        
        success, stdout, stderr = self.run_command(cmd, cwd=self.base_dir, env=env)
        
        if success:
            self.logger.info("✓ Build directory cleaned")
            return True
        else:
            self.logger.error(f"✗ Clean failed: {stderr}")
            return False
    
    def build_targets(self) -> bool:
        """Build the specified targets using mach"""
        self.logger.info(f"Building targets: {', '.join(self.config['targets'])}")
        
        mach_path = self.get_mach_path()
        if not os.path.exists(mach_path):
            self.logger.error(f"✗ Firefox mach not found at {mach_path}")
            self.logger.info("Attempting to download Firefox source code...")
            
            # Try to download Firefox source
            if not self.download_firefox_source():
                self.logger.error("✗ Failed to download Firefox source code")
                return False
            
            # Verify the source code
            if not self.verify_firefox_source():
                self.logger.error("✗ Firefox source code verification failed")
                return False
            
            # Update mach_path after download
            mach_path = self.get_mach_path()
        
        # First ensure complete Mozilla build for 'all' target
        if 'all' in self.config['targets']:
            self.logger.info("\nEnsuring complete Mozilla build first...")
            
            # Force complete build
            complete_build_cmd = f"{mach_path} build"
            self.logger.info(f"Running complete build: {complete_build_cmd}")
            
            # Set up environment for complete build
            env = os.environ.copy()
            env['MOZCONFIG'] = os.path.join(self.base_dir, 'mozconfig')
            env['PATH'] = f"{os.path.dirname(mach_path)}:{env['PATH']}"
            env['MOZ_MAKE_FLAGS'] = f"-j{self.config['jobs']}"
            
            # Set PYTHONPATH for mozbuild
            firefox_python_dir = os.path.join(self.firefox_src_dir, 'python')
            firefox_mozbuild_dir = os.path.join(self.firefox_src_dir, 'python', 'mozbuild')
            if os.path.exists(firefox_python_dir):
                env['PYTHONPATH'] = f"{firefox_python_dir}:{firefox_mozbuild_dir}:{env.get('PYTHONPATH', '')}"
            
            success, stdout, stderr = self.run_command(complete_build_cmd, cwd=self.base_dir, env=env)
            
            # Verify complete build - check for critical components
            libxul_path = os.path.join(self.firefox_src_dir, 'obj-x86_64-pc-linux-gnu', 'dist', 'bin', 'libxul.so')
            xul_path = os.path.join(self.firefox_src_dir, 'obj-x86_64-pc-linux-gnu', 'dist', 'bin', 'XUL')
            
            if not success:
                self.logger.error("❌ Complete Mozilla build failed")
                self.logger.error("STDOUT: " + stdout)
                self.logger.error("STDERR: " + stderr)
                raise BuildError("Mozilla build failed - cannot proceed")
            
            # Check for critical components
            missing_components = []
            if not os.path.exists(libxul_path):
                missing_components.append('libxul.so')
            if not os.path.exists(xul_path):
                missing_components.append('XUL')
            
            if missing_components:
                self.logger.error(f"❌ Mozilla build incomplete - missing critical components: {', '.join(missing_components)}")
                self.logger.error("STDOUT: " + stdout)
                self.logger.error("STDERR: " + stderr)
                raise BuildError(f"Mozilla build incomplete - missing: {', '.join(missing_components)}")
            
            self.logger.info("✓ Complete Mozilla build successful with all core components")
        
        all_success = True
        
        for target in self.config['targets']:
            # Skip 'all' target if we already built it above
            if target == 'all':
                self.logger.info(f"\nTarget 'all' already built during complete build phase")
                continue
            
            # Map target names to mach commands
            if target == 'faster':
                cmd = f"{mach_path} build faster"
            elif target == 'debug':
                cmd = f"{mach_path} build --debug"
            elif target == 'release':
                cmd = f"{mach_path} build --release"
            else:
                cmd = f"{mach_path} build {target}"
            
            self.logger.info(f"\nBuilding target: {target}")
            
            # Execute the build command
            self.logger.info(f"Running: {cmd}")
            result = subprocess.run(cmd, shell=True, cwd=self.config['mozillaSrcDir'], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                self.logger.error(f"Build failed for target '{target}':")
                self.logger.error("STDOUT: " + result.stdout)
                self.logger.error("STDERR: " + result.stderr)
                all_success = False
                continue
            
            self.logger.info(f"✓ Target '{target}' built successfully")
            
            # Verify critical components exist for this target
            target_components = self._get_target_components(target)
            missing_components = self._verify_components(target_components)
            
            if missing_components:
                self.logger.error(f"Target '{target}' missing components: {', '.join(missing_components)}")
                all_success = False
            else:
                self.logger.info(f"✓ Target '{target}' has all required components")
        
        if all_success:
            self.logger.info("\n✓✓✓ ALL BUILD TARGETS COMPLETED SUCCESSFULLY ✓✓✓")
            return True
        else:
            self.logger.error("\n✗✗✗ SOME BUILD TARGETS FAILED ✗✗✗")
            return False
            
    def _get_target_components(self, target):
        """Get the list of components required for a specific build target."""
        # Base components that should exist for any target
        components = [
            os.path.join(self.config['mozillaObjDir'], 'dist', 'bin', 'libxul.so'),
            os.path.join(self.config['mozillaObjDir'], 'dist', 'bin', 'XUL'),
        ]
        
        # Target-specific components
        if target == 'debug':
            components.extend([
                os.path.join(self.config['mozillaObjDir'], 'dist', 'bin', 'xpcshell'),
                os.path.join(self.config['mozillaObjDir'], 'dist', 'bin', 'mozglue'),
            ])
        elif target == 'release':
            components.extend([
                os.path.join(self.config['mozillaObjDir'], 'dist', 'bin', 'plugin-container'),
            ])
        
        return components
        
    def _verify_components(self, components):
        """Verify that all specified components exist."""
        missing = []
        for component in components:
            if not os.path.exists(component):
                missing.append(component)
        return missing
        
    def target_komodoapp(self):
        """Build the komodoapp target."""
        self.logger.info("\n=== Building komodoapp target ===")
        
        # First check if we have the required Mozilla components
        mozilla_objdir = self._get_mozilla_objdir()
        if not mozilla_objdir:
            self.logger.error("Cannot determine Mozilla object directory")
            return False
        
        # Check for critical components
        libxul_path = os.path.join(mozilla_objdir, 'dist', 'bin', 'libxul.so')
        xul_path = os.path.join(mozilla_objdir, 'dist', 'bin', 'XUL')
        
        if not os.path.exists(libxul_path):
            self.logger.error(f"Critical component missing: {libxul_path}")
            self.logger.error("Please build Mozilla first with a complete build target")
            return False
        
        if not os.path.exists(xul_path):
            self.logger.error(f"Critical component missing: {xul_path}")
            self.logger.error("Please build Mozilla first with a complete build target")
            return False
        
        self.logger.info("✓ All required Mozilla components found")
        
        # Proceed with komodoapp build
        cmd = f"{self.config['machPath']} build komodoapp"
        self.logger.info(f"Running: {cmd}")
        
        result = subprocess.run(cmd, shell=True, cwd=self.config['mozillaSrcDir'], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            self.logger.error("komodoapp build failed:")
            self.logger.error("STDOUT: " + result.stdout)
            self.logger.error("STDERR: " + result.stderr)
            return False
        
        self.logger.info("✓ komodoapp built successfully")
        return True
        
    def _get_mozilla_objdir(self):
        """Get the Mozilla object directory using mach."""
        try:
            cmd = f"{self.config['machPath']} environment --format json"
            result = subprocess.run(cmd, shell=True, cwd=self.config['mozillaSrcDir'], 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                self.logger.error("Failed to get Mozilla environment:")
                self.logger.error("STDERR: " + result.stderr)
                return None
            
            # Parse JSON output to get the object directory
            import json
            env_data = json.loads(result.stdout)
            return env_data.get('topobjdir', '')
        
        except Exception as e:
            self.logger.error(f"Error getting Mozilla object directory: {e}")
            return None


def run_build_automation(args):
    """Run the build automation script with given arguments"""
    build_automation_path = os.path.join(os.path.dirname(__file__), 'build_automation.py')
    
    if not os.path.exists(build_automation_path):
        print(f"Error: build automation script not found at {build_automation_path}")
        return False
    
    # Run the build automation script
    cmd = [sys.executable, build_automation_path] + args
    
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
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
    parser.add_argument('--version', default='14.10',
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
