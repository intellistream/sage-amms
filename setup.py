"""Setup script for isage-amms package.

This setup.py handles the building of C++ extensions for AMM algorithms.
"""

import os
import subprocess
import sys
from pathlib import Path

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


def _parse_binary_env(name: str, default: str = "0") -> bool:
    """Parse binary environment toggle with fail-fast validation."""
    raw_value = os.environ.get(name, default).strip().lower()
    if raw_value in {"1", "true", "on"}:
        return True
    if raw_value in {"0", "false", "off"}:
        return False
    raise ValueError(f"{name} must be one of: 0/1/true/false/on/off, got '{raw_value}'")


def _get_available_memory_gb() -> float:
    """Get available system memory in GiB (Linux /proc/meminfo first, then sysconf)."""
    meminfo_path = Path("/proc/meminfo")
    if meminfo_path.exists():
        try:
            for line in meminfo_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("MemAvailable:"):
                    parts = line.split()
                    if len(parts) >= 2:
                        mem_kib = int(parts[1])
                        return mem_kib / (1024 * 1024)
        except (OSError, ValueError):
            pass

    if hasattr(os, "sysconf"):
        try:
            page_size = int(os.sysconf("SC_PAGE_SIZE"))
            available_pages = int(os.sysconf("SC_AVPHYS_PAGES"))
            return (page_size * available_pages) / (1024**3)
        except (OSError, ValueError):
            pass

    return 0.0


def _resolve_build_mode() -> tuple[bool, int, str]:
    """Resolve low-memory mode and max jobs with explicit env vars taking precedence."""
    cpu_count = os.cpu_count() or 1

    low_memory_raw = os.environ.get("AMMS_LOW_MEMORY_BUILD")
    max_jobs_raw = os.environ.get("AMMS_MAX_JOBS")

    if low_memory_raw is not None:
        low_memory = _parse_binary_env("AMMS_LOW_MEMORY_BUILD", default="1")
        reason = "explicit AMMS_LOW_MEMORY_BUILD"
    else:
        fast_build_override = os.environ.get("AMMS_FAST_BUILD")
        if fast_build_override is not None:
            fast_build = _parse_binary_env("AMMS_FAST_BUILD", default="0")
            low_memory = not fast_build
            reason = "explicit AMMS_FAST_BUILD"
        else:
            fast_build_threshold_gb = int(os.environ.get("AMMS_FAST_BUILD_MEMORY_GB", "48"))
            available_memory_gb = _get_available_memory_gb()
            low_memory = available_memory_gb < fast_build_threshold_gb
            reason = (
                f"auto memory probe (available={available_memory_gb:.1f}GiB, "
                f"threshold={fast_build_threshold_gb}GiB)"
            )

    if max_jobs_raw is not None:
        max_jobs = max(1, int(max_jobs_raw))
    elif low_memory:
        max_jobs = 1
    else:
        max_jobs = max(1, cpu_count // 2)

    return low_memory, max_jobs, reason


class CMakeExtension(Extension):
    """Extension that uses CMake to build."""

    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    """Custom build command that runs CMake."""

    def run(self):
        """Run CMake build."""
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(e.name for e in self.extensions)
            )

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        """Build a single extension."""
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        try:
            import torch
        except ImportError as exc:
            raise RuntimeError(
                "PyTorch is required to build isage-amms. Install torch first in the active environment."
            ) from exc

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            "-DENABLE_PYBIND=ON",
            "-DENABLE_UNIT_TESTS=OFF",
            f"-DCMAKE_PREFIX_PATH={torch.utils.cmake_prefix_path}",
        ]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        # Platform-specific configuration
        cmake_args += [f"-DCMAKE_BUILD_TYPE={cfg}"]

        # Build mode resolution (explicit env vars > auto memory probe)
        low_memory, max_jobs, mode_reason = _resolve_build_mode()
        cmake_args.append(f"-DAMMS_LOW_MEMORY_BUILD={'ON' if low_memory else 'OFF'}")
        if low_memory:
            cmake_args += [
                "-DCMAKE_CXX_FLAGS=-g0 -O0 -fno-var-tracking -fno-inline",
            ]

        # CUDA support (explicit switch only)
        enable_cuda = _parse_binary_env("AMMS_ENABLE_CUDA", default="0")
        if enable_cuda:
            cmake_args.append("-DENABLE_CUDA=ON")
            cuda_path = os.environ.get("CUDA_HOME", "/usr/local/cuda")
            nvcc_path = Path(cuda_path) / "bin" / "nvcc"
            if not nvcc_path.exists():
                raise RuntimeError(
                    f"AMMS_ENABLE_CUDA=1 but nvcc was not found at {nvcc_path}. "
                    "Set CUDA_HOME to a valid CUDA toolkit path."
                )
            cmake_args.append(f"-DCUDACXX={cuda_path}/bin/nvcc")
        else:
            cmake_args.append("-DENABLE_CUDA=OFF")

        print(
            f"[isage-amms] build mode: {'low-memory' if low_memory else 'fast'} "
            f"(reason: {mode_reason})"
        )
        print(f"[isage-amms] parallel jobs: {max_jobs}")
        build_args += [f"-j{max_jobs}"]

        env = os.environ.copy()
        env["CXXFLAGS"] = (
            f'{env.get("CXXFLAGS", "")} -DVERSION_INFO=\\"{self.distribution.get_version()}\\"'
        )

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        print(f"Building in {self.build_temp}")
        print(f"CMake args: {cmake_args}")

        # Run CMake configure
        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)

        # Run CMake build
        subprocess.check_call(["cmake", "--build", "."] + build_args, cwd=self.build_temp, env=env)


# Read long description from README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=[CMakeExtension("PyAMM", sourcedir="sage/libs/amms/implementations")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
)
