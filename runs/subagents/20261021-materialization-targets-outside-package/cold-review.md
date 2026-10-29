# Cold ambiguity review: task-declared-materialization-targets-resolve-outside-the-indexed-package

Scope: I read the task, its 7 bound pills (all exist), its 3 referenced atoms (all exist), and the code it names. I also ran a real sandbox repro in /tmp and then deleted it. I made no edits except this file. `plan.md` and `progress.md` do not exist in the repo.

## Review

### Correct (verified)
- **The root cause is real.** I ran `deskops init`, `add atom`, then `add materialization --target-identity src/vsm/links.py --intent i` in a fresh git repo. `graph missing` then reported `missing_declared_target: materialization:materialization-m -> src/vsm/links.py` and exited 1. `_is_source_path` (extract_sources.py:136) only accepts `desk/` and `deskops/`.
- **The tracking gap is real.** After `add materialization`, `sldb stores check --format json` listed `MaterializationContractDoc` with `documents: []`, while the atom was tracked. `_track_created_artifact` (operations.py:1234) only allows atom and pill.
- **Closeout and snapshot need no change.** `build_closeout_graph_context` (closeout_gates.py:104-122), `snapshot.build_graph_snapshot` (snapshot.py:133) and `extract_declared_edges` (extract_edges.py:76) all call `extract_source_file_nodes`. A new node flows to all of them.
- **`_target_id_for` resolves new nodes without changes.** It uses `nodes_by_path`, so an existing target becomes `source_file:<path>`. A nonexistent `src/...` target falls through `_missing_target_id` (extract_edges.py:682-697) to the bare path and is still reported. "No change to `_missing_target_id`" holds.
- **self_reflection will not flag the new nodes as noise.** Materialization `target_identity` edges use `DEFAULT_ROLE = "references"` (atom_references.py:20), which is in `SOURCE_LINK_ROLES` (self_reflection.py:21). Every new `source_file` node has that inbound edge, by construction, so `_unlinked_source_file_findings` treats it as linked.
- **Existing exact-node-set tests are not affected.** The exact-set test (tests/test_graph_extract_sources.py:22) has no `desk/materializations/`. test_graph_snapshot asserts `>= 3`. The 5 real materializations target `desk/tasks/Board.md`, `tests/*.py` and `deskops/operations.py`, which path rules or doc rules already cover. So the real repo graph does not change.

### Blocker
- **B1. The store assertion in the Implementation Path names a file a fresh store does not have** (task.md, "appears under MaterializationContractDoc in .sldb/store.yaml"). A fresh `deskops init` creates `.sldb/core/{documents,models,store_index.yaml}` and **no `store.yaml`**. Only this repo's older store has one, with an explicit `paths:` list (.sldb/store.yaml:178). An executor following the text will write an assertion that can never pass. Make the alternative the required check: `sldb stores check --store .sldb --format json` lists the document under `MaterializationContractDoc.documents`, or `.sldb/core/documents/MaterializationContractDoc/<id>.yaml` exists.

### Ambiguities (the executor would have to guess)
- **A1. How to decide "already a doc node path" (Medium; affects correctness and performance).**
  - Calling `extract_doc_nodes` from `extract_source_file_nodes` reads metadata for every desk doc. The closeout path already calls `extract_source_file_nodes` twice and `extract_doc_nodes` twice (closeout_gates.py:109-112 plus extract_edges.py:75-76), so this would double that cost.
  - Copying the glob rules by hand will drift.
  - Recommend saying: use the path-only `extract_docs._iter_doc_paths(root)` (no metadata reads), or a shared path predicate.
  - The rule must stay. Without it, `nodes_by_path` (extract_edges.py:77) lets the source node silently override the doc node for paths like `docs/guide.md`.
- **A2. What counts as a "plain repo-relative path"** (Medium; also a missing guardrail).
  - Unspecified: a leading `./` (which `_target_id_for` strips), absolute paths, and `..` segments.
  - Unspecified: symlinks resolving outside the root, and directories.
  - `(root / "../x").exists()` can be true and produce a `../x` node id.
  - Specify: strip `./`, reject absolute or `..`, require `resolve()` to stay under the root, require `is_file()`.
