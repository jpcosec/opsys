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

# pron drawer → deskops: Audit big documents SLDB modeling

_Describe the incoming message with enough evidence to triage._

_Describe the incoming message with enough evidence to triage._

Movido desde pron/desk/drawer/issues/issue-audit-big-documents-sldb-modeling.md (limpieza de desks del 2026-10-18). pron no registra modelos de deskops (source/spec/01-mundo.md:33, 08:79) y este issue es trabajo de deskops sobre atoms; queda en tu desk para que lo triages: si sigue vigente, promuévelo; si no, ciérralo.
Pregunta abierta de la revisión: Which repo's big documents is this auditing? If deskops, move there; pron has no such docs.
Evidencia: Atoms/deskops work; pron spec (source/spec/01-mundo.md:33, 08-prerequisitos-y-orden.md:79) forbids deskops models/refs in pron's store; README/FAQ/diagram docs live in deskops/graph_ui, not pron

--- texto original ---

# Audit big documents SLDB modeling

## Kind

feature

## Status

open

## Problem

Large documents such as README, FAQ, knowledge materialization docs, and diagram explanations are not clearly classified as shallow SLDB documents, composed atom materializations, strict typed documents, or unmodeled prose.

## Desired Outcome

Inventory the big documents and decide their model strategy: shallow body, composed materialization, typed sections, generated projection, or intentionally unmodeled.

## Questions

- Which large docs must be tracked by SLDB now?
- Which big docs should declare source atoms and materialization metadata?
- When does a large document need typed sections instead of a shallow body?

## Related Atoms

- atom-big-documents-need-explicit-modeling-strategy
- atom-main-docs-are-composed-materializations
- atom-materialization-contracts-bind-source-output-validation

Resolución (deskops-6e, 2026-10-18): ya resuelto en deskops: inventario y decisión por documento en 989d724 (tests/test_large_doc_materialization.py).
