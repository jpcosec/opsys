# Questions Drawer

This guide is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-unwritten-knowledge-belongs-in-atoms-or-materializations.md`
- `desk/atoms/workflow-model/atom-atom-candidates-come-from-durable-answers.md`
- `desk/atoms/workflow-model/atom-drawer-is-not-active-work.md`

`desk/drawer/questions/` holds unresolved workflow questions that are not active tasks yet.

Use this drawer when a concept, connection, flow, diagram, or 5WH1+ answer is unclear enough that promoting it directly into an atom, task, spec, ritual, or implementation would create drift.

## Purpose

- Capture all questions discovered while reconstructing the deskops workflow manual.
- Preserve questions before they become tasks, atoms, diagrams, specs, or docs.
- Use 5WH1+ to expose missing definitions, missing flow boundaries, and missing query surfaces.
- Identify which existing diagrams already answer a question and which diagrams are missing.

## Files

- `workflow-questions.md` - open questions grouped by surface and 5WH1+.
- `workflow-question-map.md` - diagram of the currently suspected connections and unresolved edges.

## Promotion Rule

A question leaves this drawer only when it is promoted into one of these surfaces:

- an atom, when the answer is durable one-question knowledge
- a doc/spec/diagram update, when the answer explains or formalizes a larger surface
- a task, when the answer requires implementation or migration work
- a ritual/routine/hook, when the answer changes operational process
- an inbox note, when the answer depends on another repo or tool owner

Do not delete a question just because it feels obvious after discussion. Delete or archive it only after the answer is represented in a durable surface or intentionally rejected.
