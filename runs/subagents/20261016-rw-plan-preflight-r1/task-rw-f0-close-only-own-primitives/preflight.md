RESTATEMENT:
1. Open `deskops/operations.py` and locate `_auto_commit_task_closure` (~line 1499), the primitive glob at line 1533 (`*-{task_id}*.md`), and the amend check at line 1547 (`head_subject.startswith(f"closeout: {task_id}")`).
2. Replace the glob with an exact primitive-ownership match: a primitive belongs to the task only when its stem is `<kind>-{task_id}-<suffix>` and `<suffix>` is in the set of suffixes the task bundle creates; a stem whose remainder after `{task_id}-` begins another task-id segment is not a match.
3. Source the valid suffix set from the routine's node/edge refs when the routine exists; otherwise fall back to a hardcoded known suffix set.
4. Replace the amend decision: amend only when `git log -1 --format=%(trailers:key=Task-Id,valueonly)` equals `task_id` exactly (drop the `startswith` subject check).
5. Add two tests to `tests/test_lifecycle_end_to_end.py`: create `task-foo` and `task-foo-bar` via the real CLI; closing `task-foo` leaves all `task-foo-bar` primitives on disk and tracked.
6. Add the second test: with HEAD subject = `closeout: task-foo-bar`, closing `task-foo` creates a new commit (no amend).
7. Run `pytest tests/test_lifecycle_end_to_end.py`; run `pytest tests`.
8. Confirm both new tests fail pre-fix and pass post-fix, and `pytest tests` is green.

AMBIGUITIES:
1. "known suffix set" is never enumerated; no list, constants location, or source file given.
2. How to read suffixes "from the routine's node/edge refs" is unspecified (routine path, format, node/edge field names).
3. What `<kind>` values exist (primitive kinds/prefixes) is not listed.
4. `Task-Id` commit trailer: not confirmed to exist; no statement of who writes it, its exact key/case, or what to do when absent (would silently disable all amends).
5. Introducing/using the `Task-Id` trailer is not listed in scope, yet the amend fix depends on it — possible scope gap.
6. "remain on disk and tracked" test assertions are unspecified (git index vs tracked set, exact primitive count).
7. CLI commands to "create" tasks/primitives are not named; sandbox desk root path not specified.
8. Whether the glob/A-line numbers (1499/1533/1547) still match current source is unverifiable from the doc.
9. Rationale cites "17 primitives of `task-foo-bar`" but Goal/tests are generic — no fixed expected count stated.
10. Behavior for stems like `<kind>-{task_id}` with no trailing `-<suffix>` is undefined.
11. Fallback rule ("otherwise match the known suffix set") and the trigger for "routine exists" are undefined.
12. Whether existing test fixtures/helpers in `tests/test_lifecycle_end_to_end.py` can be reused is unknown.
13. "Both new tests" implies exactly two, but naming/structure/ordering is unspecified.
14. Validation lists pytest only; no CLI direct-invocation check despite pill `real-cli-surfaces-prove-operator-contracts`.
15. Doc states "Open Ambiguities: None", which contradicts items above.
16. No rule given for non-amend commit behavior when trailer matches but subject differs, or vice versa.
