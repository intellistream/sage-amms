# Publishing SAGE-AMMS to PyPI

This guide describes how to publish `isage-amms` to PyPI.

## Prerequisites

### 1. PyPI Account Setup

1. Create accounts on:
   - [TestPyPI](https://test.pypi.org/account/register/) (for testing)
   - [PyPI](https://pypi.org/account/register/) (for production)

2. Enable 2FA (Two-Factor Authentication) on both accounts

3. Configure Trusted Publishing on PyPI (Recommended):
   - Go to PyPI Account Settings → Publishing
   - Add a new publisher for GitHub Actions
   - Repository: `intellistream/sage-amms`
   - Workflow: `publish.yml`
   - Environment: leave empty or set to `pypi`

### 2. Repository Secrets (Alternative to Trusted Publishing)

If not using Trusted Publishing, add repository secrets:

1. Generate API tokens:
   - TestPyPI: https://test.pypi.org/manage/account/token/
   - PyPI: https://pypi.org/manage/account/token/

2. Add secrets to GitHub repository:
   - Go to: Settings → Secrets and variables → Actions
   - Add: `PYPI_API_TOKEN` (for PyPI)
   - Add: `TEST_PYPI_API_TOKEN` (for TestPyPI)

## Publishing Methods

### Method 1: Automated Release (Recommended)

The easiest way to publish is through GitHub Releases:

1. **Update Version Number**

```bash
# Edit pyproject.toml
version = "0.1.0"  # Update this

# Edit sage/__init__.py
__version__ = "0.1.0"  # Update this
```

2. **Commit and Tag**

```bash
git add pyproject.toml sage/__init__.py
git commit -m "Bump version to 0.1.0"
git tag v0.1.0
git push origin main --tags
```

3. **Create GitHub Release**

- Go to: https://github.com/intellistream/sage-amms/releases/new
- Tag: `v0.1.0`
- Title: `Release 0.1.0`
- Description: Release notes
- Click "Publish release"

The GitHub Actions workflow will automatically:
- Build wheels for all platforms (Linux, macOS, Windows)
- Build source distribution
- Run tests
- Publish to PyPI

### Method 2: Manual Workflow Dispatch

For testing or ad-hoc releases:

1. Go to: Actions → Publish to PyPI → Run workflow
2. Select:
   - Branch: `main`
   - PyPI repository: `testpypi` or `pypi`
3. Click "Run workflow"

### Method 3: Local Publishing (Not Recommended)

Only use this for testing or emergencies:

```bash
# Install build tools
pip install build twine

# Build packages
python -m build

# Test upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Production upload to PyPI
python -m twine upload dist/*
```

## Build Process Details

### Platform Wheels

The CI/CD system builds wheels for:

**Linux:**
- `manylinux2014_x86_64`
- Python 3.8, 3.9, 3.10, 3.11, 3.12

**macOS:**
- `macosx_x86_64` (Intel)
- `macosx_arm64` (Apple Silicon)
- Python 3.8, 3.9, 3.10, 3.11, 3.12

**Windows:**
- `win_amd64`
- Python 3.8, 3.9, 3.10, 3.11, 3.12

### Build Variants

1. **CPU-only** (default): Works on all platforms
2. **CUDA-enabled**: Linux only, built separately

## Testing Release

### Test on TestPyPI

```bash
# Upload to TestPyPI (via workflow dispatch or manually)

# Test installation
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    isage-amms

# Test basic functionality
python -c "import sage.libs.amms; print(sage.libs.amms.__version__)"
```

### Test Locally Built Wheels

```bash
# Build wheel
python -m build --wheel

# Test in clean environment
python -m venv test_env
source test_env/bin/activate
pip install dist/isage_amms-*.whl
python -c "import sage.libs.amms"
deactivate
rm -rf test_env
```

## Version Naming Convention

Follow [Semantic Versioning](https://semver.org/):

- **Major** (X.0.0): Breaking API changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes

Examples:
- `0.1.0` - Initial release
- `0.1.1` - Bug fix
- `0.2.0` - New algorithm added
- `1.0.0` - First stable release

## Release Checklist

Before creating a release:

- [ ] All tests passing on main branch
- [ ] Version numbers updated in:
  - [ ] `pyproject.toml`
  - [ ] `sage/__init__.py`
- [ ] CHANGELOG.md updated
- [ ] Documentation updated
- [ ] No uncommitted changes
- [ ] Tagged with version (e.g., `v0.1.0`)

## Troubleshooting

### Build Failures

**Issue**: Wheel build fails on specific platform

**Solution**:
1. Check GitHub Actions logs
2. Test locally with `cibuildwheel`:
   ```bash
   pip install cibuildwheel
   cibuildwheel --platform linux  # or macos, windows
   ```

### Import Errors

**Issue**: Package installs but imports fail

**Solution**:
1. Check that C++ extensions compiled correctly
2. Verify Python ABI compatibility
3. Test in fresh virtual environment

### Upload Errors

**Issue**: `Upload failed: ... already exists`

**Solution**:
- PyPI doesn't allow re-uploading same version
- Bump version number and re-release
- Or use `--skip-existing` flag (for testing only)

## Post-Release

After successful release:

1. Announce on project channels
2. Update main SAGE repository to use new version
3. Update documentation site
4. Close milestone on GitHub

## Rolling Back

If a release has critical issues:

1. **Yank the release** on PyPI (doesn't delete, but warns users)
   - Go to PyPI project page
   - Manage → Releases → Options → Yank

2. **Release a fixed version**
   - Bump patch version (e.g., 0.1.0 → 0.1.1)
   - Fix the issue
   - Follow normal release process

## Integration with SAGE

After publishing to PyPI, update SAGE main repository:

```toml
# In SAGE pyproject.toml
[project.optional-dependencies]
amms = ["isage-amms>=0.1.0"]
```

Then users can install with:
```bash
pip install sage[amms]
```
