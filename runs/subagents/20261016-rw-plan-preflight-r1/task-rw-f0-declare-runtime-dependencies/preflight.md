RESTATEMENT:

1. Read the task doc and confirm this is `task-rw-f0-declare-runtime-dependencies`, phase F0 of `runs/planning/deskops-rewrite-inventory.md`.
2. Check status `deferred`/`source:drawer`: locate the task file under `desk/drawer/tasks/`, then promote it to the active board (`desk/tasks/Board.md`) per the drawer-to-active promotion ritual, committing creation (if needed) and promotion before implementation.
3. Bind pill `desk/contexts/pill-008-kgdb-sldb-boundary.md` and read it.
4. Confirm import sites: `sldb` across the package, `kgdb` at `deskops/graph/snapshot.py:119` and `deskops/cli/main.py:249`.
5. Inspect `pyproject.toml`; confirm `dependencies` currently lists only `pydantic` and `PyYAML` and note the build backend.
6. Run `pip show sldb kgdb` (or equivalent) to capture installed versions.
7. Derive lower bounds as `<major.minor>` for each and append `sldb>=<X.Y>` and `kgdb>=<X.Y>` to the `dependencies` list in `pyproject.toml`.
8. Create a throwaway venv under `.tmp/`.
9. In that venv run `pip install ../sldb ../kgdb .` followed by `python -c 'import deskops.cli.main'`.
10. Run `python -m deskops --help` and `pytest tests`.
11. Confirm the declared dependencies resolve so a clean `pip install .` works with siblings available, then close out per the closeout ritual with one atomic commit.

AMBIGUITIES:

1. Task is `status: deferred` with `source:drawer`, but the instructions are written as if it is active; unclear whether promotion to `desk/tasks/Board.md` is a required precondition or if execution happens in place.
2. "installed major.minor" does not specify whether to take `major.minor` literally (e.g. `>=0.3`) or a patch-exclusive form, nor how to handle versions like `0.0.x` or pre-releases.
3. Not stated what to do if `pip show sldb kgdb` fails (siblings not installed in the working environment).
4. Unclear whether `sldb`/`kgdb` are meant to be consumed from PyPI or as path/editable sibling installs; the install command uses `../sldb ../kgdb .`, implying local paths, which a fresh-venv `pip install .` alone would not satisfy.
5. Unclear whether a peer/optional dependency group or `[project.optional-dependencies]` is acceptable, or if entries must go in the single `dependencies` array.
6. No stated build backend / metadata guidance (setuptools vs hatchling) to confirm where `dependencies` lives and whether packaging config must change.
7. "Out of scope: version pins beyond a lower bound" is given, but no upper bound policy is specified (open-ended `>=` only).
8. Validation lists `pytest tests`, but "Done When" only requires `pyproject.toml` declaration plus the throwaway-venv import check; unclear if pytest is blocking for closure.
9. `pytest tests` assumes a `tests` directory exists; unverified, and no stated fallback (e.g. bare `pytest` from AGENTS.md).
10. No acceptance criterion that Governance CI keeps passing or must be updated, though the rationale cites CI installing siblings by hand.
11. Unclear whether the `.tmp/` venv must be removed before closeout or left in place.
12. No stated requirement to verify `deskops/graph/snapshot.py` and `deskops/cli/main.py` import `kgdb` at runtime vs lazily, so it is unclear if the import check fully covers the kgdb runtime dependency.
13. Missing acceptance criteria for how to prove a "fresh venv" is genuinely clean (no inherited site-packages, no `ensure_sldb_available` bootstrap masking the dependency).
14. No guidance on whether the task should also confirm the package imports without `deskops/bootstrap.py:ensure_sldb_available` interfering, despite that being named out of scope.
