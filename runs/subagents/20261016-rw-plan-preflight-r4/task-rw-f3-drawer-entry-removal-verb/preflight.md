RESTATEMENT:
1. Confirm the two owner decisions are resolved (verb name; `from_drawer` dangling behavior). Task is `status: blocked` and `depends_on: task-rw-f3-drawer-routing-service`; stop if either is unresolved.
2. Read `deskops/services/drawer.py` to find `DrawerService`'s existing entry-resolution, file-track, and Board surfaces.
3. Read `deskops/cli/parser.py` to find the command-registration pattern; register the new verb (name from the owner decision) with its selector argument.
4. Implement removal in `DrawerService` inside a `DocTransaction`: delete the drawer file, untrack it from the store if tracked, and delete every `desk/drawer/tasks/Board.md` bullet line starting with ``- `<stem>` ``.
5. Apply the decided behavior when an active task's `from_drawer` points at the entry; reference `PROVENANCE_FIELDS` at `deskops/graph/extract_edges.py:31`.
6. Add a sandbox CLI test using `_make_repo`/`_cli` helpers from `tests/test_lifecycle_end_to_end.py`: `tmp_path`, git init, one seed commit, `desk install`, drive real CLI; assert file gone, its Board bullets gone, other bullets intact.
7. Place the test in `tests/test_inbox_promote_cli_gaps.py` per the `files` list.
8. Run `pytest tests/test_inbox_promote_cli_gaps.py` then `pytest tests`.
9. Do not commit; hand the diff to the supervisor for closeout.

AMBIGUITIES:
1. Verb name is undecided (task-stated blocker); step 3 cannot be written.
2. Behavior on dangling active-task `from_drawer` (refuse/warn/silent) is undecided; steps 5–6 cannot be implemented or tested.
3. `status: blocked` — no statement of who unblocks it or whether `depends_on` must first be closed.
4. Selector form unspecified (stem, path, task-id, glob).
5. "one drawer file" — unclear whether other `desk/drawer/*/Board.md` files exist or are in scope.
6. "several headings" — which headings and matching scope unspecified.
7. Exact bullet-match rules unspecified (dash type, spacing, trailing characters).
8. "untracks it if tracked" — no mechanism named (store op vs `sldb` command); behavior when untracked or store absent unspecified.
9. `DocTransaction` scope unspecified: whether the drawer file and Board.md are both enrolled.
10. No CLI output, exit-code, error-path, or idempotency requirement.
11. `files` names `tests/test_inbox_promote_cli_gaps.py` (inbox/promote domain) for a drawer-removal test — no placement rule.
12. Done When says "the test passes" (singular) while Validation lists two test commands.
13. No requirement to update `faq`/help/docs.
14. No acceptance criteria about verifying the `from_drawer` provenance after removal beyond the owner decision.
