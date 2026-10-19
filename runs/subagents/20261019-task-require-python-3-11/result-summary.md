# result summary: task-require-python-3-11

Done by the supervisor; the coordinator decided it on 2026-10-18.

- pyproject.toml: requires-python >=3.10 -> >=3.11. After reinstalling, importlib.metadata reports Requires-Python >=3.11.
- CHANGELOG.md [0.2.0] Changed: a line for the Python floor and the CI matrix.
- .github/workflows/tests.yml: matrix python-version 3.11/3.12/3.13 (fail-fast off); dropped the comment pinning 3.13, which has been obsolete since 623f6c7.
- StrEnum stays as it is.
- spec2viz-49 acknowledged its candidate-run inbox note; the resolution was added and the note closed.

Validation: help goldens on 3.12 (/tmp/rw/venv312): 1 passed. Full suite on 3.13: see validation.log.
1 passed, 6 deselected, 1 warning in 100.56s (0:01:40)
