FILE:desk/tasks/task-ws02-inventariar-superficies-y-operaciones-deskops.md
---
id: task-ws02-inventariar-superficies-y-operaciones-deskops
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/cierre.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/brief.md
- runs/subagents/20261031-ws02-04-checkpoint/activation.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws02.md
closeout_evidence:
- commit
- document
---

# WS02: Inventariar superficies y operaciones Deskops

## Rationale

_Explain why this task exists or the business driver behind it._

Primera capa real del núcleo del plan workspace (cierre.md). Activada por runs/subagents/20261031-ws02-04-checkpoint/activation.md; las auditorías alimentan WS06 y WS08-12 con datos comprobados.

## Goal

_Describe the concrete result this task must produce._

Producir desk/drawer/plans/workspace-documental/auditoria/deskops.md como auditoría de solo lectura del estado actual, verificable fila por fila.

## Scope

_State what is in scope and what is out of scope._

Superficie = cada archivo, comando público o modelo registrado concreto de las categorías enumeradas; una fila por superficie. Modelos y Markdown no modelado; inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs; firmas públicas, efectos Git y cierre. Modelado = tiene modelo registrado en el store (`sldb models list`); Markdown no modelado = el resto. Firmas públicas = comandos CLI de deskops y métodos de DeskopsOperations. Cierre = `deskops closeout verify|commit`. Universo: archivos de categorías enumeradas bajo desk/ de este checkout, comandos Deskops y modelos que sirven esas superficies; store local .sldb del checkout. Una fila por superficie con lista de todas sus operaciones públicas; no duplicar por comando. Para dato pasivo registrar path/hash o listado read-only; falta store se informa no comprobado con causa. Solo lectura fuera del entregable. Rutas de lectura: deskops/ (código), desk/ y .sldb de este checkout. Se escribe únicamente desk/drawer/plans/workspace-documental/auditoria/deskops.md y evidencia en runs/subagents/20261031-ws02-auditoria-deskops/. No se modifica código, otro repo, dag.yaml, reconciliacion.md, Board ajeno ni tareas de otros. Fuera de alcance: WS05 Scion, contratos nuevos, implementación. Precisiones comunes. Roles: el Executor escribe entregable y evidencia, sin commits ni closeout; el Supervisor corre las validaciones de plan, hace commits y closeout; un Tester independiente verifica. Hash = SHA-256 de los bytes del archivo. Encabezado: fecha, y por cada repo realmente leído su HEAD completo y cantidad de rutas sucias en git status; una carpeta sin git se declara sin git. Si un archivo citado está sucio, se agrega su SHA-256 para fijar lo leído. Universo exacto: desk/inbox, desk/drawer, desk/contexts (pills), desk/rituals, desk/registry, desk/roles, desk/runtimes, desk/tasks, desk/lifecycle; desk/issues, desk/faq, desk/crossroads y fases se registran comprobando si existen, y su ausencia es un dato; runs/subagents; el store .sldb. Coincidencia por ruta exacta. Secciones del entregable: A) una fila por comando de command_registry() en deskops/cli/registry.py y por método público sin guion bajo de DeskopsOperations, con su efecto (lectura, mutación desk, efecto Git); efecto Git = stage, commit, amend, tag o push hechos por el comando, y si no hace ninguno se dice. B) una fila por modelo que `sldb models list --store .sldb` lista, con los comandos que lo leen o mutan; un modelo sirve a una superficie si el store le vincula archivos de ella o un comando del universo lo usa. C) archivos: una fila por archivo en el anexo runs/subagents/20261031-ws02-auditoria-deskops/file-inventory.tsv con columnas path, sha256, modelo o «no modelado», y el entregable resume por categoría con conteo y cita el hash del anexo. Un archivo es modelado si el store lo vincula a un modelo: se decide por el store, nunca por carpeta. D) cierre: closeout verify y closeout commit con su evidencia exigida y efectos Git. Columnas de A y B: superficie, ubicación, operaciones, efecto, estado (comprobado/no comprobado + causa), evidencia.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer fuentes actuales. 2. Escribir desk/drawer/plans/workspace-documental/auditoria/deskops.md: encabezado con fecha, commit HEAD de cada repo leído y universo auditado; luego las filas. 3. Registrar comandos usados en runs/subagents/20261031-ws02-auditoria-deskops/commands.log. 4. Dejar runs/subagents/20261031-ws02-auditoria-deskops/result-summary.md (qué se hizo, huecos, qué revisar). Lo no comprobado se marca «no comprobado» con causa: no se infiere. El Executor no hace commits, no escribe en desk/ salvo desk/drawer/plans/workspace-documental/auditoria/deskops.md, y no corre closeout.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/auditoria/deskops.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente muestrea filas contra la fuente citada y deja runs/subagents/20261031-ws02-auditoria-deskops/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Cada fila incluye ubicación (archivo o símbolo de código) y la operación expuesta (comando o método que la lee o muta, o «dato pasivo»), con estado comprobado; no inferir modelo por carpeta. Estado comprobado = lectura citada con archivo:línea o salida de comando de solo lectura; lo no comprobado se marca «no comprobado» con causa (ausente, inaccesible o no encontrado). Una fila contiene lista de operaciones, no elegir solo una. La evidencia puede ser archivo:línea, hash/listado read-only o salida de comando según soporte; alcance de categorías y store local .sldb, sin inventariar binarios ajenos.

