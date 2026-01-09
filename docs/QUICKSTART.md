# Quick Start Guide

This guide helps you quickly get started with developing and publishing SAGE-AMMS.

## For Developers

### 1. Clone and Setup

```bash
git clone https://github.com/intellistream/sage-amms.git
cd sage-amms

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### 2. Make Changes

```bash
# Create a feature branch
git checkout -b feature/my-feature

# Make your changes
# Edit files in sage/libs/amms/implementations/

# Run tests
pytest tests/ -v

# Check code style
black sage/ tests/
ruff check sage/ tests/
```

### 3. Submit PR

```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/my-feature
```

Then create a Pull Request on GitHub.

## For Maintainers

### Publishing to PyPI

#### Method 1: Automated (Recommended)

1. Update version in `pyproject.toml` and `sage/__init__.py`
2. Commit and tag:
   ```bash
   git add pyproject.toml sage/__init__.py
   git commit -m "Bump version to 0.1.0"
   git tag v0.1.0
   git push origin main --tags
   ```
3. Create GitHub Release - automation handles the rest

#### Method 2: Manual

```bash
# Build
python -m build

# Test on TestPyPI
twine upload --repository testpypi dist/*

# Production
twine upload dist/*
```

## For SAGE Main Repo Integration

After publishing to PyPI, update SAGE main repository:

### 1. Add Interface Files

Copy files from `SAGE_INTEGRATION.md` to SAGE main repo:
- `sage/libs/amms/interface/` directory
- Update `sage/libs/amms/__init__.py`

### 2. Update pyproject.toml

```toml
[project.optional-dependencies]
amms = ["isage-amms>=0.1.0"]
```

### 3. Test Integration

```bash
cd /path/to/SAGE
pip install -e ".[amms]"
python -c "from sage.libs.amms import create, registered; print(registered())"
```

## Common Tasks

### Run All Tests

```bash
pytest tests/ -v --cov=sage.libs.amms
```

### Build Documentation

```bash
# Coming soon
```

### Check CI Status

Visit: https://github.com/intellistream/sage-amms/actions

### Build Locally

```bash
# CPU only
python -m build

# With CUDA
AMMS_ENABLE_CUDA=1 python -m build
```

## Troubleshooting

### Build Fails with Memory Error

```bash
# Use low memory build
AMMS_LOW_MEMORY_BUILD=1 pip install -e .
```

### Import Error After Install

```bash
# Check if C++ extension built
python -c "from sage.libs.amms.wrappers import pyamm"

# If fails, rebuild
pip install --force-reinstall --no-cache-dir -e .
```

### Tests Fail

```bash
# Run with verbose output
pytest tests/ -vv -s

# Run specific test
pytest tests/test_imports.py::test_import_amms -v
```

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines  
- [PUBLISHING.md](PUBLISHING.md) - Publishing to PyPI
- [SAGE_INTEGRATION.md](SAGE_INTEGRATION.md) - SAGE integration guide
- [README.md](README.md) - Main documentation

## Getting Help

- Issues: https://github.com/intellistream/sage-amms/issues
- Discussions: https://github.com/intellistream/sage-amms/discussions
- Email: shuhao_zhang@hust.edu.cn
