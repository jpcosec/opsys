FILE:desk/tasks/task-advance-y-doctor-ante-semillas-del-ciclo-de-vida-anteriores-a-cc31-doctor-las-reporta-y-advance-fall.md
---
sldb:
  by: agent
  at: '2026-11-10T21:19:54Z'
  authority: generated
  via: save_document_payload
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

DISPOSICIÓN DE PREFLIGHT-1 Y BUNDLE-1 (2026-11-10, coordinador del plan; decisiones revisables):
b1 (severidad de d1): error cuando difiere lo que gobierna una transición en una arista del ciclo de vida (RelationDoc de desk/lifecycle/: source_id, target_id, relation_type, condition o attributes), porque rompe advance. alert cuando una semilla managed difiere solo en el cuerpo o en notas. La justificación queda en el informe.
b2 (reproducción): los comandos exactos y su salida están en runs/subagents/20261110-repro-advance/repro.log. Son: deskops init en /dev/shm; add task task.code; `sldb fields update docs/RelationDoc/execution-task_activates/attributes '{}' --store .sldb`; recibos preflight y bundle con `deskops review record --operator --evidence` y dispose accepted; doctor 'Desk is healthy'; advance con el ValidationError; control con desk update --apply y advance que pasa. El test de reproducción replica esos pasos sobre tmp_path.
b3 (recibos del test): en el desk desechable del test, los mismos de b2: review record --kind preflight y bundle --operator con un archivo de evidencia, y dispose accepted.
b4 (guarda de pytest): antes de cada archivo, `while pgrep -f '^(\S*/)?python[0-9.]* -m pytest' >/dev/null; do sleep 60; done`. Luego `TMPDIR=/dev/shm timeout 900 systemd-run --user --scope -q -p MemoryMax=2G -E TMPDIR=/dev/shm -E PYTHONPATH=<raíz>:/dev/shm/sldb-main/src -- python -m pytest -q -p no:cacheprovider tests/<archivo>.py`.
b5 (texto de los mensajes, en inglés como el resto del CLI):
- d1, un hallazgo por archivo: "lifecycle seed out of date: desk/lifecycle/<archivo> differs from the deskops package (<campos que difieren>)", con fix "deskops desk update --apply".
- d2: "Cannot advance <task id> via <relation_type>: the edge desk/lifecycle/<archivo> does not set status <esperado> (attributes.sets.status is <visto o missing>). The desk's lifecycle seeds are out of date: run 'deskops desk update --apply'.", exit 1 y la tarea sin cambios en disco.
Los goldens de salida nuevos fijan esos textos.
b6 (fuente de verdad y punto de control de d2): advance compara la arista que va a aplicar, tal como la lee del desk, con lifecycle_table() de deskops/models/task_lifecycle.py (CC37, tabla del paquete con cache): mismo relation_type, mismo target y mismo sets.status. Si difieren, falla en deskops/lifecycle.py advance antes de aplicar efectos o escribir. No se lee ningún archivo extra por avance: la tabla ya está en cache. d1 usa la comparación de seed_desk(root, apply=False, restore_managed=True).
b7 (4 pasos del workflow de deskops, .github/workflows): sldb stores build --store .sldb; pytest, un proceso por archivo de tests/; sldb stores build --check --store .sldb; bash scripts/ci-knowledge-check.sh . Los corre el coordinador en clon limpio. El worker corre los archivos que toca y los que usan lo que cambia (test_lifecycle*, test_doctor*, test_cli, test_output_goldens).

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

