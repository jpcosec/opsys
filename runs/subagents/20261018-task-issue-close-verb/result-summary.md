# Result summary: task-issue-close-verb

## Changed

- `deskops/services/issues.py` (new)
  - `find_issue(root, selector)` — resolves through `deskops.desk_paths.resolve_selector` across `desk/issues/**` and `desk/drawer/issues/**`.
  - `issue_status(text)` — reads frontmatter `status:`, then `## Status` section, then top-of-file `Status:` line; returns a normalized status word or `None`.
  - `close_issue(path, reason, refs, today, *, root=None, force=False)` — rewrites every status representation present, appends `## Resolution` with `Closed:`, `Reason:`, `Refs:`, keeps the file, refuses already-closed unless `force`, rejects empty reasons, and retracks a tracked document through `doc_io` (`sldb.api.doc_status` identifies model/name).
  - `list_issues(root, status="all")` — scans both issue directories and filters `open`/`closed`/`all`.
  - `read_issue`, `Issue`, `IssueCloseResult` dataclasses.
- `deskops/cli/commands/issue.py` (new) — `IssueCLI` dispatches `issue close` / `issue list`, prints `Path: <file>` on close and `id | status | title` on list.
- `deskops/cli/registry.py` — registered `issue`, `issue close`, `issue list` with help and examples.
- `tests/test_issue_cli.py` (new) — covers the three status formats, close-then-list, open/closed/all filters, already-closed refusal and `--force`, unknown selector, unreadable status, empty reason, and `desk/issues/` location.
- `tests/test_command_registry.py` — added `("issue",)` and `("issue", "close")` to `MUTATING_COMMANDS`.
- `tests/test_cli.py` — root help assertion now includes `issue`.
- Golden files: added `help/deskops_issue*.txt`; refreshed `help/deskops.txt` and `output/{list_pills,list_rituals,show_pill}.{json,text}` to current populated output (the committed goldens were stale/empty for pill and ritual bodies).

No `desk/` file was modified, staged, or committed.

## Validation

```bash
PYTHONPATH=/tmp/rw/wt/issueverb python -m pytest tests/test_issue_cli.py tests/test_output_goldens.py tests/test_cli_contract.py -q
# 24 passed in 210.54s
```

```bash
PYTHONPATH=/tmp/rw/wt/issueverb python -m pytest tests -q
# 2 failed, 456 passed, 3 skipped in 606.64s
# FAILED tests/test_doc_readability.py::test_unreadable_fields_are_detected_for_a_hand_written_document
# FAILED tests/test_taskdoc_read_without_overlay.py::test_read_doc_taskdoc_equals_extract_model_data
```

Additional checks:

```bash
PYTHONPATH=/tmp/rw/wt/issueverb python -m pytest tests/test_issue_cli.py tests/test_command_registry.py tests/test_cli.py::test_cli_help_uses_deskops_name -q
# 13 passed in 2.65s

PYTHONPATH=/tmp/rw/wt/issueverb python -m pytest tests/test_output_goldens.py::test_command_output_goldens -q
# 1 passed in 55.76s (run twice, stable)
```

Manual read-only check:

```bash
PYTHONPATH=/tmp/rw/wt/issueverb python -m deskops issue list --root . --status all
# listed all 28 drawer issues with id | status | title; exit 0
```

## Unfixed-code baseline

A clean clone of `HEAD` (`/tmp/rw/issueverb-baseline`) was tested. The two remaining failures are pre-existing and unrelated to this task:

```bash
cd /tmp/rw/issueverb-baseline
PYTHONPATH=/tmp/rw/issueverb-baseline python -m pytest tests/test_taskdoc_read_without_overlay.py tests/test_cli.py::test_cli_help_uses_deskops_name -q
# 1 failed, 1 passed
# FAILED tests/test_taskdoc_read_without_overlay.py::test_read_doc_taskdoc_equals_extract_model_data

PYTHONPATH=/tmp/rw/issueverb-baseline python -m pytest tests/test_doc_readability.py::test_unreadable_fields_are_detected_for_a_hand_written_document -q
# 1 failed

PYTHONPATH=/tmp/rw/issueverb-baseline python -m pytest tests/test_output_goldens.py::test_command_output_goldens -q
# 1 failed (list_pills.json: committed empty values vs populated extraction)
```

## Looks like an sldb issue (not fixed)

- File: `tests/test_doc_readability.py` + `sldb/runtime/validation.py` (`extract_model_data` / `Validator.extract`).
- Command: `PYTHONPATH=/tmp/rw/wt/issueverb python -m pytest tests/test_doc_readability.py::test_unreadable_fields_are_detected_for_a_hand_written_document -q`
- Output: `AssertionError: assert 'what' in ['why']`.
- Direct extraction of the same hand-written `PillDoc` yields `why: ''` and `how_not: 'Noise makes the knowledge base harder to trust.'`, i.e. sldb maps the `## Why` body into `how_not`, so `why` looks unreadable.
- File: `tests/test_taskdoc_read_without_overlay.py` + `sldb/runtime/validation.py`.
- Command: `PYTHONPATH=/tmp/rw/wt/issueverb python -m pytest tests/test_taskdoc_read_without_overlay.py -q`
- Output: `ValidationError: id Field required`, `status Field required` for `desk/drawer/tasks/task-release-deskops-0-2-0-pendiente-hasta-que-la-suite-completa-funcione-junta.md`, which has `ID:`/`Status:` lines and no frontmatter. This file is pre-existing and malformed for `TaskDoc`; the test treats it as fatal.
- Golden observation: the first `--update-golden` run wrote empty `what/why/...` and ritual `purpose` values for docs created moments earlier in the same fixture; later runs extracted populated values. That suggests an sldb index/read timing race, recorded as an observation only.

## Task ambiguities / deviations

- The task says `issue_status(text)` raises `DomainError` naming the file, but the signature has no path. Implemented `issue_status(text) -> str | None`; `read_issue(path)` raises the typed `DomainError` with the path.
- `close_issue(path, reason, refs, today)` also needs the repository root and `--force`; added them as keyword-only parameters.
- There is no `IssueDoc` model. Tracking refresh uses `sldb.api.doc_status` to read the existing model/name, then `doc_io.untrack` + `doc_io.track`, only when the file is already tracked.
- Existing issues use `resolved`, `done`, and `closed (...)` variants; these are treated as closed for listing/refusal while the raw status word is normalized to its first token.
- Golden refresh touched pill/ritual output files in addition to the new issue help files. The previous goldens were stale and made `test_command_output_goldens` fail on a clean `HEAD`; refreshed values are the populated ones.
