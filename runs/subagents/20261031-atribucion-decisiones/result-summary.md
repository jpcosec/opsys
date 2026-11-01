# Resultado del Executor: atribución en decisiones.md

Único archivo editado: `desk/drawer/plans/workspace-documental/decisiones.md`. Mapa: `runs/subagents/20261031-atribucion-decisiones/attribution-map.md`.

- P01: celda de tipo marca «recepción técnica pendiente por delta» como Técnica derivada (T-P01). Resultado intacto.
- P03: resultado reducido a la premisa de la pregunta ítem 1; «canal público, autoridad compartida CLI/agentes/UI, probado; lock solo UI no basta» pasa a T-P03.
- P04: resultado conserva solo la respuesta ítem 1; «con revisión» y «recuperación» pasan a T-P04.
- P05: queda «Guardar no hace commit; cierre respeta el workflow Deskops»; «CLI/coordinador» y «refresco verificable» pasan a T-P05.
- P06: queda la premisa de la pregunta; «preparar» y «canal completo comprobado» pasan a T-P06.
- P07, P09: la fuente «Executor por encargo TaskDoc v2» se sustituye por «sin firma humana; fuente en T-P07/T-P09», con sección nueva «Procedencia técnica» (tabla, rutas, líneas, commits).
- P02, P08, columna de nodos y gates, IDs, preguntas/respuestas, source_tool_call: sin cambio.

Verificación por script: respuestas 0-2 literales (1 aparición cada una), source_tool_call 1 vez, 9 filas Pxx.

Límites: la Tabla inicial (35543965) no declara autor; "canal completo" y "refresco verificable" sin respaldo vigente en dag.yaml. Sin commits ni `context_review.py run`.

## Adenda 2026-10-31, revisión del Supervisor antes de congelar

Claude Opus 5.5, pane `w3Y:p1`, abrió cada rango de `dag.yaml` citado y corrigió tres celdas de `decisiones.md` directamente, sin Executor. Las filas anteriores de este mapa quedan como se escribieron; donde difieran, vale esto:

- T-P01: 164-167 está en G_UI_READ, no en G_SLDB_WRITE. Vigente: 161-167 (G_UI_READ) y 225-233 (G_SLDB_WRITE).
- T-P05: 1980-1984 y 1980-1981 caen en la lista de gates de WS28. Vigente: 1984-1987 (scope) y 1991-1994 (acceptance).
- «Refresco verificable»: era falso que no tuviera respaldo vigente. WS28 acceptance dice que `deskops show task` y el commit de closeout confirman el cierre y que se refresca el estado desde deskops. Lo que no aparece es esa frase literal.
- T-P07: se agrega 945-946 (WS13.3), respaldo directo de la disposición local.

Las demás citas a `dag.yaml` se abrieron y coinciden. «Canal completo» sigue sin frase vigente.

## Adenda 2 — 2026-10-31, tras Tester FAIL

Claude Opus 5.5, pane `w3Y:p1`, corrigió `decisiones.md` directamente. Donde difiera, vale esto:

- P01: la fila decía «Operador Scion se designa después»; el ítem 2 dice «Scion se designa cuando abordemos ese ramal». «Operador» pasa a T-P01, con fuente. Esto no lo marcó el Tester: lo vi al releer.
- P03: vuelve al texto de la pregunta, «con otro coordinador escribiendo, la UI queda en lectura/handoff». No cambia el sentido; quita paráfrasis.
- P04: era falso que se hubiera quitado «solo». Ahora la fila dice «Markdown editable tras probar…», como la respuesta. `source_mode=editable` se conserva como parámetro de baseline.
- P06: la corrección anterior perdió la condición «con otro coordinador escribiendo», y la fila Humana afirmaba más de lo aceptado. Recuperada. T-P06 conserva la precisión técnica.

El Tester también señaló como no literales P05 y lo que queda de P01. El criterio de root es «conserva solo lo aceptado», no copia literal; esas omisiones no agregan nada. El Tester las marcó porque mi brief pedía «literalmente», más estricto que el contrato.

## Adenda 3 — 2026-11-01, decisión root

Claude Opus 5.5, pane `w3Y:p1`, corrigió `decisiones.md` y `context-review-guide.md` directamente, por `root-decision-20261101.md`. Donde difiera, vale esto:

- P07 y P09: mi parche quitó «Executor por encargo TaskDoc v2» y este mapa no lo declaró. Fue una omisión mía contra la orden de mantener actores. No la detectaron ni la revisión del Supervisor ni los Tester v1 y v2. La levantó el revisor de WS07 en la tanda 2. Restituido como actor técnico registrado, distinto de la autoría inicial, que sigue sin localizar.
- T-P03.1, nueva: WS12 produce la definición operativa de «modo manual exclusivo». Origen: revisión root 2026-11-01, no el ítem 1.
- Guía: núcleo humano frente a derivaciones técnicas, y dry-run por aristas reales.
