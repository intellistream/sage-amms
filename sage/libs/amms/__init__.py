"""AMMS package entrypoint.

This package exposes compiled AMM implementations through the wrapper module.
Backend availability is resolved by explicit imports and fails fast on missing
compiled extension.
"""

__version__ = "0.1.1"

from sage.libs.amms.wrappers import pyamm

__all__ = ["__version__", "pyamm"]
