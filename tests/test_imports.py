"""Test package structure and configuration.

Note: Import tests are skipped in development environment where SAGE main
package is installed. These tests will pass in CI and in production installation.
"""

import pytest
from pathlib import Path
import re


def test_package_structure():
    """Test that package files exist."""
    repo_root = Path(__file__).parent.parent
    
    # Check main package files
    assert (repo_root / 'sage' / '__init__.py').exists()
    assert (repo_root / 'sage' / 'libs' / '__init__.py').exists()
    assert (repo_root / 'sage' / 'libs' / 'amms' / '__init__.py').exists()
    
    # Check wrappers
    assert (repo_root / 'sage' / 'libs' / 'amms' / 'wrappers' / '__init__.py').exists()
    assert (repo_root / 'sage' / 'libs' / 'amms' / 'wrappers' / 'pyamm.py').exists()
    
    # Check implementations
    assert (repo_root / 'sage' / 'libs' / 'amms' / 'implementations').exists()
    assert (repo_root / 'sage' / 'libs' / 'amms' / 'implementations' / 'CMakeLists.txt').exists()


def test_version_consistency():
    """Test that version is consistent across files."""
    repo_root = Path(__file__).parent.parent
    
    # Read version from pyproject.toml
    pyproject_content = (repo_root / 'pyproject.toml').read_text()
    pyproject_version = re.search(r'version = "([^"]+)"', pyproject_content).group(1)
    
    # Read version from __init__.py
    init_content = (repo_root / 'sage' / '__init__.py').read_text()
    init_version = re.search(r'__version__ = "([^"]+)"', init_content).group(1)
    
    assert pyproject_version == init_version, \
        f"Version mismatch: pyproject.toml={pyproject_version}, __init__.py={init_version}"


def test_configuration_files():
    """Test that configuration files exist."""
    repo_root = Path(__file__).parent.parent
    
    # Check essential files
    assert (repo_root / 'pyproject.toml').exists()
    assert (repo_root / 'setup.py').exists()
    assert (repo_root / 'README.md').exists()
    assert (repo_root / 'LICENSE').exists()
    assert (repo_root / 'MANIFEST.in').exists()
    
    # Check documentation
    assert (repo_root / 'ARCHITECTURE.md').exists()
    assert (repo_root / 'CONTRIBUTING.md').exists()
    assert (repo_root / 'PUBLISHING.md').exists()
    assert (repo_root / 'SAGE_INTEGRATION.md').exists()
    
    # Check GitHub workflows
    assert (repo_root / '.github' / 'workflows' / 'build.yml').exists()
    assert (repo_root / '.github' / 'workflows' / 'publish.yml').exists()


def test_package_metadata():
    """Test package metadata in pyproject.toml."""
    repo_root = Path(__file__).parent.parent
    pyproject_content = (repo_root / 'pyproject.toml').read_text()
    
    # Check essential metadata
    assert 'name = "isage-amms"' in pyproject_content
    assert 'Approximate Matrix Multiplication' in pyproject_content
    assert 'requires-python' in pyproject_content
    assert 'numpy' in pyproject_content
    assert 'torch' in pyproject_content
