#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modern local build configuration for Komodo
Replaces the legacy bklocal.py functionality
"""

import os
import sys
import platform
import time
import datetime
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
import json

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from build_config import BuildConfig


# Set up logging
log = logging.getLogger("build_local")


class ModernBuildLocal:
    """Modern local build configuration replacing legacy bklocal.py functionality"""
    
    def __init__(self):
        self.config = BuildConfig()
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def configure_version_info(self, version: str = "12.0.0-alpha1"):
        """Configure version-specific information"""
        # Modern version configuration - no more siloed licenses
        version_info = {
            "12.0.0-alpha1": {
                "modernBuildSystem": True,
                "pythonVersion": "3.11+",
                "firefoxVersion": "140.0 ESR",
                "buildType": "modern"
            },
            "11.0.0-alpha1": {
                # Legacy compatibility mode
                "modernBuildSystem": False,
                "pythonVersion": "2.6 (legacy)",
                "firefoxVersion": "legacy",
                "buildType": "legacy"
            }
        }
        
        if version in version_info:
            self.config.configure(**version_info[version])
            log.info(f"Configured version: {version}")
        else:
            # Default to modern configuration
            self.config.configure(
                modernBuildSystem=True,
                pythonVersion="3.11+",
                firefoxVersion="140.0 ESR",
                buildType="modern"
            )
            log.info(f"Using default modern configuration for version: {version}")
    
    def detect_platform_info(self):
        """Detect and configure platform-specific information"""
        # Platform detection
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        # Modern platform configuration
        if system == 'windows':
            self.config.set('platform', 'win')
            self.config.set('platformPathSep', ';')
        elif system == 'linux':
            self.config.set('platform', 'linux')
            self.config.set('platformPathSep', ':')
            # Detect Linux distribution
            try:
                import distro
                self.config.set('linuxDistro', distro.id())
            except ImportError:
                self.config.set('linuxDistro', 'unknown')
        elif system == 'darwin':
            self.config.set('platform', 'mac')
            self.config.set('platformPathSep', ':')
        else:
            self.config.set('platform', system)
            self.config.set('platformPathSep', ':')
        
        # Architecture detection
        if machine in ('x86_64', 'amd64'):
            self.config.set('architecture', 'x86_64')
        elif machine in ('i386', 'i686'):
            self.config.set('architecture', 'x86')
        else:
            self.config.set('architecture', machine)
        
        log.info(f"Detected platform: {self.config['platform']}-{self.config['architecture']}")
    
    def setup_build_directories(self):
        """Setup and configure build directories"""
        # Create build directories if they don't exist
        build_dirs = [
            'build', 'install', 'export', 'packages',
            'support', 'sdk', 'stub', 'readme', 'sysdlls'
        ]
        
        for dir_name in build_dirs:
            dir_path = PROJECT_ROOT / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                log.info(f"Created directory: {dir_path}")
            self.config.set(dir_name, str(dir_path))
    
    def configure_modern_build(self):
        """Configure modern build options"""
        # Modern build defaults
        modern_config = {
            'withSymbols': False,
            'withCrashReportSymbols': False,
            'withHTTPInspector': True,
            'withCodeBrowser': True,
            'withAPIBrowser': True,
            'withProjectManager': True,
            'withPublishing': True,
            'withSCC': True,
            'withSleuth': True,
            'withSSO': True,
            'withCollaboration': True,
            'withBinaryDBGPClients': True,
            'withRx': True,
            'withSharedSupport': True,
            'withDebugging': True,
            'withProfiling': False,
            'withDatabaseExplorer': True,
            'withPDKIntegration': True,
            'withTDKIntegration': True,
            'withTests': True,
            'withCasper': True,
            'withJSLib': True,
            'withWatchdogFSNotifications': True,
            'withPGOGeneration': False,
            'withPGOCollection': False,
            'withDocs': True,
            'withKomodoCix': True,
            'universal': False
        }
        
        for key, value in modern_config.items():
            self.config.set(key, value)
        
        log.info("Configured modern build options")
    
    def run_modern_configure(self, argv: List[str]):
        """Run modern configure process"""
        log.info("Running modern configure process")
        
        # Parse command line arguments
        import argparse
        parser = argparse.ArgumentParser(description='Modern Komodo Build Configuration')
        parser.add_argument('--release', action='store_true', help='Configure for release build')
        parser.add_argument('--debug', action='store_true', help='Configure for debug build')
        parser.add_argument('--product', choices=['ide', 'edit'], default='ide', 
                          help='Product type (ide or edit)')
        parser.add_argument('--with-symbols', action='store_true', 
                          help='Include debug symbols')
        parser.add_argument('--reconfigure', action='store_true', 
                          help='Force reconfiguration')
        
        try:
            args = parser.parse_args(argv)
        except SystemExit:
            return 1
        
        # Apply configuration based on arguments
        if args.release:
            self.config.set('buildType', 'release')
            self.config.set('withSymbols', False)
            self.config.set('withDebugging', False)
        elif args.debug:
            self.config.set('buildType', 'debug')
            self.config.set('withSymbols', True)
            self.config.set('withDebugging', True)
        
        if args.product:
            self.config.set('productType', args.product)
        
        if args.with_symbols:
            self.config.set('withSymbols', True)
        
        # Save configuration
        self.config.save_to_file()
        log.info("Modern configure completed successfully")
        return 0
    
    def run_modern_test(self, argv: List[str]):
        """Run modern test suite"""
        log.info("Running modern test suite")
        
        # Run tests using modern build system
        try:
            result = subprocess.run(
                ['python3', 'mozilla/build.py', 'test'] + argv,
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                log.info("Tests completed successfully")
                return 0
            else:
                log.error(f"Tests failed: {result.stderr}")
                return 1
                
        except Exception as e:
            log.error(f"Error running tests: {e}")
            return 1
    
    def run_modern_clean(self, argv: List[str]):
        """Run modern clean process"""
        log.info("Running modern clean process")
        
        try:
            result = subprocess.run(
                ['python3', 'mozilla/build.py', 'clean'] + argv,
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                log.info("Clean completed successfully")
                return 0
            else:
                log.error(f"Clean failed: {result.stderr}")
                return 1
                
        except Exception as e:
            log.error(f"Error running clean: {e}")
            return 1
    
    def get_configuration(self) -> Dict[str, Any]:
        """Get the full configuration"""
        return self.config.to_dict()
    
    def print_configuration(self):
        """Print the current configuration"""
        print("Modern Build Configuration:")
        print("=" * 50)
        for key, value in sorted(self.config.to_dict().items()):
            print(f"{key:30}: {value}")


def main():
    """Main entry point"""
    print("Modern Komodo Build Local Configuration")
    print("=" * 45)
    
    # Initialize modern build local configuration
    build_local = ModernBuildLocal()
    
    # Configure version information
    build_local.configure_version_info("12.0.0-alpha1")
    
    # Detect platform information
    build_local.detect_platform_info()
    
    # Setup build directories
    build_local.setup_build_directories()
    
    # Configure modern build options
    build_local.configure_modern_build()
    
    # Print configuration
    build_local.print_configuration()
    
    # Save configuration
    build_local.config.save_to_file()
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        log.error(f"Fatal error in build_local: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)