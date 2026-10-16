RESTATEMENT:
1. Read `desk/contexts/pill-008-kgdb-sldb-boundary.md` to confirm the sldb/kgdb boundary constraint before editing.
2. Open `pyproject.toml` and locate the `[project]` `dependencies` list.
3. Add `"structuredLanguageDB>=0.1.4"` and `"kgdb>=0.1.0"` to that list; change nothing else in the file (no upper bounds, no publishing config, no `deskops/bootstrap.py`).
4. Create throwaway venv: `python -m venv /tmp/deskops-venv`.
5. Run `/tmp/deskops-venv/bin/pip install ../sldb "git+https://github.com/jpcosec/kgdb.git@1247139" .` from the deskops repo root.
6. Run `/tmp/deskops-venv/bin/python -c 'import deskops.cli.main'`; expect success.
7. Run `/tmp/deskops-venv/bin/python -m deskops --help` (Validation item 1).
8. Run `pytest tests` green (Validation item 2 / Resolved Decisions).
9. If step 5 or 6 exits non-zero, keep the declaration as written and record the exact command and error for closeout.
10. Do not commit; hand the diff to the supervisor for promotion/closeout commit via `deskops closeout commit --task task-rw-f0-declare-runtime-dependencies --run-dir <dir>` or `--no-run --reason <why>`.

AMBIGUITIES:
1. Step 5 can fail on the `>=0.1.4` lower bound if `../sldb/pyproject.toml` still declares 0.1.3 (doc says main-env metadata reads 0.1.3). Task does not state the sibling pyproject's declared version, nor whether fixing it is allowed.
2. Contradiction: Implementation Path step 2 says any non-zero pip exit → keep declaration and record it, but Done When only permits the "missing kgdb source" case as an exception. Unclear which non-zero outcomes count as satisfied.
3. Unclear whether Validation (`python -m deskops --help`, `pytest tests`) must run in the throwaway venv or in the main environment (where metadata is stale at 0.1.3 plus a stale editable `sldb 0.1.0` entry).
4. No statement that a `tests/` directory exists or that `pytest tests` is the correct path (AGENTS.md says `pytest`).
5. Unclear whether the stale `sldb 0.1.0` editable entry in the main env must be cleaned; not listed in Scope.
6. Task `status: deferred` conflicts with execution, but Resolved Decisions assigns promotion to the supervisor; executor trigger is unstated.
7. No acceptance criterion for whether pip's resolved versions after install must be verified (e.g., `pip show structuredLanguageDB`).
