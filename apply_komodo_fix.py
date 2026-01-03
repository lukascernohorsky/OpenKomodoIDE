#!/usr/bin/env python3

import os
import sys

def apply_komodo_integration_fix():
    """Apply the Komodo integration fix directly to the source files"""
    
    # Paths to the files we need to modify
    ns_browser_app_path = "mozilla/build/moz14000-ko12.0/mozilla/browser/app/nsBrowserApp.cpp"
    confvars_sh_path = "mozilla/build/moz14000-ko12.0/mozilla/browser/confvars.sh"
    moz_configure_path = "mozilla/build/moz14000-ko12.0/mozilla/toolkit/moz.configure"
    toolkit_mozbuild_path = "mozilla/build/moz14000-ko12.0/mozilla/toolkit/toolkit.mozbuild"
    
    print("Applying Komodo integration fix...")
    
    # 1. Modify nsBrowserApp.cpp
    print(f"Modifying {ns_browser_app_path}...")
    
    with open(ns_browser_app_path, 'r') as f:
        content = f.read()
    
    # Add Komodo header include
    include_marker = '#include "BaseProfiler.h"'
    komodo_include = '''#ifdef MOZ_KOMODO
#include "komodo/KomodoIntegration.h"
#endif
'''
    
    if include_marker in content:
        new_content = content.replace(include_marker, include_marker + '\n' + komodo_include)
        with open(ns_browser_app_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully added Komodo include to nsBrowserApp.cpp")
    else:
        print("✗ Could not find include insertion point in nsBrowserApp.cpp")
        return False
    
    # Add Komodo shutdown call
    shutdown_marker = '  return result;'
    komodo_shutdown = '''#ifdef MOZ_KOMODO
  // Firefox 140 ESR: Komodo integration
  if (NS_SUCCEEDED(result)) {
    KomodoIntegration::Shutdown();
  }
#endif
'''
    
    if shutdown_marker in content:
        new_content = content.replace(shutdown_marker, komodo_shutdown + '\n' + shutdown_marker)
        with open(ns_browser_app_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully added Komodo shutdown to nsBrowserApp.cpp")
    else:
        print("✗ Could not find shutdown insertion point in nsBrowserApp.cpp")
        return False
    
    # 2. Modify confvars.sh
    print(f"Modifying {confvars_sh_path}...")
    
    with open(confvars_sh_path, 'a') as f:
        f.write('''
# Komodo integration for Firefox 140 ESR
MOZ_KOMODO=1
ACDEFINE(MOZ_KOMODO)

# Enable additional features required by Komodo
MOZ_EXTENSIONS=1
ACDEFINE(MOZ_EXTENSIONS)
''')
    print("✓ Successfully added Komodo configuration to confvars.sh")
    
    # 3. Modify moz.configure
    print(f"Modifying {moz_configure_path}...")
    
    with open(moz_configure_path, 'r') as f:
        content = f.read()
    
    # Add Komodo integration options
    komodo_options = '''# Komodo integration options
option('--enable-komodo', env='MOZ_KOMODO',
       help='Enable Komodo IDE integration')

set_config('MOZ_KOMODO', depends_if('--enable-komodo')(lambda _: True))
set_define('MOZ_KOMODO', depends_if('--enable-komodo')(lambda _: True))
'''
    
    # Find a good place to insert the Komodo options
    # Look for a comment or section that makes sense
    insert_marker = '# WebExtensions support'
    if insert_marker in content:
        new_content = content.replace(insert_marker, komodo_options + '\n' + insert_marker)
        with open(moz_configure_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully added Komodo options to moz.configure")
    else:
        # If we can't find a good insertion point, append to the end
        with open(moz_configure_path, 'a') as f:
            f.write('\n' + komodo_options)
        print("✓ Successfully appended Komodo options to moz.configure")
    
    # 4. Modify toolkit.mozbuild
    print(f"Modifying {toolkit_mozbuild_path}...")
    
    with open(toolkit_mozbuild_path, 'r') as f:
        content = f.read()
    
    # Add Komodo integration configuration
    komodo_config = '''if CONFIG['MOZ_KOMODO']:
    DEFINES['MOZ_KOMODO'] = True
    DEFINES['MOZ_KOMODO_INTEGRATION'] = True
    SOURCES += ['komodo/KomodoIntegration.cpp']
    EXPORTS += ['komodo/KomodoIntegration.h']
'''
    
    # Find a good place to insert the Komodo configuration
    insert_marker = '# WebExtensions support'
    if insert_marker in content:
        new_content = content.replace(insert_marker, komodo_config + '\n' + insert_marker)
        with open(toolkit_mozbuild_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully added Komodo configuration to toolkit.mozbuild")
    else:
        # If we can't find a good insertion point, append to the end
        with open(toolkit_mozbuild_path, 'a') as f:
            f.write('\n' + komodo_config)
        print("✓ Successfully appended Komodo configuration to toolkit.mozbuild")
    
    print("✓ Komodo integration fix applied successfully!")
    return True

if __name__ == "__main__":
    success = apply_komodo_integration_fix()
    sys.exit(0 if success else 1)