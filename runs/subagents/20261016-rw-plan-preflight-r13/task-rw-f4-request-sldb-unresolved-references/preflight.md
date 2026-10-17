RESTATEMENT:
1. Locate repo root `/home/jp/proyectos/SLDB_1/deskops`; confirm task deps/pills exist locally.
2. Create throwaway dir under `/tmp` via `mktemp -d`; `cd` there; `git init`.
3. Run `deskops init .` in throwaway dir; confirm it creates the store, registers deskops models, scaffolds `desk/`.
4. Run `deskops add task` twice using the CLI syntax needed to set `depends_on`; task A gets `depends_on: [task-nope]`, task B gets `depends_on: [TaskDoc:task-nope]`.
5. Inspect sldb’s edge index for both tasks using whatever sldb CLI/API is installed; capture exact commands and raw output showing bare id emits no edge and `Model:name` emits an edge.
6. Create `runs/planning/sldb-request-unresolved-references.md`.
7. Write `## Reproduction` with the exact `/tmp` repo commands and observed output, including the `_ids_in` / `resolve_edges` gap references from `../sldb/src/sldb/store/edge_index/declared_references.py:66-74` and `../sldb/src/sldb/store/edge_index/resolve.py:20-30`.
8. Write `## Proposed API`: (a) a per-field allowed-model list for declared reference fields so bare ids resolve, analogous to `__containment__`; (b) `sldb.api.edges.unresolved_references(store) -> list[{source, field, target}]`.
9. Write `## deskops caller` identifying the specific deskops function behind `deskops graph missing` that will call the new API.
10. Stop after reproduction and proposal; hand the file to the supervisor for paste to the coordinator.
11. Ensure `## Response` exists/will exist per validation; supervisor pastes coordinator’s per-gap verdict there.
12. Run validation: `test -f runs/planning/sldb-request-unresolved-references.md`, plus greps for `^## Reproduction`, `^## Proposed API`, `^## deskops caller`, `^## Response`.
13. Run `pytest tests` per Resolved Decisions; do not commit; supervisor reviews diff and runs `deskops closeout commit --task task-rw-f4-request-sldb-unresolved-references --run-dir <dir>` or `--no-run --reason <why>`.

AMBIGUITIES:
1. No exact `/tmp` subdirectory name or cleanup policy.
2. No exact `deskops add task` syntax or required flags for `depends_on`, title, id, status.
3. No exact command/API for inspecting sldb’s edge index; store path and output format unknown.
4. Dependency tasks `task-rw-f1-model-contract-snapshot`, `task-rw-f1-cli-contract-tests`, `task-rw-f1-output-golden-files` are not included; completion state and required commit unknown.
5. Pills are listed in frontmatter but not provided; required pill readings undetermined.
6. Task status is `deferred`; whether supervisor promotion to `desk/tasks/` has already happened is not stated.
7. `deskops graph missing` caller function is not named; must be discovered by code search.
8. Proposed API (a) has no exact model-contract syntax, field name, or registration change specified.
9. Proposed API (b) `list[{source, field, target}]` does not define whether entries are dicts, tuples, or objects.
10. `source`, `field`, and `target` semantics are undefined.
11. Whether executor should create an empty `## Response` header for the grep, or leave it absent until supervisor paste, is unclear.
12. Done When requires coordinator reply content, which executor cannot produce; task says executor stops after reproduction/proposal.
13. Whether `deskops` and `sldb` are installed and use local sibling `../sldb` source in the throwaway repo is unspecified.
14. Model name `TaskDoc` is asserted but not verifiable from the task alone.
15. Validation uses relative paths; required working directory for running the checks is implicit.
