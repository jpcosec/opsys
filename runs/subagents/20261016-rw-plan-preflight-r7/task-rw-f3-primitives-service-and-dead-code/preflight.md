RESTATEMENT:

1. Verify prerequisite: confirm task-rw-f3-drawer-routing-service is closed and read `deskops/services/` (or its equivalent) to copy the established service pattern, including `__init__.py`, service class shape, and constructor signature.
2. Locate each dead item and capture proof with `grep -rn '<name>' deskops tests` for: `_default_*_payloads` (claimed lines 1296-1487), `PRIMITIVE_DIRS`, and both `_setup_logging` definitions; save output for the supervisor's closeout.
3. Determine which `_setup_logging` definition the entrypoint calls (grep the entrypoint), then delete the other one.
4. Delete the `_default_*_payloads` methods and `PRIMITIVE_DIRS` from `deskops/operations.py`.
5. Create `deskops/services/primitives.py` with `PrimitivesService(root)` storing `root` and `desk_root` on the instance.
6. Move as instance methods, same parameters except dropping `self`-only duplication: `create_primitive`, `list_primitives`, `show_primitive`, `parse_primitive_input`, `_normalize_primitive_payload`, `_primitive_path`.
7. Move `PRIMITIVE_KINDS` to `deskops/services/primitives.py` as a module-level constant.
8. Rewire collaborator calls (`ensure_workspace`, `_write_new_doc`, `_read_doc`, `_resolve_glob`, `_coerce_list`) to `deskops.doc_io`, `deskops.desk_paths`, or a shared helper module.
9. In `DeskopsOperations`, replace the removed bodies with one-line wrapper methods that delegate to a `PrimitivesService` instance, preserving the public method names and signatures used by `deskops/cli/commands/operations.py` and `tests/test_operational.py`.
10. Update `tests/test_operational.py:37` so the monkeypatch of `operations._write_doc` targets the `doc_io` function the service now calls, preserving the rollback assertion.
11. Run `grep -n '_default_.*_payloads\|PRIMITIVE_DIRS' deskops` and confirm empty.
12. Run `pytest tests` and `python -m deskops next --diagram`.
13. Do not commit; hand the diff to the supervisor.

AMBIGUITIES:

1. Task `status: deferred` and depends_on task-rw-f3-drawer-routing-service: the task doc does not state whether that dependency is closed, so executability is unverifiable.
2. The "pattern set by task-rw-f3-drawer-routing-service" is not included; the referenced service file, constructor shape, registry/bootstrap wiring, and package layout are unknown.
3. The "shared helper module" is unnamed: no decision on whether to create one, its path, or which of `ensure_workspace`/`_write_new_doc`/`_read_doc`/`_resolve_glob`/`_coerce_list` belongs in `doc_io` vs `desk_paths` vs it.
4. "same parameters" is ambiguous once `root` is carried on the instance — unclear whether existing `root`/`desk_root` parameters are removed or kept.
5. Line numbers (68, 462, 729, 1012, 1115, 1218, 1296-1487, 2609) may be stale; no instruction on what to do if they do not match.
6. It is not stated which file is "the entrypoint" that calls `_setup_logging`, so which duplicate to keep is not determinable from the doc alone.
7. Exact `doc_io` function name to repoint the `tests/test_operational.py:37` monkeypatch is not given; the test's current assertion text is not provided.
8. No list of actual callers in `deskops/cli/commands/operations.py` is provided, so "keep callers working" cannot be verified against a defined set.
9. No required format/artifact location is given for the grep proof ("record in the closeout"), and the executor does not commit.
10. No guidance on whether `deskops/specs/` or `deskops/materializers/` re-exports reference moved names, so conflict risk with the "they stay" constraint is unverifiable.
11. No acceptance criterion covers service registration/discoverability, only file existence and grep emptiness.
