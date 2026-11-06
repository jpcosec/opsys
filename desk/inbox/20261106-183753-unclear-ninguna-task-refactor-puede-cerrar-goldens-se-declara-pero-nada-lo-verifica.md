---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T18:37:53'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Ninguna task.refactor puede cerrar: goldens se declara pero nada lo verifica

_Describe the incoming message with enough evidence to triage._

Hueco sistémico, hallado al cerrar CC30 (squash 93cc1943; código en main, tests verdes, evidencia 1763823b). GC01 hizo que task.refactor declare la evidencia de cierre goldens. deskops/services/closeout_gates.py tiene NOT_YET_VERIFIABLE_EVIDENCE = ("children", "goldens"), y verify_task_closeout (deskops/services/closure.py, verify_task_closeout) agrega closeout_evidence_not_verifiable por cada kind de esa tupla. Ningún nodo autorizado verifica goldens todavía, así que closeout verify falla siempre y NINGUNA task.refactor puede cerrar (lo mismo pasa con task.aggregate y children). GC06 impide además editar task_type o closeout_evidence, y no se relajó nada. Decisión del dueño, entre: (a) las task.refactor quedan abiertas, con su código en main, hasta que un nodo implemente la verificación de goldens (es lo que se aplica hoy a CC30); (b) el dueño autoriza otra forma de cerrarlas mientras tanto, por ejemplo verificar goldens como tests de tests/test_output_goldens.py, o un cierre manual con razón; (c) adelantar como nodo propio la verificación de goldens (y de children) en closeout_gates, antes de seguir creando task.refactor. Afecta a CC30 y a toda task.refactor futura del plan deskops-como-config. Coordinador de proyecto SLDB_1, por pedido del overlord, 2026-11-06.
