#!/usr/bin/env python3

import os
import sys

def apply_pyxpcom_integration_fix():
    """Apply the PyXPCOM integration fix directly to the source files"""
    
    # Paths to the files we need to modify
    js_mozbuild_path = "mozilla/build/moz14000-ko12.0/mozilla/js/xpconnect/src/moz.build"
    dom_mozbuild_path = "mozilla/build/moz14000-ko12.0/mozilla/dom/bindings/moz.build"
    toolkit_mozconfigure_path = "mozilla/build/moz14000-ko12.0/mozilla/toolkit/moz.configure"
    xpcom_mozbuild_path = "mozilla/build/moz14000-ko12.0/mozilla/xpcom/build/moz.build"
    
    print("Applying PyXPCOM integration fix...")
    
    # 1. Modify js/xpconnect/src/moz.build
    print(f"Modifying {js_mozbuild_path}...")
    
    with open(js_mozbuild_path, 'r') as f:
        content = f.read()
    
    # Add PyXPCOM integration configuration
    pyxpcom_config = '''if CONFIG['MOZ_KOMODO'] and CONFIG['MOZ_PYXPCOM']:
    DEFINES['MOZ_KOMODO_PYXPCOM'] = True
    SOURCES += ['komodo/pyxpcom/KomodoPyXPCOM.cpp']
    EXPORTS += ['komodo/pyxpcom/KomodoPyXPCOM.h']
    CXXFLAGS += ['-DMOZ_KOMODO_PYXPCOM']
'''
    
    # Find a good place to insert the PyXPCOM configuration
    insert_marker = "DEFINES['MOZ_XPCOM'] = True"
    if insert_marker in content:
        new_content = content.replace(insert_marker, insert_marker + '\n\n' + pyxpcom_config)
        with open(js_mozbuild_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully added PyXPCOM configuration to js/xpconnect/src/moz.build")
    else:
        # If we can't find a good insertion point, append to the end
        with open(js_mozbuild_path, 'a') as f:
            f.write('\n' + pyxpcom_config)
        print("✓ Successfully appended PyXPCOM configuration to js/xpconnect/src/moz.build")
    
    # 2. Modify dom/bindings/moz.build
    print(f"Modifying {dom_mozbuild_path}...")
    
    with open(dom_mozbuild_path, 'r') as f:
        content = f.read()
    
    # Add WebIDL PyXPCOM integration configuration
    webidl_pyxpcom_config = '''if CONFIG['MOZ_KOMODO'] and CONFIG['MOZ_PYXPCOM']:
    DEFINES['MOZ_KOMODO_WEBIDL'] = True
    SOURCES += ['komodo/bindings/KomodoWebIDL.cpp']
    EXPORTS += ['komodo/bindings/KomodoWebIDL.h']
    CXXFLAGS += ['-DMOZ_KOMODO_WEBIDL']
'''
    
    # Find a good place to insert the WebIDL PyXPCOM configuration
    insert_marker = "DEFINES['MOZ_WEBIDL'] = True"
    if insert_marker in content:
        new_content = content.replace(insert_marker, insert_marker + '\n\n' + webidl_pyxpcom_config)
        with open(dom_mozbuild_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully added WebIDL PyXPCOM configuration to dom/bindings/moz.build")
    else:
        # If we can't find a good insertion point, append to the end
        with open(dom_mozbuild_path, 'a') as f:
            f.write('\n' + webidl_pyxpcom_config)
        print("✓ Successfully appended WebIDL PyXPCOM configuration to dom/bindings/moz.build")
    
    # 3. Modify toolkit/moz.configure
    print(f"Modifying {toolkit_mozconfigure_path}...")
    
    with open(toolkit_mozconfigure_path, 'r') as f:
        content = f.read()
    
    # Add PyXPCOM integration options
    pyxpcom_options = '''# Komodo PyXPCOM integration
if depends('--enable-komodo', '--enable-pyxpcom')(lambda komodo, pyxpcom: komodo and pyxpcom):
    set_config('MOZ_KOMODO_PYXPCOM', True)
    set_define('MOZ_KOMODO_PYXPCOM', True)
    add_old_configure_assignment('MOZ_KOMODO_PYXPCOM', True)
'''
    
    # Find a good place to insert the PyXPCOM options
    insert_marker = "option('--enable-pyxpcom', env='MOZ_PYXPCOM'"
    if insert_marker in content:
        # Find the end of the pyxpcom option block
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if insert_marker in line:
                # Find the end of this option block (next option or end of section)
                j = i + 1
                while j < len(lines) and (lines[j].startswith((' ', '\t')) or not lines[j].strip()):
                    j += 1
                # Insert after the option block
                lines.insert(j, pyxpcom_options)
                break
        new_content = '\n'.join(lines)
        with open(toolkit_mozconfigure_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully added PyXPCOM options to toolkit/moz.configure")
    else:
        # If we can't find a good insertion point, append to the end
        with open(toolkit_mozconfigure_path, 'a') as f:
            f.write('\n' + pyxpcom_options)
        print("✓ Successfully appended PyXPCOM options to toolkit/moz.configure")
    
    # 4. Modify xpcom/build/moz.build
    print(f"Modifying {xpcom_mozbuild_path}...")
    
    with open(xpcom_mozbuild_path, 'r') as f:
        content = f.read()
    
    # Add XPCOM PyXPCOM integration configuration
    xpcom_pyxpcom_config = '''if CONFIG['MOZ_KOMODO'] and CONFIG['MOZ_PYXPCOM']:
    DEFINES['MOZ_KOMODO_XPCOM'] = True
    SOURCES += ['komodo/xpcom/KomodoXPCOM.cpp']
    EXPORTS += ['komodo/xpcom/KomodoXPCOM.h']
    CXXFLAGS += ['-DMOZ_KOMODO_XPCOM']
'''
    
    # Find a good place to insert the XPCOM PyXPCOM configuration
    insert_marker = "DEFINES['MOZ_XPCOM'] = True"
    if insert_marker in content:
        new_content = content.replace(insert_marker, insert_marker + '\n\n' + xpcom_pyxpcom_config)
        with open(xpcom_mozbuild_path, 'w') as f:
            f.write(new_content)
        print("✓ Successfully added XPCOM PyXPCOM configuration to xpcom/build/moz.build")
    else:
        # If we can't find a good insertion point, append to the end
        with open(xpcom_mozbuild_path, 'a') as f:
            f.write('\n' + xpcom_pyxpcom_config)
        print("✓ Successfully appended XPCOM PyXPCOM configuration to xpcom/build/moz.build")
    
    print("✓ PyXPCOM integration fix applied successfully!")
    return True

if __name__ == "__main__":
    success = apply_pyxpcom_integration_fix()
    sys.exit(0 if success else 1)