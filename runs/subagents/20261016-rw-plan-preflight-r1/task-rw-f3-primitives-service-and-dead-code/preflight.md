RESTATEMENT:

1. Locate and read the task doc, `desk/tasks/Board.md`, and `desk/rituals/{phase,execution,testing,closeout}.md`; confirm dependency `task-rw-f3-drawer-routing-service` is closed and this task is promoted from drawer to active before touching code.
2. Read `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md` and bind it.
3. Grep for non-test callers of each dead item: `_default_*_payloads` (operations.py:1296-1487), `PRIMITIVE_DIRS`, `_setup_logging`, imports of `deskops/specs/mermaid.py`, imports of `deskops/materializers/atoms.py`. Record raw grep output for closeout.
4. Grep for existing primitive path/read helpers in `deskops/operations.py` that must keep working.
5. Create `deskops/services/primitives.py` containing primitive path constants and the read/lookup helpers moved out of operations.py.
6. Leave wrappers in the previous location(s) so existing callers keep resolving.
7. Delete `deskops/specs/mermaid.py`, `deskops/materializers/atoms.py`, `_default_*_payloads`, `PRIMITIVE_DIRS`, and the duplicate `_setup_logging`.
8. Delete test files/cases that exist only to exercise the deleted code.
9. Run `pytest`.
10. Run `python -m deskops next --diagram` against a sandbox desk root.
11. Compare `wc -l deskops/operations.py` before/after; confirm ≥190 line reduction.
12. Run closeout: record grep proofs, line delta, deleted tests; make one atomic commit.

AMBIGUITIES:

1. The Rationale, Goal, Scope, and Implementation Path headers contain unfilled template placeholders while "Open Ambiguities" says "None" — contradictory.
2. No acceptance criteria define the service's public API (function/constant names, signatures, return types).
3. "Move primitive helpers into the service with wrappers" does not say which helpers, where the wrappers live, or whether wrappers are temporary or permanent.
4. `PRIMITIVE_DIRS` location is not given in the doc and is not in the `files` list.
5. `_setup_logging` "duplicated" — the two locations are not identified.
6. Unclear whether `specs/mermaid.py` and `materializers/atoms.py` are deleted entirely, trimmed, or replaced; the doc only says "used only by tests".
7. Unclear what replaces the test coverage for behavior those modules/tests covered, if any is behaviorally required.
8. "tests that exist only to exercise it" — no test paths or names given.
9. `python -m deskops next --diagram` validation does not specify the desk root (repo `desk/` vs sandbox), despite the AGENTS rule to use a sandbox root.
10. `operations.py` line ranges (1296-1487) may be stale and are not verifiable from the doc.
11. Task doc file path is not given, so it is unverified whether it is in `desk/drawer/tasks/` (status `deferred`) and whether promotion is required first.
12. "Done When" fixes only a line-count threshold for one file; it does not state the required end state for `specs/mermaid.py`, `materializers/atoms.py`, or the service.
13. No statement of whether `deskops/services/primitives.py` must be exported via `deskops/__init__.py` or any CLI surface.
14. No coverage or lint gate specified beyond `pytest`.
15. Unclear whether "dead code is gone" permits zero-caller public functions to remain for external consumers.
