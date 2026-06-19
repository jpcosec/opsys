# Self Reflection Graph Questions

This document is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-kgdb-owns-relations-between-knowledge-surfaces.md`
- `desk/atoms/knowledge-model/atom-self-reflection-is-a-feedback-loop.md`
- `desk/atoms/knowledge-model/atom-networkx-is-first-graph-runtime.md`

ID: self-reflection-graph-questions

## Purpose

This document defines the first graph-backed self-reflection questions for deskops. The questions are read-only contracts for future reflection routines: they describe what to ask, what graph pattern to inspect, what shape a finding should have, and when later automation may propose a write.

Self-reflection must not create atoms, issues, or inbox notes directly from weak inference. A finding is reviewable evidence first. Later automation may write only when the finding is deduplicated, provenance-backed, and meets the confidence requirement stated for the question.

## Shared Finding Shape

Each future finding should be serializable as a small record with these fields:

| Field | Meaning |
|---|---|
| `question_id` | Stable id of the question that produced the finding. |
| `kind` | Controlled finding kind for grouping and dedupe. |
| `source_id` | Graph node carrying the evidence, when one node owns the claim. |
| `target_id` | Missing, dangling, or expected graph node id, when applicable. |
| `role` | Edge role involved in the question, when applicable. |
| `provenance_path` | Repository-relative file path where evidence was found. |
| `provenance_locator` | Section, line, field, edge id, or rule locator for the evidence. |
| `confidence` | `high`, `medium`, or `low` confidence in the finding. |
| `reason` | Short human-readable explanation. |
| `later_action` | One of `none`, `atom_candidate`, `issue_candidate`, or `routed_inbox_note_candidate`. |
| `dedupe_key` | Stable key used to avoid duplicate generated work. |

## Questions

### Q1. Which declared atom references point to atoms that do not exist?

ID: `missing-atom-references`

This asks whether a document, task, issue, spec, diagram, or validation surface declares an atom reference that cannot be resolved to an extracted `atom` node.

Graph pattern:

```text
(source)-[role in {references, documents, specifies, constrains, validates}]->(target)
where target.id starts with "atom:"
and target.id is absent from graph nodes
```

Also include declared targets reported by the existing missing check as `dangling_source_atom_reference` when `target_id` starts with `atom:`.

Expected finding shape:

```yaml
question_id: missing-atom-references
kind: dangling_source_atom_reference
source_id: <referencing node id>
target_id: atom:<missing-atom-id>
role: <declared atom-reference role, if known>
provenance_path: <path containing the atom reference>
provenance_locator: <field, section, or line locator>
confidence: high
reason: declared atom reference target was not found among graph nodes
later_action: atom_candidate
dedupe_key: missing-atom-references:<source_id>:<target_id>:<role>
```

Confidence requirement:

- `high` only when the source explicitly declares the atom id through modeled metadata, a recognized atom-reference section, or a snapshot edge with provenance.
- `medium` when a content scan recognizes an atom-shaped id but the role or source surface is inferred.
- `low` findings must stay review-only and must not produce atom candidates.

Later automation may create:

- Atom candidate: yes, only for `high` confidence findings after dedupe and review of nearby text for a durable one-question knowledge gap.
- Issue candidate: yes, if the missing atom blocks validation or closeout and the right atom content is unclear.
- Routed inbox note candidate: yes, if the missing reference depends on another repo or on missing SLDB/KGDB capability.

### Q2. Which source files are unlinked from desk knowledge surfaces?

ID: `unlinked-source-files`

This asks whether implementation source files exist as `source_file` nodes but have no graph relationship to atoms, tasks, issues, specs, docs, commands, primitives, tests, or configuration surfaces.

Graph pattern:

```text
(source_file {kind: "source_file"})
where source_file has no incident edges with role in {
  references, documents, specifies, constrains, supports, uses,
  materializes, implements, validates, tests, violates, invokes,
  defines, routes, configures
}
```

The first implementation should treat this as a coverage question over extracted nodes, not as proof that the file lacks meaning. Generated, vendored, migration, cache, and tool-output paths should be excluded before reporting.

Expected finding shape:

```yaml
question_id: unlinked-source-files
kind: unlinked_source_file
source_id: source_file:<path>
target_id: null
role: null
provenance_path: <source file path>
provenance_locator: node:<source file id>
confidence: medium
reason: source file has no graph edge connecting it to a desk knowledge surface
later_action: issue_candidate
dedupe_key: unlinked-source-files:<source_id>
```

Confidence requirement:

- `medium` is the default maximum because absence of edges may reflect extractor limits rather than a true knowledge gap.
- `high` requires a complete graph snapshot for the relevant extractors and an explicit inclusion rule saying the path should be modeled.
- `low` applies when the file path is likely generated, transitional, or outside the current source-file extraction boundary.

Later automation may create:

- Atom candidate: no, not directly. A disconnected file is not durable knowledge by itself.
- Issue candidate: yes, when `high` or repeated `medium` findings show a source area lacks traceability.
- Routed inbox note candidate: yes, when the missing link is caused by a missing KGDB/SLDB extractor or graph capability owned outside deskops.

### Q3. Which generated artifacts have no live source or no source edge?

ID: `dangling-generated-artifacts`

This asks whether generated or rendered artifacts remain in the graph without a live source relation, or whether their declared generator/source target is absent.

Graph pattern:

```text
(artifact)-[generated_from|renders|materializes|source_for]-(source)
where artifact.kind in {doc, diagram, spec, config_file}
and artifact is known or declared to be generated
and (
  source is absent from graph nodes
  or artifact has no generated_from/materializes/renders edge
  or source_for points to an artifact path that no longer exists
)
```

Until generated-artifact metadata is formalized, this question should rely only on explicit generated-file metadata, materializer output metadata, build manifests, diagram source declarations, or graph snapshot edges. Path convention alone is insufficient for a high-confidence finding.

Expected finding shape:

```yaml
question_id: dangling-generated-artifacts
kind: dangling_generated_artifact
source_id: <generated artifact node id>
target_id: <missing source/generator node id, if known>
role: generated_from|renders|materializes|source_for
provenance_path: <artifact path or manifest path>
provenance_locator: <metadata field, manifest row, or edge locator>
confidence: <high|medium|low>
reason: generated artifact has no live source relation or points to a missing source
later_action: issue_candidate
dedupe_key: dangling-generated-artifacts:<source_id>:<target_id>:<role>
```

Confidence requirement:

- `high` requires declared generated-artifact metadata or a graph edge with provenance whose source or target node is missing.
- `medium` may come from a documented diagram source declaration or materializer manifest that names both sides but lacks full graph coverage.
- `low` path-pair or filename-convention matches are review-only and must not create issues or atoms.

Later automation may create:

- Atom candidate: no, unless human review determines the finding exposes a reusable materialization rule not already captured as an atom.
- Issue candidate: yes, for `high` confidence stale generated artifacts or missing source/generator links.
- Routed inbox note candidate: yes, when the missing source relation belongs to another tool such as a diagram renderer, KGDB snapshot writer, or SLDB materializer.

### Q4. Which open issues have no related atom?

ID: `open-issues-without-related-atoms`

This asks whether an open issue is routed but not connected to any atom that explains the durable concept, guardrail, policy, or unresolved question behind it.

Graph pattern:

```text
(issue {kind: "issue", status: "open"})
where no outgoing edge exists from issue to atom with role in {
  references, documents, specifies, constrains, validates, supports
}
and no declared Related Atoms section resolves to an atom node
```

If issue status is not a graph property yet, the first implementation may read the issue document's `Status` section or explicit metadata as provenance. Closed or resolved issues should be excluded.

Expected finding shape:

```yaml
question_id: open-issues-without-related-atoms
kind: open_issue_without_related_atom
source_id: issue:<issue-id>
target_id: null
role: references
provenance_path: <issue path>
provenance_locator: status:<locator>;related-atoms:<locator-or-missing>
confidence: <high|medium>
reason: open issue has no resolved related atom edge
later_action: routed_inbox_note_candidate
dedupe_key: open-issues-without-related-atoms:<source_id>
```

Confidence requirement:

- `high` requires an explicit open status and either a missing `Related Atoms` section or an empty section after declared references are extracted.
- `medium` applies when open status is inferred from drawer location but the issue has no resolved atom edge.
- `low` findings should be suppressed because issue routing without atom linkage can be intentional during intake.

Later automation may create:

- Atom candidate: yes, only after review confirms the issue contains durable, reusable knowledge and no existing atom covers it.
- Issue candidate: no. The issue already exists; opening another issue would be duplicate noise.
- Routed inbox note candidate: yes, when the issue lacks enough information to pick or create an atom and needs owner review.

## Noise Control Rules

- Do not write atoms from `low` confidence findings.
- Do not open duplicate issues for the same `dedupe_key`.
- Prefer a reviewable finding over an atom or issue when absence may be caused by extractor coverage.
- Route cross-tool capability gaps to the owning repo inbox instead of creating deskops-specific workarounds.
- Use declared graph evidence before inferred path or filename evidence.
- Treat these questions as self-reflection inputs only; they do not close tasks, prove implementation coverage, or mutate source artifacts.

## Related Context

- `docs/knowledge-graph/desk-source-graph-vocabulary.md`
- `desk/drawer/issues/issue-define-self-reflection-loop.md`
- `desk/contexts/pill-011-self-reflection-noise-control.md`
