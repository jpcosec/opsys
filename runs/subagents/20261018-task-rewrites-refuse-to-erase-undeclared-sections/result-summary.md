# result summary: task-rewrites-refuse-to-erase-undeclared-sections

Done by the supervisor directly (small fix; no worker dispatched).

## What changed

- `deskops/operations.py` `_write_doc`: before overwriting an existing document, runs sldb's `find_structural_noise(model, existing)` and keeps the undeclared heading lines that re-rendering the file's own extracted payload loses (so atoms split/merge, which deliberately replace a field carrying headings, are not refused; the first version compared against the new payload and broke tests/test_atoms_split.py). It also adds the top-level frontmatter keys from sldb's `undeclared_frontmatter_keys(model, existing)` (graph-ui-59 lost `domain` and `priority` that way). If any remain, raises ValueError naming them, and the file stays unchanged. Headings inside a field that the render keeps are not counted.
- `tests/test_cli.py`: `test_edit_task_refuses_to_erase_undeclared_content` (a hand-written `## Out of scope` section, then an undeclared `priority:` key).

## Validation

- Reproduced on a sandbox desk: `edit task ... goal` erased a hand-written `## Out of scope` section.
- Regression test on the unfixed code: 1 failed (edit exits 0). With the fix: 1 passed.
- Full suite: see validation.log.

## Not covered here

- Code fences as list items are lost in sldb's `rev,list` round-trip (sldb side; reported to sldb-04).
- Migrating undeclared sections into declared fields during `desk update`: not done.

## Reported by

graph-ui-59.
