# result summary: task-desk-update-archives-rituals-the-model-cannot-carry

Done by the supervisor directly while running the store migration; no worker dispatched.

## What changed

- `deskops/lifecycle.py`:
  - `_ensure_ritual_readable` also refuses rituals with headings RitualDoc does not declare, using sldb's `find_structural_noise`. sldb itself refuses to track those (TraderBot).
  - When a ritual cannot be carried, `ensure_lifecycle_graph` calls `_archive_legacy_ritual`. It moves the file byte for byte to `desk/drawer/rituals/legacy-<name>.md`, which is not modeled, writes the ritual `deskops init` writes, re-checks it, and reports both paths.
- `deskops/workspace.py`: `default_ritual_text(ritual_id, name)` exposes the init templates.
- `deskops/cli/commands/desk.py`: `desk update --apply` registers the deskops models before the lifecycle migration when the store lacks RitualDoc. hum-core had failed with "Model 'RitualDoc' not registered".
- `tests/test_lifecycle_graph.py`: `test_a_ritual_the_model_cannot_carry_is_archived_and_replaced`, with two cases: no frontmatter, and its own sections.

## Validation

- New tests on the unfixed code: 2 failed. With the fix: tests/test_lifecycle_graph.py 15 passed.
- hum-core migrated with the fix: `stores check` PASS (29 documents, 19 models), `edges check` OK.
- Full suite: see validation.log. A first run gave 13 failed and 59 errors because it overlapped a stopped run that was still alive. The test that failed passed on its own, and the clean rerun is green.

## Owner-visible effect

Repos whose rituals were hand-written keep them in `desk/drawer/rituals/legacy-*.md`. Their owners decide whether to fold that text into the new rituals.
