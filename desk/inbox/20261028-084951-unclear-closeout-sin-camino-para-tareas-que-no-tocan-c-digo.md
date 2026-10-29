---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: mepu_ocs_dev
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-28T08:49:51'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-29T10:45:11'
---

# closeout sin camino para tareas que no tocan código

_Describe the incoming message with enough evidence to triage._

deskops closeout commit --no-run exige evidencia de tests y un átomo (missing_tests_evidence, missing_atom_or_materialization_link). Una tarea ejecutada fuera del repo, como LIN-1 (limpieza de Linear en mepu, 28-10), no tiene ninguna de las dos, y no hay forma de cerrarla sin citar un test que no la verifica. Propuesta: un modo de cierre para tareas sin código (p. ej. --external con la referencia externa como evidencia) o que la validación de la tarea declare que no lleva tests.
