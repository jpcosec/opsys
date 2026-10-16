RESTATEMENT:
1. Confirm `task-rw-f3-drawer-routing-service` is closed and its `deskops/services/` pattern exists; read the new `deskops/services/drawer_routing.py` (or equivalent) as the template.
2. In `deskops/operations.py`, locate each dead item: `_default_*_payloads` (~lines 1296-1487), `PRIMITIVE_DIRS`, and the duplicate `_setup_logging`.
3. Run `grep -rn '<name>' deskops tests` for each dead item and record the output for the closeout.
4. Identify which `_setup_logging` definition the entrypoint calls (inspect the CLI entrypoint / `deskops/__main__.py` or equivalent) and keep that one; delete the other.
5. Delete `_default_*_payloads` methods, `PRIMITIVE_DIRS`, and the unused `_setup_logging`.
6. Create `deskops/services/primitives.py` with class `PrimitivesService(root)` holding `PRIMITIVE_KINDS`, `create_primitive`, `list_primitives`, `show_primitive`, `parse_primitive_input`, `_normalize_primitive_payload`, `_primitive_path`, preserving their signatures/behavior.
7. In `DeskopsOperations`, add one-line wrapper methods delegating to a `PrimitivesService` instance so `deskops/cli/commands/operations.py` and `tests/test_operational.py` keep working.
8. Run `pytest tests`; fix fallout.
9. Run `python -m deskops next --diagram`; confirm it works.
10. Verify `grep -n '_default_.*_payloads\|PRIMITIVE_DIRS' deskops` is empty and `_setup_logging` is defined once.
11. Do not commit; leave the diff for supervisor review.

AMBIGUITIES:
1. Line numbers (1296-1487, 68, 462, 729, 1012, 1115, 1218, 2609) may be stale; no instruction on how to handle drift.
2. "unchanged signatures" vs `PrimitivesService(root)` constructor: unclear whether helpers keep their current params (including any `self`-carried state) or become methods taking `root`/state explicitly.
3. "Callers (deskops/cli/commands/operations.py and tests/test_operational.py)" — the exact call sites are not shown; unclear whether callers use private helpers (`_normalize_primitive_payload`, `_primitive_path`) directly and therefore also need wrappers.
4. "keeps one-line wrappers" — unspecified whether wrappers are required for all seven helpers or only externally-called ones.
5. Which `_setup_logging` is "the one the entrypoint calls" is not stated; requires inspection not described.
6. Entrypoint file for the `_setup_logging` check is not named.
7. Depends_on `task-rw-f3-drawer-routing-service` is not stated as done; status is `deferred`, so trigger/completion condition is unclear.
8. Grep proof must be "recorded in the closeout," but closeout is out of the stated validation list and the artisan command/artifact for that record is unspecified.
9. `python -m deskops next --diagram` — no described expected output or pass criteria.
10. Out-of-scope mentions "self-reflection ledger" with no file path, so its boundary is unverifiable.
11. No run-dir is provided for the supervisor's `deskops closeout commit` invocation.
12. `PRIMITIVE_DIRS` "unused" — grep may show references in docs/pills/tests; no rule for that case.
