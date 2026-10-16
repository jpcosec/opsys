RESTATEMENT:

1. Open `pyproject.toml` and locate the table that holds runtime dependencies (presumed `[project] dependencies`, keeping existing `pydantic` and `PyYAML`).
2. Add `"sldb>=0.1.4"` and `"kgdb>=0.1.0"` to that dependency list.
3. Change nothing else: no `deskops/bootstrap.py`, no `ensure_sldb_available`, no upper bounds, no publishing metadata.
4. Create a throwaway venv: `python -m venv /tmp/deskops-venv`.
5. Install from source into it: `/tmp/deskops-venv/bin/pip install ../sldb "git+https://github.com/jpcosec/kgdb.git@1247139" .` (run from repo root).
6. Run the import check: `/tmp/deskops-venv/bin/python -c 'import deskops.cli.main'`; capture exit code.
7. If that command exits non-zero, still keep the declaration and record the exact command plus error output for the closeout.
8. Run `python -m deskops --help`.
9. Run `pytest tests` (must be green).
10. Report the diff, the venv command, its exit code/output, and the pytest result to the supervisor; do not commit. Supervisor promotes the drawer task and makes the closeout commit.

AMBIGUITIES:

1. Which dependency table: the task says "the `dependencies` list in pyproject.toml" but not whether the project uses `[project].dependencies`, `[tool.poetry.dependencies]`, `[dependency-groups]`, or an optional extra; I cannot see the file.
2. Whether a lockfile or constraints file also needs updating; `files:` lists only `pyproject.toml`, so I would not, but that is a guess.
3. Contradiction: Done When allows "the missing kgdb source is reported" while Implementation Path asserts the kgdb source is already known (`git+...@1247139`); it is unclear which branch applies if the git URL is unreachable.
4. Missing criterion for the failure path: if the pip install fails, is the task still "done", and does `pytest tests` green still gate closing per Resolved Decisions?
5. Validation says `pytest tests` but the repo convention in AGENTS.md is `pytest`; ambiguous whether a `tests` path exists or the specific directory is required.
6. Ambiguous which interpreter runs `python -m deskops --help` — the throwaway venv, or the ambient environment (where the fix is unverified).
7. `../sldb` is assumed to be a pip-installable local checkout; not stated in the task.
8. Network/git access to `github.com/jpcosec/kgdb.git@1247139` is assumed; no fallback specified.
9. Task frontmatter says `status: deferred` and `source:drawer`, but Resolved Decisions says the supervisor promotes it before dispatch; unclear whether I should execute against the drawer copy or the promoted copy.
10. No stated acceptance criterion for Python version support or that `pydantic`/`PyYAML` must be retained.
11. Referenced plan file `runs/planning/deskops-rewrite-inventory.md` is not in `files:` and its contents are not provided; it may carry criteria I cannot see.
12. No instruction on what to do with `/tmp/deskops-venv` afterwards (cleanup vs leave for reviewer).
