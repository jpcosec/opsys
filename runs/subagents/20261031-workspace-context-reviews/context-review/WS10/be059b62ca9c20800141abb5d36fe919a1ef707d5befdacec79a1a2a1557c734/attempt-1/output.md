## REFORMULACION
WS10 es un encargo de planificación en `deskops` para precisar el índice y la convención de `borradores/manual.md`. El resultado esperado es un esquema de capítulos conceptuales con propósito/entradas/salidas, un ejemplo fijo —Taller, `graph_ui:.tmp/workspace-documental-ejemplo/`, productor WS40— y etiquetas de disponibilidad: disponible solo con versión/commit implementado, pruebas y acta humana; propuesto sin esa evidencia; bloqueado con dependencia/contrato pendiente. Límites: no redactar el manual completo, no inventar capturas ni pasos, no implementar UI y no alterar otras tareas. Depende de WS02 y WS07; G_PRODUCT está satisfecho.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml#node:WS10`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/manual.md`, la auditoría de WS02 (`auditoria/deskops.md`) y el registro de WS07 (`decisiones.md`/`owner-decisions.json`), más las auditorías WS03/WS04 que el scope declara transitivas.

Cambios previstos: solo en `borradores/manual.md`. Precisaría el índice existente, añadiría por capítulo conceptual propósito, entradas y salidas; fijaría el ejemplo Taller con su ruta y productor WS40; aplicaría las tres etiquetas de disponibilidad; mantendría la referencia al manual CLI y evitaría duplicarlo. No tocaría código ni otros nodos.

Dependencias y gates: consumiría la auditoría WS02 y las decisiones WS07; comprobaría G_PRODUCT satisfecho con su evidencia registrada. Si falta una auditoría o un contrato que debía producir una dependencia, se detendría y registraría el hueco con repo dueño, sin crear sustituto. Si WS40 aún no generó el corpus, lo describiría como futuro, sin capturas ni pasos inventados.

Validación esperada: cada capítulo tendrá propósito/entradas/salidas; cada etiqueta “disponible” citará versión/commit, pruebas y acta; “propuesto” no fingirá evidencia; “bloqueado” nombrará dependencia/contrato; el ejemplo fijo aparecerá como corpus futuro mientras falte WS40; no habrá capturas ficticias.

## FUTURO
WS09 reutilizará las etiquetas de WS10 para el catálogo de vistas; WS31 incorporará el índice al manual publicado; WS40 generará el corpus Taller; WS30/WS43 producirán actas de prueba y publicación; la aceptación humana y la promoción quedan fuera de este nodo.
