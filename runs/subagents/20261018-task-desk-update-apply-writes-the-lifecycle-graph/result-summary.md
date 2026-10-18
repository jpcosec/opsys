# Result: task-desk-update-apply-writes-the-lifecycle-graph

## Changes

- `deskops/cli/commands/desk.py` — `DeskCLI.update`: at the end of the `--apply` repair path, after store/document repairs, if the store exists and `lifecycle_graph_present(root)` is false, calls `ensure_lifecycle_graph(root)` and prints each change as `Lifecycle graph: ...`.
  - Root cause: the graph was only written by `migrate_legacy_lifecycle`, which ran only when `legacy_pending` was true (legacy docs, tasks to rewrite, or graph missing on an existing desk). On a fresh repo, `legacy` is `None` because `desk/` does not exist yet, so scaffolding + store init never reached the graph step.
  - Placement after untracked-document tracking ensures rituals are tracked under their lifecycle ids rather than by file stem.
- `tests/test_desk_sync.py` — added `test_desk_update_apply_on_a_fresh_repo_writes_the_lifecycle_graph`: fresh `tmp_path`, first `desk update --apply` exits 0, second `desk update` exits 0 and prints `Desk is up to date.`

## Validation

- `PYTHONPATH=/tmp/rw/wt/deskupd python -m pytest tests/test_desk_sync.py -q`
  - `3 passed in 15.93s`
- `PYTHONPATH=/tmp/rw/wt/deskupd python -m pytest tests -q`
  - `387 passed, 3 skipped in 311.18s (0:05:11)`
- Manual reproduction in `/tmp/freshdesk` (fresh `git init`, outside the worktree):
  - `python -m deskops desk update --root . --apply` → exit 0, prints `Lifecycle graph: ...` lines
  - `python -m deskops desk update --root .` → `Desk is up to date.`, exit 0
  - `python -m sldb stores check --store .sldb --format json` → exit 0

## Test against unfixed code

- New test run before the fix: `1 failed` — second `cli.run(["desk","update",...])` returned 1 with report `Legacy task lifecycle: ... lifecycle graph missing ...`.

## Notes / ambiguities

- Task's line-number hints were not present in the doc; implementation path matched the real code.
- `desk update --apply` on a fresh repo also leaves an `.sldb/deskops` symlink to this checkout (existing `init_local_store` behavior), unrelated to this task.
- No sldb bug encountered.
- `desk/tasks/task-desk-update-apply-writes-the-lifecycle-graph.md` still has `status: draft`, `current_node: ritual-execution`, and empty `summary`; not touched per instructions.
