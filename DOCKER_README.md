# OpenKomodoIDE Docker Build Environment

This directory contains Docker configuration for building OpenKomodoIDE in isolated containers.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Docker Setup](#docker-setup)
3. [Available Services](#available-services)
4. [Customization](#customization)
5. [ARM64 Support](#arm64-support)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### Build and run the complete build process

```bash
docker-compose build
docker-compose up komodo-build
```

### Start an interactive shell

```bash
docker-compose run komodo-shell
```

### Run tests

```bash
docker-compose run komodo-test
```

## Docker Setup

### Prerequisites

- Docker (version 20.10+ recommended)
- Docker Compose (version 1.29+)
- At least 16GB RAM recommended
- 50GB+ free disk space

### Building the Docker Image

```bash
docker-compose build
```

This will create a Docker image with all required build dependencies.

### Running the Build

```bash
docker-compose up komodo-build
```

This will:
1. Start a container with the build environment
2. Mount the current directory as `/home/builduser/build`
3. Run the complete build process
4. Save build artifacts in the current directory

## Available Services

### 1. komodo-build

Runs the complete build process:

```bash
docker-compose run komodo-build
```

Environment variables:
- `KOMODO_VERSION=12.0` - Version to build
- `FIREFOX_VERSION=140.0` - Firefox version
- `DEBUG=0` - Set to 1 for debug build
- `CLEAN=0` - Set to 1 to clean before build

### 2. komodo-test

Runs the test suite:

```bash
docker-compose run komodo-test
```

### 3. komodo-shell

Starts an interactive shell for manual building:

```bash
docker-compose run komodo-shell
```

## Customization

### Custom Build Configuration

Create a `build_config.json` file to customize the build:

```json
{
  "version": "12.0",
  "firefox_version": "140.0",
  "platform": "linux",
  "build_type": "release",
  "jobs": 8,
  "enable_debug": false,
  "enable_symbols": true,
  "targets": ["all"],
  "clean_build": false
}
```

### Custom Dockerfile

For different platforms, create custom Dockerfiles:

- `Dockerfile.debian` - Debian Bookworm (default)
- `Dockerfile.ubuntu` - Ubuntu 22.04 LTS
- `Dockerfile.arm64` - ARM64 build environment

## ARM64 Support

### Building for ARM64

To build for ARM64, use the ARM64 Dockerfile:

```bash
docker build -f Dockerfile.arm64 -t openkomodoide-build:arm64 .
docker run -it --rm -v $(pwd):/home/builduser/build openkomodoide-build:arm64
```

### Cross-compilation

For cross-compilation from x86_64 to ARM64:

```bash
docker run -it --rm \
  -v $(pwd):/home/builduser/build \
  -e PLATFORM=linux-arm64 \
  -e KOMODO_VERSION=12.0 \
  openkomodoide-build:latest \
  build
```

## Troubleshooting

### Common Issues

#### 1. Out of Memory

```bash
# Limit memory usage
docker run --memory=8g ...

# Or increase swap
docker run --memory-swap=16g ...
```

#### 2. Permission Issues

```bash
# Ensure proper permissions
chmod -R 755 .
chown -R $(id -u):$(id -g) .
```

#### 3. Build Cache Issues

```bash
# Clear Docker cache
docker system prune -a

# Clear ccache
docker-compose run komodo-shell rm -rf /home/builduser/.ccache/*
```

#### 4. Missing Dependencies

```bash
# Update the Dockerfile with missing dependencies
# Rebuild the image
docker-compose build --no-cache
```

## Advanced Usage

### Multi-stage Builds

For production builds, use multi-stage Docker builds to reduce image size.

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: OpenKomodoIDE Build

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      
      - name: Build Docker image
        run: docker-compose build
      
      - name: Run build
        run: docker-compose run komodo-build
      
      - name: Run tests
        run: docker-compose run komodo-test
```

### Custom Build Targets

To build specific targets:

```bash
docker-compose run komodo-shell build_automation.py build --targets mozilla pyxpcom
```

## Docker Image Structure

```
/
├── home/
│   └── builduser/
│       ├── build/          # Build directory (mounted from host)
│       ├── .ccache/        # Build cache (persistent volume)
│       └── .local/         # User-specific files
├── usr/
│   ├── local/             # Installed tools
│   └── bin/               # System tools
└── var/
    └── cache/             # APT cache
```

## Performance Optimization

### Build Cache

The Docker setup uses ccache for faster rebuilds. The cache is stored in a Docker volume for persistence.

### Parallel Builds

The build system automatically uses all available CPU cores for parallel compilation.

### Volume Mounting

The current directory is mounted into the container for easy access to build artifacts.

## Security

- The container runs as a non-root user (`builduser`)
- Sensitive operations require sudo
- Build artifacts are owned by the build user

## Cleanup

```bash
# Remove containers
docker-compose down

# Remove images
docker rmi openkomodoide-build:latest

# Remove volumes
docker volume rm docker_komodo-cache
```

## Support

For issues with the Docker setup:

1. Check Docker logs: `docker logs komodo-build`
2. Enter the container: `docker-compose run komodo-shell`
3. Check build logs in the `logs/` directory

## License

This Docker configuration is provided under the same license as OpenKomodoIDE.