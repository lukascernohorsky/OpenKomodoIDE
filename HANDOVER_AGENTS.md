# OpenKomodoIDE Build Handover Documentation

## Project Status and Context

This document provides complete information for the AI agent taking over the OpenKomodoIDE build process.

### Current State
- **Project**: OpenKomodoIDE (Firefox 140 ESR + Python 3.11+ integration)
- **Current Branch**: `test-build-fix`
- **Build System**: Modern build automation supporting Firefox 140 ESR
- **Configuration**: Ready for Komodo 14.10 with Firefox 140.0 ESR

### Build Requirements

#### System Requirements
- **OS**: Linux (Debian 12+ recommended), macOS, or Windows
- **CPU**: x86_64 (ARM64 supported with patches)
- **RAM**: 8GB+ (16GB recommended for full build)
- **Disk**: 50GB+ free space

#### Software Requirements
- **Python**: 3.11+ (system Python, no prebuilt versions needed)
- **Autoconf**: 2.71+ (CRITICAL - documentation incorrectly says 2.69)
- **Build Tools**: gcc/g++ 10+, make, patch, zip, tar
- **Git**: 2.30+
- **Rust**: 1.60+ (for Firefox 140 ESR build)
- **Node.js**: 16+ (for build tools)

### Build Process Overview

#### Phase 1: Preparation
```bash
# Install dependencies (Debian/Ubuntu)
sudo apt-get update
sudo apt-get install -y git make gcc g++ patch zip tar autoconf271 python3 python3-pip
pip3 install packaging

# Create patches symlink
cd /home/lc/projekty/OpenKomodoIDE
ln -s mozilla/patches-new patches-new
```

#### Phase 2: Source Download
```bash
cd mozilla
python3 build.py src
```

#### Phase 3: Patch Application
```bash
python3 build.py patch
```

#### Phase 4: Configuration
```bash
python3 build.py configure
```

#### Phase 5: Full Build
```bash
python3 build.py all
```

#### Phase 6: Testing and Packaging
```bash
python3 build.py test
python3 build.py packages
```

### Critical Issues Resolved

1. **Autoconf Version**: Build system correctly uses autoconf 2.71+ for Firefox 140 ESR
2. **Python 3.11**: System Python integration working correctly
3. **Patch System**: Modern patch application system in place
4. **Build Configuration**: Properly configured for Firefox 140 ESR

### Known Issues and Workarounds

1. **Documentation Inaccuracy**: Some docs still reference autoconf 2.69 (should be 2.71+)
   - Files to update: `docs/Linux_build_guide.md`, `docs/BUILD.txt`

2. **Patch Application**: Some patches marked as "temporarily disabled" in `__patchinfo__.py`
   - Review and enable as needed for complete functionality

3. **Build Time**: Full build can take 1-4 hours depending on system

### Build System Architecture

```
OpenKomodoIDE/
├── build.py                  # Main build entry point
├── build_automation.py       # Modern build automation
├── mozilla/
│   ├── build.py              # Mozilla-specific build logic
│   ├── patches-new/          # Patch system for Firefox 140 ESR
│   │   ├── komodo-140.0/     # Komodo integration patches
│   │   └── mozilla-140.0/    # Firefox 140 ESR patches
│   └── config.py             # Current build configuration
└── docs/                     # Documentation (needs autoconf version updates)
```

### Expected Build Output

- **Build Directory**: `mozilla/build/moz14000-ko14.10/`
- **Firefox Source**: `mozilla/build/moz14000-ko14.10/mozilla/`
- **Build Artifacts**: `mozilla/build/moz14000-ko14.10/mozilla/obj-x86_64-pc-linux-gnu/`
- **Final Packages**: `dist/` directory

### Debugging and Troubleshooting

1. **Build Failures**: Check `mozilla/build.log` for detailed error information
2. **Patch Conflicts**: Run `python3 build.py patch --dry-run` to test patches
3. **Dependency Issues**: Use `python3 build.py check-deps` to verify requirements

### Next Steps for AI Agent

1. **Immediate Tasks**:
   - Update documentation to correct autoconf version (2.71+)
   - Execute the build process step by step
   - Monitor for any patch application issues

2. **Long-term Tasks**:
   - Review and enable disabled patches in `__patchinfo__.py`
   - Optimize build process for faster compilation
   - Update documentation with modern build instructions

### Success Criteria

- ✅ Firefox 140 ESR source downloaded and patched
- ✅ Build configuration completed without errors
- ✅ Full build completes with Komodo integration
- ✅ Distribution packages created successfully
- ✅ All tests pass

### Contact and Support

For any issues beyond this documentation:
- Refer to `docs/DEVELOPER_GUIDE.md`
- Check `docs/FIREFOX_140_ESR_PATCHES.md` for patch details
- Review `docs/PYTHON3_MIGRATION_BUILD.md` for Python 3 specifics