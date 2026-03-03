"""Regression tests for issue #6: build matrix coverage and performance baseline."""

from __future__ import annotations

import statistics
import time
from pathlib import Path

import numpy as np
import pytest


def test_issue6_build_workflow_has_cpu_cuda_matrix() -> None:
    """CI workflow includes explicit CPU/CUDA build-path matrix coverage."""
    repo_root = Path(__file__).parent.parent
    workflow_content = (repo_root / ".github" / "workflows" / "build.yml").read_text(
        encoding="utf-8"
    )

    assert "build_mode: [cpu, cuda]" in workflow_content
    assert "amms_enable_cuda" in workflow_content
    assert "AMMS_ENABLE_CUDA: ${{ matrix.amms_enable_cuda }}" in workflow_content
    assert "Prepare CUDA toolchain switch path" in workflow_content


def test_issue6_setup_has_explicit_cuda_cpu_switch_contract() -> None:
    """Root setup.py keeps explicit CUDA/CPU switch contract with fail-fast checks."""
    repo_root = Path(__file__).parent.parent
    setup_content = (repo_root / "setup.py").read_text(encoding="utf-8")

    assert "AMMS_ENABLE_CUDA" in setup_content
    assert "-DENABLE_CUDA=ON" in setup_content
    assert "-DENABLE_CUDA=OFF" in setup_content
    assert "AMMS_ENABLE_CUDA=1 but nvcc was not found" in setup_content


def _collect_mm_latencies(rounds: int = 4) -> list[float]:
    """Collect end-to-end latency samples for the core AMM operator."""
    try:
        from sage.libs.amms.wrappers import pyamm
    except ModuleNotFoundError:
        pytest.skip("PyAMM extension is not available in the current environment")

    if not hasattr(pyamm, "createAMM"):
        pytest.skip("PyAMM.createAMM is unavailable in the current build")

    algorithm = pyamm.createAMM("mm")

    matrix_a = np.random.default_rng(42).standard_normal((64, 64), dtype=np.float32)
    matrix_b = np.random.default_rng(7).standard_normal((64, 64), dtype=np.float32)

    for _ in range(2):
        _ = algorithm.amm(matrix_a, matrix_b, 16)

    samples: list[float] = []
    for _ in range(rounds):
        start = time.perf_counter()
        result = algorithm.amm(matrix_a, matrix_b, 16)
        elapsed = time.perf_counter() - start

        assert result.shape == (64, 64)
        assert np.isfinite(result).all()
        samples.append(elapsed)

    return samples


def test_issue6_core_operator_perf_baseline_stability() -> None:
    """Core operator latency remains within a relaxed, reproducible baseline envelope."""
    first_run = _collect_mm_latencies()
    second_run = _collect_mm_latencies()

    first_median = statistics.median(first_run)
    second_median = statistics.median(second_run)

    # Absolute guardrail for CI-scale matrices.
    assert first_median < 2.0
    assert second_median < 2.0

    # Relative stability guardrail across two short runs.
    slower = max(first_median, second_median)
    faster = max(min(first_median, second_median), 1e-9)
    assert slower / faster < 3.0
