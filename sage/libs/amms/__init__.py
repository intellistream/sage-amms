"""AMMS - Approximate Matrix Multiplication algorithms.

This package provides Python bindings for C++ AMM algorithm implementations.
The unified interface should be imported from the main SAGE package.

Example:
    # In SAGE main repo:
    from sage.libs.amms import create, registered
    
    # This package provides the implementations that get registered
"""

__version__ = "0.1.0"

# Import wrappers to trigger auto-registration when available
try:
    from sage.libs.amms.wrappers import pyamm
    _has_pyamm = True
except ImportError:
    _has_pyamm = False

__all__ = ["__version__"]
