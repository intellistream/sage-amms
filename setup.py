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

        # Memory optimization flags
        low_memory = _parse_binary_env("AMMS_LOW_MEMORY_BUILD", default="0")
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

        # Number of parallel jobs
        # AMMS_MAX_JOBS overrides; low-memory mode caps at 2; default is cpu/2
        cpu_count = os.cpu_count() or 1
        if "AMMS_MAX_JOBS" in os.environ:
            max_jobs = max(1, int(os.environ["AMMS_MAX_JOBS"]))
        elif low_memory:
            max_jobs = min(cpu_count, 2)
        else:
            # Use half the CPUs by default to leave headroom for torch headers
            max_jobs = max(1, cpu_count // 2)
        print(f"[isage-amms] parallel jobs: {max_jobs} (low_memory={low_memory})")
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
