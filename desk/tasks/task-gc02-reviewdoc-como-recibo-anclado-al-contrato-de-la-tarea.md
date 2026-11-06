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
- deskops/cli/registry.py
- deskops/cli/commands/desk.py
- .sldb/core/models/
- tests/
- tests/fixtures/model_contract_hashes.json
- tests/fixtures/golden/help/
- CHANGELOG.md
task_type: task.code
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

Repo deskops. Archivos: deskops/models/review.py, deskops/models/__init__.py, deskops/bootstrap.py (MODEL_REFS), deskops/workspace.py (desk/reviews), deskops/operations.py (edit refuses verdict), tests/, tests/fixtures/model_contract_hashes.json, CHANGELOG.md. Depende de: nada; requiere gates: ninguno. Fuera de alcance: brief.md §Fuera de alcance, los demás nodos GC del plan y todo cambio en sldb. Precisiones del preflight (2026-11-05, runs/subagents/deskops-gates-por-tipo-context-reviews/context-review/GC02-preflight/e77782ff.../attempt-1): (1) Hipótesis resuelta, por código: el sldb actual NO resuelve un valor doc:Model:name en un campo __references__ (sldb store/edge_index/declared_references.py:84, is_export_id, lo lee como store:Model:name con store "doc", que queda sin resolver). Por eso ReviewDoc declara __doc_anchors__ = ["subject"] y NO declara subject en __references__; el atributo queda inerte hasta GO07 (G_SLDB_ANCHORS), que trata __doc_anchors__ como references. La línea de aceptación "sldb edges show lo enlaza a la tarea por subject" pasa a ser un test marcado xfail(strict=True, reason="G_SLDB_ANCHORS: sldb GO07") que hoy falla y que se vuelve rojo al cumplirse, como señal para quitar la marca. No se escribe Python que suplante la arista. (2) subject y subject_ref son mutuamente excluyentes y exactamente uno no está vacío. subject: ^doc:[A-Z][A-Za-z0-9_]*:[^\s:@]+(@sha256:[0-9a-f]{64})?$ (el sufijo @sha256 se acepta para cuando sldb lo pinnee; deskops no lo calcula). subject_ref: ^[^\s#]+#node:[A-Za-z0-9_-]+$. (3) Superficie de edit: GC02 registra el sujeto review en ARTIFACT_SUBJECTS (artifact.review → deskops edit review <id> <campo> <valor>); edit review rechaza verdict, reason, disposed_at y disposed_by con exit 1 y el mensaje "verdict is written by deskops review dispose (GC03); a new review is a new document"; los demás campos siguen la regla general de edit. Help y goldens de help se regeneran. (4) id = review-<task-id>-<kind>-<n> es la autoridad (nombre del documento); la ruta desk/reviews/<task-id>/<kind>-<n>.md se compone a partir de (task-id, kind, n) al escribir; nada parsea el id de vuelta. Validación del id: ^review-.+-(preflight|bundle|reproduction|goldens|owner)-[0-9]+$. El caso de nodos de plan (subject vacío) lo nombra GC03. (5) La validación de subject es solo de forma; que el documento exista es de sldb anchors check (GO07), no de deskops. (6) created_at, disposed_at: str ISO 8601 (como RunDoc.started_at/ended_at), disposed_at y disposed_by vacíos mientras verdict = pending; run_dir: str relativa a la raíz del repositorio, bajo runs/ (como RunDoc.run_dir); input_sha256 y output_sha256: str hex de 64 o vacío.

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
- en un desk temporal un ReviewDoc guardado con deskops (doc_io) queda tracked como ReviewDoc:<id> y un test xfail(strict, G_SLDB_ANCHORS) documenta que sldb edges show lo enlazará a la tarea por subject cuando exista GO07
- edit review verdict falla con el mensaje que remite a review dispose
- tests/fixtures/model_contract_hashes.json actualizado
- CHANGELOG.
- PYTHONPATH=$PWD python -m pytest -q tests (suite completa verde en robocop2)

## Done When

_Name the observable condition that makes the task complete._

ReviewDoc renderiza y extrae ida y vuelta con un payload de ejemplo; un kind fuera del vocabulario falla al validar; verdict accepted sin reason falla; subject "task-x" (sin prefijo doc:) falla; subject "doc:TaskCodeDoc:task-x" valida; en un desk temporal un ReviewDoc guardado con deskops (doc_io) queda tracked como ReviewDoc:<id> y un test xfail(strict, G_SLDB_ANCHORS) documenta que sldb edges show lo enlazará a la tarea por subject cuando exista GO07; edit review verdict falla con el mensaje que remite a review dispose; tests/fixtures/model_contract_hashes.json actualizado; CHANGELOG.
