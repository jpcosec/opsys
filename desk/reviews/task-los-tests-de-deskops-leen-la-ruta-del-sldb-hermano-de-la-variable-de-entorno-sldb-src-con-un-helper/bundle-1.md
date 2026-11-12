---
sldb:
  by: agent
  at: '2026-11-12T02:30:58Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
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
run_dir: runs/subagents/20261112-022848/context-review/task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper/bundle/8202a6347dcb9df6ffda43fe1cb11a8e2c0cd95196e29f133b7bf9c98ef31ae3/attempt-1
input_sha256: 8202a6347dcb9df6ffda43fe1cb11a8e2c0cd95196e29f133b7bf9c98ef31ae3
output_sha256: a0620ef135749fe7979fbc89cd64a15a7e9fea401d22e260f2578b584eecbc86
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
created_at: '2026-11-12T02:29:03.338182+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-12T02:30:55.612114+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261112-022848/context-review/task-los-tests-de-deskops-leen-la-ruta-del-sldb-hermano-de-la-variable-de-entorno-sldb-src-con-un-helper/bundle/8202a6347dcb9df6ffda43fe1cb11a8e2c0cd95196e29f133b7bf9c98ef31ae3/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) test_scion_runtime: se edita el bloque de sys.path de su cabecera como en los otros 17; la prueba que arma un árbol de trabajo falso con una carpeta sldb dentro no se toca. 'Fuera' se refiere a esa prueba concreta, no al archivo. (2) Ruta inexistente: pytest.UsageError al cargar el conftest (colecta), con el texto 'SLDB_SRC=<ruta> does not exist'. (3) El grep literal es grep -rn 'ROOT.parent / "sldb" / "src"' tests/, y debe quedar vacío (sí puede aparecer la ruta por defecto dentro del helper). (4) Los 4 pasos del CI de deskops: sldb stores build, pytest por archivo, sldb stores build --check y scripts/ci-knowledge-check.sh; los corre el coordinador. (5) docs/ no se toca (files solo trae tests/ y CHANGELOG.md): la línea sobre SLDB_SRC va al CHANGELOG y al docstring del helper. (6) 'Suite completa de a un archivo' es cada tests/**/test_*.py en su propia invocación de pytest, precedida por wait-pytest; nunca pytest tests/ entero. (7) El informe es runs/subagents/sldbsrc-worker-report.md y dice si el helper vive en conftest o en un módulo, y por qué. (8) Dispatch: esta tarea toca los mismos tests que CC35d resto; el coordinador la despacha cuando CC35d resto esté en main. (9) Baja del ítem de origen: deskops drawer remove al cierre.
