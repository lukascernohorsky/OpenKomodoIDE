#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modern Python 3 build configuration for Komodo
Replaces the legacy Perl-based Construct file
"""

import os
import sys
import platform
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Add the project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))


class BuildConfig:
    """Modern build configuration replacing legacy bkconfig functionality"""
    
    def __init__(self):
        self._config = {}
        self._platform = self._detect_platform()
        self._architecture = self._detect_architecture()
        
        # Initialize default values
        self._initialize_defaults()
        
    def _detect_platform(self) -> str:
        """Detect the current platform"""
        system = platform.system().lower()
        if system == 'windows':
            return 'win'
        elif system == 'linux':
            return 'linux'
        elif system == 'darwin':
            return 'mac'
        else:
            return system
    
    def _detect_architecture(self) -> str:
        """Detect the current architecture"""
        machine = platform.machine().lower()
        if machine in ('x86_64', 'amd64'):
            return 'x86_64'
        elif machine in ('i386', 'i686'):
            return 'x86'
        else:
            return machine
    
    def _initialize_defaults(self):
        """Initialize default configuration values"""
        # Build directories
        self._config['build'] = PROJECT_ROOT / 'build'
        self._config['install'] = PROJECT_ROOT / 'install'
        self._config['export'] = PROJECT_ROOT / 'export'
        self._config['packages'] = PROJECT_ROOT / 'packages'
        
        # Platform and architecture
        self._config['platform'] = self._platform
        self._config['architecture'] = self._architecture
        
        # Build options (defaults)
        self._config['withSymbols'] = False
        self._config['withCrashReportSymbols'] = False
        self._config['withHTTPInspector'] = True
        self._config['withCodeBrowser'] = True
        self._config['withAPIBrowser'] = True
        self._config['withProjectManager'] = True
        self._config['withPublishing'] = True
        self._config['withSCC'] = True
        self._config['withSleuth'] = True
        self._config['withSSO'] = True
        self._config['withCollaboration'] = True
        self._config['withBinaryDBGPClients'] = True
        self._config['withRx'] = True
        self._config['withSharedSupport'] = True
        self._config['withDebugging'] = True
        self._config['withProfiling'] = False
        self._config['withDatabaseExplorer'] = True
        self._config['withPDKIntegration'] = True
        self._config['withTDKIntegration'] = True
        self._config['withTests'] = True
        self._config['withCasper'] = True
        self._config['withJSLib'] = True
        self._config['withWatchdogFSNotifications'] = True
        self._config['withPGOGeneration'] = False
        self._config['withPGOCollection'] = False
        self._config['withDocs'] = True
        self._config['withKomodoCix'] = True
        self._config['universal'] = False
        
        # Version information (will be loaded from version info)
        self._config['komodoVersion'] = '12.0.0'
        self._config['buildNum'] = '0'
        self._config['productType'] = 'ide'  # or 'edit'
        
        # Directories
        self._config['supportDir'] = PROJECT_ROOT / 'support'
        self._config['sdkDir'] = PROJECT_ROOT / 'sdk'
        self._config['stubDir'] = PROJECT_ROOT / 'stub'
        self._config['readmeDir'] = PROJECT_ROOT / 'readme'
        self._config['sysdllsDir'] = PROJECT_ROOT / 'sysdlls'
        
        # Python configuration (legacy versions kept for reference, but not used)
        self._config['python24'] = None
        self._config['python25'] = None
        # self._config['python26'] = None  # Legacy Python 2.6 - removed
        self._config['python27'] = None
        self._config['python31'] = None
        self._config['python32'] = None
        self._config['python33'] = None
        self._config['unsiloedPythonExe'] = sys.executable
        
        # Modern Python 3.11+ is the primary Python
        self._config['pythonInstallDir'] = Path(sys.prefix)
        
    def load_from_file(self, config_file: Optional[Path] = None):
        """Load configuration from a JSON file"""
        if config_file is None:
            config_file = PROJECT_ROOT / 'build_config.json'
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                self._config.update(file_config)
    
    def save_to_file(self, config_file: Optional[Path] = None):
        """Save configuration to a JSON file"""
        if config_file is None:
            config_file = PROJECT_ROOT / 'build_config.json'
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=2, default=str)
    
    def configure(self, **kwargs):
        """Configure build options"""
        for key, value in kwargs.items():
            if key in self._config:
                self._config[key] = value
            else:
                print(f"Warning: Unknown configuration option '{key}'")
    
    def get(self, key: str, default=None):
        """Get a configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a configuration value"""
        self._config[key] = value
    
    def __getattr__(self, name: str):
        """Allow attribute-style access to configuration"""
        if name in self._config:
            return self._config[name]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")
    
    def __getitem__(self, key: str):
        """Allow dict-style access to configuration"""
        return self._config[key]
    
    def __contains__(self, key: str):
        """Check if a configuration key exists"""
        return key in self._config
    
    def to_dict(self) -> Dict[str, Any]:
        """Get the full configuration as a dictionary"""
        return dict(self._config)
    
    def print_config(self):
        """Print the current configuration"""
        print("Current Build Configuration:")
        print("=" * 50)
        for key, value in sorted(self._config.items()):
            print(f"{key:30}: {value}")


# Global build configuration instance
build_config = BuildConfig()


def main():
    """Main entry point for build configuration"""
    print("Komodo Modern Build Configuration")
    print("=" * 40)
    
    # Load existing configuration if available
    build_config.load_from_file()
    
    # Print current configuration
    build_config.print_config()
    
    # Save updated configuration
    build_config.save_to_file()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())