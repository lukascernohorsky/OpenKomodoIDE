#!/usr/bin/env python3

import os
import sys

def apply_webextensions_integration_fix():
    """Apply the WebExtensions integration fix directly to the source files"""
    
    # Paths to the files we need to modify
    extensions_mozbuild_path = "mozilla/build/moz14000-ko12.0/mozilla/toolkit/components/extensions/moz.build"
    
    print("Applying WebExtensions integration fix...")
    
    # 1. Modify toolkit/components/extensions/moz.build
    print(f"Modifying {extensions_mozbuild_path}...")
    
    with open(extensions_mozbuild_path, 'r') as f:
        content = f.read()
    
    # Add WebExtensions integration configuration
    webextensions_config = '''if CONFIG['MOZ_KOMODO'] and CONFIG['MOZ_WEBEXTENSIONS']:
    DEFINES['MOZ_KOMODO_WEBEXTENSIONS'] = True
    SOURCES += ['komodo/extensions/KomodoExtensions.cpp']
    EXPORTS += ['komodo/extensions/KomodoExtensions.h']
    CXXFLAGS += ['-DMOZ_KOMODO_WEBEXTENSIONS']
'''
    
    # Find a good place to insert the WebExtensions configuration
    insert_marker = "DEFINES['MOZ_WEBEXTENSIONS'] = True"
    if insert_marker in content:
        new_content = content.replace(insert_marker, insert_marker + '\n\n' + webextensions_config)
        with open(extensions_mozbuild_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully added WebExtensions configuration to toolkit/components/extensions/moz.build")
    else:
        # If we can't find a good insertion point, append to the end
        with open(extensions_mozbuild_path, 'a') as f:
            f.write('\n' + webextensions_config)
        print("✓ Successfully appended WebExtensions configuration to toolkit/components/extensions/moz.build")
    
    print("✓ WebExtensions integration fix applied successfully!")
    return True

if __name__ == "__main__":
    success = apply_webextensions_integration_fix()
    sys.exit(0 if success else 1)