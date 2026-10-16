RESTATEMENT:

1. Read bound pill `desk/contexts/pill-008-kgdb-sldb-boundary.md` for constraints on the sldb/kgdb boundary.
2. Open `pyproject.toml` at repo root (`/home/jp/proyectos/SLDB_1/deskops/pyproject.toml`) and locate the `dependencies` list under `[project]`.
3. Add two entries: `"structuredLanguageDB>=0.1.4"` and `"kgdb>=0.1.0"`. No upper bounds. No other file changes.
4. Do not touch `ensure_sldb_available` in `deskops/bootstrap.py`.
5. Create throwaway venv: `python -m venv /tmp/deskops-venv`.
6. Install into it: `/tmp/deskops-venv/bin/pip install ../sldb "git+https://github.com/jpcosec/kgdb.git@1247139" .`
7. Run import check: `/tmp/deskops-venv/bin/python -c 'import deskops.cli.main'`.
8. If the pip command exits non-zero, keep the declaration and capture the exact command and error text for the closeout.
9. Run validation: `python -m deskops --help` and `pytest tests`.
10. Do not commit. Leave the working-tree diff for supervisor review and closeout commit.

AMBIGUITIES:

1. `pyproject.toml` path is given as bare filename; assumed repo root, not confirmed.
2. `dependencies` list location is not stated (which table/section); assumed `[project].dependencies`.
3. Which Python interpreter/binaries to use for `python -m venv`, `python -m deskops --help`, and `pytest tests` is unspecified (system python vs. `/tmp/deskops-venv/bin/python`).
4. Validation commands do not say which environment they run in; if run in the throwaway venv, `pytest` is not installed there (only sldb, kgdb, deskops are).
5. `pytest tests` assumes a `tests/` directory at repo root; not confirmed and no collection target specified.
6. Whether `pip install` should use `-e` (editable) for `.` is unspecified; the command uses plain `.` but the rationale references `pip install -e .`.
7. Installing `kgdb` from a git URL at a fixed commit, then requiring `kgdb>=0.1.0` in deskops metadata, may not resolve unless that commit declares version ≥0.1.0; behavior is unstated.
8. Done When allows "or the missing kgdb source is reported", yet Implementation Path supplies a concrete kgdb source (the git URL). Contradiction: what qualifies as a "missing kgdb source" failure is undefined.
9. "Record the exact command and error in the closeout" conflicts with Resolved Decisions that the executor does not commit/closeout; owner of that recording is unstated.
10. Whether failures at step 6/7 for reasons other than "missing kgdb source" (e.g., wheel build failure, import error) still permit closing is not specified.
11. No acceptance criterion defines what counts as the venv import check "succeeding" beyond exit code 0; stdout/stderr expectations unstated.
12. Whether `python -m deskops --help` must be run inside the throwaway venv or the main env (where the noted structuredLanguageDB 0.1.3 / stale `sldb 0.1.0` metadata issue exists) is unspecified.
13. The task is `status: deferred`; how the executor should treat it before the supervisor's promotion is unstated.
14. Whether `pytest tests` must be green before the executor returns, versus before the supervisor closes, is ambiguous given the executor does not commit.
