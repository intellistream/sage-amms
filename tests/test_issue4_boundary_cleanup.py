"""Regression checks for issue #4: AMM interface/implementation boundary cleanup."""

from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_issue4_amms_package_has_no_import_fallback() -> None:
    """AMMS package entry should not keep ImportError fallback branches."""
    content = _read("sage/libs/amms/__init__.py")

    assert "except ImportError" not in content
    assert "_has_pyamm" not in content
    assert "warnings.warn" not in content
    assert "from sage.libs.amms.wrappers import pyamm" in content


def test_issue4_pyamm_wrapper_has_no_compatibility_warning_path() -> None:
    """PyAMM wrapper should use direct import without compatibility warning branch."""
    content = _read("sage/libs/amms/wrappers/pyamm.py")

    assert "except ImportError" not in content
    assert "_has_extension" not in content
    assert "warnings.warn" not in content
    assert "from PyAMM import *" in content
