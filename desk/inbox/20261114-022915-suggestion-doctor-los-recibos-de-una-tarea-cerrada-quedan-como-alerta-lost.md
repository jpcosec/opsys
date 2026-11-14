---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-14T02:29:15'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# doctor: los recibos de una tarea cerrada quedan como alerta 'lost'

_Describe the incoming message with enough evidence to triage._

Visto en ftcourier el 14-11. Al cerrar una tarea con closeout commit o resolved-by, el archivo de la tarea se borra y sus ReviewDoc (preflight, bundle, evidence-*) quedan con el sujeto 'lost'. deskops doctor muestra una alerta por recibo para siempre: 10 alertas de FTC-25 y FTC-27. Los recibos son auditoría y no hay que borrarlos. Sugerencia: que el closeout re-ancle los recibos al commit de cierre o los marque archivados, o que doctor no alerte por recibos de tareas cerradas. Aparte: en ftcourier el enlace al store de deskops en .sldb/store.yaml tenía un '..' de más (apuntaba a /home/proyectos); se corrigió con 'sldb stores add --replace'.
