## REFORMULACION

**Objetivo:** dejar `desk/drawer/plans/workspace-documental/decisiones.md` con procedencia humana y técnica explícita y fuentes reales en P01, P03–P07 y P09, sin alterar ninguna decisión, y renovar las 73 revisiones.

**Alcance:** parche único en `decisiones.md`. Contrato obligatorio: `runs/subagents/20261031-atribucion-decisiones/review-source.md`; hallazgos en `runs/subagents/20261031-ws07-decisiones/coverage-report.md`. En P01/P03–P06 la afirmación humana conserva solo lo aceptado en pregunta/respuesta; las precisiones técnicas pasan a una derivación técnica rotulada con fuente exacta. P07/P09 siguen técnicas y se sustituye la fuente sin ruta por la real. Mapa en `attribution-map.md`. El Executor edita solo `decisiones.md` y escribe `attribution-map.md` y `result-summary.md`, sin commits; el Supervisor congela, ejecuta `context_review.py run --stale`, valida y cierra.

**Repo:** `deskops` (cwd `/home/jp/proyectos/SLDB_1/deskops`). Baseline de diff: `7b045a6f..HEAD`.

**Límites:** no cambian IDs, preguntas/respuestas literales, `source_tool_call`, decisiones, restricciones, actores, nodos ni gates; P02/P08 no se reescriben; no WS45, O1–O5, helper, validadores, código, UI, Scion, WS08-12, push, suite general ni preguntas al solicitante.

## AMBIGUEDADES

1. "las 73 revisiones renovadas" / "las 73 entradas se renuevan": no se enumeran. Obligaría a inventar qué 73 unidades cuentan (entradas, bundles o revisiones).
2. "commit si aplica": no define cuándo aplica. Obligaría a inventar hashes o criterio de inclusión.
3. "Buscar el registro técnico histórico de rutas/aliases, registry y WS43": no da rutas ni ventana temporal. Obligaría a inventar ubicaciones de fuentes.
4. "helper sin cambios": no nombra el helper; se infiere `context_review.py`. Obligaría a inventar el binario si no se infiere.
5. "disposiciones actuales con v2": no define "v2". Obligaría a inventar el formato de disposición.
6. "Agente preparatorio: puede redactar borradores de disposición": no aclara si sus borradores son vinculantes. Obligaría a inventar su autoridad.
7. "Tester independiente de solo lectura": no fija criterio de independencia. Obligaría a inventar el mecanismo de verificación.

## DRY-RUN

1. Leer contrato, coverage-report, `decisiones.md`, `owner-decisions.json`, `context-review.md`; revisar `git log` de `decisiones.md` y runs previos del plan para el registro histórico.
2. Redactar `runs/subagents/20261031-atribucion-decisiones/attribution-map.md`: por fragmento P01–P09, tipo (humana/técnica/derivada), fuente exacta (path, sección/líneas, commit) y límite.
3. Editar solo `decisiones.md`: P01/P03–P06 separan afirmación humana y derivación técnica rotulada; P07/P09 sustituyen fuente sin ruta por la real o se etiquetan derivadas declarando el límite. No tocar IDs, Q&A, `source_tool_call`, decisiones, actores ni gates.
4. Escribir `result-summary.md`; no commitear.
5. Errores previstos: fuente histórica inexistente → etiquetar derivada sin inventar autor/fecha; diff fuera de alcance; `build --check`/`validate --check` en rojo; `status` con stale.
6. Resultado esperado: `attribution-map.md` no vacío, diff limitado a `decisiones.md` y artefactos del run, 73 bundles renovados, checks y Tester en verde.
