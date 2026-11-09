---
id: task-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# atoms split no se puede alimentar por el CLI desde CC35a: sldb rechaza encabezados en el field

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/inbox-note-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/inbox-note-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

atoms split no se puede alimentar por el CLI desde CC35a: sldb rechaza encabezados dentro de un field.

Qué pasa: deskops atoms split parte un átomo por las secciones con encabezado de su answer (deskops/services/atoms.py:583, _split_atom_answer_sections, que exige «## ...»/«### ...» en el answer). Desde CC35a (8d0e23fe) toda escritura de deskops pasa por sldb.api.transaction, y sldb rechaza los encabezados dentro de un field como ruido estructural (sldb src/sldb/api/documents/refuse_structural_noise.py, desde create_document): «ruido estructural en '<átomo>': el documento trae N headings que AtomDoc no declara ... Un heading dentro de un field es un campo que falta en el modelo. Creá un modelo que herede de AtomDoc y declare esas secciones como campos». Por eso «deskops add atom --answer '### Part one ...'» falla, y ningún átomo partible se puede crear por el CLI.

tests/test_atoms_split.py pasa solo porque escribe el archivo del átomo a mano (_write_sectioned_atom), sin pasar por sldb. El bloque 29 de docs/operator-manual.md (la demo de split) fallaba por esto; se quitó del manual como decisión revisable del 2026-11-09, para dejar test_operator_manual verde.

Opciones:
(a) split toma las partes sin encabezados en el field: por ejemplo, «deskops atoms split <atom> --into a b --part a="texto" --part b="texto"», o partir por párrafos. Es task.code en deskops; cambia la gramática de atoms split y sus goldens de ayuda.
(b) Un modelo de átomo con las secciones declaradas como campos, como sugiere sldb. Es más grande y toca el formato de los átomos del desk.
(c) Sin split en el manual (hecho) y dejar split como está, inalcanzable por el CLI.

Recomendación del coordinador del plan: (a). Cambia la gramática del CLI y choca con el invariante 2 de alcance.md del plan deskops-como-config. La deciden el coordinador de proyecto y el overlord al cerrar la ola; no se promueve antes.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
