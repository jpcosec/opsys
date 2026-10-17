# task-rw-f0-declare-runtime-dependencies — executor summary

## Changes

- `pyproject.toml` — `[project].dependencies`: added `"kgdb>=0.1.0"` after `"structuredLanguageDB>=0.1.9"` (now line 11). No other file changed.
- Final `git status --short`: `M pyproject.toml` only.

## Cited line numbers verified before editing

- `pyproject.toml:10` → `"structuredLanguageDB>=0.1.9"` (correct).
- `deskops/graph/snapshot.py:119` → `from kgdb.contracts.io import GraphSnapshot` (correct).
- `deskops/cli/main.py:251` → `from kgdb.graph import load_graph` (correct).

## Throwaway venv

- Venv: `/tmp/rw/f0/venv-deps` (Python 3.13.5, pip 25.1.1).
- sldb source installed from `/home/jp/proyectos/SLDB_1/sldb` → `structuredLanguageDB-0.1.10` (built wheel, exit 0).
  - The sldb checkout now declares version 0.1.10, not the 0.1.9 mentioned in the task text.

### Exact task install command (failed, as anticipated by the task)

```
cd /tmp/rw/wt/deps
/tmp/rw/f0/venv-deps/bin/pip install /home/jp/proyectos/SLDB_1/sldb \
  "git+https://github.com/jpcosec/kgdb.git@1247139" .
```

Exit: `1`. Final error lines:

```
INFO: pip is looking at multiple versions of kgdb to determine which version is compatible with other requirements. This could take a while.
ERROR: Could not find a version that satisfies the requirement sldb (from kgdb) (from versions: none)
ERROR: No matching distribution found for sldb
```

- Cause: kgdb 0.1.0 metadata requires distribution `sldb`, but the sibling checkout's distribution is named `structuredLanguageDB`. `pip install .` alone fails identically even though both packages are already installed.
- `deskops` and `kgdb` were then installed with `--no-deps`:
  - `pip install --no-deps "git+https://github.com/jpcosec/kgdb.git@1247139"` → exit 0, kgdb 0.1.0 (commit resolved to 1247139).
  - `pip install --no-deps .` → exit 0, deskops 0.1.0.
- Import check: `/tmp/rw/f0/venv-deps/bin/python -c 'import deskops.cli.main'` → `import OK` (exit 0).
- `/tmp/rw/f0/venv-deps/bin/python -c 'from kgdb.contracts.io import GraphSnapshot'` → OK.

## Validation commands and results

| Command | Result |
|---|---|
| `PYTHONPATH=/tmp/rw/wt/deps python -m deskops --help` | exit 0, help printed |
| `PYTHONPATH=/tmp/rw/wt/deps python -m pytest tests -q` (first run) | `1 failed, 334 passed, 3 skipped in 205.95s` |
| `PYTHONPATH=/tmp/rw/wt/deps python -m pytest tests -q` (after env fix) | `335 passed, 3 skipped in 180.14s` |

- The single first-run failure was `tests/test_skill_cli_drift.py::test_use_deskops_copies_document_the_from_drawer_authoring_path`: `.pi/skills/use-deskops/SKILL.md` is absent from the worktree because `.pi/` is gitignored (`.gitignore:10`). Copied the gitignored `.pi/skills` surface from the main checkout into the worktree; it does not appear in git status or the diff. Test then passed (and full suite green).

## Test against unfixed code

- Copied `deskops/`, `README.md`, and the pre-change `pyproject.toml` (without `kgdb`) to `/tmp/rw/f0/unfixed`; fresh venv `/tmp/rw/f0/venv-unfixed` with only `/home/jp/proyectos/SLDB_1/sldb`.
- `pip install .` → exit 0 (no kgdb required).
- `python -c "import deskops.cli.main"` → OK (imports lazily).
- `python -c "from kgdb.contracts.io import GraphSnapshot"` → `ModuleNotFoundError: No module named 'kgdb'` (exit 1).
- Confirms the undeclared dependency leaves KGDB-backed graph paths broken in a clean install.

## Wrong/ambiguous things found

- The task's venv recipe cannot succeed as written even with the declaration, because of kgdb's own packaging metadata. Done When's "or the pip error is recorded" clause applies; keep the declaration.
- kgdb packaging defect (not sldb, not deskops): kgdb 0.1.0 declares `sldb` as its distribution requirement instead of `structuredLanguageDB`. Reproduced with the exact command/output above. Not fixed (out of scope).
- The task's check `import deskops.cli.main` does not prove kgdb is installed: kgdb imports are function-local. Verified on the fixed code with `sys.modules["kgdb"] = None` → CLI still imported. A real capability check is `from kgdb.contracts.io import GraphSnapshot` or `deskops graph build`.
- No sldb bug found: sldb built and imported normally in the venv at version 0.1.10.
