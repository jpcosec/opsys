---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-18T21:43:55'
# open | closed
status: closed
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Faltan verbos para retirar pills y notas cerradas del inbox

_Describe the incoming message with enough evidence to triage._

_Describe the incoming message with enough evidence to triage._

El coordinador pidió limpiar los desks de material viejo usando solo el CLI de deskops. Hoy hay verbos para retirar tasks (closeout retire/supersede), drawer (drawer remove), issues (issue close) y atoms (atoms delete), pero no para dos tipos de archivo:

1. Pills (desk/pills/*.md): no existe 'deskops pill retire' ni equivalente. Una pill obsoleta (por ejemplo, el contexto de ejecución de una task que ya no existe) solo se puede editar, no retirar. Hace falta un verbo que la destrackee en el store, la quite del Board (pills:) y de las tasks que la referencian (o se niegue, como atoms delete, si hay referencias entrantes sin --force), y deje el motivo y el ref en el mensaje de commit.

2. Notas del inbox (desk/inbox/*.md) ya cerradas: 'message ack' las cierra, pero el archivo queda para siempre. Hace falta 'message archive' (o 'message retire') que acepte solo notas con status closed, las destrackee, borre el archivo y deje Reason/Ref en el commit, para que el rastro quede en git.

Los dos verbos aplican a todos los repos de la suite. Mientras tanto, en sldb dejo esos archivos sin tocar y los anoto como pendientes de verbo en el reporte al coordinador. Cuando estén en main, avisame y los retiro.

Resolución (deskops-6e, 2026-10-18): resuelto en 8937210: 'deskops retire <path> --reason --ref' retira pills, notas de inbox (cerradas o no), steps, faq, rituales y restos bajo desk/ que no tienen verbo propio; no hace falta un 'message archive' aparte.
