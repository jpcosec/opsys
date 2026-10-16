RESTATEMENT:

1. Follow AGENTS.md startup route: read `README.md`, `docs/faq.md`, `desk/tasks/Board.md`, routed pills, rituals (`phase`, `execution`, `testing`, `closeout`); load `use-deskops` skill.
2. Confirm this task is routed/active on `desk/tasks/Board.md` (status is `deferred`, `source:drawer`) and that `depends_on: task-rw-f3-closeout-gates-service` is closed.
3. Add a test (location unspecified) that, for every TaskDoc under `desk/` and `tests/fixtures/`, compares `parse_task_sections` overlay output against `extract_model_data` and asserts equality.
4. Run that test; for each divergence, edit the divergent TaskDoc so `extract_model_data` matches (do not keep the overlay).
5. In `deskops/operations.py`, delete the overlay branch in `_read_doc` (lines ~2904-2910) for TaskDoc.
6. Move `parse_task_sections` (operations.py:154-208) to wherever `deskops/cli/commands/promote.py:47` uses it; update that import.
7. Create `deskops/services/tasks.py`; move the task create/advance/next lifecycle methods out of `operations.py` into it; update imports in `deskops/operations.py`, `deskops/cli/commands/operations.py`, `deskops/cli/commands/promote.py`.
8. Create `deskops/cli/parse_input.py`; move `parse_*_input` (operations.py:1068-1183) there; update all callers.
9. Run `pytest tests`; run `deskops list tasks --root .`; run `deskops show task task-write-end-to-end-deskops-operator-manual --root .`; run `grep -n 'parse_task_sections' deskops/operations.py` and confirm empty.
10. Run execution/testing/closeout rituals; leave the diff uncommitted for supervisor closeout.

AMBIGUITIES:

1. Task status is `deferred` with `source:drawer`; AGENTS.md says drawer/unrouted work must be promoted before implementation. Unclear whether to execute now or promote first.
2. `depends_on: task-rw-f3-closeout-gates-service` — no information on whether it is closed or where to check.
3. "create/advance/next" lifecycle methods are not named or located; I would have to guess which `operations.py` symbols move.
4. Destination of `parse_task_sections` is unspecified ("next to promote.py's use") — inline in promote.py, a helper module, or elsewhere.
5. No list of callers of `parse_*_input` or of the lifecycle methods; import rewrites would be guessed.
6. Whether `deskops/services/` and `deskops/services/tasks.py` already exist is unstated.
7. Whether `deskops/operations.py` should keep re-export shims for moved functions (backward compat) is unstated.
8. `_read_doc` handling of non-TaskDoc types after overlay removal is unstated; unclear if the branch is TaskDoc-specific in code.
9. Divergence resolution rule ("fix the document") gives no criterion when `extract_model_data` cannot parse a doc at all, nor whether to skip, error, or coerce.
10. Test location, name, and the exact fixture set under `tests/fixtures/` are unspecified; unclear whether TaskDoc fixtures exist there.
11. Acceptance criteria cover only `parse_task_sections` absence; nothing verifies `parse_*_input` moved or that the service owns lifecycle.
12. Validation id `task-write-end-to-end-deskops-operator-manual` conflicts with the id referenced elsewhere in this repo context (`task-write-end-to-end-operator-manual`); unclear which task exists.
13. Pill `pill-list-surfaces-must-expose-malformed-docs` is bound but the task gives no requirement for how list surfaces must handle docs that fail `extract_model_data` after overlay removal.
