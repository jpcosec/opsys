# Result summary: task-lifecycle-graph-checks-rituals-are-readable

## Changes

### `deskops/lifecycle.py`
- Added `_ensure_ritual_readable(path, ritual_id, relative) -> bool`:
  - extracts `RitualDoc` data from the ritual file and renders it with `render_model_markdown`;
  - verifies the data-level round trip (`extract(render(payload)) == payload`);
  - additionally checks `is_unreadable_by_model(RitualDoc, text)`, because the data round trip alone does not detect the reported failure;
  - re-renders the file from the extracted payload when either check fails;
  - re-checks the re-rendered file for readability and extraction equality and raises `LifecycleGraphMissing` naming the file, ritual id, and missing fields if it still fails.
- `ensure_lifecycle_graph`: split the ritual loop into a preflight pass that existence-checks and repairs every untracked ritual, and a second pass that untracks/re-tracks them. A failure therefore happens before any ritual is tracked. Re-renders are reported as `re-rendered <path> to the current RitualDoc template`.

### `tests/test_lifecycle_graph.py`
- Added `test_an_old_ritual_without_step_details_is_rerendered_before_tracking`: builds a full current-template execution ritual, removes `## Step Details` (which makes `completion` unreadable), runs `ensure_lifecycle_graph`, asserts the file was re-rendered and readable, contains `## Step Details`, and that `deskops doctor` returns 0.

## Validation (all prefixed with `PYTHONPATH=/tmp/rw/wt/rituals`)

- `python -m pytest tests/test_lifecycle_graph.py -q` -> `13 passed in 14.75s`
- `python -m pytest tests -q` -> `347 passed, 3 skipped in 284.22s (0:04:44)`

## Test against unfixed code

- Restored `deskops/lifecycle.py` from `HEAD` and ran:
  `PYTHONPATH=/tmp/rw/wt/rituals python -m pytest tests/test_lifecycle_graph.py -q -k old_ritual`
- Result: `1 failed, 12 deselected in 4.20s` (`AssertionError` on the expected `re-rendered` change; the ritual stayed unreadable).

## Task issues found

- The implementation path's literal round-trip check, `extract_model_data(RitualDoc, render_model_markdown(RitualDoc, extract_model_data(RitualDoc, text))) == extract_model_data(RitualDoc, text)`, returns true for the broken file. Extraction maps the old file to a payload, rendering that payload is stable, yet the source is unreadable by the model. The implemented check also uses `is_unreadable_by_model`, the predicate behind `deskops doctor`'s finding.
- "Execution ritual lacks `## Step Details`" is not by itself sufficient: the scaffolded ritual in `scaffold_desk` has almost no body sections, so removing `## Step Details` is still readable. The test first renders a full ritual and then removes the section; that reproduces `completion` as unreadable.
- The cited `deskops/lifecycle.py:221-235` range has moved; the ritual loop now starts around line 263.
- No sldb bug observed; no sldb files changed.
