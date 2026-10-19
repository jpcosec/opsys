# result-summary: task-desk-replace-verb-for-unmodeled-files

## What changed

- `deskops/services/replace.py` (new)
  - `replace_text(root, target, old, new, *, count=1) -> ReplaceResult`
  - Resolves the path under `desk/` (root-relative, or desk-relative for bare paths), validates UTF-8, refuses modeled subjects, requires the exact occurrence count, writes only after all checks, and re-tracks tracked documents via `doc_io.DocTransaction` (untrack + track, mirroring `DocTransaction.write`).
  - `_modeled_subject`, `_is_task_doc` classify refused/editable paths.
  - Refuses: `desk/tasks/`, `desk/contexts/`, `desk/rituals/`, `desk/materializations/`, `desk/registry/`, `desk/inbox/`, `desk/faq/`, `desk/steps/`, `desk/atoms/**/*.md`, and valid `TaskDoc` files under `desk/drawer/tasks/`.
  - Allows: all other `desk/drawer/**` files, legacy (non-TaskDoc) `desk/drawer/tasks/**`, `desk/issues/**`, `desk/atoms/tag-namespaces.yaml`, `desk/roles/**`, and leftover paths such as `desk/logbook/**` / `desk/models/**`.
- `deskops/cli/commands/desk.py`
  - Added `DeskCLI.replace`; routes `desk_command == "replace"`.
  - Prints `Replaced <n> occurrence(s) in <path>`.
- `deskops/cli/registry.py`
  - Added `("desk", "replace")`, `mutates=True`, args: positional `path`, `--old` (required), `--new` (required), `--count` (int, default 1), `--root`.
- `deskops/services/retire.py`
  - Added `_REQUIRED_STRUCTURE = {desk/config.json, desk/drawer, desk/rituals/phase.md, desk/tasks/Board.md}`.
  - `retire_document` now refuses those paths with `required desk structure: deskops doctor repairs it, so it cannot be retired`.
  - Structure check runs after the existing dedicated-verb check (so `desk/tasks/Board.md` still points at `closeout`) and before the reference check.
- Tests
  - `tests/test_desk_replace.py` (new): unmodeled drawer edit, missing old text, exact-count mismatch, tracked RoleDoc re-track + `check_store(ok=True)`, pill refusal pointing at `deskops edit pill`, `desk/issues` edit, legacy drawer task edit + valid TaskDoc refusal.
  - `tests/test_retire_cli.py`: added `test_retire_refuses_required_desk_structure` for `desk/rituals/phase.md` and `desk/config.json`.
  - `tests/test_command_registry.py`: added `("desk", "replace")` to `MUTATING_COMMANDS`.
  - Help goldens: updated `deskops_desk.txt`, added `deskops_desk_replace.txt`.

## Validation (final results)

- `PYTHONPATH=/tmp/rw/wt/replace python -m pytest tests/test_desk_replace.py tests/test_command_registry.py tests/test_output_goldens.py tests/test_cli_grammar.py tests/test_cli.py -q`
  - `117 passed in 308.55s (0:05:08)`
- `PYTHONPATH=/tmp/rw/wt/replace python -m pytest tests -q`
  - `549 passed, 3 skipped in 771.19s (0:12:51)`
- `PYTHONPATH=/tmp/rw/wt/replace python -m pytest tests/test_output_goldens.py::test_help_goldens --update-golden -q`
  - `1 passed in 115.44s (0:01:55)` (golden regeneration)
- `PYTHONPATH=/tmp/rw/wt/replace python -m deskops desk replace --help`
  - exit 0, usage line: `usage: deskops desk replace [-h] [--root ROOT] --old OLD --new NEW [--count COUNT] path`

## Intermediate / unfixed-code results

- Intermediate run after first implementation: `tests/test_desk_replace.py tests/test_retire_cli.py` → `11 passed, 1 failed`. Failure: `Store error: Doc 'deskops-supervisor' already tracked` because re-tracking must untrack the existing name first. Fixed in `replace_text` by calling `transaction.untrack(path)` before `transaction.track(...)`; the single test then passed.
- Against unfixed HEAD (`git archive HEAD` into `/tmp/rw/unfixed`, new tests copied in):
  - `PYTHONPATH=/tmp/rw/unfixed python -m pytest tests/test_desk_replace.py::test_replace_edits_an_unmodeled_drawer_file tests/test_retire_cli.py::test_retire_refuses_required_desk_structure -q`
  - Result: `2 failed in 8.66s`
    - `test_replace_edits_an_unmodeled_drawer_file`: new `desk replace` command does not exist on HEAD.
    - `test_retire_refuses_required_desk_structure`: HEAD refuses `desk/rituals/phase.md` only because Board.md references it, with `Refusing to retire ... still referenced by desk/tasks/Board.md`, not with the structure message.

## Task ambiguities / deviations

- The addendum explicitly extends the original implementation path: allow `desk/issues/**` and legacy non-TaskDoc `desk/drawer/tasks/**`; still refuse valid TaskDocs there. Implemented that.
- The original path mapping said "allow desk/drawer/**" but `deskops edit task` can also resolve valid TaskDocs under `desk/drawer/tasks`; the addendum's classification resolves this.
- `desk/drawer` is a directory and `retire` only deletes files, so its structure guard is unreachable in practice except for a non-directory path with that exact name; it is still included to match the required-structure list.
- The task's required-structure examples do not mention `desk/contexts/pills.md`; doctor/desk update do not require it, so it was not added.
- Path resolution accepts both `desk/...` root-relative paths and bare desk-relative paths (e.g. `drawer/README.md`); the task did not specify which form.

## sldb observation (not fixed)

- `sldb.api.track_document_file(..., force=True)` still rejects re-indexing an existing document name: `Store error: Doc 'deskops-supervisor' already tracked`.
- Reproduced through the new service when calling `doc_io.DocTransaction.track` after a content write; resolved in deskops by untracking first, which is the existing pattern in `DocTransaction.write`.
- This looks like intended name-uniqueness behavior rather than a bug, so no sldb change was made.
