---
sldb:
  by: agent
  at: '2026-11-11T22:50:10Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com@sha256:ac1473c253a28d7138bd53cd675f0f63560dca300988ea0b39649a0e241c6dc1
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261111-224928/context-review/task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com/bundle/30436bab32b0df9096437deb00e9f978c3a77ba11a5807bfa94492fa1638d53d/attempt-1
input_sha256: 30436bab32b0df9096437deb00e9f978c3a77ba11a5807bfa94492fa1638d53d
output_sha256: c28e2d31268a056aa55cc76bd1f402a26717b34ad493fac6d5c40190efb7c9df
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Lugar
  único: la normalización vive en un helper de deskops/doc_access.py (o junto a él),
  y la llama DeskopsOperations.edit_artifact_field antes de escribir, de modo que
  todos los subjects de edit pasan por ahí. (2) Fuente de verdad de los placeholders:
  la plantilla del propio modelo, es decir, los párrafos literales en cursiva que
  extract descarta (el mismo criterio de cff4f30a y de sldb 9dcabd9a), no una lista
  escrita a mano. Si _TASK_SECTION_PLACEHOLDERS de promote.py coincide con la plantilla,
  pasa a leer de la misma fuente; si difiere, el worker lo dice en el informe y gana
  la plantilla. workspace.py solo tiene el placeholder de nombre de proyecto (CC36),
  que no es de sección: no se toca. (3) Alcance: los campos string de sección de los
  modelos cuya plantilla tiene párrafos placeholder; el worker los enumera en el informe
  por grep de las plantillas. Un campo no string (lista, frontmatter) no se normaliza.
  (4) ''Vacío'' es el string vacío del campo. (5) El segundo subject cubierto es inbox-note,
  cuya plantilla trae ''_Describe the incoming message with enough evidence to triage._''.
  (6) El informe es runs/subagents/placeholder-worker-report.md, y la causa raíz va
  commiteada antes del arreglo. (7) Los 4 pasos del CI de deskops son sldb stores
  build, pytest por archivo, sldb stores build --check y scripts/ci-knowledge-check.sh;
  los corre el coordinador.'
# ISO 8601 timestamp
created_at: '2026-11-11T22:49:46.078998+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-11T22:50:07.437415+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261111-224928/context-review/task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com/bundle/30436bab32b0df9096437deb00e9f978c3a77ba11a5807bfa94492fa1638d53d/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Lugar único: la normalización vive en un helper de deskops/doc_access.py (o junto a él), y la llama DeskopsOperations.edit_artifact_field antes de escribir, de modo que todos los subjects de edit pasan por ahí. (2) Fuente de verdad de los placeholders: la plantilla del propio modelo, es decir, los párrafos literales en cursiva que extract descarta (el mismo criterio de cff4f30a y de sldb 9dcabd9a), no una lista escrita a mano. Si _TASK_SECTION_PLACEHOLDERS de promote.py coincide con la plantilla, pasa a leer de la misma fuente; si difiere, el worker lo dice en el informe y gana la plantilla. workspace.py solo tiene el placeholder de nombre de proyecto (CC36), que no es de sección: no se toca. (3) Alcance: los campos string de sección de los modelos cuya plantilla tiene párrafos placeholder; el worker los enumera en el informe por grep de las plantillas. Un campo no string (lista, frontmatter) no se normaliza. (4) 'Vacío' es el string vacío del campo. (5) El segundo subject cubierto es inbox-note, cuya plantilla trae '_Describe the incoming message with enough evidence to triage._'. (6) El informe es runs/subagents/placeholder-worker-report.md, y la causa raíz va commiteada antes del arreglo. (7) Los 4 pasos del CI de deskops son sldb stores build, pytest por archivo, sldb stores build --check y scripts/ci-knowledge-check.sh; los corre el coordinador.
