# result summary: task-promote-writes-drawer-tasks-as-taskdoc

Done by the supervisor directly; no worker dispatched. The faqdoc worker found the bug.

- `deskops/services/drawer.py` `_render_drawer_task`: renders the drawer task through TaskDoc with status deferred. Goal, scope, implementation path, validation and done-when come from the note's sections; `why` names the source note. The note is deleted on promotion, so it goes in `why` and not in `references`, where `graph missing` would flag it.
- `tests/test_promotion_nesting.py`: reads the promoted fields through TaskDoc. The rendered template now carries its instruction lines.
- `desk/drawer/tasks/task-release-deskops-0-2-0-...md`: replaced through the CLI with `drawer remove`, `message send` and `promote inbox-to-drawer-task`.

Validation: tests/test_taskdoc_read_without_overlay.py failed on main before the fix and passes after it. Full suite: see validation.log.
