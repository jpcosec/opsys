---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-18T21:44:51'
# open | closed
status: closed
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# pron drawer → deskops: Validate atoms and trace composed usage

_Describe the incoming message with enough evidence to triage._

_Describe the incoming message with enough evidence to triage._

Movido desde pron/desk/drawer/issues/issue-atom-validation-and-traceability.md (limpieza de desks del 2026-10-18). pron no registra modelos de deskops (source/spec/01-mundo.md:33, 08:79) y este issue es trabajo de deskops sobre atoms; queda en tu desk para que lo triages: si sigue vigente, promuévelo; si no, ciérralo.
Pregunta abierta de la revisión: Trace half is done (cdabbfa); is the remaining 'load every desk/atoms/** as AtomDoc' test still wanted? If so move to deskops.
Evidencia: Atoms/deskops work; pron spec (source/spec/01-mundo.md:33, 08-prerequisitos-y-orden.md:79) forbids deskops models/refs in pron's store; deskops tests/test_graph_atom_trace.py and cdabbfa closeout cover trace; AtomDoc load-all test not confirmed

--- texto original ---

# Validate atoms and trace composed usage

## Issue

Atoms now have a stricter `AtomDoc` contract, but there is no project-level command or test that validates every atom and traces where composed documents use them.

## Core Need

Provide validation and traceability for `desk/atoms/**/*.md` without reintroducing outgoing relations in atoms.

## Constraints

- Validation should prove every atom roundtrips through `AtomDoc`.
- Trace should inspect documents/compositions that reference atoms.
- Traceability should not rely on `source-atom:*` tags produced by atom-to-task materializers.

## Follow-Up Shape

- Add a test that loads all `desk/atoms/**/*.md` as `AtomDoc`.
- Add a read-side trace command once document-to-atom composition is defined.
- Report unresolved atom references as findings.

## Tags

- system:deskops
- topic:atoms
- topic:validation
- topic:traceability

Resolución (deskops-6e, 2026-10-18): ya resuelto: 'deskops atoms validate' valida cada atom y la traza derivada de usos es deskops/graph/atom_trace.py (cdabbfa).
