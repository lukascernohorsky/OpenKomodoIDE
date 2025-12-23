"""Apply these patches to the Mozilla Mercurial checkout for Gentoo platforms."""

import sys
import os

def applicable(config):
    """Check if these patches should be applied."""
    # Check if we're on Gentoo (either by platform detection or by checking for Gentoo files)
    is_gentoo = (sys.platform == 'gentoo' or 
                 os.path.exists('/etc/gentoo-release'))
    
    return (config.mozVer == 140.0 and 
            config.patch_target == "mozilla" and 
            is_gentoo)

def patch_args(config):
    # use -p1 to better match hg patches
    return ['-p1']