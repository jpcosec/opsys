## REFORMULACION
WS31 es un encargo de documentación en `deskops`: publicar el manual documental básico probado (`docs/workspace-user-manual.md`, `docs/assets/workspace-user-manual/` y átomos vinculados), partiendo del índice de WS10 y de las actas de WS30/WS43. Debe cubrir navegación, edición, captura, trabajo manual y revisión demostradas, remitiendo cada instrucción a evidencia existente. Límites: no implementa UI ni contratos; Scion solo como capítulo propuesto hasta WS38; no atomiza permisos ni aceptaciones técnicas inexistentes; personalización/impacto no bloquean el manual básico.

## AMBIGUEDADES
1. «cada instrucción remite al acta de WS30 o al acta de publicación de WS43 de la versión publicada». No se define qué identifica «la versión publicada» ni cómo corresponderla con el manual y el mapa de WS43. Obligaría a inventar el criterio de versión/commit/hash y la trazabilidad instrucción→versión.
2. «un átomo por cada decisión Pxx humana o técnica ya registrada y vigente en decisiones.md y por cada contrato en contratos/» frente a WS43: «los acuerdos durables aplicados al mapa (...) quedan en átomos enlazados desde él». No se indica si WS31 reutiliza átomos ya creados por WS43 o crea otros. Obligaría a inventar la política de deduplicación y el vínculo átomo→documento.
3. «Tester independiente verifica esos criterios antes del cierre». No se nombra repo, canal ni evidencia del Tester. Obligaría a inventar quién prueba, dónde registra y cómo se comprueba su independencia.

## DRY-RUN
- Lecturas previstas: guía, brief, alcance, decisiones, cobertura, `borradores/manual.md`, nodo WS31, gates, actas de WS30/WS43, `contratos/` y átomos existentes.
- Cambios previstos: redactar/actualizar manual, añadir capturas y crear/vincular átomos.
- Dependencias: WS10, WS30 y WS43; `G_HUMAN_MANUAL` pendiente. Contratos y actas deben existir o aplicarse la regla común de detención.
- Validaciones futuras: links resolubles, etiquetas coherentes con actas/commits, referencias a actas, átomo→doc con fuente, capítulos Scion y WS29 etiquetados como propuestos si falta evidencia.
- Sin ejecución.

## FUTURO
WS10 entrega el índice; WS30 produce acta y `G_HUMAN_MANUAL`; WS43 publica mapa/acta real; WS38 añade capítulos Scion; WS39 resuelve `G_HUMAN_MODEL`; WS29 aporta pruebas para impacto. El humano aprueba `G_HUMAN_MANUAL`; la promoción fijará archivos, pills y evidencias en TaskDoc.
