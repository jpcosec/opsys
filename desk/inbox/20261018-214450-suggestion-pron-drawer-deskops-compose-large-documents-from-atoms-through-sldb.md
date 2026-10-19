---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-18T21:44:50'
# open | closed
status: closed
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# pron drawer → deskops: Compose large documents from atoms through sldb

_Describe the incoming message with enough evidence to triage._

_Describe the incoming message with enough evidence to triage._

Movido desde pron/desk/drawer/issues/issue-atom-composition-documents-through-sldb.md (limpieza de desks del 2026-10-18). pron no registra modelos de deskops (source/spec/01-mundo.md:33, 08:79) y este issue es trabajo de deskops sobre atoms; queda en tu desk para que lo triages: si sigue vigente, promuévelo; si no, ciérralo.
Pregunta abierta de la revisión: Is atom composition still wanted in deskops (no closeout found in deskops git log)? If yes, move it to deskops' drawer; pron has no atom model so it cannot own it.
Evidencia: Atoms/deskops work; pron spec (source/spec/01-mundo.md:33, 08-prerequisitos-y-orden.md:79) forbids deskops models/refs in pron's store

--- texto original ---

# Compose large documents from atoms through sldb

## Issue

Large documents should be materializations/compositions of atoms through `sldb`, but the concrete composition contract is not defined yet.

## Core Need

Define how a larger document declares and renders the atoms it composes without pushing outgoing references into the atom itself.

## Constraints

- Atoms do not point outward.
- Large documents declare their own composition.
- Composition should use `sldb` mechanisms such as model fields, `__compositions__`, links, or a sidecar composition document.
- The result must be roundtrippable and testable.

## Follow-Up Shape

- Create or identify a document model for composed atom documents.
- Add a composition test that renders a document from multiple `AtomDoc` files.
- Decide whether atom references live in frontmatter fields, body links, or a dedicated composition spec.

## Tags

- system:deskops
- system:sldb
- topic:atoms
- topic:composition

Resolución (deskops-6e, 2026-10-18): ya resuelto en deskops: los documentos grandes declaran sus atoms en frontmatter (campo atoms, rol documents) y se componen como materializaciones (989d724); la convención de referencias es 2c36318.
