"""Python wrapper for PyAMM C++ implementations.

This module provides Python bindings for the C++ AMM algorithms.
Algorithms will be automatically registered with the SAGE registry when imported.
"""

# Try to import the compiled C++ extension
try:
    from PyAMM import *  # noqa: F401, F403
    _has_extension = True
except ImportError as e:
    _has_extension = False
    _import_error = str(e)

__all__ = []

if not _has_extension:
    import warnings
    warnings.warn(
        f"PyAMM C++ extension not available: {_import_error}. "
        "The package was installed but the C++ extensions failed to build. "
        "You may need to rebuild from source.",
        ImportWarning
    )
