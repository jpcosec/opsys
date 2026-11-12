---
sldb:
  by: agent
  at: '2026-11-12T02:30:43Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-add-task-y-el-doctor-sugieren-task-external-o-una-tarea-espejo-cuando-los-files-o-las-referencias-de-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-add-task-y-el-doctor-sugieren-task-external-o-una-tarea-espejo-cuando-los-files-o-las-referencias-de@sha256:a0ca8b107bef4c2dfd8569e00d6f41469a599b0774db37e58ff55708a84bf3c6
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261112-022557/context-review/task-add-task-y-el-doctor-sugieren-task-external-o-una-tarea-espejo-cuando-los-files-o-las-referencias-de/preflight/c972a6fe16a6557a839713dd93a2ee46cb2c8813120b302aa06140dd596212b6/attempt-1
input_sha256: c972a6fe16a6557a839713dd93a2ee46cb2c8813120b302aa06140dd596212b6
output_sha256: 59148cab8807bb67412eff4267be62b3f4ef61c39921edec2bbd6e621b367fd3
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Alcance:
  solo los files del TaskDoc disparan el aviso y la alerta; las references no (el
  título las nombra, pero el cambio, a1-a3, habla solo de files). (2) Precondición:
  antes de empezar el worker comprueba en main la función que lee el registro del
  ecosistema en closeout_gates (la de las referencias calificadas de resolved-by);
  si no está, para y avisa. (3) Base de una ruta relativa: la raíz del repo del desk;
  una ruta que empieza por la carpeta padre se resuelve contra ella con resolve normal
  y se compara con las raíces registradas. (4) Tarea abierta: status distinto de closed,
  resolved, done, complete, superseded y cancelled; no cuentan las del drawer. (5)
  task.external se identifica por task_type igual a task.external. (6) Aviso en add
  task: texto exacto ''Files of <id> belong to repository <repo-id>; if the work lives
  there consider task_type task.external or a mirror task in its desk.'' a stdout
  en el formato de texto; si add task ya tiene una salida estructurada, va en su clave
  warnings, y si no la tiene no hay nada que decidir. (7) Alerta del doctor: severidad
  alert, en el formato de las demás alertas de doctor_findings, sin cambiar el código
  de salida. (8) El informe es runs/subagents/xrepoa-worker-report.md; los desks reales
  de AntonIA no son accesibles: la evidencia son el caso de la nota a79fe2d6 y fixtures
  en tmp_path con dos repos registrados; no se toca ningún desk real. (9) Baja del
  ítem de origen: deskops drawer remove <id>. (10) Los 4 pasos del CI de deskops:
  sldb stores build, pytest por archivo, sldb stores build --check y scripts/ci-knowledge-check.sh;
  los corre el coordinador.'
# ISO 8601 timestamp
created_at: '2026-11-12T02:26:10.938516+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-12T02:30:41.061291+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-add-task-y-el-doctor-sugieren-task-external-o-una-tarea-espejo-cuando-los-files-o-las-referencias-de

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261112-022557/context-review/task-add-task-y-el-doctor-sugieren-task-external-o-una-tarea-espejo-cuando-los-files-o-las-referencias-de/preflight/c972a6fe16a6557a839713dd93a2ee46cb2c8813120b302aa06140dd596212b6/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Alcance: solo los files del TaskDoc disparan el aviso y la alerta; las references no (el título las nombra, pero el cambio, a1-a3, habla solo de files). (2) Precondición: antes de empezar el worker comprueba en main la función que lee el registro del ecosistema en closeout_gates (la de las referencias calificadas de resolved-by); si no está, para y avisa. (3) Base de una ruta relativa: la raíz del repo del desk; una ruta que empieza por la carpeta padre se resuelve contra ella con resolve normal y se compara con las raíces registradas. (4) Tarea abierta: status distinto de closed, resolved, done, complete, superseded y cancelled; no cuentan las del drawer. (5) task.external se identifica por task_type igual a task.external. (6) Aviso en add task: texto exacto 'Files of <id> belong to repository <repo-id>; if the work lives there consider task_type task.external or a mirror task in its desk.' a stdout en el formato de texto; si add task ya tiene una salida estructurada, va en su clave warnings, y si no la tiene no hay nada que decidir. (7) Alerta del doctor: severidad alert, en el formato de las demás alertas de doctor_findings, sin cambiar el código de salida. (8) El informe es runs/subagents/xrepoa-worker-report.md; los desks reales de AntonIA no son accesibles: la evidencia son el caso de la nota a79fe2d6 y fixtures en tmp_path con dos repos registrados; no se toca ningún desk real. (9) Baja del ítem de origen: deskops drawer remove <id>. (10) Los 4 pasos del CI de deskops: sldb stores build, pytest por archivo, sldb stores build --check y scripts/ci-knowledge-check.sh; los corre el coordinador.
