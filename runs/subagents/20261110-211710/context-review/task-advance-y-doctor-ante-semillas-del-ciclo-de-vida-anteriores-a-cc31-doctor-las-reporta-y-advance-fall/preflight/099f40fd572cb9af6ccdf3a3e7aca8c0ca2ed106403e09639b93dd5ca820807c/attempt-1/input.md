FILE:desk/tasks/task-advance-y-doctor-ante-semillas-del-ciclo-de-vida-anteriores-a-cc31-doctor-las-reporta-y-advance-fall.md
---
sldb:
  by: agent
  at: '2026-11-10T21:16:55Z'
  authority: generated
  via: create_document
id: task-advance-y-doctor-ante-semillas-del-ciclo-de-vida-anteriores-a-cc31-doctor-las-reporta-y-advance-fall
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
- deskops/doctor_findings.py
- deskops/cli/commands/doctor.py
- deskops/lifecycle.py
- deskops/workspace.py
- deskops/cli/commands/desk.py
- deskops/services/tasks.py
- tests/
- docs/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-advance-falla-con-status-draft-does-not-follow-history-task-activates-en-un-desk-con-el-ciclo-de-vida-anterior-a-cc31.md
---

# advance y doctor ante semillas del ciclo de vida anteriores a CC31: doctor las reporta y advance falla nombrando la arista sin efecto sets

## Rationale

_Explain why this task exists or the business driver behind it._

Prioridad del overlord (2026-11-10). Un desk con el ciclo de vida anterior a CC31 (kit Chatbot_Infra) no puede avanzar tareas y doctor no avisa. El error que ve el usuario es un ValidationError que no dice la causa.

## Goal

_Describe the concrete result this task must produce._

deskops doctor reporta las semillas managed del ciclo de vida desactualizadas y sugiere desk update --apply; deskops advance falla antes de escribir, con un mensaje que nombra la arista sin efecto sets.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/doctor_findings.py, deskops/cli/commands/doctor.py, deskops/lifecycle.py, deskops/workspace.py, deskops/cli/commands/desk.py, deskops/services/tasks.py, tests/, docs/, CHANGELOG.md. Fuera: el validador de CC37, la migración del kit y la gramática del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

REPORTE (nota de inbox 5106e3f8, AntonIA, kit Chatbot_Infra con deskops-runtime 5ccc29a3): `deskops advance` falla con 'Validation error: TaskCodeDoc ... lifecycle is inconsistent: status draft does not follow history task_activates; expected active'. El desk del kit tiene desk/lifecycle/execution-task_activates.md con 'attributes: {}' (migración 2d69e9c6). La semilla managed desde CC31 trae 'attributes: {sets: {status: active}, terminal: false}'. advance agrega task_activates a history sin mover status, y el validador de CC37 (deskops/models/task_lifecycle.py) rechaza la escritura. El kit se arregla con 'deskops desk update --apply'.

DEFECTOS DE DESKOPS (con causa raíz escrita antes del arreglo):
d1 (doctor): 'deskops doctor' dice 'Desk is healthy' aunque las semillas managed del ciclo de vida (RelationDoc de desk/lifecycle/) difieren de las del paquete. Debe reportarlas, con severidad alert o error a decidir y justificar en el informe: un hallazgo por archivo, con qué difiere, y el fix 'deskops desk update --apply'. Para comparar se usa lo mismo que desk update (seed_desk(root, apply=False, restore_managed=True), deskops/workspace.py:239). No se escribe una comparación aparte.
d2 (advance): con una arista cuya transición no trae attributes.sets.status (o cuyo efecto no lleva al estado que el validador exige), advance debe fallar antes de escribir. El mensaje nombra la arista (archivo y relation_type), dice que su efecto sets falta o difiere de la semilla del paquete y sugiere 'deskops desk update --apply'. No sale un ValidationError de pydantic. La tarea queda sin cambios en disco.

REPRODUCCIÓN: un desk limpio (deskops init en /dev/shm) con la arista execution-task_activates sin attributes, puesta vía sldb (fields update), no a mano; una tarea con recibos de activación; 'deskops advance' reproduce el error. Evidencia en el recibo reproduction de esta tarea.

FUERA: cambiar el validador de CC37, migrar el kit Chatbot_Infra (lo hace su dueño con desk update --apply) y la gramática del CLI (goldens de ayuda idénticos). Los de salida también, salvo los mensajes nuevos de d1 y d2, que llevan golden propio.

REGLAS COMUNES: tests de a uno con TMPDIR=/dev/shm y la guarda de pgrep anclada; nada a mano en desk/ ni .sldb/; nunca git add -A; CHANGELOG y doc en docs/ (manual de operador: doctor y advance); 4 pasos del workflow de deskops en clon limpio los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test de reproducción: desk limpio con la arista sin attributes; advance falla con el mensaje nuevo y la tarea queda sin cambios
- Test de doctor: reporta la semilla desactualizada con fix desk update --apply; tras desk update --apply, doctor sin ese hallazgo y advance pasa draft a active
- Goldens de ayuda idénticos; los de salida, salvo los mensajes nuevos con golden propio
- 4 pasos del workflow en clon limpio

## Done When

_Name the observable condition that makes the task complete._

d1 y d2 arreglados con causa raíz escrita, con tests de reproducción verdes, doc en docs/ y CHANGELOG.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-advance-y-doctor-ante-semillas-del-ciclo-de-vida-anteriores-a-cc31-doctor-las-reporta-y-advance-fall: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

