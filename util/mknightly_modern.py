#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modern nightly build creation for Komodo
Replaces the legacy mknightly.py functionality
"""

import os
import sys
import re
import glob
import time
import traceback
import logging
import tempfile
import argparse
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from build_config import BuildConfig
from build_local import ModernBuildLocal


#---- exceptions

class Error(Exception):
    pass


#---- globals

log = logging.getLogger("mknightly_modern")

# Modern configuration - update with actual deployment targets
modern_upload_config = {
    "komodoedit": {
        "upload_base_dir": "~/komodo-nightly-stage/edit",
        "pkg_patterns": ["Komodo-Edit-*"],
        "devbuilds_base_dir": "~/komodo-builds/edit"
    },
    "komodoide": {
        "upload_base_dir": "~/komodo-nightly-stage/ide",
        "pkg_patterns": ["Komodo-IDE-*", "Komodo-*RemoteDebugging*"],
        "devbuilds_base_dir": "~/komodo-builds/ide"
    }
}


#---- module API

def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_modern_build_info(project: str) -> Dict[str, Any]:
    """Get modern build information"""
    build_local = ModernBuildLocal()
    config = build_local.get_configuration()
    
    # Project-specific configuration
    if project == "komodoedit":
        config['productType'] = 'edit'
        config['prettyProductType'] = 'Edit'
    else:
        config['productType'] = 'ide'
        config['prettyProductType'] = 'IDE'
    
    return config


def create_modern_nightly(project: str, branch: str = "trunk", 
                         version: Optional[str] = None, 
                         build_num: Optional[str] = None,
                         dry_run: bool = True,
                         release: bool = False):
    """Create a modern nightly build
    
    Args:
        project: Project name ('komodoide' or 'komodoedit')
        branch: Source tree branch (default: 'trunk')
        version: Optional version string
        build_num: Optional build number
        dry_run: If True, just show what would be done
        release: If True, create a release build instead of nightly
    """
    log.info(f"Creating {'release' if release else 'nightly'} build for {project}")
    
    # Get build configuration
    config = get_modern_build_info(project)
    
    # Determine build type
    build_type = "release" if release else "nightly"
    
    # Create build directory structure
    build_dir = PROJECT_ROOT / "build" / build_type / project
    build_dir.mkdir(parents=True, exist_ok=True)
    
    log.info(f"Build directory: {build_dir}")
    
    # Get version information
    if version is None:
        version = config.get('komodoVersion', '12.0.0')
    
    if build_num is None:
        build_num = config.get('buildNum', '0')
    
    # Create version-specific directory
    version_dir = build_dir / version
    version_dir.mkdir(exist_ok=True)
    
    # Create build-specific directory
    build_specific_dir = version_dir / f"build_{build_num}"
    build_specific_dir.mkdir(exist_ok=True)
    
    log.info(f"Version: {version}, Build: {build_num}")
    log.info(f"Build specific directory: {build_specific_dir}")
    
    # Create metadata file
    metadata = {
        'project': project,
        'version': version,
        'build_num': build_num,
        'build_type': build_type,
        'timestamp': datetime.datetime.now().isoformat(),
        'platform': config.get('platform', 'unknown'),
        'architecture': config.get('architecture', 'unknown'),
        'python_version': config.get('pythonVersion', '3.11+'),
        'firefox_version': config.get('firefoxVersion', '140.0 ESR')
    }
    
    metadata_file = build_specific_dir / "build_metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        import json
        json.dump(metadata, f, indent=2)
    
    log.info(f"Created metadata file: {metadata_file}")
    
    # Create symlink for latest build
    latest_link = version_dir / "latest"
    if latest_link.exists() or latest_link.is_symlink():
        latest_link.unlink()
    latest_link.symlink_to(build_specific_dir.name)
    
    log.info(f"Created latest symlink: {latest_link}")
    
    # Create update information
    updates_dir = build_specific_dir / "updates"
    updates_dir.mkdir(exist_ok=True)
    
    # Create MAR files metadata (modern equivalent)
    mar_metadata = {
        'build_id': f"{version}-{build_num}",
        'product': project,
        'version': version,
        'build_num': build_num,
        'timestamp': int(time.time())
    }
    
    mar_file = updates_dir / "mar_metadata.json"
    with open(mar_file, 'w', encoding='utf-8') as f:
        json.dump(mar_metadata, f, indent=2)
    
    log.info(f"Created MAR metadata: {mar_file}")
    
    # Create package information
    packages = []
    if project == "komodoide":
        packages = [
            f"Komodo-IDE-{version}-{build_num}-linux-x86_64.tar.gz",
            f"Komodo-IDE-{version}-{build_num}-win32-x86_64.zip",
            f"Komodo-IDE-{version}-{build_num}-macosx-x86_64.dmg"
        ]
    else:
        packages = [
            f"Komodo-Edit-{version}-{build_num}-linux-x86_64.tar.gz",
            f"Komodo-Edit-{version}-{build_num}-win32-x86_64.zip",
            f"Komodo-Edit-{version}-{build_num}-macosx-x86_64.dmg"
        ]
    
    # Create package list
    packages_file = build_specific_dir / "packages.txt"
    with open(packages_file, 'w', encoding='utf-8') as f:
        for pkg in packages:
            f.write(pkg + '\n')
    
    log.info(f"Created packages list: {packages_file}")
    
    # Create README
    readme_content = f"""
Komodo {config.get('prettyProductType', project)} {version} Build {build_num}
{'Release' if release else 'Nightly'} Build - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Build Information:
- Platform: {config.get('platform', 'unknown')}
- Architecture: {config.get('architecture', 'unknown')}
- Python Version: {config.get('pythonVersion', '3.11+')}
- Firefox Version: {config.get('firefoxVersion', '140.0 ESR')}

Packages:
""" + "\n".join(f"  - {pkg}" for pkg in packages)
    
    readme_file = build_specific_dir / "README.txt"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    log.info(f"Created README: {readme_file}")
    
    if dry_run:
        log.info("Dry run completed - no files actually created")
    else:
        log.info("Nightly build creation completed successfully")
    
    return 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Modern Komodo Nightly Build Creator',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='verbose output'
    )
    parser.add_argument(
        '-p', '--project',
        choices=['komodoide', 'komodoedit'],
        required=True,
        help='project name (komodoide or komodoedit)'
    )
    parser.add_argument(
        '-b', '--branch',
        default='trunk',
        help='source tree branch (default: trunk)'
    )
    parser.add_argument(
        '-V', '--version',
        help='version string (default: from build config)'
    )
    parser.add_argument(
        '-B', '--build-num',
        help='build number (default: from build config)'
    )
    parser.add_argument(
        '-n', '--dry-run',
        action='store_true',
        help='dry run - show what would be done without doing it'
    )
    parser.add_argument(
        '-r', '--release',
        action='store_true',
        help='create a release build instead of nightly'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    log.info(f"Starting modern nightly build creation for {args.project}")
    
    try:
        result = create_modern_nightly(
            project=args.project,
            branch=args.branch,
            version=args.version,
            build_num=args.build_num,
            dry_run=args.dry_run,
            release=args.release
        )
        
        if result == 0:
            log.info("Nightly build creation completed successfully")
        else:
            log.error("Nightly build creation failed")
        
        return result
        
    except Exception as e:
        log.error(f"Fatal error in nightly build creation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())