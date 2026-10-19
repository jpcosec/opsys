---
# ritual-xxx
id: ritual-knowledge-distillation-pass
# Ordered prose steps; not document references
steps:
- Capture the raw context and name the distillation scope.
- Read existing modeled knowledge through SLDB or deskops instead of relying only
  on raw text search.
- Classify each statement as durable (atom), unresolved (question), or actionable
  (drawer task).
- Create or update one-question atoms for durable answers.
- Track new atoms with `sldb docs track`.
- Refresh the store with `sldb stores update`.
- Replace answered question prose with atom mappings instead of leaving duplicate
  prose in drawer questions.
- Write actionable missing work as deferred drawer tasks.
- Declare relations with `## Related Atoms` or another supported source surface.
- Rebuild the graph with `deskops graph build`.
- Reject dangling references with `deskops graph missing`.
- Query one representative atom with `deskops graph neighbors atom:<id>`.
- Prove store integrity with `sldb stores check --store .sldb`.
- Run focused tests for touched behavior.
- Commit with a descriptive message.
# e.g., layer:workflow, system:sldb
tags:
- system:deskops
- system:sldb
- workspace:desk
- topic:atoms
- topic:knowledge-distillation
- topic:workflow
---

# Knowledge distillation pass

## Purpose

_Explain why this ritual exists._

Convert raw context into integrated desk knowledge: atoms, questions, deferred tasks, graph relations, store state, validation evidence, and a descriptive commit.

## Trigger

_State when this ritual should start._

When a conversation, investigation, drift finding, or unclear workflow area contains enough signal that leaving it in chat or notes would lose durable knowledge.

## Preconditions

_List the conditions that must hold before running the ritual._

- The distillation scope is named.
- Existing atoms, docs, specs, diagrams, tasks, pills, and drawer items have been read through sldb or deskops where possible.

## Validation

_List the checks that prove the ritual was performed correctly._

- Every new atom is a tracked AtomDoc visible through `sldb docs show`.
- `sldb stores check --store .sldb` passes.
- `deskops graph missing` reports no real missing references.
- At least one representative new or updated atom has an incoming relation from the distilled surface.
- Answered questions are not left as open questions.
- Unresolved questions remain in desk/drawer/questions/.
- Actionable work is represented in desk/drawer/tasks/.
- Focused tests pass when code behavior changed.
- A descriptive commit exists before the pass is considered closed.

## Failure Modes

_List common mistakes this ritual prevents._

- Creating Markdown atom files without tracking them in SLDB.
- Using only raw text search when sldb or the graph can answer structurally.
- Leaving obvious answers duplicated as drawer questions after creating atoms.
- Creating graph nodes with no declared relation from any source surface.
- Ignoring `graph missing` because a placeholder or example looks harmless.
- Letting implementation work remain buried inside a question document.
- Closing the pass without a commit.

## Completion

_Describe what completion looks like._

Durable answers live in tracked atoms, unresolved questions and deferred work are routed, the store and graph validate, and one descriptive commit records the pass.
