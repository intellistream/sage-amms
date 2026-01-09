# Files to Add to SAGE Main Repository

This document describes the files that should be added to the main SAGE repository to integrate with `isage-amms`.

## Directory Structure in SAGE

```
SAGE/
└── sage/
    └── libs/
        └── amms/
            ├── __init__.py          # Main interface
            ├── interface/
            │   ├── __init__.py
            │   ├── base.py          # AmmIndex abstract class
            │   ├── factory.py       # create(), register(), registered()
            │   └── registry.py      # Algorithm registry
            └── README.md
```

## File Contents

### sage/libs/amms/__init__.py

```python
"""AMMS - Approximate Matrix Multiplication unified interface.

This module provides a unified interface for various AMM algorithms.
Actual implementations are provided by the isage-amms package.
"""

from sage.libs.amms.interface.base import AmmIndex, AmmIndexMeta
from sage.libs.amms.interface.factory import (
    create,
    register,
    registered,
    get_algorithm_class,
    is_registered,
)

__all__ = [
    "AmmIndex",
    "AmmIndexMeta",
    "create",
    "register",
    "registered",
    "get_algorithm_class",
    "is_registered",
]

# Auto-import implementations if isage-amms is installed
try:
    import sage.libs.amms.implementations  # from isage-amms package
    _has_implementations = True
except ImportError:
    _has_implementations = False
    import warnings
    warnings.warn(
        "AMM implementations not available. "
        "Install with: pip install isage-amms",
        ImportWarning,
        stacklevel=2
    )
```

### sage/libs/amms/interface/base.py

```python
"""Base interface for AMM algorithms."""

from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Dict

import numpy as np


class AmmIndexMeta(ABCMeta):
    """Metaclass for AMM index classes."""
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        return cls


class AmmIndex(ABC, metaclass=AmmIndexMeta):
    """Abstract base class for all AMM algorithms."""
    
    def __init__(self, **kwargs):
        self.params = kwargs
    
    @abstractmethod
    def build(self, matrix: np.ndarray) -> None:
        """Build/preprocess the index for a matrix."""
        pass
    
    @abstractmethod
    def multiply(self, matrix_a: np.ndarray, matrix_b: np.ndarray) -> np.ndarray:
        """Perform approximate matrix multiplication."""
        pass
    
    def get_params(self) -> Dict[str, Any]:
        """Get the parameters of this AMM index."""
        return self.params.copy()
    
    def set_params(self, **params) -> "AmmIndex":
        """Set the parameters of this AMM index."""
        self.params.update(params)
        return self
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of this AMM algorithm."""
        pass
    
    def __repr__(self) -> str:
        params_str = ", ".join(f"{k}={v}" for k, v in self.params.items())
        return f"{self.__class__.__name__}({params_str})"
```

### sage/libs/amms/interface/registry.py

```python
"""AMM algorithm registry."""

from typing import Dict, Type
from sage.libs.amms.interface.base import AmmIndex


class AmmRegistry:
    """Registry for AMM algorithm implementations."""
    
    def __init__(self):
        self._algorithms: Dict[str, Type[AmmIndex]] = {}
    
    def register(self, name: str, cls: Type[AmmIndex]) -> None:
        """Register an AMM algorithm implementation."""
        if name in self._algorithms:
            raise ValueError(f"Algorithm '{name}' is already registered")
        if not issubclass(cls, AmmIndex):
            raise TypeError(f"Class {cls} must be a subclass of AmmIndex")
        self._algorithms[name] = cls
    
    def unregister(self, name: str) -> None:
        """Unregister an AMM algorithm."""
        if name not in self._algorithms:
            raise KeyError(f"Algorithm '{name}' is not registered")
        del self._algorithms[name]
    
    def get(self, name: str) -> Type[AmmIndex]:
        """Get an AMM algorithm class by name."""
        if name not in self._algorithms:
            raise KeyError(
                f"Algorithm '{name}' is not registered. "
                f"Available algorithms: {list(self._algorithms.keys())}"
            )
        return self._algorithms[name]
    
    def list(self) -> Dict[str, Type[AmmIndex]]:
        """Get all registered algorithms."""
        return self._algorithms.copy()
    
    def __contains__(self, name: str) -> bool:
        return name in self._algorithms
    
    def __repr__(self) -> str:
        return f"AmmRegistry({list(self._algorithms.keys())})"


# Global registry instance
_registry = AmmRegistry()
```

### sage/libs/amms/interface/factory.py

```python
"""Factory functions for creating AMM algorithm instances."""

from typing import List, Type
from sage.libs.amms.interface.base import AmmIndex
from sage.libs.amms.interface.registry import _registry


def register(name: str, cls: Type[AmmIndex]) -> None:
    """Register an AMM algorithm implementation."""
    _registry.register(name, cls)


def create(name: str, **kwargs) -> AmmIndex:
    """Create an instance of an AMM algorithm."""
    cls = _registry.get(name)
    return cls(**kwargs)


def registered() -> List[str]:
    """Get a list of all registered AMM algorithms."""
    return list(_registry.list().keys())


def get_algorithm_class(name: str) -> Type[AmmIndex]:
    """Get the class for a registered AMM algorithm."""
    return _registry.get(name)


def is_registered(name: str) -> bool:
    """Check if an AMM algorithm is registered."""
    return name in _registry
```

### sage/libs/amms/interface/__init__.py

```python
"""Interface module for AMM algorithms."""

from sage.libs.amms.interface.base import AmmIndex, AmmIndexMeta
from sage.libs.amms.interface.factory import (
    create,
    get_algorithm_class,
    is_registered,
    register,
    registered,
)
from sage.libs.amms.interface.registry import AmmRegistry

__all__ = [
    "AmmIndex",
    "AmmIndexMeta",
    "AmmRegistry",
    "create",
    "register",
    "registered",
    "get_algorithm_class",
    "is_registered",
]
```

## Update SAGE pyproject.toml

Add to the main SAGE `pyproject.toml`:

```toml
[project.optional-dependencies]
amms = ["isage-amms>=0.1.0"]
```

## Installation Instructions for Users

After these changes, users can install SAGE with AMM support:

```bash
# Install SAGE with AMM algorithms
pip install sage[amms]

# Or separately
pip install sage
pip install isage-amms
```

## Usage Example

```python
from sage.libs.amms import create, registered
import numpy as np

# Check available algorithms
print(registered())  # ['countsketch', 'fastjlt', ...]

# Create and use an algorithm
amm = create("countsketch", sketch_size=1000)
A = np.random.randn(1000, 500)
B = np.random.randn(500, 800)
result = amm.multiply(A, B)
```
