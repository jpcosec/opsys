---
record: true
---

# Coverage extractor removed from the graph snapshot

## Kind

decision

## Status

resolved

## Resolution

`deskops/graph/extract_coverage.py` and `tests/test_graph_extract_coverage.py` were deleted, and `build_graph_snapshot` no longer merges coverage nodes or edges. The coverage extractor produced no consumer: no deskops code read the coverage nodes, edges, or scores, and no gate depended on them. Last commit containing the module before deletion: `c378d15641e423ca1cee29da0809eb45a74ddf8a` (`closeout: task-rw-f0-graph-skips-vendored-trees`, 2026-10-17). Recover with `git checkout c378d15641e423ca1cee29da0809eb45a74ddf8a -- deskops/graph/extract_coverage.py tests/test_graph_extract_coverage.py`.

## What the extractor did

- Extracted atom records from `desk/atoms/*.md` (`id`, `title`, `five_wh_one_plus` facets, tags, aliases, provenance path).
- Discovered Mermaid views from Markdown fences and generated HTML sections, parsed `flowchart`/`graph` (component) and `stateDiagram[-v2]` diagrams into diagram, element, and edge nodes.
- Created `facet:what|why|when|who|where|how` nodes and `answers` edges from atoms to facets, `materializes`/`expects_facet`/`covers_facet` edges between diagram elements and atoms, with `confidence`, `score`, `atom_id`, `facet`, `match_basis`, `evidence`, and `source_field` metadata.
- Scored element-to-atom matches with fixed thresholds: 0.70 minimum cutoff; title exact 1.00 / contained 0.90 / overlap 0.75; alias exact 0.95 / contained 0.85 / overlap 0.70; tag exact 0.88 / contained 0.78 / overlap 0.65; semantics-token subset 0.72 / overlap 0.60.
- The tag-overlap (0.65) and token-overlap (0.60) scores were below the 0.70 cutoff and could never win; `confidence` was hard-coded to `high` for every emitted edge.
- In `build_graph_snapshot`, it added six `facet:*` nodes per snapshot, atom/diagram/element nodes for matched views, and coverage edges to `metadata.source_extractors` as `desk_kgdb_coverage_v1`.
- Golden fixture impact: `graph_snapshot.kg.json` went from 13 nodes / 9 edges to 7 nodes / 7 edges; `graph_snapshot.nx.json` dropped the same six facet nodes and two `answers` edges.

## Problem

The extractor added 907 lines of scoring, diagram parsing, and vocabulary that nothing consumed, and its metadata advertised `confidence: high` for every match regardless of score. Removing it reduces the graph snapshot to document, source-file, and declared-reference nodes and edges.

## Evidence

- Deleted: `deskops/graph/extract_coverage.py`, `tests/test_graph_extract_coverage.py`
- Updated: `deskops/graph/__init__.py`, `deskops/graph/snapshot.py`, `tests/test_graph_snapshot.py`, `tests/fixtures/golden/graph_snapshot.kg.json`, `tests/fixtures/golden/graph_snapshot.nx.json`
- Inventory finding S13 in `runs/planning/deskops-rewrite-inventory.md`

## Desired Outcome

Graph snapshots contain only document, source-file, and declared-reference data, and no dead coverage scorer remains in the codebase.

## Questions

- Should atom facets and diagram coverage return later as an explicit report command?
- If coverage returns, which consumer or gate should depend on it?

## Related Atoms

- atom-docs-are-human-facing-atom-materializations
