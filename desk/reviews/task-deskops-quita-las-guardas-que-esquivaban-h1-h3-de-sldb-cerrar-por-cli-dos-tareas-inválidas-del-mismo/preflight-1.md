---
sldb:
  by: agent
  at: '2026-11-12T02:30:53Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-quita-las-guardas-que-esquivaban-h1-h3-de-sldb-cerrar-por-cli-dos-tareas-inválidas-del-mismo-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-quita-las-guardas-que-esquivaban-h1-h3-de-sldb-cerrar-por-cli-dos-tareas-inválidas-del-mismo@sha256:09aa564df958d09f86f85bc34db5106be9fb65dd2f80834d8ada946ecb0527b6
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261112-022721/context-review/task-deskops-quita-las-guardas-que-esquivaban-h1-h3-de-sldb-cerrar-por-cli-dos-tareas-inválidas-del-mismo/preflight/9dc98c47fae33473e4b8bd661dcd127ae1d0ccd599d66de0d22d5e328f249f76/attempt-1
input_sha256: 9dc98c47fae33473e4b8bd661dcd127ae1d0ccd599d66de0d22d5e328f249f76
output_sha256: feddaee1a19604f97442589a6106b0823b1eaa0042c58262707f6df30b1acb6e
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) doctor_findings.py
  SÍ se modifica (g3): ''fuera de alcance'' significa que el listado de tareas inválidas
  por frontmatter se queda como está y solo se le suma la lectura del hallazgo store/doc-invalid
  de sldb. (2) Las dos funciones de g1 son _other_invalid_tasks y _blocked_by_invalid_tasks
  de closure.py; ''sin uso'' es un grep sin llamadores en deskops/ y en tests/. (3)
  ''Falla de verdad'' en g2: stores check sin JSON parseable en stdout y con rc distinto
  de 0; se mantiene el DeskopsEnvironmentError de hoy. La rama store_check_error desaparece:
  con sldb corregido stores check siempre entrega informe aunque haya documentos inválidos.
  (4) Qué sldb usar: un clon de sldb origin/main en /dev/shm, comprobando antes con
  un grep que su código trae el hallazgo store/doc-invalid; si la tarea de SLDB_SRC
  ya entró, se apunta con la variable SLDB_SRC, y si no, con la ruta hermana de la
  copia. Si el sldb de main todavía no trae el hallazgo, el worker para y avisa. (5)
  Deduplicación en g3: la clave es la ruta relativa del documento; el listado por
  frontmatter manda y el hallazgo de sldb suma solo los que el frontmatter no listó;
  orden por ruta. (6) Caché frío: en cada test, el .sldb_cache del store se borra
  y XDG_CACHE_HOME apunta a un directorio vacío dentro de tmp_path, con un helper
  o fixture común que el worker agrega a los tests de este cambio. (7) Los 4 pasos
  del CI de deskops: sldb stores build, pytest por archivo, sldb stores build --check
  y scripts/ci-knowledge-check.sh; los corre el coordinador. (8) El informe es runs/subagents/guards-worker-report.md;
  el ítem de drawer 75e33dab se da de baja con deskops drawer remove.'
# ISO 8601 timestamp
created_at: '2026-11-12T02:27:39.444754+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-12T02:30:50.750424+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-deskops-quita-las-guardas-que-esquivaban-h1-h3-de-sldb-cerrar-por-cli-dos-tareas-inválidas-del-mismo

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261112-022721/context-review/task-deskops-quita-las-guardas-que-esquivaban-h1-h3-de-sldb-cerrar-por-cli-dos-tareas-inválidas-del-mismo/preflight/9dc98c47fae33473e4b8bd661dcd127ae1d0ccd599d66de0d22d5e328f249f76/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) doctor_findings.py SÍ se modifica (g3): 'fuera de alcance' significa que el listado de tareas inválidas por frontmatter se queda como está y solo se le suma la lectura del hallazgo store/doc-invalid de sldb. (2) Las dos funciones de g1 son _other_invalid_tasks y _blocked_by_invalid_tasks de closure.py; 'sin uso' es un grep sin llamadores en deskops/ y en tests/. (3) 'Falla de verdad' en g2: stores check sin JSON parseable en stdout y con rc distinto de 0; se mantiene el DeskopsEnvironmentError de hoy. La rama store_check_error desaparece: con sldb corregido stores check siempre entrega informe aunque haya documentos inválidos. (4) Qué sldb usar: un clon de sldb origin/main en /dev/shm, comprobando antes con un grep que su código trae el hallazgo store/doc-invalid; si la tarea de SLDB_SRC ya entró, se apunta con la variable SLDB_SRC, y si no, con la ruta hermana de la copia. Si el sldb de main todavía no trae el hallazgo, el worker para y avisa. (5) Deduplicación en g3: la clave es la ruta relativa del documento; el listado por frontmatter manda y el hallazgo de sldb suma solo los que el frontmatter no listó; orden por ruta. (6) Caché frío: en cada test, el .sldb_cache del store se borra y XDG_CACHE_HOME apunta a un directorio vacío dentro de tmp_path, con un helper o fixture común que el worker agrega a los tests de este cambio. (7) Los 4 pasos del CI de deskops: sldb stores build, pytest por archivo, sldb stores build --check y scripts/ci-knowledge-check.sh; los corre el coordinador. (8) El informe es runs/subagents/guards-worker-report.md; el ítem de drawer 75e33dab se da de baja con deskops drawer remove.
