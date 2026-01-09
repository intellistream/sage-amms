# sage-amms Chat Mod Notes

## Scope
- Repo: `intellistream/sage-amms` (PyPI package `isage-amms`)
- Role: C++ AMM implementations + PyBind bindings and thin Python wrappers under `sage.libs.amms`
- The **unified AMM interface/registry lives in the main SAGE repo**, not here.

## Do
- Keep build paths pointing to `sage/libs/amms/implementations`.
- Ensure `pyproject.toml`, `setup.py`, `MANIFEST.in` include binaries/headers under that path.
- Update version in both `pyproject.toml` and `sage/__init__.py` together.
- Use existing CI workflows: `.github/workflows/build.yml` (build/test CPU+CUDA), `publish.yml` (cibuildwheel + PyPI), `codeql.yml`.
- Keep tests lightweight (structure/metadata). If adding binding tests, guard GPU/CUDA cases with env flags.
- Python style: Black/Ruff, line length 100. C++: C++14, follow current CMake/layout.

## Don’t
- Don’t reintroduce AMM interface/registry code here.
- Don’t import other SAGE subpackages in tests (avoids namespace clashes with installed SAGE).
- Don’t move implementations out of `sage/libs/amms/implementations`.

## Release
- Preferred publishing via GitHub Actions `publish.yml` with trusted publishing.
- Tag + release to publish; otherwise use workflow dispatch (testpypi/pypi).

## Gotchas
- Namespace conflicts with installed SAGE: avoid runtime imports of `sage.libs` beyond this package.
- Include `.so/.pyd/.dll` artifacts in MANIFEST; keep CMake args aligned with torch + optional CUDA.
