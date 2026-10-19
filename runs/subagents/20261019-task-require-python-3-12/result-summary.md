# result summary: task-require-python-3-12

Done by the supervisor; the owner decided it on 2026-10-19 (Python 3.10 reaches end of life this month).

- pyproject.toml: requires-python >=3.11 -> >=3.12. After reinstalling, the metadata reports >=3.12.
- .github/workflows/tests.yml: matrix 3.12 and 3.13.
- CHANGELOG.md [0.2.0] Changed: the 3.12 floor, the reason, and the removal of the old-interpreter test.
- tests/test_python_floor_compat.py removed. It only existed to keep the package importable on 3.10/3.11 (the PEP 701 f-string guard).
- Compatibility shim search: grepped deskops/, tests/, scripts/, docs/ and README for sys.version_info, typing_extensions, tomli, importlib_metadata, importlib_resources and try/except imports. The only `except ImportError` (deskops/graph/snapshot.py) guards an sldb API capability, not a Python version, so it stays. No doc states a Python version.

Full suite: see validation.log.
