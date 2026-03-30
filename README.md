# SAGE-AMMS - Approximate Matrix Multiplication Algorithms

[![PyPI version](https://badge.fury.io/py/isage-amms.svg)](https://badge.fury.io/py/isage-amms)
[![Build Status](https://github.com/intellistream/sage-amms/workflows/Build%20and%20Test/badge.svg)](https://github.com/intellistream/sage-amms/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

> Independent C++ implementation package for Approximate Matrix Multiplication (AMM) algorithms, extracted from the [SAGE project](https://github.com/intellistream/SAGE).

**Status**: 🚀 Active Development
**PyPI Package**: [`isage-amms`](https://pypi.org/project/isage-amms/)
**Parent Project**: [SAGE - Unified ML System](https://github.com/intellistream/SAGE)

## Overview

SAGE-AMMS provides high-performance C++ implementations of various approximate matrix multiplication algorithms with Python bindings. This package was extracted from the main SAGE repository to:

- ✅ Enable independent versioning and releases
- ✅ Reduce main SAGE repository size
- ✅ Allow optional installation
- ✅ Simplify CI/CD for C++ builds
- ✅ Make AMM algorithms reusable in other projects

## Quick Start

### Installation

#### From PyPI (Recommended)

```bash
pip install isage-amms
```

#### From Source

**Prerequisites**:
- CMake >= 3.14
- C++14 compatible compiler
- Python >= 3.8
- PyTorch >= 2.0.0

```bash
# Clone the repository
git clone https://github.com/intellistream/sage-amms.git
cd sage-amms

# Install in development mode
pip install -e .

# Or build wheel
python -m build --wheel
pip install dist/*.whl
```

### Usage

This package provides the algorithm implementations. The unified interface is provided by the main SAGE package:

```python
# Install both packages
# pip install sage isage-amms

# Import from SAGE (provides the interface)
from sage.libs.amms import create, registered

# Check available algorithms
print(registered())
# Output: ['countsketch', 'fastjlt', 'crs', 'bcrs', ...]

# Create an algorithm instance
amm = create("countsketch", sketch_size=1000)

# Perform approximate matrix multiplication
import numpy as np
A = np.random.randn(1000, 500)
B = np.random.randn(500, 800)
result = amm.multiply(A, B)  # Approximate A @ B
```

## Architecture

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

AMMS provides a unified interface for various approximate matrix multiplication algorithms, similar
to how ANNS provides a unified interface for approximate nearest neighbor search algorithms.

## Structure

```
sage-amms/
├── sage/libs/amms/
│   ├── __init__.py              # Package initialization
│   ├── implementations/         # C++ source code
│   │   ├── include/             # C++ headers
│   │   │   ├── CPPAlgos/        # Core AMM algorithm implementations
│   │   │   ├── MatrixLoader/    # Matrix loading utilities
│   │   │   ├── Utils/           # Utility functions
│   │   │   └── ...
│   │   ├── src/                 # C++ implementation files
│   │   │   ├── CPPAlgos/        # Algorithm implementations
│   │   │   ├── PyAMM.cpp        # Python bindings
│   │   │   └── ...
│   │   └── CMakeLists.txt       # Build configuration
│   └── wrappers/                # Python wrappers
│       └── pyamm.py             # PyAMM wrapper
├── tests/                       # Unit tests
├── pyproject.toml               # Package metadata
└── setup.py                     # Build configuration
```

## Algorithms Included

This package provides implementations of various AMM algorithms:

### Sketching-based Algorithms

- **CountSketch**: Count-Min Sketch based AMM
- **FastJLT**: Fast Johnson-Lindenstrauss Transform
- **RIP**: Random Index Projection
- **TugOfWar**: Tug-of-war sketch

### Sampling-based Algorithms

- **CRS**: Coordinate-wise Random Sampling
- **CRSV2**: Improved CRS
- **BCRS**: Block-wise CRS
- **EWS**: Entry-wise Sampling

### Quantization-based Algorithms

- **ProductQuantization**: Product quantization for AMM
- **VectorQuantization**: Vector quantization
- **INT8**: 8-bit integer quantization

### Advanced Algorithms

- **CoOccurringFD**: Co-occurring Feature Detection
- **BetaCoOFD**: Beta Co-occurring Feature Detection
- **BlockLRA**: Block Low-Rank Approximation
- **CLMM**: Clustered Low-rank Matrix Multiplication
- **SMPCA**: Symmetric Matrix PCA
- **WeightedCR**: Weighted Cross-Ranking

## Installation

### From PyPI (Recommended)

```bash
# Install CPU-only version
pip install isage-amms
```

This installs the **CPU-only version** with all core AMM algorithms.

### From Source

**Prerequisites**:
- CMake >= 3.14
- C++14 compatible compiler (GCC 7+, Clang 5+, MSVC 2017+)
- Python 3.8-3.12
- PyTorch >= 2.0.0
- 64GB+ RAM recommended for building

```bash
# Clone repository
git clone https://github.com/intellistream/sage-amms.git
cd sage-amms

# CPU-only build
pip install -e .

# CUDA-enabled build
AMMS_ENABLE_CUDA=1 pip install -e .

# Explicitly disable CUDA
AMMS_ENABLE_CUDA=0 pip install -e .
```

### Build Options

#### CUDA Support

`AMMS_ENABLE_CUDA` is an explicit switch. Use `1` to enable CUDA and `0` to force CPU build.

```bash
# Enable CUDA
AMMS_ENABLE_CUDA=1 pip install isage-amms --no-binary :all:

# Force CPU-only build
AMMS_ENABLE_CUDA=0 pip install isage-amms --no-binary :all:

# Specify CUDA path
CUDA_HOME=/usr/local/cuda AMMS_ENABLE_CUDA=1 pip install isage-amms --no-binary :all:
```

#### Low Memory Build

Build mode is now selected automatically by memory probe:

- If available memory >= `AMMS_FAST_BUILD_MEMORY_GB` (default `48`), fast build is enabled.
- Otherwise low-memory mode is enabled to reduce OOM risk.

```bash
# Default behavior (auto memory probe)
pip install -e .
```

You can still set it explicitly:

```bash
AMMS_LOW_MEMORY_BUILD=1 pip install isage-amms --no-binary :all:
```

If you have enough RAM and want faster compilation:

```bash
AMMS_FAST_BUILD=1 AMMS_MAX_JOBS=4 pip install -e .
```

Adjust auto fast-build threshold:

```bash
AMMS_FAST_BUILD_MEMORY_GB=64 pip install -e .
```
instructions.

```bash
# Navigate to amms directory
cd packages/sage-libs/src/sage/libs/amms

# Quick build
./quick_build.sh

# Or use the full build script with options
./publish_to_pypi.sh --build-only --low-memory

# Install locally
pip install dist/isage_amms-*.whl
```

### Build Options

The build system supports various options:

```bash
# Low-memory build (default)
export AMMS_LOW_MEMORY_BUILD=1

# Default parallelism is 1 job in low-memory mode
export AMMS_MAX_JOBS=1

# Enable CUDA support
export AMMS_ENABLE_CUDA=1
export CUDA_HOME=/usr/local/cuda

# Override parallel jobs when memory is sufficient
export AMMS_MAX_JOBS=4
```

## Build and Publish to PyPI

For maintainers who want to build and publish to PyPI:

```bash
# Build only (dry-run, no upload)
./publish_to_pypi.sh

# Build and upload to TestPyPI
./publish_to_pypi.sh --test-pypi --no-dry-run

# Build and upload to PyPI (production)
./publish_to_pypi.sh --no-dry-run

# With CUDA and low-memory options
./publish_to_pypi.sh --cuda --low-memory --no-dry-run
```

See [BUILD_PUBLISH.md](BUILD_PUBLISH.md) for comprehensive build and publish documentation.

## Usage

### Using the Unified Interface

```python
from sage.libs.amms import create_amm_index

# Create an AMM index using the factory
amm = create_amm_index("countsketch", config={
    "sketch_size": 1000,
    "hash_functions": 5
})

# Perform approximate matrix multiplication
result = amm.multiply(matrix_a, matrix_b)
```

### Direct Algorithm Usage

```python
from sage.libs.amms.wrappers.pyamm import PyAMM

# Create a specific AMM algorithm instance
amm = PyAMM.CountSketch(sketch_size=1000)

# Use the algorithm
result = amm.multiply(matrix_a, matrix_b)
```

## Benchmarking

For benchmarking AMM algorithms, see the `sage-benchmark` package:

```bash
# Run AMM benchmarks
sage-dev benchmark amm --algorithms countsketch,fastjlt --datasets dataset1
```

See `packages/sage-benchmark/src/sage/benchmark/benchmark_libamm/README.md` for details.

### Issue #6 regression checks

```bash
# Build-path matrix + perf baseline regression
pytest -q tests/test_issue6_build_matrix_and_perf_baseline.py

# CUDA/CPU switch cleanup regression
pytest -q tests/test_issue5_cuda_cpu_switch_cleanup.py
```

## Migration from libamm

This module is refactored from the original libamm submodule:

- **Algorithm implementations**: Moved from `libamm/include/CPPAlgos` and `libamm/src/CPPAlgos` to
  `amms/implementations/`
- **Benchmarking code**: Moved from `libamm/benchmark/` to `sage-benchmark/benchmark_libamm/`
- **Python bindings**: Refactored into `amms/wrappers/pyamm/`
- **Interface layer**: New unified interface similar to ANNS

## Architecture Alignment

AMMS follows SAGE's architecture principles:

- **Layer 3 (L3-libs)**: Algorithm implementations and interfaces
- **Separation of concerns**: Core algorithms (amms/) vs benchmarking (benchmark_libamm/)
- **Unified interfaces**: Factory pattern for algorithm creation
- **Modular design**: Independent wrappers for different algorithm families

## References

- Original LibAMM paper and documentation
- PyTorch integration guide
- AMM algorithm theory and applications

## Contributing

When adding new AMM algorithms:

1. Add C++ implementation to `implementations/include/CPPAlgos/` and `implementations/src/CPPAlgos/`
1. Create Python wrapper in `wrappers/`
1. Register algorithm in `interface/registry.py`
1. Add tests in `sage-libs/tests/`
1. Add benchmark configuration in `sage-benchmark/benchmark_libamm/`

See `CONTRIBUTING.md` at project root for detailed guidelines.
