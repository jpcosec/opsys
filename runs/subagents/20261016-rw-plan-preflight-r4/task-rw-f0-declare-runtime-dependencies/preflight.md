RESTATEMENT:

1. Read `pyproject.toml` and confirm the current `dependencies` list (pydantic, PyYAML).
2. Read bound pill `desk/contexts/pill-008-kgdb-sldb-boundary.md` for boundary constraints.
3. Add `"sldb>=0.1.4"` and `"kgdb>=0.1.0"` to the `project.dependencies` list in `pyproject.toml`.
4. From the deskops repo root, run `/tmp` venv check: `python -m venv /tmp/deskops-venv && /tmp/deskops-venv/bin/pip install ../sldb "git+https://github.com/jpcosec/kgdb.git@1247139" . && /tmp/deskops-venv/bin/python -c 'import deskops.cli.main'`.
5. If step 4 exits non-zero, keep the declaration and capture the exact command plus error text for the closeout record.
6. Run `python -m deskops --help`.
7. Run `pytest tests`.
8. Do not commit; hand the diff to the supervisor for closeout commit.

AMBIGUITIES:

1. Task status is `deferred` with `source:drawer`; no promotion record exists in the document. Working location (`desk/drawer/tasks/` vs `desk/tasks/`) is unspecified.
2. "Done When" hedges with "or the missing kgdb source is reported," but the Implementation Path states the kgdb source explicitly. This is contradictory and leaves the true completion condition undefined.
3. "record the exact command and error in the closeout" — no artifact, file, or field is named for where this record goes.
4. `../sldb` lower bound: if the sibling checkout's version metadata is below `0.1.4`, `pip install ../sldb` fails resolution. The checkout's current version is not stated.
5. `git+https://github.com/jpcosec/kgdb.git@1247139` is a short SHA; whether it is fetchable from the remote default branch (vs. requiring a full SHA) is unspecified, and network access is assumed but not stated.
6. Command cwd is not stated; `../sldb` and `.` are only valid from `/home/jp/proyectos/SLDB_1/deskops`.
7. Validation says `pytest tests`, but no `tests` path or contents are confirmed to exist at repo root; repo AGENTS.md says `pytest`.
8. Pill `pill-008-kgdb-sldb-boundary.md` is bound but no requirement from it is stated in the task text.
9. Whether other dependency-declaration sites exist (requirements files, setup.cfg, optional-dependencies) and must also be updated is not stated; scope names only the pyproject `dependencies` list.
10. Referenced plan file `runs/planning/deskops-rewrite-inventory.md` is not listed in `files` and is not stated as required reading.
11. No acceptance criterion exists for step 4's failure branch (who verifies the "report"), so partial completion is undecidable.
