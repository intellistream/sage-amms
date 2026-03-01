"""Regression checks for issue #5: remove redundant CUDA/CPU compatibility branches."""

from pathlib import Path


def test_issue5_redundant_implementation_setup_removed() -> None:
    """The redundant legacy implementation-level setup.py is removed."""
    repo_root = Path(__file__).parent.parent
    legacy_setup = repo_root / "sage" / "libs" / "amms" / "implementations" / "setup.py"
    assert not legacy_setup.exists()


def test_issue5_root_setup_uses_explicit_cuda_switch() -> None:
    """Root setup.py uses explicit ON/OFF CUDA switch without auto fallback."""
    repo_root = Path(__file__).parent.parent
    content = (repo_root / "setup.py").read_text(encoding="utf-8")

    assert "AMMS_ENABLE_CUDA" in content
    assert "-DENABLE_CUDA=ON" in content
    assert "-DENABLE_CUDA=OFF" in content
    assert "Warning: PyTorch not found, building without PyTorch support" not in content
