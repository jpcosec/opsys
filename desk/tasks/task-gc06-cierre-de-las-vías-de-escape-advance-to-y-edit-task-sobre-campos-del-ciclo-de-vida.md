---
id: task-gc06-cierre-de-las-vías-de-escape-advance-to-y-edit-task-sobre-campos-del-ciclo-de-vida
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-gc01-tipos-de-tarea-como-modelos-con-jerarquía-y-evidencia-de-cierre-declarada-en-el-tipo
pills: []
files:
- deskops/cli/registry.py
- deskops/services/tasks.py
- deskops/operations.py
- deskops/cli/commands/operations.py
- tests/
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

# GC06: Cierre de las vías de escape: advance --to y edit task sobre campos del ciclo de vida

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GC06 del plan desk/drawer/plans/gates-por-tipo (dag.yaml rev 2, paquete PC02): lado consumidor del plan grafo-operable de sldb; los gates del ciclo de vida pasan a ser documentos que sldb evalúa (D2, DC1-DC7).

## Goal

_Describe the concrete result this task must produce._

Se retira la opción --to de deskops advance (registry y tasks.py:179-192); cada uso documentado se reemplaza: cerrar → closeout commit; superseded → closeout supersede; blocked → nada que escribir (DC4: blocked es la regla que no se cumple; mientras GC05 no exista, el mensaje de bloqueo de advance ya lo dice). edit task rechaza status, current_node, task_type, closeout_evidence e history con un error que dice quién escribe cada campo (advance y closeout; add task para task_type) y con exit 1 (error de dominio); el resto de campos sigue editable. El inbox 20261029-213633 (advance --to superseded no cambia status) se cierra con ack porque la opción desaparece. Sin dependencia de sldb: con task_activates aún sin condición (hasta GC05) retirar --to no bloquea a nadie.

## Scope

_State what is in scope and what is out of scope._

Repo deskops. Archivos: deskops/cli/registry.py, deskops/services/tasks.py, deskops/operations.py (edit_artifact_field), deskops/cli/commands/operations.py, tests/, tests/fixtures (goldens de help), docs/operator-manual.md, desk/inbox/20261029-213633-unclear-advance-to-superseded-no-cambia-status.md (ack), CHANGELOG.md. Depende de: GC01; requiere gates: ninguno. Fuera de alcance: brief.md §Fuera de alcance, los demás nodos GC del plan y todo cambio en sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

Se retira la opción --to de deskops advance (registry y tasks.py:179-192); cada uso documentado se reemplaza: cerrar → closeout commit; superseded → closeout supersede; blocked → nada que escribir (DC4: blocked es la regla que no se cumple; mientras GC05 no exista, el mensaje de bloqueo de advance ya lo dice). edit task rechaza status, current_node, task_type, closeout_evidence e history con un error que dice quién escribe cada campo (advance y closeout; add task para task_type) y con exit 1 (error de dominio); el resto de campos sigue editable. El inbox 20261029-213633 (advance --to superseded no cambia status) se cierra con ack porque la opción desaparece. Sin dependencia de sldb: con task_activates aún sin condición (hasta GC05) retirar --to no bloquea a nadie. Aceptación: deskops advance task-x --to ritual-testing falla con error de uso (exit 2) y el help de advance no menciona --to; deskops edit task task-x status closed falla con exit 1 y el mensaje nombra closeout commit; lo mismo para current_node, task_type, closeout_evidence e history; deskops edit task task-x goal "..." sigue funcionando; el golden del help se actualiza; tests/test_cli.py y test_cli_help_examples.py pasan; CHANGELOG con entrada breaking; docs/operator-manual.md sin --to. Reglas comunes (alcance.md §Reglas comunes): validación con pytest tests en robocop2, ningún nodo cierra con tests rojos ni saltados; toda capacidad nueva entra con modelo o documento, comando CLI con envelope, pruebas, entrada en CHANGELOG.md y doc en docs/; nada de Python supliendo una regla que sldb debería evaluar: si sldb (grafo-operable rev 9) no fija lo que el nodo necesita, se registra la hipótesis en este TaskDoc y, si bloquea, se manda nota con deskops message send --to sldb; compatibilidad: los desks existentes migran con deskops desk update --apply de forma idempotente y probada; ninguna bandera para saltar un gate (D2). Reglas del dueño: no tocar el repo sldb; nada escrito a mano en desk/ ni .sldb/ (solo los CLI deskops y sldb); código, tests y docs se editan normal; trabajo en el worktree deskops-wt-gates, rama wt/gates-por-tipo, nunca push a main; nunca git add -A.

## Validation

_List the checks required before this task can close._

- deskops advance task-x --to ritual-testing falla con error de uso (exit 2) y el help de advance no menciona --to
- deskops edit task task-x status closed falla con exit 1 y el mensaje nombra closeout commit
- lo mismo para current_node, task_type, closeout_evidence e history
- deskops edit task task-x goal "..." sigue funcionando
- el golden del help se actualiza
- tests/test_cli.py y test_cli_help_examples.py pasan
- CHANGELOG con entrada breaking
- docs/operator-manual.md sin --to.
- PYTHONPATH=$PWD python -m pytest -q tests (suite completa verde en robocop2)

## Done When

_Name the observable condition that makes the task complete._

deskops advance task-x --to ritual-testing falla con error de uso (exit 2) y el help de advance no menciona --to; deskops edit task task-x status closed falla con exit 1 y el mensaje nombra closeout commit; lo mismo para current_node, task_type, closeout_evidence e history; deskops edit task task-x goal "..." sigue funcionando; el golden del help se actualiza; tests/test_cli.py y test_cli_help_examples.py pasan; CHANGELOG con entrada breaking; docs/operator-manual.md sin --to.
