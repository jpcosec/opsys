---
id: task-gc03-comando-deskops-review-que-reemplaza-a-los-dos-scripts-de-revisión-en-frío
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-gc02-reviewdoc-como-recibo-anclado-al-contrato-de-la-tarea
pills: []
files:
- deskops/cli/registry.py
- deskops/cli/commands/review.py
- deskops/services/review.py
- deskops/workspace.py
- desk/runtimes/
- desk/drawer/plans/workspace-documental/context_review.py
- tests/
- tests/test_context_review_helper.py
- tests/fixtures/golden/help/
- docs/operator-manual.md
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

# GC03: Comando deskops review que reemplaza a los dos scripts de revisión en frío

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GC03 del plan desk/drawer/plans/gates-por-tipo (dag.yaml rev 2, paquete PC01): lado consumidor del plan grafo-operable de sldb; los gates del ciclo de vida pasan a ser documentos que sldb evalúa (D2, DC1-DC7).

## Goal

_Describe the concrete result this task must produce._

Comando deskops review con subcomandos: node <plan-dir> [IDS...] (revisa nodos de un dag.yaml del drawer: contrato del nodo con las claves KEEP del script gobernado, vecinos como edge, gates, y los cuatro archivos base del plan si existen: context-review-guide.md, brief.md, alcance.md, decisiones.md), preflight <task> (input = solo el TaskDoc), bundle <task> (TaskDoc + rituales enrutados por el Board + pills ligadas + átomos ligados + archivos que files nombra, menores de 60 KB + validación), status [<task> | <plan-dir>] (compara el hash del input vigente con los ReviewDoc existentes; sin llamar al modelo), dispose <review-id> --verdict accepted|rejected|incomplete --reason <texto> (escribe verdict, reason, disposed_at, disposed_by; falla si el ReviewDoc ya tiene veredicto distinto de pending). Cada corrida escribe la evidencia que el ritual pide bajo runs/subagents/<run>/context-review/<clave>/<sha256 del input>/attempt-N/ (input.md con FILE:<ruta> en orden documentado, manifest.json con argv, modelo, perfil, selection_reason, fuentes con sha256; output.md; stderr.log; receipt.json) y además un ReviewDoc (GC02) con verdict pending, subject = doc:<Modelo>:<id> de la tarea (sin hash: lo pinnea sldb cuando exista GO07; para node, subject vacío y subject_ref = <plan>/dag.yaml#node:<ID>), engine, run_dir, input_sha256, output_sha256. Motor: --engine <RuntimeProfileDoc> con default el perfil pi deepseek-flash del ritual (context-review.md paso 3), escrito por init como desk/runtimes/runtime-pi-deepseek-flash.md con los flags de aislamiento (--offline --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools) y el system prompt SYSTEM del script gobernado como texto del perfil; el perfil Scion queda como opción futura detrás de --engine y este nodo no lo implementa. Topes (D9): un input sin cambios no se vuelve a revisar (status lo dice); --max-attempts 2 por clave a nivel de plan; para preflight y bundle una por hash de contrato de la tarea, y una repetición exige --force con --reason, que queda en manifest.json y en el ReviewDoc. Falla de transporte (exit distinto de 0 o salida sin la sección REFORMULACION) deja receipt.json con technical_ok false y ReviewDoc con verdict incomplete y reason "technical", separado de los hallazgos de comprensión (ritual, paso 5). Retiro: se borran desk/drawer/plans/workspace-documental/context_review.py y tests/test_context_review_helper.py (los sustituyen los tests de este nodo); sldb/desk/drawer/plans/grafo-operable/context_review.py es de sldb y no se toca: se le manda nota por deskops message send --to sldb de que deskops review lo cubre. Produce G_RECEIPTS.

## Scope

_State what is in scope and what is out of scope._

Repo deskops. Archivos: deskops/cli/registry.py, deskops/cli/commands/review.py, deskops/services/review.py, deskops/workspace.py (runtime-pi-deepseek-flash), desk/runtimes/, desk/drawer/plans/workspace-documental/context_review.py (borrado), tests/, docs/operator-manual.md, CHANGELOG.md. Depende de: GC02; requiere gates: ninguno. Fuera de alcance: brief.md §Fuera de alcance, los demás nodos GC del plan y todo cambio en sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Comando deskops review con subcomandos: node <plan-dir> [IDS...] (revisa nodos de un dag.yaml del drawer: contrato del nodo con las claves KEEP del script gobernado, vecinos como edge, gates, y los cuatro archivos base del plan si existen: context-review-guide.md, brief.md, alcance.md, decisiones.md), preflight <task> (input = solo el TaskDoc), bundle <task> (TaskDoc + rituales enrutados por el Board + pills ligadas + átomos ligados + archivos que files nombra, menores de 60 KB + validación), status [<task> | <plan-dir>] (compara el hash del input vigente con los ReviewDoc existentes; sin llamar al modelo), dispose <review-id> --verdict accepted|rejected|incomplete --reason <texto> (escribe verdict, reason, disposed_at, disposed_by; falla si el ReviewDoc ya tiene veredicto distinto de pending). Cada corrida escribe la evidencia que el ritual pide bajo runs/subagents/<run>/context-review/<clave>/<sha256 del input>/attempt-N/ (input.md con FILE:<ruta> en orden documentado, manifest.json con argv, modelo, perfil, selection_reason, fuentes con sha256; output.md; stderr.log; receipt.json) y además un ReviewDoc (GC02) con verdict pending, subject = doc:<Modelo>:<id> de la tarea (sin hash: lo pinnea sldb cuando exista GO07; para node, subject vacío y subject_ref = <plan>/dag.yaml#node:<ID>), engine, run_dir, input_sha256, output_sha256. Motor: --engine <RuntimeProfileDoc> con default el perfil pi deepseek-flash del ritual (context-review.md paso 3), escrito por init como desk/runtimes/runtime-pi-deepseek-flash.md con los flags de aislamiento (--offline --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools) y el system prompt SYSTEM del script gobernado como texto del perfil; el perfil Scion queda como opción futura detrás de --engine y este nodo no lo implementa. Topes (D9): un input sin cambios no se vuelve a revisar (status lo dice); --max-attempts 2 por clave a nivel de plan; para preflight y bundle una por hash de contrato de la tarea, y una repetición exige --force con --reason, que queda en manifest.json y en el ReviewDoc. Falla de transporte (exit distinto de 0 o salida sin la sección REFORMULACION) deja receipt.json con technical_ok false y ReviewDoc con verdict incomplete y reason "technical", separado de los hallazgos de comprensión (ritual, paso 5). Retiro: se borran desk/drawer/plans/workspace-documental/context_review.py y tests/test_context_review_helper.py (los sustituyen los tests de este nodo); sldb/desk/drawer/plans/grafo-operable/context_review.py es de sldb y no se toca: se le manda nota por deskops message send --to sldb de que deskops review lo cubre. Produce G_RECEIPTS. Aceptación: En un desk temporal con un ejecutable pi falso (fixture que devuelve una salida con REFORMULACION), deskops review preflight task-x escribe attempt-1 con los cinco archivos y un ReviewDoc review-task-x-preflight-1 con verdict pending, subject doc:TaskCodeDoc:task-x, run_dir e input_sha256 iguales a los del manifest; una segunda corrida sin cambios no llama al ejecutable y status lo reporta como reviewed; editar goal de la tarea hace que status la reporte stale y la siguiente corrida cree attempt bajo otro sha; bundle incluye en input.md los rituales del Board, las pills ligadas y los archivos de files, en ese orden, con FILE: por archivo; node sobre este mismo plan (gates-por-tipo) escribe un ReviewDoc por nodo con subject vacío y subject_ref; review dispose review-task-x-preflight-1 --verdict accepted --reason "..." escribe verdict, reason, disposed_at y disposed_by y una segunda dispose falla; un tercer intento sobre la misma clave a nivel de plan falla sin --force; un pi falso que sale con exit 1 deja technical_ok false y verdict incomplete; grep de context_review.py en desk/drawer de deskops no devuelve nada; CHANGELOG; docs/operator-manual.md con la sección deskops review. Reglas comunes (alcance.md §Reglas comunes): validación con pytest tests en robocop2, ningún nodo cierra con tests rojos ni saltados; toda capacidad nueva entra con modelo o documento, comando CLI con envelope, pruebas, entrada en CHANGELOG.md y doc en docs/; nada de Python supliendo una regla que sldb debería evaluar: si sldb (grafo-operable rev 9) no fija lo que el nodo necesita, se registra la hipótesis en este TaskDoc y, si bloquea, se manda nota con deskops message send --to sldb; compatibilidad: los desks existentes migran con deskops desk update --apply de forma idempotente y probada; ninguna bandera para saltar un gate (D2). Reglas del dueño: no tocar el repo sldb; nada escrito a mano en desk/ ni .sldb/ (solo los CLI deskops y sldb); código, tests y docs se editan normal; trabajo en el worktree deskops-wt-gates, rama wt/gates-por-tipo, nunca push a main; nunca git add -A.

## Validation

_List the checks required before this task can close._

- En un desk temporal con un ejecutable pi falso (fixture que devuelve una salida con REFORMULACION), deskops review preflight task-x escribe attempt-1 con los cinco archivos y un ReviewDoc review-task-x-preflight-1 con verdict pending, subject doc:TaskCodeDoc:task-x, run_dir e input_sha256 iguales a los del manifest
- una segunda corrida sin cambios no llama al ejecutable y status lo reporta como reviewed
- editar goal de la tarea hace que status la reporte stale y la siguiente corrida cree attempt bajo otro sha
- bundle incluye en input.md los rituales del Board, las pills ligadas y los archivos de files, en ese orden, con FILE: por archivo
- node sobre este mismo plan (gates-por-tipo) escribe un ReviewDoc por nodo con subject vacío y subject_ref
- review dispose review-task-x-preflight-1 --verdict accepted --reason "..." escribe verdict, reason, disposed_at y disposed_by y una segunda dispose falla
- un tercer intento sobre la misma clave a nivel de plan falla sin --force
- un pi falso que sale con exit 1 deja technical_ok false y verdict incomplete
- grep de context_review.py en desk/drawer de deskops no devuelve nada
- CHANGELOG
- docs/operator-manual.md con la sección deskops review.
- PYTHONPATH=$PWD python -m pytest -q tests (suite completa verde en robocop2)

## Done When

_Name the observable condition that makes the task complete._

En un desk temporal con un ejecutable pi falso (fixture que devuelve una salida con REFORMULACION), deskops review preflight task-x escribe attempt-1 con los cinco archivos y un ReviewDoc review-task-x-preflight-1 con verdict pending, subject doc:TaskCodeDoc:task-x, run_dir e input_sha256 iguales a los del manifest; una segunda corrida sin cambios no llama al ejecutable y status lo reporta como reviewed; editar goal de la tarea hace que status la reporte stale y la siguiente corrida cree attempt bajo otro sha; bundle incluye en input.md los rituales del Board, las pills ligadas y los archivos de files, en ese orden, con FILE: por archivo; node sobre este mismo plan (gates-por-tipo) escribe un ReviewDoc por nodo con subject vacío y subject_ref; review dispose review-task-x-preflight-1 --verdict accepted --reason "..." escribe verdict, reason, disposed_at y disposed_by y una segunda dispose falla; un tercer intento sobre la misma clave a nivel de plan falla sin --force; un pi falso que sale con exit 1 deja technical_ok false y verdict incomplete; grep de context_review.py en desk/drawer de deskops no devuelve nada; CHANGELOG; docs/operator-manual.md con la sección deskops review.
