---
id: task-lifecycle-graph-checks-rituals-are-readable
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-doctor-separates-desk-repair-from-sldb-health.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/lifecycle.py
- tests/test_lifecycle_graph.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- topic:lifecycle
- topic:migration
---

# The lifecycle graph tracks a ritual only if RitualDoc can read it

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 through spec2viz-49 (2026-10-17) after migrating the graph_ui desk with `deskops desk update --apply`. `ensure_lifecycle_graph` (deskops/lifecycle.py:221-235) tracks desk/rituals/{execution,testing,closeout}.md as RitualDoc as they are, without checking that the model can read them. A desk whose rituals predate the current RitualDoc template (graph_ui's had no `## Step Details`) ends up with the rituals tracked but unreadable, and `deskops doctor` reports "model cannot read its own content". The workaround was `deskops edit ritual <file> completion ...` followed by another `--apply`. spec2viz's rituals were readable and migrated cleanly in a copy, so the gap only shows on desks with older ritual files.

## Goal

_Describe the concrete result this task must produce._

`ensure_lifecycle_graph`, and therefore `deskops init` and `deskops desk update --apply`, never leaves a lifecycle ritual tracked when RitualDoc cannot round-trip its file. It either stops with `LifecycleGraphMissing` naming the file and the missing sections, before tracking anything, or re-renders the ritual through the model.

## Scope

_State what is in scope and what is out of scope._

In scope: the ritual loop in `ensure_lifecycle_graph` and one test with an old-style ritual. Out of scope: doctor's readability check, and the other lifecycle documents (RelationTypeDoc, RelationDoc), which deskops writes itself.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. In the ritual loop of `ensure_lifecycle_graph`, before `_track`, check the round trip (`render_model_markdown(RitualDoc, extract_model_data(RitualDoc, text))` re-extracts the same data). If it fails, re-render the file from what RitualDoc extracts, filling missing sections with the template's placeholders, and check again; if it still fails, raise `LifecycleGraphMissing`.
2. Test in tests/test_lifecycle_graph.py: a desk whose execution ritual lacks `## Step Details` migrates with a readable ritual and a clean `deskops doctor`.

## Validation

_List the checks required before this task can close._

- pytest tests/test_lifecycle_graph.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

A desk whose execution ritual has no `## Step Details` either fails `desk update --apply` with a message naming the file, with no ritual tracked, or is migrated with a readable ritual. `deskops doctor` is clean afterwards.

## Resolved Decisions
- Owner decision (2026-10-18, delegated to the SLDB_1 coordinator): re-render. `ensure_lifecycle_graph` re-renders a ritual RitualDoc cannot read to the current template (keeping the content RitualDoc can extract) before tracking it; if the re-rendered file still does not round-trip, it raises `LifecycleGraphMissing` naming the file and tracks nothing.

## Open Ambiguities

None.
