# task-rw-package-runs-outside-editable-install — execution summary

## What changed

- `deskops/paths.py` (new): `package_pythonpath()` returns the directory containing the `deskops` package; `data_path(*parts)` resolves package data.
- `pyproject.toml`: added `[tool.setuptools.package-data] deskops = ["spec/**/*.yaml", "data/faq.md"]`.
- Moved `spec/` -> `deskops/spec/` (`git mv`, 60 files).
- Added packaged FAQ copy `deskops/data/faq.md` (byte-identical to `docs/faq.md`; pinned by test).
- Replaced every `Path(__file__)` location:
  - `deskops/bootstrap.py`: `default_pythonpath`; removed `_package_root`; `_resolve_sldb_checkout`; `_deskops_owner_store`.
  - `deskops/doc_io.py`: `_PACKAGE_ROOT` removed; `_pythonpath`.
  - `deskops/lifecycle.py`: `SPEC_PATH`, `_pythonpath`.
  - `deskops/lifecycle_migration.py`: `migrate_legacy_lifecycle`.
  - `deskops/operations.py`: `DeskopsOperations.__init__` (`spec_root`).
  - `deskops/services/atoms.py`: `_retarget_atom_documents`, `_untrack_atom_document`.
  - `deskops/services/tasks.py`: `next_action_report` workflow source label.
  - `deskops/cli/main.py`: `PACKAGE_ROOT`.
  - `deskops/cli/commands/desk.py`: three repair paths.
  - `deskops/cli/commands/faq.py`: packaged FAQ fallback.
- `deskops/bootstrap.py` fallback: when no owner store exists next to the installed package (wheel/non-editable install), `_register_models_directly()` registers every `MODEL_REFS` entry with `doc_io.register_model(..., pythonpath=package_pythonpath())` instead of linking/inheriting; it prints one clear line naming the missing owner path.
- `deskops/cli/commands/desk.py`: `copied_models` is now only reported when an owner store is available. Without that, `desk update` treated the expected directly-registered models as permanently "copied" and exited 1.
- Tests updated: `tests/test_specs.py`, `tests/test_materialization_contract.py`, `tests/test_cli.py`; new `tests/test_packaging.py` covering helper paths, packaged data, FAQ equality, owner-store fallback, and clean `desk update` in non-editable mode.
- Docs updated to `deskops/spec/`: `README.md`, `docs/faq.md` (and the packaged copy), `deskops/lifecycle.py` docstring.

## Validation

Commands ran with `PYTHONPATH=/tmp/rw/wt/packaging` where noted.

1. `PYTHONPATH=/tmp/rw/wt/packaging python -m pytest tests -q`
   - `443 passed, 3 skipped in 451.95s (0:07:31)`
2. `PYTHONPATH=/tmp/rw/wt/packaging python -m pytest tests`
   - `443 passed, 3 skipped in 451.62s (0:07:31)`
3. `grep -rn "Path(__file__)" deskops/ --include="*.py"`
   - only `deskops/paths.py:15`.
4. Wheel build: `python -m pip wheel . --no-deps -w /tmp/rw/f0/wheels`
   - wheel contains 60 `deskops/spec/**` data files and `deskops/data/faq.md`.
5. Fresh venv `/tmp/rw/f0/venv3`:
   - `python -m venv /tmp/rw/f0/venv3`
   - `pip install /home/jp/proyectos/SLDB_1/sldb`
   - `pip install --no-deps deskops-0.1.0-py3-none-any.whl`
   - installed path: `/tmp/rw/f0/venv3/lib/python3.13/site-packages/deskops/__init__.py`
6. Sandbox `/tmp/rw/f0/sandbox3` (`git init`, `HOME=/tmp/rw/f0/home3`, `PYTHONPATH` unset, cwd outside the checkout):
   - `deskops init .` -> 0
   - `deskops add task --root . --title T --goal g --scope s --implementation-path i --done-when d --validation pytest` -> 0
   - `deskops advance task task-t --root .` -> 0
   - `deskops desk update --root .` -> 0 (`Desk is up to date.`)
   - `deskops faq` -> 0
7. `PYTHONPATH=/tmp/rw/wt/packaging python -m deskops --help` -> 0.

## Tests against unfixed code

- None were executed before editing. The failure was established from the cited source locations; the new tests target the new behavior.

## Task issues / ambiguities found

- Cited line numbers were stale, as the task anticipated. Actual sites were found with `grep -rn "Path(__file__)" deskops/`; some Rationale lines (`operations.py:1830`, `:1859`, `:2333`, `:2434`) no longer exist.
- kgdb steps were skipped as instructed; kgdb does not exist here.
- Non-editable `init` initially made `desk update` exit 1 because directly registered models were classified as "copied deskops models" that should be inherited. Fixed by gating that classification on the presence of an owner store.
- `deskops/graph/extract_docs.py` and `extract_sources.py` intentionally still treat `<repo>/spec` as the generic user-repo spec convention. Consequence: graph extraction on the deskops repo itself no longer indexes `deskops/spec/*`. The task scoped moving package data, so this generic extractor was left unchanged; it is not a runtime location.
- No sldb bug observed. No sldb changes made.

## Notes

- No commit, `git add`, or desk-mutating command was run against this worktree.
- The stray `build/` directory from `pip wheel` was removed.
