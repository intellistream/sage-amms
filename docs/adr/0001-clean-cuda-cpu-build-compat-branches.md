# ADR 0001: Clean CUDA/CPU build compatibility branches

- Date: 2026-03-01
- Status: Accepted
- Issue: https://github.com/intellistream/sage-amms/issues/5

## Context

Build logic existed in two places:

1. root `setup.py` (package build entry)
2. `sage/libs/amms/implementations/setup.py` (redundant implementation-level path)

The implementation-level setup introduced extra auto-detection/branching behavior for CUDA and PAPI,
which duplicated and blurred the build capability boundary.

## Decision

1. Remove redundant `sage/libs/amms/implementations/setup.py`.
2. Keep a single build entry at root `setup.py`.
3. Use explicit capability toggles in root build flow:
   - `AMMS_ENABLE_CUDA` parsed as strict binary switch (`0/1/true/false/on/off`)
   - `AMMS_LOW_MEMORY_BUILD` parsed as strict binary switch
4. Fail fast when required prerequisites are missing:
   - missing PyTorch
   - `AMMS_ENABLE_CUDA=1` but `nvcc` not found under `CUDA_HOME`

## Consequences

- CUDA/CPU build path is single and explicit.
- Redundant branch path is removed directly.
- No shim/re-export/fallback path is introduced.

## Validation

- `ruff check setup.py tests/test_issue5_cuda_cpu_switch_cleanup.py`
- `pytest -q tests/test_issue5_cuda_cpu_switch_cleanup.py tests/test_structure.py`
