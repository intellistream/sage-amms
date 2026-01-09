# SAGE-AMMS Scripts

This directory contains helper scripts for building, testing, and maintaining the project.

## Available Scripts

### Build Scripts
- **[build.sh](build.sh)** - Build the package with CPU or CUDA support
  ```bash
  # CPU-only build
  ./scripts/build.sh
  
  # CUDA-enabled build
  ./scripts/build.sh --cuda
  
  # Verbose output
  ./scripts/build.sh --verbose
  ```

### Testing Scripts
- **[test.sh](test.sh)** - Run quick tests to verify package structure
  ```bash
  ./scripts/test.sh
  ```

### Maintenance Scripts
- **[clean.sh](clean.sh)** - Clean build artifacts and temporary files
  ```bash
  ./scripts/clean.sh
  ```

## Usage from Root Directory

All scripts can be executed from the repository root:

```bash
# Build
./scripts/build.sh

# Test
./scripts/test.sh

# Clean
./scripts/clean.sh
```

## Adding New Scripts

When adding new scripts:
1. Make them executable: `chmod +x scripts/your-script.sh`
2. Add shebang line: `#!/bin/bash`
3. Add error handling: `set -e`
4. Document usage in this README
5. Update pre-commit hooks if needed
