# ADR 0002: Build matrix and performance baseline gate

- Date: 2026-03-01
- Status: Accepted
- Issue: https://github.com/intellistream/sage-amms/issues/6

## Context

Issue #6 requires explicit coverage for CPU/CUDA build paths and a reproducible performance
regression baseline for core AMM operators.

Before this change:

1. CI used a single CPU build path only.
2. There was no dedicated regression test to guard core operator runtime stability.

## Decision

1. Upgrade `.github/workflows/build.yml` to a two-entry build matrix:
   - `build_mode=cpu` with `AMMS_ENABLE_CUDA=0`
   - `build_mode=cuda` with `AMMS_ENABLE_CUDA=1`
2. Keep CUDA path explicit by preparing a deterministic toolchain switch path (`CUDA_HOME=/tmp/fake-cuda`)
   for matrix validation.
3. Add `tests/test_issue6_build_matrix_and_perf_baseline.py` to enforce:
   - workflow matrix presence and wiring
   - explicit setup switch contract for CUDA/CPU
   - core operator (`createAMM("mm")`) latency stability baseline
4. Remove CUDA helper fallback behavior in `buildWithCuda.sh` so missing CUDA fails fast.

## Consequences

- CPU and CUDA build switches are continuously validated in CI.
- Performance regressions on core AMM operator can be detected early.
- No compatibility branch/shim/re-export/fallback is introduced.

## Validation

- `ruff check tests/test_issue6_build_matrix_and_perf_baseline.py tests/test_imports.py tests/test_structure.py`
- `pytest -q tests/test_issue6_build_matrix_and_perf_baseline.py tests/test_issue5_cuda_cpu_switch_cleanup.py`
