RESTATEMENT:

1. Confirm dependency artifacts exist/are readable: `runs/planning/deskops-rewrite-inventory.md` (phase F4), pills `desk/contexts/pill-008-kgdb-sldb-boundary.md` and `desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md`, plus the three `task-rw-f1-*` tasks.
2. Read the cited sldb sources to confirm the gaps: `../sldb/src/sldb/store/edge_index/declared_references.py:66-74` (`_ids_in` keeps only `Model:name`) and `../sldb/src/sldb/store/edge_index/resolve.py:20-30` (`resolve_edges` silently drops untracked-target schema edges).
3. Create a throwaway store under /tmp (e.g. `mktemp -d`), copy a minimal desk into it, and run `sldb stores init` there. Never touch `../sldb` or its desk.
4. In that throwaway store, track a TaskDoc with `depends_on: [task-nope]` and a TaskDoc with `depends_on: [TaskDoc:task-nope]`.
5. Run the sldb commands that build the edge index / edges; capture exact command lines and output showing: bare id yields no edge, and `TaskDoc:task-nope` yields an edge dropped by `resolve_edges` with no report.
6. Create `runs/planning/sldb-request-unresolved-references.md` with headings `## Reproduction`, `## Proposed API`, `## deskops caller`, `## Response`.
7. Under `## Reproduction`, paste the commands and raw output from step 5.
8. Under `## Proposed API`, write (a) how a declared-reference field can resolve bare ids (e.g. a per-field allowed-model list as `__containment__` has) and (b) a function such as `sldb.api.edges.unresolved_references(store) -> list[{source, field, target}]`.
9. Under `## deskops caller`, state that `deskops graph missing` will call it.
10. Hand the file to the coordinator and paste the coordinator's reply under `## Response`.
11. Run the four validation commands: `test -f` the file; `grep -q '^## Reproduction'`; `grep -q '^## Proposed API'`; `grep -q '^## Response'`.
12. Do not commit; supervisor reviews the diff and runs the closeout commit.

AMBIGUITIES:

1. `status: deferred` and three `depends_on` tasks — no way to verify from the document whether those dependencies are complete or whether this task is actually cleared to execute.
2. "copy a minimal desk" — undefined: which files, source path, and required TaskDoc fields/model registration are not specified.
3. No expected/acceptance output for the reproduction; "show the gaps" has no concrete observable criteria beyond prose.
4. `## deskops caller` is required by the Implementation Path but not covered by any validation grep, so compliance is unverifiable.
5. Delivery mechanism to "hand the file to the coordinator" is unspecified; obtaining and pasting the reply is an external blocking dependency an isolated executor cannot satisfy.
6. Contradiction risk: scope says the coordinator routes/handles the request, yet the Implementation Path assigns the executor to hand off and paste the reply.
7. `## Proposed API` location/signature (`sldb.api.edges.unresolved_references`) is phrased as "such as" — exact target module and full signature are unspecified.
8. Whether `runs/planning/sldb-request-unresolved-references.md` already exists / should be overwritten is not stated.
9. Line-number citations (`declared_references.py:66-74`, `resolve.py:20-30`) may be stale; no rule given if they don't match.
10. No template/format required for `## Response` content — any text passes the grep.
