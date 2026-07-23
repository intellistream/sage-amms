# ADR 0002: AMM interface and implementation boundary cleanup

- Date: 2026-03-01
- Status: Accepted
- Issue: https://github.com/DataSysResearch/AMM-Algorithms/issues/4

## Context

The AMMS package kept compatibility-style import branches in package/wrapper entrypoints:

1. `sage/libs/amms/__init__.py` used `try/except ImportError` and `_has_pyamm` flags.
2. `sage/libs/amms/wrappers/pyamm.py` used `try/except ImportError` with warning fallback.

These branches blurred interface and implementation boundaries by masking backend failures.

## Decision

1. Remove compatibility import fallback branches from AMMS package entrypoints.
2. Keep explicit import path from package to wrappers to compiled extension.
3. Preserve fail-fast behavior when compiled backend is unavailable.

## Consequences

- Boundary is explicit: Python entrypoints do not hide missing backend artifacts.
- No shim/re-export/fallback compatibility path is introduced.
- Failure surface is deterministic and easier to debug.

## Validation

- `ruff check sage/libs/amms/__init__.py sage/libs/amms/wrappers/__init__.py sage/libs/amms/wrappers/pyamm.py tests/test_issue4_boundary_cleanup.py`
- `pytest -q tests/test_issue4_boundary_cleanup.py`
