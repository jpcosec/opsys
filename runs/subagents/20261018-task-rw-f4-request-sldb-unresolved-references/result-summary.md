# Result summary — task-rw-f4-request-sldb-unresolved-references

## Changed

- Added `runs/planning/sldb-request-unresolved-references.md` (new file, 194 lines). No code, desk data, or sldb files changed.
- Document sections:
  - `## What deskops needs` — names the two gaps and the relevant sldb functions.
  - `## Reproduction` — throwaway-repo commands (`git init`, `deskops init .`, two `deskops add task` calls) and four outputs:
    - `sldb edges show TaskDoc:task-bare-id-repro --relation references` → `[]`
    - `sldb edges show TaskDoc:task-qualified-id-repro --relation references` → `[]`
    - `declared_reference_edges(...)` on `["task-nope", "TaskDoc:task-other"]` → only the qualified edge
    - `declared_reference_edges` + `resolve_edges` on `TaskDoc:task-missing` → declared edge present, `kept: []`, `problems: []`
    - shard `grep` showing the qualified `relation: references` edge was in the shard and dropped at compose time.
  - `## Proposed API` — (a) `__reference_models__` per-field map with resolution order (export id, tracked path, single allowed model, else unresolved/ambiguous), note on contract hashing and `EDGE_INDEX_VERSION` bump to 4; (b) `sldb.api.unresolved_references(store, include_linked=True, exclude_tags=()) -> list[UnresolvedReference]` with fields `source`, `model`, `field`, `target`, `target_export_id`, `relation`, `reason`.
  - `## deskops caller` — `deskops.graph.checks.find_missing_graph_references(root, graph_path=None)`, reached from `deskops/cli/main.py:_graph_missing` and `deskops.operations.OperationService._build_atom_from_graph_finding`.
  - `## Response` — placeholder awaiting the coordinator's reply (per task Scope and preflight r7 decision; executor stops before the reply exists).

## Validation

Ran from `/tmp/rw/wt/sldbreq`:

```bash
test -f runs/planning/sldb-request-unresolved-references.md
grep -q '^## Reproduction' runs/planning/sldb-request-unresolved-references.md
grep -q '^## Proposed API' runs/planning/sldb-request-unresolved-references.md
grep -q '^## deskops caller' runs/planning/sldb-request-unresolved-references.md
grep -q '^## Response' runs/planning/sldb-request-unresolved-references.md
```

Final result: `ALL DOC CHECKS PASS` (all five checks exit 0).

```bash
PYTHONPATH=/tmp/rw/wt/sldbreq python -m pytest tests -q
```

Final result: `369 passed, 3 skipped in 325.99s (0:05:25)`.

## Tests against unfixed code

No pytest test was added or run against unfixed code (doc-only task). The reproduction snippets were run against the current, unfixed structuredLanguageDB 0.1.11 and reproduced both gaps exactly (results quoted in the document).

## Discrepancies and ambiguities found

- Cited line numbers drifted slightly: `_ids_in` is at `declared_references.py:67-74` (task says 66-74; 66 is blank) and `resolve_edges` is at `resolve.py:23-34` (task says 20-30; the silent drop is line 32). The document uses the real lines.
- `../sldb` does not exist relative to this worktree. The installed sldb is an editable checkout at `/home/jp/proyectos/SLDB_1/sldb`; the document uses `src/sldb/...` paths without the `../sldb` prefix.
- Deskops reference values are of two kinds, not just "bare ids": bare names (`depends_on`) and repo-relative paths (`pills`, `atoms`, `from_drawer`). Allowed-model lists alone cannot resolve paths, so proposal (a) adds a path-owner rule reusing `composition_targets._owners_by_path`. This was implicit in the task's "pill paths".
- `__containment__` already carries allowed models, but `_ids_in` ignores them, so containment bare ids are also dropped. The document states this.
- `sldb.api.edges` is a package that does not re-export API functions (noted in the prior sldb reply); therefore the proposal names `sldb.api.unresolved_references`, not `sldb.api.edges.unresolved_references`.
- Done When cannot be satisfied by the executor: `## Response` must hold the coordinator's reply, which arrives only after the supervisor delivers the file. Left as an explicit placeholder.
- No sldb bug found beyond the two requested gaps. The silent drop is the second gap, not an unreported additional defect.

## Git state

- `git status --short` shows only `?? runs/planning/sldb-request-unresolved-references.md`.
- No commit, no `git add`, no desk-mutating deskops command run in this worktree.
