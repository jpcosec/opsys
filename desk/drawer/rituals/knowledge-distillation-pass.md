# Knowledge Distillation Pass

ID: ritual-knowledge-distillation-pass
Status: deferred

## Purpose

Convert raw context into integrated deskops knowledge: atoms, deferred questions, deferred tasks, graph relations, SLDB indexes, KGDB query state, validation evidence, and a descriptive commit.

Use this ritual when a conversation, investigation, drift finding, missing manual, or unclear workflow area contains enough signal that leaving it in chat history would lose project knowledge.

## Inputs

- conversation context
- existing docs, atoms, specs, diagrams, tasks, pills, inbox notes, and drawer items
- code or CLI behavior observed during investigation
- SLDB query results
- KGDB graph results
- test results
- unresolved user questions

## Outputs

- stable answers moved into `desk/atoms/` as `AtomDoc` documents
- unresolved questions kept in `desk/drawer/questions/`
- implementation work kept in `desk/drawer/tasks/`
- source surfaces declaring `## Related Atoms` or another supported relation surface
- SLDB store updated and valid
- KGDB graph rebuilt and queryable
- tests or validation evidence recorded in the closeout note or commit context
- descriptive git commit

## Deskops Tools Used

- `python -m deskops show atom <atom-id>` to verify nested atoms through the deskops artifact layer.
- `python -m deskops graph build --root .` to rebuild the deskops KGDB snapshot and runtime graph.
- `python -m deskops graph missing --root .` to reject dangling declared references before closeout.
- `python -m deskops graph neighbors <node-id> --root .` to verify that questions, docs, diagrams, or other surfaces point to relevant atoms.
- `desk/drawer/questions/` to hold unresolved questions that are not active work.
- `desk/drawer/tasks/` to hold deferred implementation work discovered during distillation.
- `desk/atoms/` to hold durable one-question answers.

## SLDB Tools Used

- `sldb docs track <path> --model AtomDoc --store .sldb` to make new atom files real tracked `AtomDoc` documents.
- `sldb docs show <atom-id> --store .sldb --pythonpath .` to inspect payload, semantic tags, sections, and parsed fields.
- `sldb docs list --store .sldb` to verify which atoms are tracked.
- `sldb find <query> --in semantic --store .sldb --pythonpath .` to discover atoms and semantic surfaces by modeled tags.
- `sldb stores update --store .sldb --pythonpath .` to refresh semantic indexes, section indexes, and hashes after adding modeled documents.
- `sldb stores check --store .sldb --pythonpath .` to prove the local store is coherent before closeout.

## KGDB Tools Used

- KGDB runtime output written by `deskops graph build` under `.sldb/runtime/knowledge_graph.kg.json` and `.sldb/runtime/knowledge_graph.nx.json`.
- KGDB node identity conventions such as `atom:<id>` and `question:<path>` through the deskops graph vocabulary.
- KGDB edge queries exposed by `deskops graph neighbors` to verify relation direction and provenance at the deskops level.

## Routine Steps

1. Capture the raw context and name the distillation scope.
1. Read existing modeled knowledge through SLDB or deskops where possible instead of relying only on raw text search.
1. Ask what statements are stable enough to become atoms.
1. Ask what remains unresolved and should stay in `desk/drawer/questions/`.
1. Ask what requires implementation and should become deferred work in `desk/drawer/tasks/`.
1. Create or update one-question atoms for durable answers.
1. Track new atoms with `sldb docs track`.
1. Refresh SLDB with `sldb stores update`.
1. Replace answered question text with atom mappings instead of leaving duplicate prose in drawer questions.
1. Keep unresolved questions grouped by decision area.
1. Write actionable missing work as deferred drawer tasks.
1. Add supported relation declarations such as `## Related Atoms` on question maps, docs, diagrams, or other source surfaces.
1. Rebuild the graph with `python -m deskops graph build --root .`.
1. Check for graph dangling references with `python -m deskops graph missing --root .`.
1. Query at least one representative atom with `python -m deskops graph neighbors atom:<id> --root .`.
1. Check SLDB integrity with `sldb stores check --store .sldb --pythonpath .`.
1. Run focused tests for touched behavior.
1. Commit with a descriptive message.

## Validation Gates

- Every new atom is a tracked `AtomDoc` visible through `sldb docs show`.
- `sldb stores check --store .sldb --pythonpath .` passes.
- `python -m deskops graph missing --root .` reports no real missing references.
- At least one representative new or updated atom has an incoming relation from the distilled surface.
- Answered questions are not left as open questions.
- Unresolved questions remain in drawer questions.
- Actionable work is represented in drawer tasks.
- Focused tests pass when code behavior changed.
- A descriptive commit exists before the routine is considered closed.

## Failure Modes

- Creating Markdown atom files without tracking them in SLDB.
- Using only raw text search when SLDB or KGDB can answer the query structurally.
- Leaving obvious answers duplicated as drawer questions after creating atoms.
- Creating graph nodes with no declared relation from any source surface.
- Ignoring `graph missing` because a placeholder or example looks harmless.
- Letting implementation work remain buried inside a question document.
- Closing the routine without a commit.

## Promotion Rule

This ritual is deferred until it is converted into an active `desk/rituals/` document or decomposed into routines, hooks, and gates. The first implementation task should preserve the validation gates above.

## Tags

- system:deskops
- system:sldb
- system:kgdb
- workspace:drawer
- topic:atoms
- topic:knowledge-distillation
- topic:workflow
