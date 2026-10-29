---
id: task-closeout-verify-no-ve-materializaciones-de-archivos-fuera-del-desk-en-repos-con-src
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

# closeout verify no ve materializaciones de archivos fuera del desk en repos con src/

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261020-102639-suggestion-closeout-verify-no-ve-materializaciones-de-archivos-fuera-del-desk-en-repos-con-src.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261020-102639-suggestion-closeout-verify-no-ve-materializaciones-de-archivos-fuera-del-desk-en-repos-con-src.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Desde Governance (sesión governance-00), 2026-10-20. Al cerrar task-pulse-reproduce-los-stores-enlazados en heyantonia/Governance: 'deskops closeout verify' reporta missing_changed_file_link para src/vsm/organs/links.py, .github/workflows/pulse.yml y .github/workflows/ci.yml, aunque hay un atom (atom-los-stores-enlazados-se-reproducen-en-ci-con-vsm-enlaces) y tres MaterializationContractDoc creados con 'deskops add materialization --source-atoms <atom> --target-identity <archivo>'. En 'deskops graph build' esos archivos no son nodos (solo tests/ entra como test_file por path_rule), y el nodo materialization solo tiene la arista references→atom, ninguna hacia su target_identity. _changed_file_link_evidence (operations.py:761) exige node_ids_by_path[archivo]. Esperado: que la materialización declarada cubra su target_identity aunque el archivo esté fuera del paquete que el extractor indexa (src/<paquete>, .github/, docs/), o una forma de declarar qué rutas son fuente. Lo mismo bloquea el cierre de una tarea de documentación cuyos archivos son docs/environment/*.md (documentos sldb). Las dos tareas quedan en ritual-testing hasta que esto exista; no se cierran con una referencia de seguimiento ficticia.

Agregado: además, una MaterializationContractDoc cuyo target_identity no es nodo del grafo hace fallar 'deskops graph missing' (missing_declared_target), y pulse lo corre en CI; 'deskops add materialization' no la trackea en el store (no entra en store.yaml) y no hay comando para quitarla. En Governance se borraron a mano las tres, sin commitear.

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
