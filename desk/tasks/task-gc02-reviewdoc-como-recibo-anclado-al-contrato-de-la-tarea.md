---
id: task-gc02-reviewdoc-como-recibo-anclado-al-contrato-de-la-tarea
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
- deskops/models/review.py
- deskops/models/__init__.py
- deskops/bootstrap.py
- deskops/workspace.py
- deskops/operations.py
- .sldb/core/models/
- tests/
- tests/fixtures/model_contract_hashes.json
- CHANGELOG.md
task_type: code
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence:
- tests
- commit
- atom
- materialization
---

# GC02: ReviewDoc como recibo anclado al contrato de la tarea

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GC02 del plan desk/drawer/plans/gates-por-tipo (dag.yaml rev 2, paquete PC01): lado consumidor del plan grafo-operable de sldb; los gates del ciclo de vida pasan a ser documentos que sldb evalúa (D2, DC1-DC7).

## Goal

_Describe the concrete result this task must produce._

Modelo deskops/models/review.py ReviewDoc (StructuredNLDoc, como RunDoc) con campos: id (review-<task>-<kind>-<n>), title, kind (preflight | bundle | reproduction | goldens | owner; vocabulario cerrado validado), subject (str; valor doc:<Modelo>:<id> o vacío para revisiones de nodos de plan), subject_ref (str libre: ruta#node:ID cuando subject está vacío), engine (nombre del RuntimeProfileDoc o "human"), actor (identidad que corrió o dispuso; deskops/identity.py), run_dir (ruta relativa bajo runs/), input_sha256, output_sha256, verdict (pending | accepted | rejected | incomplete), reason (str), created_at, disposed_at, disposed_by, tags; cuerpo: sección Summary y sección Disposition. __doc_anchors__ = ["subject"] y __references__ = ["subject"] (GO07 trata __doc_anchors__ también como references; antes de GO07 el campo es una referencia normal que resuelve doc:Model:name sin sufijo, hipótesis: la versión actual de sldb acepta en un campo __references__ un valor con prefijo doc: o GC02 lo declara solo en __doc_anchors__ y espera a GO07; el TaskDoc fija cuál). Un ReviewDoc vive en desk/reviews/<task-id>/<kind>-<n>.md y se trackea; deskops init/desk update crean desk/reviews/. Validación al escribir: kind y verdict en su vocabulario; verdict accepted o rejected exige reason no vacía y disposed_by; subject con forma doc:<Modelo>:<id> o vacío. Un ReviewDoc no se edita con edit review verdict: edit lo rechaza (el veredicto se escribe con deskops review dispose, GC03). Registro en MODEL_REFS. Este nodo no escribe ReviewDocs desde ningún comando; GC03 lo hace.

## Scope

_State what is in scope and what is out of scope._

Repo deskops. Archivos: deskops/models/review.py, deskops/models/__init__.py, deskops/bootstrap.py (MODEL_REFS), deskops/workspace.py (desk/reviews), deskops/operations.py (edit refuses verdict), tests/, tests/fixtures/model_contract_hashes.json, CHANGELOG.md. Depende de: nada; requiere gates: ninguno. Fuera de alcance: brief.md §Fuera de alcance, los demás nodos GC del plan y todo cambio en sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Modelo deskops/models/review.py ReviewDoc (StructuredNLDoc, como RunDoc) con campos: id (review-<task>-<kind>-<n>), title, kind (preflight | bundle | reproduction | goldens | owner; vocabulario cerrado validado), subject (str; valor doc:<Modelo>:<id> o vacío para revisiones de nodos de plan), subject_ref (str libre: ruta#node:ID cuando subject está vacío), engine (nombre del RuntimeProfileDoc o "human"), actor (identidad que corrió o dispuso; deskops/identity.py), run_dir (ruta relativa bajo runs/), input_sha256, output_sha256, verdict (pending | accepted | rejected | incomplete), reason (str), created_at, disposed_at, disposed_by, tags; cuerpo: sección Summary y sección Disposition. __doc_anchors__ = ["subject"] y __references__ = ["subject"] (GO07 trata __doc_anchors__ también como references; antes de GO07 el campo es una referencia normal que resuelve doc:Model:name sin sufijo, hipótesis: la versión actual de sldb acepta en un campo __references__ un valor con prefijo doc: o GC02 lo declara solo en __doc_anchors__ y espera a GO07; el TaskDoc fija cuál). Un ReviewDoc vive en desk/reviews/<task-id>/<kind>-<n>.md y se trackea; deskops init/desk update crean desk/reviews/. Validación al escribir: kind y verdict en su vocabulario; verdict accepted o rejected exige reason no vacía y disposed_by; subject con forma doc:<Modelo>:<id> o vacío. Un ReviewDoc no se edita con edit review verdict: edit lo rechaza (el veredicto se escribe con deskops review dispose, GC03). Registro en MODEL_REFS. Este nodo no escribe ReviewDocs desde ningún comando; GC03 lo hace. Aceptación: ReviewDoc renderiza y extrae ida y vuelta con un payload de ejemplo; un kind fuera del vocabulario falla al validar; verdict accepted sin reason falla; subject "task-x" (sin prefijo doc:) falla; subject "doc:TaskCodeDoc:task-x" valida; en un desk temporal un ReviewDoc guardado con deskops (doc_io) queda tracked como ReviewDoc:<id> y sldb edges show lo enlaza a la tarea por subject; edit review verdict falla con el mensaje que remite a review dispose; tests/fixtures/model_contract_hashes.json actualizado; CHANGELOG. Reglas comunes (alcance.md §Reglas comunes): validación con pytest tests en robocop2, ningún nodo cierra con tests rojos ni saltados; toda capacidad nueva entra con modelo o documento, comando CLI con envelope, pruebas, entrada en CHANGELOG.md y doc en docs/; nada de Python supliendo una regla que sldb debería evaluar: si sldb (grafo-operable rev 9) no fija lo que el nodo necesita, se registra la hipótesis en este TaskDoc y, si bloquea, se manda nota con deskops message send --to sldb; compatibilidad: los desks existentes migran con deskops desk update --apply de forma idempotente y probada; ninguna bandera para saltar un gate (D2). Reglas del dueño: no tocar el repo sldb; nada escrito a mano en desk/ ni .sldb/ (solo los CLI deskops y sldb); código, tests y docs se editan normal; trabajo en el worktree deskops-wt-gates, rama wt/gates-por-tipo, nunca push a main; nunca git add -A.

## Validation

_List the checks required before this task can close._

- ReviewDoc renderiza y extrae ida y vuelta con un payload de ejemplo
- un kind fuera del vocabulario falla al validar
- verdict accepted sin reason falla
- subject "task-x" (sin prefijo doc:) falla
- subject "doc:TaskCodeDoc:task-x" valida
- en un desk temporal un ReviewDoc guardado con deskops (doc_io) queda tracked como ReviewDoc:<id> y sldb edges show lo enlaza a la tarea por subject
- edit review verdict falla con el mensaje que remite a review dispose
- tests/fixtures/model_contract_hashes.json actualizado
- CHANGELOG.
- PYTHONPATH=$PWD python -m pytest -q tests (suite completa verde en robocop2)

## Done When

_Name the observable condition that makes the task complete._

ReviewDoc renderiza y extrae ida y vuelta con un payload de ejemplo; un kind fuera del vocabulario falla al validar; verdict accepted sin reason falla; subject "task-x" (sin prefijo doc:) falla; subject "doc:TaskCodeDoc:task-x" valida; en un desk temporal un ReviewDoc guardado con deskops (doc_io) queda tracked como ReviewDoc:<id> y sldb edges show lo enlaza a la tarea por subject; edit review verdict falla con el mensaje que remite a review dispose; tests/fixtures/model_contract_hashes.json actualizado; CHANGELOG.
