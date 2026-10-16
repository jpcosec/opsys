RESTATEMENT:
1. Read `runs/planning/deskops-rewrite-inventory.md` (phase F4) and the two bound pills (`desk/contexts/pill-008-kgdb-sldb-boundary.md`, `desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md`) for boundary wording to reuse.
2. Create `runs/planning/sldb-request-unresolved-references.md` with heading sections `## Reproduction`, `## Proposed API`, `## deskops caller`, `## Response`.
3. Build the throwaway repro repo: `mkdir /tmp/<dir> && cd /tmp/<dir> && git init`.
4. Run `deskops init .` there (creates store, registers deskops models, scaffolds `desk/`).
5. Run `deskops add task` twice: task A with `depends_on: [task-nope]` (bare id), task B with `depends_on: [TaskDoc:task-nope]` (qualified id).
6. Inspect sldb's edge index for both entries; capture that A emits no edge (`_ids_in` at `../sldb/src/sldb/store/edge_index/declared_references.py:66-74` keeps only `Model:name`) and that `resolve_edges` (`../sldb/src/sldb/store/edge_index/resolve.py:20-30`) silently drops unresolved schema edges.
7. Paste exact commands and verbatim output under `## Reproduction`.
8. Under `## Proposed API`, write proposal (a): per-field allowed-model list on declared reference fields so bare ids resolve (analogous to `__containment__`), and proposal (b): `sldb.api.edges.unresolved_references(store) -> list[{source, field, target}]`.
9. Under `## deskops caller`, name the deskops function behind `deskops graph missing` that would consume the new API.
10. Leave `## Response` present; stop after writing the file. Supervisor pastes the file to the coordinator and pastes the coordinator's reply into `## Response`.
11. Do not write into `../sldb`, its desk, or its inbox; do not commit (supervisor promotes and closeout-commits).
12. Verify: `test -f runs/planning/sldb-request-unresolved-references.md` and the four `grep -q '^## …'` checks.

AMBIGUITIES:
1. Task `status: deferred` with three `depends_on` entries; nothing states whether those tasks are complete or whether promotion to `desk/tasks/` has already happened.
2. `deskops add task` syntax/flags are not given, including how to set `depends_on` (flag vs. edit after creation) and the `TaskDoc:` qualification syntax.
3. Edge-index inspection method unspecified: no path, format (file/DB/CLI), or sldb command for "inspect sldb's edge index".
4. No required fidelity for `## Reproduction` output (how much verbatim output, which commands verbatim).
5. Proposal (a) has no required naming/signature for the per-field allowed-model list; only "for example".
6. Proposal (b) uses "such as", so the module path `sldb.api.edges` and exact return type are not fixed acceptance criteria.
7. `## deskops caller` requires "which deskops function", but no function name is given; can only be looked up in `deskops` code without a stated location.
8. Done When requires the coordinator's reply with accepted/changed/rejected per gap, but the executor must stop before the reply exists — the executor cannot verify its own completion condition.
9. Delivery mechanics ("supervisor pastes the file to the coordinator") have no specified channel or confirmation artifact.
10. `runs/planning/` and the referenced inventory file are not confirmed to exist.
11. No criteria for what makes the reproduction "correct" (e.g., must demonstrate zero edges emitted, must show the dropped `resolve_edges` target).
