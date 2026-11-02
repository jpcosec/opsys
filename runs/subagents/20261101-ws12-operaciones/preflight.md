## REFORMULACION

**Objetivo:** crear `desk/drawer/plans/workspace-documental/contratos/operaciones.md` con 13 secciones obligatorias que fijen la matriz de operaciones (modelo, campo, canal, actor, revisión, Git, efectos, estado) y separen capacidades existentes con evidencia citable de huecos con dueño y productor.

**Alcance:** solo ese contrato y `runs/subagents/20261101-ws12-operaciones/result-summary.md`. Debe leer referencias, código real en el commit citado, auditorías, flujos y vistas.

**Repo:** `/home/jp/proyectos/SLDB_1/deskops`, workspace `desk`.

**Límites:** sin commits ni revisiones; sin código UI/API/sldb; sin actas interrepo; sin habilitar mutaciones; sin Scion, push, `dag.yaml`, fuentes comunes, helper, validadores ni suite general; repos hermanos solo lectura; no preguntar al solicitante. `execution_authorized` global sigue `false`.

## AMBIGUEDADES

1. **“los comandos de diagnóstico clasificados por efectos”**: no enumera comandos. Obligaría a inventar el conjunto y su clasificación.
2. **“WS12 elige justificadamente la representación, las operaciones y los escritores alcanzados”**: no fija criterios de elección. Obligaría a inventar la justificación.
3. **“G_WRITE_CONTRACT y G_UI_WRITE por IDs y efecto”**: no da los IDs. Obligaría a inventarlos.
4. **“sección por delta de WS34.1 y WS34.2”**: no enumera deltas. Obligaría a inventar el desglose.
5. **“con prueba real”** (captura a drawer): no define prueba ni harness. Obligaría a inventar qué cuenta como prueba.
6. **“revisiones afectadas renovadas solo si hay staleness medida”**: no define cómo medirla. Obligaría a inventar el criterio.

## DRY-RUN

El ejecutor futuro, sin ejecutar aquí:

1. Leería `review-source.md` (última parte), `dag.yaml` (WS12), `decisiones.md` (T-P03.1), `navegacion.md`, auditorías, `user-flows.md` y `vistas.md`.
2. Abriría el código real citado y anotaría `path:línea` o símbolo del commit.
3. Escribiría `operaciones.md` en el orden de las 13 secciones, con matriz, huecos, trazabilidad y distinción existe/aceptado y estático/runtime.
4. Escribiría `result-summary.md`.
5. Ejecutaría: `test -s .../operaciones.md`, `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status`; un Tester independiente dejaría `tester-result-summary.md`.

**Errores esperables:** archivo ausente, check en rojo, Tester FAIL, staleness no medida, evidencia sin línea. **Resultado esperado:** contrato publicado, checks verdes, Tester PASS, sin commits.
