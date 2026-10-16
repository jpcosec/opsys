RESTATEMENT:
1. Read `desk/contexts/pill-008-kgdb-sldb-boundary.md` and `desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md`; read `runs/planning/deskops-rewrite-inventory.md` (phase F4) for context.
2. Create throwaway repo: `mktemp -d` under `/tmp`, `git init`, then `deskops init .` to create the store, register deskops models, scaffold `desk/`.
3. Add two tasks via `deskops add task`: one with `depends_on: [task-nope]` (bare id), one with `depends_on: [TaskDoc:task-nope]` (`Model:name`).
4. Inspect sldb's edge index for both tasks (find the index artifacts under the created `.sldb` store; run any `sldb` inspection command that reveals declared/resolved edges); capture commands and raw output.
5. Write `runs/planning/sldb-request-unresolved-references.md` with sections `## Reproduction` (commands + output), `## Proposed API`, `## deskops caller`, `## Response` (empty placeholder until coordinator replies).
6. Under `## Proposed API` write: (a) how a declared reference field resolves bare ids (e.g. per-field allowed-model list, as `__containment__` has); (b) `sldb.api.edges.unresolved_references(store) -> list[{source, field, target}]`.
7. Under `## deskops caller` state that `deskops graph missing` is the caller.
8. Stop; hand the file to the coordinator via the supervisor (supervisor pastes it, supervisor pastes the reply).
9. After the reply arrives, paste it under `## Response`.
10. Run validation: `test -f` and the four `grep -q` checks on the four headings.

AMBIGUITIES:
1. Executor is told to stop after writing the reproduction/proposal, but Done When requires `## Response` to hold the coordinator reply; unclear whether the executor resumes to paste the reply or the supervisor does.
2. Task `status: deferred`, yet Resolved Decisions say the supervisor promotes it to `desk/tasks/` before dispatch; unclear whether the executor runs against a drawer or promoted path.
3. How to set `depends_on` values via `deskops add task` (flags/syntax) is not specified.
4. Which sldb command(s) or files constitute "inspect sldb's edge index" is not specified; no expected inspection output given.
5. No acceptance criteria for the reproduction's content (e.g. what output proves the gaps), only heading presence.
6. No template/format defined for a "request" document beyond the four heading names.
7. `deskops init .` behavior/flag correctness is assumed, not verifiable from the doc.
8. Exact string format expected under `## Proposed API`/`## deskops caller` is unspecified beyond the examples.
9. Document language (English vs other) not specified.
10. Whether `pytest tests` must be run by the executor (closeout constraint) is unclear since the executor does not commit.
11. Contradiction risk: `depends_on` lists task IDs `task-rw-f1-*` while drawers/tasks live elsewhere; no path given to confirm they are satisfied.
