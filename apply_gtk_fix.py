#!/usr/bin/env python3

import os
import sys

def apply_gtk_integration_fix():
    """Apply the GTK integration fix directly to the source files"""
    
    # Paths to the files we need to modify
    moz_build_path = "mozilla/build/moz14000-ko12.0/mozilla/widget/gtk/moz.build"
    ns_window_path = "mozilla/build/moz14000-ko12.0/mozilla/widget/gtk/nsWindow.cpp"
    
    print("Applying GTK integration fix...")
    
    # First, let's modify the moz.build file
    print(f"Modifying {moz_build_path}...")
    
    with open(moz_build_path, 'r') as f:
        content = f.read()
    
    # Find the location to insert the Komodo integration code
    # We'll insert it after the MOZ_WAYLAND section
    insert_marker = 'if CONFIG["MOZ_ENABLE_DBUS"]:'
    komodo_integration = '''    # Komodo GTK integration for Firefox 140 ESR
    if CONFIG['MOZ_KOMODO']:
        DEFINES['MOZ_KOMODO_GTK'] = True
        SOURCES += ['komodo/gtk/KomodoGTKIntegration.cpp']
        EXPORTS += ['komodo/gtk/KomodoGTKIntegration.h']
        CXXFLAGS += ['-DMOZ_KOMODO_GTK']

'''
    
    if insert_marker in content:
        new_content = content.replace(insert_marker, komodo_integration + insert_marker)
        with open(moz_build_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully modified moz.build")
    else:
        print("✗ Could not find insertion point in moz.build")
        return False
    
    # Now modify the nsWindow.cpp file
    print(f"Modifying {ns_window_path}...")
    
    with open(ns_window_path, 'r') as f:
        content = f.read()
    
    # Insert Komodo initialization in Create method
    create_marker = '  BaseCreate(aParent, aInitData);'
    komodo_create_code = '''#ifdef MOZ_KOMODO_GTK
    // Komodo GTK integration for Firefox 140 ESR
    KomodoGTKIntegration::InitializeWindow(this);
    mKomodoWindow = new KomodoWindowWrapper(this);
#endif

'''
    
    if create_marker in content:
        new_content = content.replace(create_marker, create_marker + '\n' + komodo_create_code)
        with open(ns_window_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully modified nsWindow.cpp Create method")
    else:
        print("✗ Could not find Create method insertion point")
        return False
    
    # Insert Komodo cleanup in Destroy method
    destroy_marker = '  if (mRootAccessible) {\n    mRootAccessible = nullptr;\n  }\n#endif'
    komodo_destroy_code = '''\n#ifdef MOZ_KOMODO_GTK
    // Cleanup Komodo GTK integration
    KomodoGTKIntegration::CleanupWindow(this);
    delete mKomodoWindow;
#endif
'''
    
    if destroy_marker in content:
        new_content = content.replace(destroy_marker, destroy_marker + komodo_destroy_code)
        with open(ns_window_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully modified nsWindow.cpp Destroy method")
    else:
        print("✗ Could not find Destroy method insertion point")
        return False
    
    print("✓ GTK integration fix applied successfully!")
    return True

if __name__ == "__main__":
    success = apply_gtk_integration_fix()
    sys.exit(0 if success else 1)