RESTATEMENT:
1. Create `runs/planning/sldb-request-unresolved-references.md` with section headers `## Reproduction`, `## Proposed API`, `## deskops caller`, `## Response`.
2. Build a throwaway repo under `/tmp`: `git init`, `deskops init .` (creates store, registers deskops models, scaffolds `desk/`).
3. `deskops add task` twice: one with `depends_on: [task-nope]` (bare id), one with `depends_on: [TaskDoc:task-nope]` (qualified id).
4. Inspect sldb's edge index for both tasks; capture exact commands and output.
5. Paste those commands/output under `## Reproduction`.
6. Under `## Proposed API` write: (a) mechanism for a declared reference field to resolve bare ids (e.g. per-field allowed-model list, mirroring `__containment__`); (b) function like `sldb.api.edges.unresolved_references(store) -> list[{source, field, target}]`.
7. Under `## deskops caller` state the deskops function that will call it (`deskops graph missing`).
8. Hand the file to the coordinator (supervisor pastes it); paste the coordinator's reply under `## Response`.
9. Run the five validation greps (`test -f`, `grep -q '^## ...'` for each header).
10. Stop after writing reproduction + proposal; do not write into `../sldb` or its inbox; do not commit (supervisor promotes/commits).

AMBIGUITIES:
1. No path/name specified for the /tmp throwaway repo.
2. Inspection method for sldb's edge index is unspecified (which CLI/Python API, which store path).
3. `deskops add task` invocation form for supplying `depends_on` is unspecified (flags vs. body content).
4. No format spec for `## Reproduction` (code fences, prose, exact transcript shape).
5. "Proposed API" detail level unspecified — whether one recommendation, options, or exact signatures are required.
6. `## Response` must exist for the grep to pass, but it is unknown whether an empty placeholder is acceptable pre-reply.
7. Done When depends on an external coordinator reply that the executor cannot produce or verify.
8. `runs/planning/` may be gitignored; whether the file must be tracked is unstated.
9. Whether `depends_on` tasks (`task-rw-f1-*`) must be closed before this executes is unstated; task is `status: deferred`.
10. Cited sldb line numbers (`declared_references.py:66-74`, `resolve.py:20-30`) may be stale; no requirement to re-verify them.
11. Tension: bound pill `pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md` implies inbox delivery, but Scope says writing into sldb's inbox is out of scope; resolution depends on the supervisor-mediated paste.
