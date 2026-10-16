RESTATEMENT:

1. Verify `task-rw-f3-atoms-service` is closed (dependency satisfied).
2. Verify the owner's issue-2 decision (A, B, or C) is recorded in this task doc; if absent, stop.
3. Read `runs/planning/deskops-rewrite-inventory.md` (finding S1) and `desk/rituals/closeout.md`.
4. Read current implementations: `deskops/operations.py` (`advance` path), `deskops/cli/commands/closeout.py` (`closeout commit`), and existing `deskops/services/closure.py` if present.
5. Read `closeout_gates` module (path not given) and `doc_io` module (path not given) to learn their APIs.
6. Implement/rewrite `deskops/services/closure.py` as the single closure function: run closeout gates, edit Board via doc_io to remove/update the task, delete the bundle (subagent run-dir), commit.
7. Rewire `advance` (in `deskops/operations.py`) to call `closure.py` instead of its inline gate+commit logic.
8. Rewire `advance --to complete` to call the same `closure.py` path (no gate skipping, no Board residue).
9. Rewire `closeout commit` (in `deskops/cli/commands/closeout.py`) to call the same `closure.py` path per the chosen option (A: `--no-run --reason <text>` + `Closeout-Mode: manual` trailer; B: tool generates run snapshots, requires only `result-summary.md`, run dir outside `runs/subagents/`; C: mark `advance` as the official no-subagent path).
10. Update `desk/rituals/closeout.md` to describe the single path.
11. Update the executor role doc (path not given) to match.
12. Update the closeout atom (path not given) to match.
13. Run `pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py`.
14. Run `pytest`.
15. Confirm all three entry points yield identical closure results (Board updated, bundle removed, commit made) and stop only when docs describe one path.

AMBIGUITIES:

1. Task status is `blocked` and scope explicitly says do not start until the owner's issue-2 decision is recorded here — the decision is not present, so the task is not executable.
2. Which option (A, B, or C) applies is unknown; each implies different CLI flags, artifacts, and doc changes.
3. Where the decision must be "recorded here" (which field, `status`, a new section, a linked artifact) is unspecified.
4. Whether dependency `task-rw-f3-atoms-service` is actually closed is not stated.
5. Module paths for `closeout_gates` and `doc_io` are not given.
6. Path of the "executor role doc" is not given; `desk/rituals/closeout.md` is the only doc in `files`.
7. Path of the "closeout atom" is not given.
8. `deskops/operations.py` is listed, but where `advance` is defined (operations.py vs elsewhere) is not verified.
9. Definition of "the bundle" to remove is not given (subagent run-dir? task bundle? Board bundle?).
10. "Same closure result" is undefined: exit code, Board state, git commit, run-dir disposition, or all?
11. Acceptance criteria for docs are subjective ("docs describe the one path") with no checkable condition.
12. Whether `advance --to complete` flag is changed, deprecated, or preserved is unspecified.
13. Whether the fabricated run-dir workaround (`runs/subagents/20260901-manual-task-fix-...`) is removed or retained is unspecified.
14. Commit message format/content for the single closure path is unspecified (only pill-001 says atomic commit).
15. `tests/test_closeout.py` and `tests/test_lifecycle_end_to_end.py` current contents are unknown; whether they must be modified is unspecified.
16. `references: []` is empty and no linked atoms are listed, so no evidence trail for the S1 finding is available from the task alone.
17. `runs/planning/deskops-rewrite-inventory.md` is not included, so S1 details and phase-F3 context cannot be confirmed.
18. No fallback is given if option B's snapshot generation scope (what runs, what format) is larger than the task's file list.
19. Whether `closeout commit` keeps requiring a subagent run-dir in any option is not stated for A/B/C boundary cases.
20. No statement of whether CLI changes need sandbox-desk UX testing (per repo rules) or only pytest.
