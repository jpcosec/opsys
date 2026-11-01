## REFORMULACION

**Objetivo.** Verificar con evidencia si el registro P01–P09 de `desk/drawer/plans/workspace-documental/decisiones.md` ya satisface la aceptación de WS07 y dejar el dictamen en `runs/subagents/20261031-ws07-decisiones/coverage-report.md`. Si está cubierto, no se reescribe nada.

**Alcance.** Solo lectura de `decisiones.md`, `runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json`, `dag.yaml` y `phase-closeout.md`. Escritura limitada a `coverage-report.md` (y `result-summary.md` según Scope/Path). Por cada Pxx: resultado, tipo humano/técnico, actor, fuente, nodos y gates; citas literales de ítems 0–2; P07/P09 como defaults técnicos; baseline_proposal y `source_mode`; estado G_PRODUCT/G_WRITE_POLICY; defecto real se describe, no se corrige.

**Repo.** `/home/jp/proyectos/SLDB_1/deskops` (cwd `deskops`).

**Límites.** Sin editar `decisiones.md`, `dag.yaml`, código, Scion ni UI; sin preguntar al solicitante; sin WS08–12; sin push ni suite general.

## AMBIGUEDADES

1. «Primero verificar. Comprobar en runs/subagents/20261031-ws07-decisiones/coverage-report.md, por cada Pxx…» frente a «dejar el resultado en» el mismo archivo. No queda claro si el informe preexiste (de una corrida previa) y se audita, o si se crea ahora. Obliga a inventar el estado inicial.
2. «Comprobar que baseline_proposal y parameters.source_mode coinciden con las respuestas». No nombra el archivo ni la ruta exacta donde vive `parameters.source_mode`. Obliga a inventar ubicación y clave.
3. `files:` declara solo `coverage-report.md`, pero Scope e Implementation Path ordenan escribir también `result-summary.md`. Obliga a decidir si ese archivo está autorizado aunque no figure en `files`.
4. `closeout_evidence: [commit, document]` no identifica qué documento satisface `document`. Obliga a asumir que es `coverage-report.md`.

## DRY-RUN

1. Comprobar existencia de `runs/subagents/20261031-ws07-decisiones/` y de `coverage-report.md`; si falta el directorio, crearlo; si falta el informe, crearlo.
2. Leer `decisiones.md`, `owner-decisions.json` y `dag.yaml`.
3. Redactar tabla P01–P09: ID, resultado, tipo/actor, fuente (ítem literal para humanas), nodos y gates; para P07/P09 marcar «técnica delegada, sin firma humana».
4. Cotejar literalmente las respuestas 0–2 de `owner-decisions.json` contra las citas de `decisiones.md`.
5. Verificar que cada nodo/gate citado existe en `dag.yaml`.
6. Contrastar `baseline_proposal` y `source_mode` con las respuestas; registrar estado de G_PRODUCT y G_WRITE_POLICY sin inferir API/UI ni Scion.
7. Emitir dictamen: cubierto, o defecto real con cita textual y ubicación (sin corregir).
8. Escribir `result-summary.md`.

**Errores esperables:** archivo o nodo/gate inexistente → defecto real documentado; cita no literal → defecto; discrepancia de `source_mode` → defecto.

**Resultado esperado:** `coverage-report.md` no vacío y trazable; `build --check`, `validate --check` y `status` en verde; Tester independiente PASS. No se ejecuta nada aquí.
