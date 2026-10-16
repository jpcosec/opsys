RESTATEMENT:
1. Load `runs/planning/deskops-rewrite-inventory.md` (phase F3) and the two pills to confirm constraints.
2. Read `deskops/operations.py`; identify the drawer/inbox→drawer promotion and drawer lookup methods and their callers.
3. Read `desk_paths` and `doc_io` modules to learn the helper APIs the service must use.
4. Create `deskops/services/__init__.py`.
5. Create `deskops/services/drawer.py` implementing inbox→drawer promotion and drawer lookup, using `desk_paths` and `doc_io`.
6. Move the identified method bodies from `deskops/operations.py` into the service, preserving logic exactly.
7. Leave thin wrapper methods on `DeskopsOperations` delegating to the service so signatures/returns are unchanged.
8. Run `pytest tests/test_inbox_promote_cli_gaps.py tests/test_promotion_nesting.py`.
9. Run `pytest`.
10. Verify behavior unchanged and suite passes; commit the change.

AMBIGUITIES:
1. The exact drawer methods in `operations.py` are not enumerated; cannot tell which code is "drawer routing" vs. the other 14 domains without guessing.
2. Service construction/DI is unspecified: whether it receives `desk_paths`/`doc_io` as modules, instances, or constants, and how `DeskopsOperations` passes them.
3. Import paths and APIs of `desk_paths` and `doc_io` are not given.
4. "Leave wrappers" — required signatures, return values, and error-propagation behavior are unspecified; exact-parity is asserted but not defined.
5. No inventory of external importers/callers of the moved methods; moving may break unseen imports.
6. Contents/exports of `deskops/services/__init__.py` are unspecified.
7. "the F1 contract tests" is undefined; only two test files are named, and it is unclear if they are the F1 contract tests.
8. Dependency `task-rw-f2-transactional-doc-io` is not provided; its interface/status cannot be verified, and the task is marked `deferred`.
9. Referenced pills (`pill-cli-gaps-become-tracked-work.md`, `pill-operational-cli-grammar-follows-spoken-workflow.md`) are not included; their obligations are unknown.
10. AGENTS.md workflow (drawer creation, promotion commit, fresh-context subagent execution, gating rituals) is not reflected in the task steps; unclear whether it applies.
11. "Done When ... suite passes unchanged" gives no explicit behavior-parity check beyond passing tests; test coverage of drawer paths is unknown.
12. Task says "Open Ambiguities: None," which contradicts the above unresolved items.
