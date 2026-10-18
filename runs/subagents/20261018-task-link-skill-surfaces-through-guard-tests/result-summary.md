# Result: task-link-skill-surfaces-through-guard-tests

## Changes

- `deskops/constants.py`
  - Added `SKILL_TREE_PREFIXES = (".pi/skills/", ".agents/skills/", ".opencode/skills/")`.
- `deskops/operations.py`
  - Imported `SKILL_TREE_PREFIXES`.
  - `_closeout_link_gate`: extends `file_evidence` with `_skill_guard_test_evidence(...)` before the follow-up fallback; all other behavior unchanged.
  - Added `_skill_guard_test_evidence(relative_path, graph_context)`: returns `[]` for non-skill paths; otherwise emits `guard-test:<test_path> -> <relative_path>` for each `tests/` file whose text contains the matching skill-tree token (without trailing slash) or the exact relative path, plus `SKILL.md`.
  - Added `_atom_linked_test_paths(graph_context)`: collects `test_file:` nodes targeted by `atom:` edges or by `materialization:` edges, skipping `invalid_materializations`.
- `desk/materializations/materialization-skill-drift-guards.md`
  - New `MaterializationContractDoc` with id `materialization-skill-drift-guards`, source atoms `atom-git-ignored-skill-trees-need-tracked-drift-guards` and `atom-tasks-enable-zero-context-subagents`, `target_kind: test_file`, `target_identity: tests/test_skill_cli_drift.py`, validation `python -m pytest tests/test_skill_cli_drift.py -q`.
- `tests/test_closeout_skill_links.py`
  - `test_atom_linked_guard_test_covers_a_changed_skill_file`
  - `test_guard_test_without_materialization_link_is_not_evidence`
  - `test_non_skill_changed_file_keeps_the_existing_gate_behavior`

## Validation (all run with `PYTHONPATH=/tmp/rw/wt/skilllinks`)

- `python -m pytest tests/test_closeout_skill_links.py -q`
  - `3 passed in 0.81s`
- `python -m pytest tests/test_closeout.py tests/test_skill_cli_drift.py -q`
  - `25 passed in 5.23s`
- `python -m pytest tests -q`
  - `474 passed, 3 skipped in 816.10s (0:13:36)`

## Unfixed-code run

- Ran the new test module with `_skill_guard_test_evidence` monkeypatched to `[]` (the pre-change behavior):
  - `1 failed, 2 passed in 0.29s`
  - Failure: `test_atom_linked_guard_test_covers_a_changed_skill_file` — `assert False is True` at the link gate assertion.

## Notes / ambiguity

- Task says the guard test must contain "the skill tree prefix"; the constant includes a trailing `/` while the real guard test spells `".pi/skills"`. Implemented the text match against the prefix without the trailing slash (`rstrip("/")`).
- "The same repo without the materialization/atom link" was interpreted as removing the materialization contract, since the atom alone cannot link a test node without a materialization or a test→atom edge.
- No sldb defect encountered.
- Full-suite runtime was ~13.5 minutes here, not the ~3 minutes stated in the executor prompt; no timeout-related failures.

## Supervisor note
The worker wrote desk/materializations/materialization-skill-drift-guards.md by hand. In main the same contract was created through `deskops add materialization` as materialization-skill-drift-guard-tests.md; the tests use their own fixture.
