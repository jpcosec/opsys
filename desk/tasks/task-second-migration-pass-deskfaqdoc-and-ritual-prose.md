---
id: task-second-migration-pass-deskfaqdoc-and-ritual-prose
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- runs/planning/store-migration-20261018-pass2.md
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Second migration pass: DeskFAQDoc and the prose RitualDoc contract reach every federated store

## Rationale

_Explain why this task exists or the business driver behind it._

On 2026-10-18, two deskops model changes moved the contracts that federated stores import. FAQDoc was renamed to DeskFAQDoc in c468749, and RitualDoc steps became prose in e60cdb3. The dry-run shows 35 of the 40 stores with RitualDoc to re-sign. A store that still registers deskops.models:FAQDoc under the name FAQDoc now points at a class that no longer exists. The coordinator asked for this pass as soon as the batch closed.

## Goal

_Describe the concrete result this task must produce._

Every store from the first migration's list has run desk update --apply again. That pass re-signs RitualDoc and moves a legacy FAQDoc entry to DeskFAQDoc. The log records each store's stores check, edges check and edges unresolved result. In sldb, only desk/ and .sldb/ are committed, and sldb-04 gets the hash.

## Scope

_State what is in scope and what is out of scope._

In scope: the 40 stores, with a fresh backup of desk/, knowledge/ and .sldb/, the commit in sldb, and notes to the agents whose repos change. Out of scope: other owners' data problems, which their inbox notes already route.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Back up every repo to /tmp/rw/mig2/backup. 2. Run /tmp/rw/mig/drive.py over the store list. 3. Write the log to runs/planning/store-migration-20261018-pass2.md, so it does not overwrite the first pass. 4. Run the final checks per store. 5. In sldb, run stores update and commit desk/ and .sldb/ with an explicit pathspec. 6. Message sldb-04, spec2viz-49, graph-ui-59, chatbot-95 and mepu-ocs-dev-29 about their changes.

## Validation

_List the checks required before this task can close._

- python -m pytest tests -q
- sldb stores check on each migrated store (in the log)

## Done When

_Name the observable condition that makes the task complete._

The pass-2 log lists every store with its final checks, sldb has its commit, and the affected agents have been told.
