# GitHub Copilot Instructions for sage-amms

## Project Context
- **Repository**: `intellistream/sage-amms`
- **PyPI Package**: `isage-amms`
- **Purpose**: Independent C++ AMM (Approximate Matrix Multiplication) algorithm implementations with PyBind11 bindings
- **Python Namespace**: `sage.libs.amms`
- **C++ Sources**: `sage/libs/amms/implementations/`
- **Important**: The unified AMM interface/registry lives in the main SAGE repo, NOT here. This repo only provides implementations.

## Coding Guidelines
- Do NOT add interface/registry code here (that belongs to SAGE main). This repo only hosts implementations, bindings, and wrappers.
- Keep package metadata in sync: version is defined in `pyproject.toml` and `sage/__init__.py`.
- Preserve CMake/pybind build paths pointing to `sage/libs/amms/implementations`.
- Avoid importing other SAGE subpackages in tests; tests should validate structure/files, not SAGE main interfaces.
- When adding files, ensure MANIFEST and packaging include the new paths under `sage/libs/amms/implementations`.

## CI/CD Expectations
- GitHub Actions workflows: `.github/workflows/build.yml` (build/test CPU+CUDA), `publish.yml` (cibuildwheel + PyPI), `codeql.yml`.
- Preferred publishing: trusted publishing via `publish.yml`. Version bumps must update both `pyproject.toml` and `sage/__init__.py`.
- Pre-commit: configure/keep `.pre-commit-config.yaml` with black+ruff+basic hooks; run `pre-commit run -a` before commits.

## Tests
- Current tests are structure/metadata checks (no imports of SAGE main). Keep tests lightweight and isolated.
- If adding functional tests for bindings, gate GPU/CUDA-specific cases behind env flags.

## Style
- Python: line length 100, Black/Ruff ready. Respect existing formatting.
- C++: C++14, use existing CMake style and headers layout.

## Gotchas
- Namespace conflicts with installed SAGE main: avoid import-based tests that pull `sage.libs` from elsewhere.
- Ensure binaries and headers are included via MANIFEST; keep wheel build working for cibuildwheel.

## Directory Structure
```
sage-amms/
├── .github/
│   ├── COPILOT_INSTRUCTIONS.md  # This file
│   └── workflows/               # CI/CD workflows
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md
│   ├── CONTRIBUTING.md
│   ├── PUBLISHING.md
│   └── ...
├── scripts/                     # Helper scripts
│   ├── build.sh
│   ├── test.sh
│   └── clean.sh
├── sage/libs/amms/
│   ├── __init__.py
│   ├── implementations/         # C++ source code
│   └── wrappers/               # Python wrappers
├── tests/                      # Test suite
├── pyproject.toml             # Package metadata
└── setup.py                   # Build configuration
```

## Quick Commands
```bash
# Run tests
pytest tests/ -v

# Build package
./scripts/build.sh

# Clean build artifacts
./scripts/clean.sh

# Run pre-commit hooks
pre-commit run -a
```
