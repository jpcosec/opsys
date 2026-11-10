---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: ftcourier
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-10T09:45:18'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# deskops derrama reglas de activacion y runtimes centrales en el desk del proyecto consumidor

_Describe the incoming message with enough evidence to triage._

Al correr 'deskops advance' y 'deskops closeout' sobre una tarea en un proyecto consumidor (ftcourier), deskops materializo sus reglas centrales de activacion (desk/lifecycle/rule-activation-task-*.md, 7 archivos) y el runtime de sistema (desk/runtimes/runtime-pi-deepseek-flash.md) dentro del desk del proyecto, como archivos SIN trackear. Son genericos (tag system:deskops) y su copia canonica vive en deskops/data/rules/. Otros proyectos (mepu) no los trackean. No deberian derramarse en el desk de cada consumidor. Sugerencia: leerlos desde el deskops central y no escribirlos en el desk del proyecto (o escribirlos de forma consistente y trackeable, no como spill suelto).