- **A3. `kind:id` targets** (Low–Medium). `source_file:src/x.py` or `config_file:.github/workflows/ci.yml` will still be missing, because `_target_id_for` returns any `:` value unchanged and the helper ignores prefixed values. The task excludes these, but the materialization field description says "Stable target node id **or** path" (models/materialization.py:45). State explicitly that prefixed ids stay out of scope (and are still reported), or also accept `source_file:<existing path>`.
- **A4. Which declaration sites count** (Low). `extract_edges._declarations_from_mapping` (extract_edges.py:569-583) reads `target_identity` and nested `materialization.target_identity` from **any** doc frontmatter and from yaml fences in atoms. The new helper only reads top-level `target_identity` in `desk/materializations/**/*.md`, so out-of-package targets declared elsewhere stay missing. Confirm this is intended, and say whether nested `materialization.target_identity` inside a materialization doc counts.
- **A5. Where to reference the atom** (Low). "Reference it from this task" could mean `references:` or `atoms:` (currently `atoms: []`). Name the field.
- **A6. Frontmatter parsing details** (Low). Say whether to match extract_edges' exact parsing (`startswith("---\n")`, split on `"\n---"`). CRLF and BOM files will otherwise behave differently in the two readers. Also confirm that a non-string `target_identity` is skipped.

### Missing guardrails
- **G1. This task's own closeout coverage is not planned** (Medium).
  - Nothing in desk/atoms or desk/materializations links `deskops/graph/extract_sources.py` (my grep found no hits).
  - The new test file and `tests/test_graph_extract_sources.py` are unlinked too.
  - Only `deskops/operations.py` has a materialization (materialization-closeout-link-policy).
  - `deskops closeout verify` for this task will raise `missing_changed_file_link`.
  - Add a step: create materialization contracts with `deskops add materialization --source-atoms <new atom> --target-identity <file>` for each changed code and test file. Prior tasks did this, e.g. materialization-closeout-atomless-regressions.
- **G2. Silent exclusion** (Low). EXCLUDED_DIRS includes `tools`, `build`, `dist`, `.tmp` and `node_modules`. A Governance target under `tools/` stays `missing_declared_target` with the generic reason. Either accept and document this, or add a test that pins it.
- **G3. No backfill** (Low). 3 of the 5 materializations already in this repo are untracked. Store tracking applies only to new `add materialization` calls. Say whether a doctor or backfill step is out of scope, or route it as follow-up.
- **G4. Run related tests explicitly** (Low).
  - `tests/test_output_goldens.py` creates a materialization, now tracked; make sure its goldens and stdout don't change.
  - `tests/test_materialization_contract.py:107` (a `docs/guide.md` target must stay a `doc:` node) covers the non-duplication rule.
  - Name both in Validation, before the full `pytest` run.

### Likely missed pills (desk/contexts/)
- `pill-011-self-reflection-noise-control.md`. Its When covers "graph missing checks"; this task changes what `graph missing` reports and adds new `source_file` nodes.
- `pill-atom-lifecycle-preserves-provenance-and-materialization-links.md`. Its Where covers "materialization contracts, graph links".
- `pill-008-kgdb-sldb-boundary.md`. Its When covers "emits … graph data involving SLDB documents". This applies weakly: node provenance gains a new `source_kind`.
- Not needed: pill-010, since no runtime output is written.

### Risks / notes
- **R1. Undocumented `source_kind` value** (Low). The new provenance `source_kind: "declared_materialization_target"` is not in the vocabulary doc (docs/knowledge-graph/desk-source-graph-vocabulary.md:149 lists declared, sldb_semantic, path_rule, content_scan, test_name, manual). That list is for edges, but nodes reuse the key. Per AGENTS.md the atom comes first, then the doc can be updated; otherwise record it as follow-up.
- **R2. `source_file` kind for non-code files** (Low). `.github/workflows/*.yml` gets kind `source_file` and file_kind `source`. That is semantically loose, but the task requires it. A materialization with `target_kind: config_file` would have a `target_kind` that does not match the node kind; nothing validates that today.
- **R3. Performance** (Low). Reading `desk/materializations/**/*.md` frontmatter is cheap (5 files here). The real cost risk is A1, if `extract_doc_nodes` is called from inside the extractor.
- **R4. Baseline is not clean** (Info). `deskops graph missing --root .` reports 4 findings right now, all from this task's own body referencing files that don't exist yet (the new test and atom). Done-When should compare against that baseline; the findings resolve once those files exist.
- **R5. Graph contents depend on file existence** (Info). The extraction now depends on whether target files exist on disk. Deleting a target file turns a node back into a `missing_declared_target`. That is the intended behaviour, but tests must create real files.
