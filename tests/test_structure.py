"""Tests for SAGE-AMMS package content (no imports)."""

import pytest
from pathlib import Path


def test_implementations_exist():
    """Test that C++ implementation files exist."""
    repo_root = Path(__file__).parent.parent
    impl_dir = repo_root / 'sage' / 'libs' / 'amms' / 'implementations'
    
    # Check CMake
    assert (impl_dir / 'CMakeLists.txt').exists()
    
    # Check include directory
    include_dir = impl_dir / 'include'
    assert include_dir.exists()
    assert (include_dir / 'LibAMM.h').exists()
    assert (include_dir / 'CPPAlgos').is_dir()
    assert (include_dir / 'MatrixLoader').is_dir()
    assert (include_dir / 'Utils').is_dir()
    
    # Check src directory
    src_dir = impl_dir / 'src'
    assert src_dir.exists()
    assert (src_dir / 'CMakeLists.txt').exists()
    assert (src_dir / 'PyAMM.cpp').exists()


def test_wrapper_content():
    """Test wrapper file content."""
    repo_root = Path(__file__).parent.parent
    pyamm_file = repo_root / 'sage' / 'libs' / 'amms' / 'wrappers' / 'pyamm.py'
    
    content = pyamm_file.read_text()
    assert 'PyAMM' in content
    assert 'import' in content


def test_package_exports():
    """Test that package __init__.py has correct structure."""
    repo_root = Path(__file__).parent.parent
    init_file = repo_root / 'sage' / 'libs' / 'amms' / '__init__.py'
    
    content = init_file.read_text()
    assert '__version__' in content
    assert '0.1.0' in content


def test_build_scripts():
    """Test that build scripts exist."""
    repo_root = Path(__file__).parent.parent
    
    assert (repo_root / 'build.sh').exists()
    assert (repo_root / 'test.sh').exists()
    
    # Check they're executable
    import os
    assert os.access(repo_root / 'build.sh', os.X_OK)
    assert os.access(repo_root / 'test.sh', os.X_OK)
