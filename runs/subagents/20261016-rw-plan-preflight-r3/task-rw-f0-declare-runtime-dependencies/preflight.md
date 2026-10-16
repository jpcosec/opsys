RESTATEMENT:
1. Confirm the task is a drawer item (`status: deferred`) whose promotion to `desk/tasks/` and pre-dispatch commit are done by the supervisor, so no commit is made by me.
2. Read `pyproject.toml` and locate the `[project]` `dependencies` list.
3. Confirm the sibling checkout at `../sldb` exposes a version >= 0.1.4 (its own `pyproject.toml`/`__init__`), to justify the lower bound.
4. Add `"sldb>=0.1.4"` and `"kgdb>=0.1.0"` to that list, preserving the existing `pydantic` and `PyYAML` entries and the file's formatting.
5. Leave out of scope: publishing metadata, upper bounds, and `ensure_sldb_available` in `deskops/bootstrap.py`.
6. Create `/tmp/deskops-venv` via `python -m venv /tmp/deskops-venv`.
7. Obtain a kgdb artifact with `/tmp/deskops-venv/bin/pip download kgdb==0.1.0`; if no installable artifact is produced, skip the install and record that fact for closeout.
8. Install into the venv: `/tmp/deskops-venv/bin/pip install ../sldb <kgdb artifact> .` from the deskops repo root.
9. Run `/tmp/deskops-venv/bin/python -c 'import deskops.cli.main'` and confirm it exits 0.
10. Run `python -m deskops --help` in the repo environment.
11. Run `pytest tests` and confirm green.
12. Report the pyproject diff, venv result, and any skipped kgdb step to the supervisor; make no commit.

AMBIGUITIES:
1. Exact key/path of the dependency list in `pyproject.toml` is not stated (assumed `[project] dependencies`); no evidence whether optional-dependency groups also need the entries.
2. The PyPI distribution name for kgdb is unverified: `pip download kgdb==0.1.0` may fetch an unrelated public package, and no required-hashes or index constraint is given.
3. No definition of what counts as "no installable kgdb artifact" (pip failure, 404, or an unrelated package) or how that must be recorded.
4. Python version to use for `python -m venv` is unspecified; the local interpreter is anaconda3/python3.13, and sldb/kgdb version compatibility is unknown.
5. Whether deskops should be installed editable (`-e .`) or as a built wheel in the venv is not stated.
6. It is unstated whether a `tests` directory or `pytest` config exists, and whether `pytest tests` is meaningful for a packaging-only change.
7. The declared lower bound `sldb>=0.1.4` cannot be confirmed: nothing states how to read the sibling sldb version, and nothing requires `../sldb` to be a valid installable source.
8. `kgdb>=0.1.0` (declared) vs `kgdb==0.1.0` (downloaded) is an undocumented mismatch with no criterion for which is authoritative.
9. `python -m deskops --help` runs in the pre-existing environment that already has sldb/kgdb installed, so it does not validate the new declarations; no separate criterion covers that.
10. The cited locations `deskops/graph/snapshot.py:119` and `deskops/cli/main.py:249` are unverifiable from the task document alone.
11. No acceptance criterion defines a failing outcome: it is unstated whether the task can close with the venv check skipped and only the deletion/absence of the kgdb artifact reported.
12. `runs/planning/deskops-rewrite-inventory.md` is referenced as the plan source but is not in the `files` list and its existence/content is unstated.
