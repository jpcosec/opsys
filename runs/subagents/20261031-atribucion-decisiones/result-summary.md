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
