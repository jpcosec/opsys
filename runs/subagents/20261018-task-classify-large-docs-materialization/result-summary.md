# Result Summary

## Changes

- `deskops/graph/extract_docs.py` — `_iter_doc_paths()` now adds root `README.md` and `deskops/data/**/*.md` as `doc` nodes when present.
- `README.md`, `docs/atoms.md`, `docs/faq.md`, `docs/how-to-report.md`, `docs/how-to-test-ux-cli.md`, `docs/knowledge-materialization-model.md`, `docs/quickstart.md`, `docs/sldb-templates.md`, `docs/workflow-policy-reference.md` — added `atoms:` YAML frontmatter with `role: documents`; replaced the duplicated top "This ... is a human-facing materialization of these atoms" bullet list with `Source atoms are declared in the YAML frontmatter.`; preserved existing atom ids and all other prose.
- `deskops/data/faq.md` — copied byte-for-byte from `docs/faq.md`.
- `tests/test_large_doc_materialization.py` — new tests for frontmatter presence, allowed roles, FAQ byte equality, and a `doc:README.md -> atom:...` declared edge.

## Validation

- `PYTHONPATH=/tmp/rw/wt/largedocs python -m pytest tests/test_large_doc_materialization.py -q`
  - `3 passed in 2.49s`
- `PYTHONPATH=/tmp/rw/wt/largedocs python -m deskops graph missing --root .`
  - `24 missing, 124 informational` (exit 1; same exit status as baseline)
- `PYTHONPATH=/tmp/rw/wt/largedocs python -m pytest tests -q`
  - `485 passed, 3 skipped in 704.43s (0:11:44)`
  - Equivalent to `python -m pytest -q` because `testpaths = ["tests"]`.

## Against unfixed baseline

- Created a detached worktree at `HEAD` before changes, copied the new test in, and ran:
  `PYTHONPATH=<baseline> python -m pytest tests/test_large_doc_materialization.py -q`
  - `2 failed, 1 passed` (frontmatter test and declared-edge test failed; byte-equality test passed).
- Baseline `deskops graph missing --root .`: `34 missing, 124 informational`.
- Diff of missing findings before/after showed no new findings; three unique findings disappeared because `deskops/data/faq.md` and `tests/test_large_doc_materialization.py` now exist as graph nodes.
- Baseline worktree was removed afterward.

## Ambiguities / Notes

- `docs/knowledge-materialization-model.md` also contains a tail `## Source Atoms` list. I left it unchanged because the task only asked to remove the top "This ... is a human-facing materialization" bullet list and said to keep all other prose unchanged. Its atoms are different from the removed top list and still extract as `references` edges.
- `graph missing` returns exit 1 both before and after this task due to pre-existing missing targets; the task's condition is "no new dangling atom target", which holds.
- No sldb defects encountered.
