---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-18T21:44:52'
# open | closed
status: closed
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# pron drawer → deskops: Define knowledge promotion criteria

_Describe the incoming message with enough evidence to triage._

_Describe the incoming message with enough evidence to triage._

Movido desde pron/desk/drawer/issues/issue-define-knowledge-promotion-criteria.md (limpieza de desks del 2026-10-18). pron no registra modelos de deskops (source/spec/01-mundo.md:33, 08:79) y este issue es trabajo de deskops sobre atoms; queda en tu desk para que lo triages: si sigue vigente, promuévelo; si no, ciérralo.
Pregunta abierta de la revisión: Is a promotion policy still wanted? If so it belongs in deskops and must drop the drawer-to-task promotion path removed in d35726a.
Evidencia: Atoms/deskops work; pron spec (source/spec/01-mundo.md:33, 08-prerequisitos-y-orden.md:79) forbids deskops models/refs in pron's store; deskops d35726a dropped drawer-to-task promotion, so text is partly stale

--- texto original ---

# Define knowledge promotion criteria

## Kind

feature

## Status

open

## Problem

The workflow distinguishes raw signals, inbox notes, drawer items, atoms, docs, specs, diagrams, and tasks, but it does not define criteria for promoting a signal from one layer to another.

## Desired Outcome

Define a small promotion policy for common moves: inbox to drawer, inbox to task, drawer to atom, atom to doc/spec/diagram, and issue to active board task.

## Questions

- What evidence is required before a conversation insight becomes an atom?
- When should an unclear item stay as an issue instead of becoming an atom?
- Who or what is allowed to promote drawer items into active board work?

## Related Atoms

- atom-raw-signals-need-distillation-before-formalization
- atom-promotion-needs-explicit-criteria
- atom-available-tasks-are-board-routed-work

Resolución (deskops-6e, 2026-10-18): cubierto: el flujo de promoción (inbox -> drawer -> task con 'add task --from-drawer', pills -> atoms -> docs) está en AGENTS.md y docs/workflow-policy-reference.md; la vía drawer-to-task vieja se retiró a propósito.
