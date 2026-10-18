# result-summary - task-detect-and-clean-task-policy-leaks

## What changed

- `deskops/task_policy.py` (new): `TaskPolicyLeak(path, line, phrase)` dataclass and `scan_task_policy_leaks(root)`.
  - Scans only `desk/tasks/task-*.md` and `desk/drawer/tasks/task-*.md`; skips `Board.md` and frontmatter.
  - Applies the five sentence-level regexes from the task, case-insensitive; reports at most one finding per sentence.
  - Skips fenced code blocks, inline code spans, and double-quoted examples so documentation of a phrase is not a finding.
  - Never writes to task files.
- `deskops/graph/self_reflection.py` (`drift_check_knowledge_surfaces`): added finding 5, `task-policy-leak: <path>:<line> repeats global policy phrase '<phrase>'; reference desk/rituals/closeout.md or a pill instead`.
- `tests/test_task_policy_leaks.py` (new): 7 tests covering one finding per leaked sentence, task-local validation text, ignored frontmatter, drawer scanning, ignored code/quoted examples, byte preservation, and drift integration.

## Validation

Commands run with `PYTHONPATH=/tmp/rw/wt/policyleak`.

- `python -m pytest tests/test_task_policy_leaks.py -q` -> `7 passed in 0.10s` (exit 0)
- `python -m pytest tests/test_graph_self_reflection.py -q` -> `2 passed in 0.03s` (exit 0)
- `python -m deskops drift check --root .` -> exit 1; `21` findings: `19` pre-existing + `2` new `task-policy-leak` (listed below). No other new finding kinds.
- `python -m pytest -q` -> `506 passed, 3 skipped in 757.98s` (exit 0)
- `python -m pytest tests -q` -> `506 passed, 3 skipped in 798.66s` (exit 0)

## Unfixed-code check

- Before adding the scanner, `python -m deskops drift check --root .` printed `24` findings and **zero** `task-policy-leak` findings (exit 1). After wiring, the two findings below appear.
- The new test module cannot pass at HEAD: it imports `deskops.task_policy`, which does not exist there.

## Desk cleanup the supervisor must apply (do not taken as done)

1. `desk/tasks/task-detect-and-clean-task-policy-leaks.md`
   - Field/section: `Rationale` paragraph.
   - Replace: `..., but at least one active task restates supervisor, executor, commit, and closing rules. There is no drift check for this leakage.`
   - With: `..., but at least one active task restated global workflow rules. There is no drift check for this leakage.`
   - Reason: line 32 matches `\b(supervisor|executor)\b.*\b(commit|promote|close)` in the task's own rationale.
2. `desk/tasks/task-edit-reaches-drawer-tasks-and-rituals-by-id.md`
   - Field/section: `Rationale` paragraph, second sentence.
   - Replace: `To change the release drawer task, the supervisor had to remove it and recreate it through message send plus promote.`
   - With: `To change the release drawer task, it had to be removed and recreated through message send plus promotion.`
   - Reason: line 28 matches the same regex, but it describes local reproduction evidence rather than restating policy.

After both edits, `deskops drift check` has no `task-policy-leak` finding (verified by the scanner's output set; the other regexes only fired on code/quoted examples, which are skipped).

The task's original cleanup target `desk/tasks/task-init-repairs-a-broken-owner-link.md` no longer exists (closed and deleted in commit `33c0482`), so no cleanup is possible or needed there.

## Wrong or ambiguous in the task

- The named cleanup target is already closed and deleted; the "current leak" the task refers to is not in the tree.
- Done When ("no task-policy-leak finding for the repository") is unreachable during this task's own execution: the mandated regexes match two existing task rationales, one of them this task's own text. That conflicts with "everything must be green" for the drift command.
- The first mandated regex has no trailing word boundary. Adding `\b` after the group would fail to detect the original leak, because it used `promotes`, `commits`, and `promotion`. The literal pattern was kept.
- Sentence-level matching required two interpretations not stated in the task: (a) one finding per sentence even when two patterns match, and (b) ignoring fenced code, inline code, and double-quoted examples so the task's own regex/example text is not flagged. Both are covered by tests.

## Supervisor note
The worker listed two text cleanups. The task's own rationale was rewritten with `deskops edit task ... why`, and the stale reference to the closed owner-link task was dropped from its files, scope and implementation path. The second listed leak (the edit-gap task) was already gone: that task closed in b970352. `deskops drift check` reports 0 task-policy-leak findings.
