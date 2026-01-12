# OpenKomodoIDE

OpenKomodoIDE is an open-source implementation of Komodo IDE based on Firefox 140 ESR. This project aims to provide a modern, extensible IDE platform built on web technologies.

## Features

- **Modern Architecture**: Built on Firefox 140 ESR with modern web technologies
- **Extensible**: Designed for easy extension and customization
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Developer-Friendly**: Built with developers in mind

## Getting Started

### Prerequisites

- Node.js (>=14.0.0)
- npm (>=6.0.0)
- Python 3.11+
- Git
- autoconf 2.71+
- Firefox 140 ESR source code (automatically downloaded)

**For complete build dependencies, see:** [BUILD_DEPENDENCIES.md](BUILD_DEPENDENCIES.md)

### Critical Dependencies

The following packages are **required** for building with Firefox 140 ESR:

```bash
# WASM/WebAssembly support (critical)
sudo apt-get install lld-19 wasi-libc clang-19 libclang-rt-19-dev-wasm32
```

If you encounter WASM-related errors, you can build without WASM sandboxing:
```bash
./mach configure --without-wasm-sandboxed-libraries
```

### Job Configuration

The build system defaults to 2 jobs but can be configured:

```bash
# Use default 2 jobs
python3 build.py build

# Use custom job count
python3 build.py build --jobs 4
python3 build.py build --jobs 8
```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/OpenKomodo/OpenKomodoIDE.git
   cd OpenKomodoIDE
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Initialize build environment:
   ```bash
   python3 build_automation.py --init
   ```

4. Build the project:
   ```bash
   python3 build_automation.py build
   ```

5. Create distribution package:
   ```bash
   python3 build_automation.py package
   ```

## Firefox Patch System

OpenKomodoIDE uses a sophisticated patch system to apply necessary modifications to the Firefox 140 ESR source code. This system ensures that all changes are versioned, testable, and easily maintainable.

### How It Works

1. **Patch Files**: All modifications to Firefox source code are stored as patch files in the `patches/` directory
2. **Automatic Application**: Patches are automatically applied during the build process
3. **Revert Capability**: Patches can be easily reverted if needed
4. **Testing**: The build system includes comprehensive testing

### Patch Directory Structure

```
patches/
├── firefox-import-fixes/      # Fixes for Python import statements
├── firefox-configure-fixes/   # Fixes for moz.configure files  
├── firefox-missing-files/     # Missing files required by OpenKomodoIDE
└── README.md                  # Complete patch system documentation
```

### Manual Patch Application



### Reverting Patches

To revert all applied patches:

```bash
python3 build_automation.py --revert-patches
```

### Creating New Patches

To create a new patch for a modified file:

```bash
cd mozilla/build/moz1400-ko120/mozilla
git diff path/to/modified/file.py > ../../../../patches/category/new-patch.patch
```

See `patches/README.md` for complete documentation.

### Patch Creation Tool

OpenKomodoIDE includes a patch creation tool to simplify the process:

```bash
# Create a new patch
python3 tools/create_patch.py python/mozbuild/mozbuild/base.py base-import-fix --category import-fixes

# Show patch content after creation
python3 tools/create_patch.py python/mozbuild/mozbuild/base.py base-import-fix --category import-fixes --show
```

The tool automatically:
- Validates file paths
- Creates proper patch structure
- Places patches in correct categories
- Shows change statistics
=======
=======

## Build System

OpenKomodoIDE uses a simplified build system that automatically:

- Downloads Firefox 140 ESR source code
- Creates the correct directory structure
- Builds the complete IDE
- Creates distribution packages

### Directory Structure

```
OpenKomodoIDE/
├── mozilla/
│   └── build/
│       └── moz14000-ko14.10/  # Version-specific
│           └── mozilla/       # Firefox source code
├── build/                # Build outputs
├── dist/                 # Distribution packages
└── logs/                 # Build logs
```

### Build Commands

- **Initialize**: Sets up the build environment
  ```bash
  python3 build_automation.py --init
  ```

- **Build**: Compiles the IDE (auto-downloads source if needed)
  ```bash
  python3 build_automation.py build
  ```

- **Package**: Creates distribution packages
  ```bash
  python3 build_automation.py package
  ```

- **Clean**: Removes build outputs
  ```bash
  python3 build_automation.py --clean
  ```

### Patch Management Commands



- **Revert Patches**: Revert all applied patches
  ```bash
  python3 build_automation.py --revert-patches
  ```

### Advanced Patch Features

- **Patch Validation**: Automatic validation before application
- **Patch Dependencies**: Define dependencies between patches
- **Platform-Specific Patches**: Automatic platform detection
- **Auto-Generation**: Create patches for modified files automatically

```bash
# Auto-detect and create patches for all modified files
python3 tools/create_patch.py auto --show
```
=======
=======

### Configuration

Edit `build_config.json` to customize the build:

```json
{
  "platform": "linux",
  "version": "12.0",
  "firefox_version": "140.0",
  "build_type": "release",
  "jobs": 6,
  "enable_debug": false,
  "enable_symbols": true
}
```

## Project Structure

```
src/
├── main/              # Main application code
│   ├── application/   # Application entry point
│   └── core/          # Core functionality
```

## Migration Notes

This project has been migrated from Python 2.x to Python 3.11 and from older Firefox versions to Firefox 140 ESR. The following legacy files have been removed:

### Removed Python 2.x Files
- Build scripts: `mk24`, `mk25`, `mk26`
- Python 2.x specific UDL files
- Platform-specific Python 2.7 libraries
- Prebuilt Python 2.7 binaries

### Removed Firefox 35.0 Files
- All patches in `mozilla/patches-new/komodo-35.0/`
- All patches in `mozilla/patches-new/mozilla-35.0/`
- All patches in `mozilla/patches-new/mozilla-35.0-pyxpcom/`

### Updated Files
- `src/install/wix/feature-core.ini` - Removed Python 2.7 DLL references
├── components/        # Reusable components
├── integrations/      # Integration layers
│   └── firefox/       # Firefox integration
└── tests/             # Test suite
```

## Development

### Running Tests

```bash
npm test
```

### Linting

```bash
npm run lint
```

### Building

```bash
npm run build
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MPL-2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Mozilla Foundation for Firefox
- All contributors and supporters

## Support

For support, please open an issue on the GitHub repository.

## Roadmap

- Complete Firefox 140 ESR integration
- Implement core IDE functionality
- Add extension system
- Improve performance and stability
- Add more language support

## Contact

For more information, please visit our [GitHub repository](https://github.com/OpenKomodo/OpenKomodoIDE).