# AMM-Algorithms Copilot Instructions

## Scope
- Package: `isage-amms`, import path `sage.libs.amms` (legacy: `sage/libs/amms/`).
- Layer: **L3** — C++/Python Approximate Matrix Multiplication (AMM) library; no L4+ dependencies.
- Purpose: Unified interface for AMM algorithms with optional CUDA acceleration.

## Polyrepo Context (Important)
SAGE was restructured from a monorepo into a polyrepo. `AMM-Algorithms` is a **standalone L3 C++ extension repo** providing AMM backends. It integrates with `sage-libs` via the `sage.libs.amms` interface layer.

## Critical rules
- C++ extension built via setuptools + pybind11 + CMake; do not break `CMakeLists.txt`.
- Python package layout lives under `sage/libs/amms/` (legacy `setup.py` layout).
- Do not create new local virtual environments (`venv`/`.venv`); use the existing configured Python environment.
- In conda environments, use `python -m pip` (never plain `pip`).
- No fallback logic; fail fast.

## Build
```bash
./quickstart.sh           # installs hooks
./buildCPUOnly.sh         # CPU-only build
./buildWithCuda.sh        # CUDA-enabled build
pip install -e .          # editable install (triggers CMake)
```

## Architecture focus
- `sage/libs/amms/implementations/` — C++ AMM algorithm implementations.
  - Contains sub-dirs for each algorithm (`cmake/`, `include/`, `src/`).
- `sage/libs/amms/` — Python interface layer (`base.py`, `factory.py`, `algorithms/`).
- `include/` — shared C++ headers.
- `tests/` — unit and integration tests.

## Dependencies
- **Depends on**: pybind11, PyTorch, CMake ≥ 3.14, `isage-libs` (L3 amms interfaces).
- **Depended on by**: `sage-libs`, `sage-middleware`, matrix computation application repos.

## Workflow
1. Make minimal changes; verify C++ builds cleanly before committing.
2. Keep Python API stable and document breaking changes.
3. Run `pytest tests/ -v` after any Python/binding change.
4. For C++ changes, rebuild with `pip install -e .` and run tests.

## Git Hooks (Mandatory)
- Never use `git commit --no-verify` or `git push --no-verify`.
- If hooks fail, fix the issue first.
- Run `./quickstart.sh` after cloning to install hooks.

## 🚫 NEVER_CREATE_DOT_VENV_MANDATORY

- 永远不要创建 `.venv` 或 `venv`（无任何例外）。
- NEVER create `.venv`/`venv` in this repository under any circumstance.
- 必须复用当前已配置的非-venv Python 环境（如现有 conda 环境）。
- If any script/task suggests creating a virtualenv, skip that step and continue with the existing environment.
