# Graph node id mapping (F4)

The document node ids keep the shape `<kind>:<id>`. Only drawer tasks change: their
kind was `drawer_task` and their identity was the path; they are now `task` nodes keyed
by the frontmatter `id`. Old ids have no alias.

## Rules

| Document surface | Old id | New id |
| --- | --- | --- |
| atom | `atom:<frontmatter id>` | `atom:<frontmatter id>` |
| active task | `task:<frontmatter id>` | `task:<frontmatter id>` |
| drawer task | `drawer_task:<path>` | `task:<frontmatter id>` |
| pill | `pill:<frontmatter id>` | `pill:<frontmatter id>` |
| board | `board:<frontmatter id>` (path when the board has no id) | unchanged |
| ritual, step, run, role, runtime profile, crossroad, materialization | `<kind>:<frontmatter id>` | unchanged |
| issue | `issue:<frontmatter id or slug>` | unchanged |
| question, feature, use case, stress test, drawer board | `<kind>:<path>` | unchanged |
| doc | `doc:<path>` | unchanged |
| spec | `spec:<path>` | unchanged |
| diagram | `diagram:<path>` | unchanged |
| source file | `source_file:<path>` | unchanged |
| test file | `test_file:<path>` | unchanged |

## Concrete changes in this repository

| Old id | New id |
| --- | --- |
| `drawer_task:desk/drawer/tasks/task-adhoc-subagent-launcher-tmux-multi-cli.md` | `task:task-adhoc-subagent-launcher-tmux-multi-cli` |
| `drawer_task:desk/drawer/tasks/task-rename-deskops-faqdoc.md` | `task:task-rename-deskops-faqdoc` |
| `drawer_task:desk/drawer/tasks/task-rw-f4-coverage-extractor-decision.md` | `task:task-rw-f4-coverage-extractor-decision` |
| `drawer_task:desk/drawer/tasks/task-rw-f4-single-snapshot-reader.md` | `task:task-rw-f4-single-snapshot-reader` |
| `drawer_task:desk/drawer/tasks/task-rw-f5-command-registry.md` | `task:task-rw-f5-command-registry` |
| `drawer_task:desk/drawer/tasks/task-rw-f5-deprecated-aliases.md` | `task:task-rw-f5-deprecated-aliases` |
| `drawer_task:desk/drawer/tasks/task-rw-f5-output-renderer.md` | `task:task-rw-f5-output-renderer` |
| `drawer_task:desk/drawer/tasks/task-rw-f5-root-resolution-and-sandbox-guard.md` | `task:task-rw-f5-root-resolution-and-sandbox-guard` |
| `drawer_task:desk/drawer/tasks/task-rw-f6-bootstrap-registers-all-models.md` | `task:task-rw-f6-bootstrap-registers-all-models` |
| `drawer_task:desk/drawer/tasks/task-rw-f6-migrate-tracking-stores.md` | `task:task-rw-f6-migrate-tracking-stores` |
| `drawer_task:desk/drawer/tasks/task-rw-f6-taskdoc-contract-cleanup.md` | `task:task-rw-f6-taskdoc-contract-cleanup` |
| `drawer_task:desk/drawer/tasks/task-rw-package-runs-outside-editable-install.md` | `task:task-rw-package-runs-outside-editable-install` |
