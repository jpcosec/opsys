---
sldb:
  by: agent
  at: '2026-11-12T02:31:03Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper@sha256:d536fe6ec80904ac936f6f6946a8a7efe1f52fda1477489fc4bde6c087e463f2
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261112-022829/context-review/task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper/preflight/8fd8636c1e85b4662e1426ace2e22148414ff9aea96c8df311cb5f7037417e8a/attempt-1
input_sha256: 8fd8636c1e85b4662e1426ace2e22148414ff9aea96c8df311cb5f7037417e8a
output_sha256: 6cdfbeb8f65878a34b1240c87c9c3f6cf4fd1d3750559326f4e80f098f715f02
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) test_scion_runtime:
  se edita el bloque de sys.path de su cabecera como en los otros 17; la prueba que
  arma un árbol de trabajo falso con una carpeta sldb dentro no se toca. ''Fuera''
  se refiere a esa prueba concreta, no al archivo. (2) Ruta inexistente: pytest.UsageError
  al cargar el conftest (colecta), con el texto ''SLDB_SRC=<ruta> does not exist''.
  (3) El grep literal es grep -rn ''ROOT.parent / "sldb" / "src"'' tests/, y debe
  quedar vacío (sí puede aparecer la ruta por defecto dentro del helper). (4) Los
  4 pasos del CI de deskops: sldb stores build, pytest por archivo, sldb stores build
  --check y scripts/ci-knowledge-check.sh; los corre el coordinador. (5) docs/ no
  se toca (files solo trae tests/ y CHANGELOG.md): la línea sobre SLDB_SRC va al CHANGELOG
  y al docstring del helper. (6) ''Suite completa de a un archivo'' es cada tests/**/test_*.py
  en su propia invocación de pytest, precedida por wait-pytest; nunca pytest tests/
  entero. (7) El informe es runs/subagents/sldbsrc-worker-report.md y dice si el helper
  vive en conftest o en un módulo, y por qué. (8) Dispatch: esta tarea toca los mismos
  tests que CC35d resto; el coordinador la despacha cuando CC35d resto esté en main.
  (9) Baja del ítem de origen: deskops drawer remove al cierre.'
# ISO 8601 timestamp
created_at: '2026-11-12T02:28:46.336114+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-12T02:31:00.403349+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261112-022829/context-review/task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper/preflight/8fd8636c1e85b4662e1426ace2e22148414ff9aea96c8df311cb5f7037417e8a/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) test_scion_runtime: se edita el bloque de sys.path de su cabecera como en los otros 17; la prueba que arma un árbol de trabajo falso con una carpeta sldb dentro no se toca. 'Fuera' se refiere a esa prueba concreta, no al archivo. (2) Ruta inexistente: pytest.UsageError al cargar el conftest (colecta), con el texto 'SLDB_SRC=<ruta> does not exist'. (3) El grep literal es grep -rn 'ROOT.parent / "sldb" / "src"' tests/, y debe quedar vacío (sí puede aparecer la ruta por defecto dentro del helper). (4) Los 4 pasos del CI de deskops: sldb stores build, pytest por archivo, sldb stores build --check y scripts/ci-knowledge-check.sh; los corre el coordinador. (5) docs/ no se toca (files solo trae tests/ y CHANGELOG.md): la línea sobre SLDB_SRC va al CHANGELOG y al docstring del helper. (6) 'Suite completa de a un archivo' es cada tests/**/test_*.py en su propia invocación de pytest, precedida por wait-pytest; nunca pytest tests/ entero. (7) El informe es runs/subagents/sldbsrc-worker-report.md y dice si el helper vive en conftest o en un módulo, y por qué. (8) Dispatch: esta tarea toca los mismos tests que CC35d resto; el coordinador la despacha cuando CC35d resto esté en main. (9) Baja del ítem de origen: deskops drawer remove al cierre.
