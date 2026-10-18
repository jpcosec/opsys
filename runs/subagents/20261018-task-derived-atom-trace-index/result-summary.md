# Result summary: task-derived-atom-trace-index

## What changed

- `deskops/graph/atom_trace.py` (new)
  - `AtomUseSite` frozen dataclass: `source_id`, `role`, `path`, `locator`.
  - `atom_use_sites(root: Path, atom_id: str) -> list[AtomUseSite]`: calls `extract_declared_edges(root)`, keeps edges with `target_id == f"atom:{atom_id.removeprefix('atom:')}"`, returns sites sorted by `(path, locator)`. No atom file reads/writes.
- `tests/test_graph_atom_trace.py` (new)
  - `test_atom_use_sites_reports_document_without_mutating_atom`: doc frontmatter `atoms: [{id: atom-consumer-target, role: documents}]`; asserts `doc:docs/guide.md` / `documents` / `docs/guide.md` / `frontmatter`, plus byte-identical atom file.
  - `test_atom_use_sites_reports_task_source`: task frontmatter `atoms: [atom-consumer-target]`; asserts the task use site is present.
- `docs/knowledge-graph/desk-source-graph-vocabulary.md`
  - Added one paragraph under "Atom Reference Field And Roles": reverse atom traceability is derived from declared edges at read time and is not stored in atoms.

## Validation commands and final result lines

- `PYTHONPATH=/tmp/rw/wt/atomtrace python -m pytest tests/test_graph_atom_trace.py -q` -> `2 passed in 0.12s`
- `PYTHONPATH=/tmp/rw/wt/atomtrace python -m pytest tests/test_graph_extract_edges.py -q` -> `3 passed in 0.13s`
- `PYTHONPATH=/tmp/rw/wt/atomtrace python -m pytest -q` (root, task validation) -> `501 passed, 3 skipped in 764.56s (0:12:44)`
- `PYTHONPATH=/tmp/rw/wt/atomtrace python -m pytest tests -q` (required extra run) -> `501 passed, 3 skipped in 880.17s (0:14:40)`

## Test against unfixed code

Temporarily moved `deskops/graph/atom_trace.py` aside and ran the new test file:

- Result: `ERROR tests/test_graph_atom_trace.py` during collection, `ModuleNotFoundError: No module named 'deskops.graph.atom_trace'` (`1 error in 0.08s`). Module was restored immediately.

## Task issues / ambiguities

- The task text did not cite line numbers that needed re-checking; implementation was based on the current `extract_declared_edges` API.
- Step 5 expected the task use site to report `references`, but `TaskDoc.__references__` already contains `atoms`. Existing extractor behavior therefore emits two edges for the same task atom declaration: role `atoms` (model field pass) and role `references` (canonical atom mapping pass). The test asserts the `references` site exists instead of exact list equality. This duplicate-role behavior is pre-existing and was not changed (out of scope).
- The prompt estimate of ~3 minutes for the full suite was wrong: runs took ~13-15 minutes.
- No sldb bug observed during this task.
