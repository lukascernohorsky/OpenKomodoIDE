"""Apply these patches to the Mozilla Mercurial checkout.

Note that any patches that have an "_ide.patch" suffix only apply for Komodo
IDE, and these patches will not be included in the mozilla-patches.zip that gets
added to the main downloads area.
"""

def applicable(config):
    return config.mozVer == 140.0 and \
           config.patch_target == "mozilla"

def patch_args(config):
    # use -p1 to better match hg patches
    return ['-p1']

def get_patches(config):
    """Return list of patches to apply for Firefox 140 ESR"""
    patches = []
    
    # Core integration patches
    patches.extend([
        # 'upstream/komodo_integration.patch',  # Temporarily disabled - applied manually
        # 'upstream/pyxpcom_integration.patch',  # Temporarily disabled - applied manually
        # 'upstream/webextensions_integration.patch',  # Temporarily disabled - applied manually
    ])
    
    # Platform-specific patches
    if config.platform.startswith('linux'):
        # patches.append('gtk/gtk_integration.patch')  # Temporarily disabled
        pass
    elif config.platform == 'darwin':
        patches.append('cocoa/cocoa_integration.patch')
    elif config.platform == 'win32':
        patches.append('windows/windows_integration.patch')
    
    # Architecture-specific patches
    if config.arch == 'arm64':
        patches.append('arm64/arm64_optimization.patch')
    
    return patches