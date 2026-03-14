#!/usr/bin/env python3
"""
Dynamic Komodo version detector
Detects the Komodo version from existing directory structure
"""

import os
import re
import sys
from pathlib import Path


def detect_komodo_version(base_dir=None):
    """
    Detect Komodo version from existing mozilla/build directory structure
    
    Returns:
        tuple: (firefox_version, komodo_version) or (None, None) if not found
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    mozilla_build_dir = os.path.join(base_dir, 'mozilla', 'build')
    
    if not os.path.exists(mozilla_build_dir):
        print(f"Mozilla build directory not found: {mozilla_build_dir}")
        return None, None
    
    # Look for directories matching pattern moz{firefox}-ko{komodo}
    pattern = re.compile(r'^moz(\d+)-ko(\d+(?:\.\d+)*)$')
    
    found_versions = []
    
    for item in os.listdir(mozilla_build_dir):
        match = pattern.match(item)
        if match:
            firefox_ver = match.group(1)
            komodo_ver = match.group(2)
            found_versions.append((firefox_ver, komodo_ver))
    
    if not found_versions:
        print(f"No version directories found in {mozilla_build_dir}")
        return None, None
    
    if len(found_versions) > 1:
        print(f"Multiple version directories found: {found_versions}")
        print("Using the first one found")
    
    firefox_version, komodo_version = found_versions[0]
    
    # Add dots back to Firefox version (1400 -> 140.0)
    if len(firefox_version) == 4:
        firefox_version = f"{firefox_version[:3]}.{firefox_version[3:]}"
    elif len(firefox_version) == 3:
        firefox_version = f"{firefox_version[:2]}.{firefox_version[2:]}"
    
    # Add dots back to Komodo version (1410 -> 14.10)
    if len(komodo_version) == 4:
        komodo_version = f"{komodo_version[:2]}.{komodo_version[2:]}"
    elif len(komodo_version) == 3:
        komodo_version = f"{komodo_version[:1]}.{komodo_version[1:]}"
    
    print(f"Detected versions:")
    print(f"  Firefox: {firefox_version}")
    print(f"  Komodo:  {komodo_version}")
    
    return firefox_version, komodo_version


def main():
    """Main function to detect and display versions"""
    print("OpenKomodoIDE Version Detector")
    print("=" * 40)
    
    firefox_ver, komodo_ver = detect_komodo_version()
    
    if firefox_ver and komodo_ver:
        print(f"\n✓ Successfully detected versions:")
        print(f"  Firefox: {firefox_ver}")
        print(f"  Komodo:  {komodo_ver}")
        print(f"\nYou can use these versions in your build configuration:")
        print(f"  --version {komodo_ver}")
        print(f"  --firefox {firefox_ver}")
        return 0
    else:
        print(f"\n✗ Could not detect versions automatically")
        print(f"Please specify versions manually using:")
        print(f"  --version X.X")
        print(f"  --firefox XXX.X")
        return 1


if __name__ == "__main__":
    sys.exit(main())