# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- CI/CD workflows for automated building and testing
- PyPI publishing automation
- Comprehensive documentation

## [0.1.0] - 2026-01-09

### Added
- Initial release of SAGE-AMMS as independent package
- Extracted from main SAGE repository
- C++ implementations of AMM algorithms:
  - Sketching-based: CountSketch, FastJLT, RIP, TugOfWar
  - Sampling-based: CRS, CRSV2, BCRS, EWS
  - Quantization-based: ProductQuantization, VectorQuantization, INT8
  - Advanced: CoOccurringFD, BetaCoOFD, BlockLRA, CLMM, SMPCA, WeightedCR
- Python bindings via PyBind11
- CMake-based build system
- Support for CPU-only and CUDA builds
- Unit tests and integration tests
- Comprehensive documentation (README, ARCHITECTURE, CONTRIBUTING, PUBLISHING)

### Changed
- Reorganized directory structure for independent distribution
- Updated package metadata for PyPI publication
- Simplified installation process

### Fixed
- Build system compatibility across platforms
- Memory usage during compilation

[Unreleased]: https://github.com/intellistream/sage-amms/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/intellistream/sage-amms/releases/tag/v0.1.0
