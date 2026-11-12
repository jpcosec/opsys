---
sldb:
  by: agent
  at: '2026-11-12T03:40:17Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta@sha256:5691bcd2ef45f2f82f13edb7d3d7800ff6d57bfc06fe0c8f730258c5c57c8197
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261112-033829/context-review/task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta/preflight/85e401bd354af5d51a8490b87a026006a0178f663cd7a2327e9af462145acd29/attempt-1
input_sha256: 85e401bd354af5d51a8490b87a026006a0178f663cd7a2327e9af462145acd29
output_sha256: 1e1d2cc5beba5ef8a951b57c1ab7260b6609f6cde877812b77f822c7ab19b485
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Estados
  de caché: caliente es el store construido (sldb stores build hecho) con la caché
  de composición de H11 ya escrita por una corrida anterior en otro proceso; frío
  es sin ninguna caché de disco (sin .sldb_cache y con XDG_CACHE_HOME vacío). La meta
  de 2,5 s aplica en caliente; en frío solo se mide y se informa, y no puede empeorar.
  (2) Qué sldb: el worker clona sldb origin/main en /dev/shm, comprueba con un grep
  que trae la caché de composición de H11 (el módulo composed_disk en store/edge_index)
  y mide contra ese clon con PYTHONPATH; si no la trae, para y avisa. (3) Layout:
  lo arma el benchmark que dejó H11 en sldb main (tests/perf/h11_bench_run_view.sh),
  tal cual, con worktrees en /dev/shm de deskops (la rama del worker), spec2viz, pron
  y scion; el informe registra los SHA. (4) Llamadas a open_store (p3): el perfil
  de p1 cuenta las de hoy (31 según el h11-worker); la meta es bajar al menos a la
  mitad (15 o menos) y, si el mínimo posible es mayor, el worker lo justifica con
  el perfil. El manejo de errores observable se conserva: _gates sigue convirtiendo
  una falla de transiciones en el error de la tarjeta y _closeout sigue registrando
  verify_task_closeout failed; un test fuerza cada falla y lo fija. (5) Comparación
  de salida (p4): el test compara contra una captura de la salida de hoy de view board
  y de view task sobre un desk de prueba, tomada y commiteada ANTES del cambio (en
  p1); si los goldens de test_view_goldens ya cubren tarjetas en varios nodos, se
  usan, y si no, el worker agrega la fixture. (6) view task entra en la comparación
  siempre, porque comparte show_task y el closeout; el cambio no la altera. (7) Los
  4 pasos del CI de deskops: sldb stores build, pytest por archivo, sldb stores build
  --check y scripts/ci-knowledge-check.sh; los corre el coordinador. (8) El informe
  es runs/subagents/boardperf-worker-report.md.'
# ISO 8601 timestamp
created_at: '2026-11-12T03:38:47.770329+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-12T03:40:15.103797+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261112-033829/context-review/task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta/preflight/85e401bd354af5d51a8490b87a026006a0178f663cd7a2327e9af462145acd29/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptada; las ambigüedades se resuelven así (coord2, revisable). (1) Estados de caché: caliente es el store construido (sldb stores build hecho) con la caché de composición de H11 ya escrita por una corrida anterior en otro proceso; frío es sin ninguna caché de disco (sin .sldb_cache y con XDG_CACHE_HOME vacío). La meta de 2,5 s aplica en caliente; en frío solo se mide y se informa, y no puede empeorar. (2) Qué sldb: el worker clona sldb origin/main en /dev/shm, comprueba con un grep que trae la caché de composición de H11 (el módulo composed_disk en store/edge_index) y mide contra ese clon con PYTHONPATH; si no la trae, para y avisa. (3) Layout: lo arma el benchmark que dejó H11 en sldb main (tests/perf/h11_bench_run_view.sh), tal cual, con worktrees en /dev/shm de deskops (la rama del worker), spec2viz, pron y scion; el informe registra los SHA. (4) Llamadas a open_store (p3): el perfil de p1 cuenta las de hoy (31 según el h11-worker); la meta es bajar al menos a la mitad (15 o menos) y, si el mínimo posible es mayor, el worker lo justifica con el perfil. El manejo de errores observable se conserva: _gates sigue convirtiendo una falla de transiciones en el error de la tarjeta y _closeout sigue registrando verify_task_closeout failed; un test fuerza cada falla y lo fija. (5) Comparación de salida (p4): el test compara contra una captura de la salida de hoy de view board y de view task sobre un desk de prueba, tomada y commiteada ANTES del cambio (en p1); si los goldens de test_view_goldens ya cubren tarjetas en varios nodos, se usan, y si no, el worker agrega la fixture. (6) view task entra en la comparación siempre, porque comparte show_task y el closeout; el cambio no la altera. (7) Los 4 pasos del CI de deskops: sldb stores build, pytest por archivo, sldb stores build --check y scripts/ci-knowledge-check.sh; los corre el coordinador. (8) El informe es runs/subagents/boardperf-worker-report.md.
