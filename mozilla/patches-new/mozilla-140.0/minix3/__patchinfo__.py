"""Apply these patches to the Mozilla Mercurial checkout for Minix3 platforms."""

import sys

def applicable(config):
    """Check if these patches should be applied."""
    return (config.mozVer == 140.0 and 
            config.patch_target == "mozilla" and 
            sys.platform.startswith('minix'))

def patch_args(config):
    # use -p1 to better match hg patches
    return ['-p1']