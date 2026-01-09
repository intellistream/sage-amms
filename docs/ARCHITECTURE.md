# SAGE-AMMS Architecture

This document describes the architecture and relationship between `sage-amms` and the main SAGE repository.

## Repository Structure

```
sage-amms/                          # This repository (independent AMM library)
├── sage/
│   └── libs/
│       └── amms/
│           ├── __init__.py         # Package initialization
│           ├── py.typed            # Type hints marker
│           ├── implementations/    # C++ source code
│           │   ├── include/        # C++ headers
│           │   │   ├── CPPAlgos/   # AMM algorithm implementations
│           │   │   ├── MatrixLoader/
│           │   │   ├── Utils/
│           │   │   └── ...
│           │   ├── src/            # C++ source files
│           │   │   ├── CPPAlgos/
│           │   │   ├── PyAMM.cpp   # Python bindings
│           │   │   └── ...
│           │   └── CMakeLists.txt
│           └── wrappers/           # Python wrappers
│               ├── __init__.py
│               └── pyamm.py        # PyAMM wrapper
├── tests/                          # Unit tests
├── pyproject.toml                  # Package metadata
├── setup.py                        # Build configuration
└── README.md
```

## Architecture Overview

### sage-amms (This Repository)

**Purpose**: Independent C++ AMM algorithm library with Python bindings

**Responsibilities**:
- C++ implementations of AMM algorithms
- PyBind11 bindings to expose C++ code to Python
- Building and distributing binary wheels via PyPI
- Low-level algorithm wrappers

**Does NOT contain**:
- Unified Python interface definitions
- Registry/factory pattern (that's in SAGE main repo)
- High-level abstractions

### SAGE Main Repository

**Purpose**: Unified machine learning system

**Responsibilities**:
- Define unified `AmmIndex` interface (abstract base class)
- Provide `register()`, `create()`, `registered()` factory functions
- Central algorithm registry
- Depend on `isage-amms` as optional dependency

**Location in SAGE**:
```python
# In SAGE main repo: sage/libs/amms/
sage/
└── libs/
    └── amms/
        ├── __init__.py              # Exports create, register, etc.
        ├── interface/
        │   ├── base.py              # AmmIndex abstract class
        │   ├── factory.py           # create(), register()
        │   └── registry.py          # Algorithm registry
        └── wrappers/                # (optional) additional wrappers
```

## Integration Pattern

### In SAGE Main Repo

```python
# sage/libs/amms/__init__.py (in SAGE main repo)
from sage.libs.amms.interface.base import AmmIndex
from sage.libs.amms.interface.factory import create, register, registered

# Auto-import implementations if available
try:
    import sage.libs.amms.implementations  # from isage-amms package
except ImportError:
    pass  # isage-amms not installed
```

### In sage-amms (This Repo)

```python
# sage/libs/amms/__init__.py (in this repo)
__version__ = "0.1.0"

# Just import wrappers, they register themselves
try:
    from sage.libs.amms.wrappers import pyamm
except ImportError:
    pass
```

### User Experience

```python
# Install
pip install sage  # Main SAGE package
pip install isage-amms  # AMM implementations

# Use
from sage.libs.amms import create, registered

print(registered())  # ['countsketch', 'fastjlt', 'crs', ...]

amm = create("countsketch", sketch_size=1000)
result = amm.multiply(matrix_a, matrix_b)
```

## PyPI Publication

### Package Name
`isage-amms` (with 'i' prefix for implementations)

### Version Scheme
- Follow semantic versioning: MAJOR.MINOR.PATCH
- Independent from SAGE main version
- SAGE main repo specifies: `isage-amms>=0.1.0`

### Distribution Strategy

1. **Wheels**: Pre-built binary wheels for multiple platforms
   - Linux: manylinux2014_x86_64
   - macOS: x86_64 and arm64
   - Windows: AMD64
   
2. **Source Distribution**: For custom builds

3. **Build Variants**:
   - CPU-only (default)
   - CUDA-enabled (optional, specify AMMS_ENABLE_CUDA=1)

## Build Process

### Local Development

```bash
# CPU-only build
python -m pip install -e .

# CUDA build
AMMS_ENABLE_CUDA=1 python -m pip install -e .
```

### CI/CD

- **GitHub Actions**: Automated builds for all platforms
- **cibuildwheel**: Multi-platform wheel building
- **Trusted Publishing**: Secure PyPI deployment

## Dependencies

### sage-amms Dependencies
- numpy>=1.20.0
- torch>=2.0.0 (for PyTorch integration)
- Build tools: CMake, C++14 compiler

### SAGE Main Repo
```toml
[project.optional-dependencies]
amms = ["isage-amms>=0.1.0"]
```

## Testing Strategy

### In sage-amms
- Test C++ algorithm correctness
- Test Python bindings work
- Test installation and imports

### In SAGE Main Repo  
- Test interface compliance
- Test registry functionality
- Integration tests with actual algorithms

## Migration Notes

This repository was extracted from the main SAGE repository to:
1. Allow independent versioning and releases
2. Reduce main SAGE repository size
3. Enable optional installation
4. Simplify CI/CD for C++ builds
5. Make AMM algorithms reusable in other projects
