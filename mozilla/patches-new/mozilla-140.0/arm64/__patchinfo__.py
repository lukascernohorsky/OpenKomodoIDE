"""Apply these patches to the Mozilla Mercurial checkout for ARM64 platforms."""

import sys
import platform

def applicable(config):
    """Check if these patches should be applied."""
    # Check if we're on an ARM64 platform
    is_arm64 = (platform.machine() in ('aarch64', 'arm64') or 
                sys.platform in ('linux_aarch64', 'linux_arm64'))
    
    return (config.mozVer == 140.0 and 
            config.patch_target == "mozilla" and 
            is_arm64)

def patch_args(config):
    # use -p1 to better match hg patches
    return ['-p1']