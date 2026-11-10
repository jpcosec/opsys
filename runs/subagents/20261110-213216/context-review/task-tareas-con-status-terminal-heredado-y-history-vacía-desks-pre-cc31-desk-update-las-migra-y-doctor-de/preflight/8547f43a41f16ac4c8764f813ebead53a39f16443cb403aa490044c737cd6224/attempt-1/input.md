FILE:desk/tasks/task-tareas-con-status-terminal-heredado-y-history-vacía-desks-pre-cc31-desk-update-las-migra-y-doctor-de.md
---
sldb:
  by: agent
  at: '2026-11-10T21:32:05Z'
  authority: generated
  via: create_document
id: task-tareas-con-status-terminal-heredado-y-history-vacía-desks-pre-cc31-desk-update-las-migra-y-doctor-de
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
- deskops/models/task_lifecycle.py
- deskops/cli/commands/desk.py
- deskops/workspace.py
- deskops/services/closure.py
- deskops/cli/commands/closeout.py
- deskops/doctor_findings.py
- tests/
- docs/
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-tasks-con-status-terminal-heredado-y-history-vac-a-el-validador-las-rechaza-desks-pre-cc31.md
---

# Tareas con status terminal heredado y history vacía (desks pre-CC31): desk update las migra y doctor/desk update no caen por un documento inválido

## Rationale

_Explain why this task exists or the business driver behind it._

Prioridad del overlord (2026-11-10), mismo origen que el task.debug de advance/doctor. En shared_llm-gateway una sola tarea superseded con history vacía hace fallar sldb stores check, doctor y desk update, y deja sin registrar los modelos de tareas. Hay 6 en el kit Chatbot_Infra y más en Governance y labchile.

## Goal

_Describe the concrete result this task must produce._

deskops desk update --apply migra las tareas heredadas según la tabla de d1 y reporta las que no puede decidir; doctor y desk update reportan los documentos inválidos uno por uno sin caer.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/models/task_lifecycle.py, deskops/cli/commands/desk.py, deskops/workspace.py, deskops/services/closure.py, deskops/cli/commands/closeout.py, deskops/doctor_findings.py, tests/, docs/, CHANGELOG.md. Fuera: relajar el validador más allá de cancelled, los desks de AntonIA y la gramática del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

REPORTE (nota de inbox cb515a4e, coordinador de AntonIA): desks migrados antes de CC31 tienen tareas con un status terminal heredado y history vacía, en current_node ritual-execution. Por ejemplo /srv/repos/Chatbot_Infra/desk/tasks/task-pyme-como-satelite.md (superseded). Conteos: kit Chatbot_Infra 6 (superseded); Governance varias (cancelled, y una active con history vacía); labchile 1; shared_llm-gateway 4. El validador de TaskDoc de CC37 (deskops/models/task_lifecycle.py, lifecycle_errors) las rechaza en toda lectura con modelo.

REPRODUCCIÓN (coordinador, copia de /srv/repos/shared_llm-gateway en 479b415, log runs/subagents/20261110-repro-legacy/repro.log):
- task-ci-propio-del-gateway y task-workflow-check-obligatorio-del-gateway: superseded, ritual-execution, history [].
- task-tope-por-tipo-y-pedidos-bloqueados: deferred, ritual-execution, history [].
- task-linea-base-de-lint-del-gateway y task-logs-de-llm-gateway-servir-sin-pii: draft, ritual-closeout, history [task_activates, task_hands_to_closeout].
- sldb stores check: 'Unexpected: 1 validation error for TaskDoc', rc 1.
- deskops doctor: 'SLDB store check crashed' más 'Unregistered models: ReviewDoc, Task*Doc'.
- deskops desk update (dry-run): falla con el mismo error. Con un solo documento inválido no hay forma de migrar ni de registrar modelos.

DEFECTOS DE DESKOPS (causa raíz escrita antes del arreglo):
d1 (sin vía de migración): no hay comando que lleve una tarea en un estado heredado incoherente a un estado que el validador acepte. Arreglo: 'deskops desk update --apply' migra esas tareas antes de registrar modelos. Escribe por la ruta de documentos sin pasar por el modelo, porque el modelo las rechaza, y reporta una línea por tarea: archivo, estado anterior y estado nuevo. Tabla de migración, con history vacía y current_node no vacío:
- superseded: history [superseded] (estado de closeout de CLOSEOUT_STATES); current_node se queda.
- closed, resolved, done, complete, cancelled: current_node '' (tarea fuera del ciclo de vida); status se queda. 'cancelled' se suma a LEGACY_RESOLVED_STATUSES, decisión revisable.
- deferred y candidate: current_node '' (estado de drawer).
- cualquier otro caso incoherente (active con history vacía; draft con history [task_activates, task_hands_to_closeout]; etc.): no se escribe. Se reporta como hallazgo con el arreglo sugerido (deskops advance o closeout según el caso), porque decidir su estado es del dueño de la tarea.
La migración es idempotente: una segunda corrida no cambia nada.
d2 (doctor y desk update caen enteros): con documentos inválidos por el validador del ciclo de vida, doctor y desk update deben reportarlos uno por uno, con archivo y mensaje, y seguir con el resto (registro de modelos incluido). Hoy caen con el ValidationError del primero. Si el corte está en sldb (stores check aborta en el primer documento inválido en lugar de dar un hallazgo), se deja como hipótesis con nota a sldb y deskops lo esquiva leyendo por la ruta de documentos.

FUERA: relajar el validador de CC37 para estados terminales con current_node (la tabla solo crece con 'cancelled' en LEGACY_RESOLVED_STATUSES); tocar los desks de AntonIA (sus dueños corren desk update --apply); la gramática del CLI (goldens de ayuda idénticos; los de salida, salvo los mensajes nuevos con golden propio).

REGLAS COMUNES: tests de a uno con TMPDIR=/dev/shm y la guarda de pgrep anclada; nada a mano en desk/ ni .sldb/; nunca git add -A; CHANGELOG (Fixed) y doc en docs/operator-manual.md (desk update y doctor); informe runs/subagents/<worker>-report.md con causa raíz; 4 pasos del workflow de deskops en clon limpio, los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test de reproducción sobre tmp_path con las cinco formas de la reproducción del gateway: antes falla, después desk update --apply migra o reporta según la tabla, y una segunda corrida no cambia nada
- doctor con una tarea inválida reporta el documento y sigue (registro de modelos incluido)
- Goldens de ayuda idénticos; los de salida, salvo los mensajes nuevos con golden propio
- En una copia de shared_llm-gateway en /dev/shm: desk update --apply y luego sldb stores check rc 0
- 4 pasos del workflow en clon limpio

## Done When

_Name the observable condition that makes the task complete._

d1 y d2 arreglados con causa raíz escrita y tests de reproducción verdes; la copia del gateway pasa stores check; doc y CHANGELOG.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-tareas-con-status-terminal-heredado-y-history-vacía-desks-pre-cc31-desk-update-las-migra-y-doctor-de: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

