## REFORMULACION

Encargo de planificación: validar de punta a punta el flujo UF06 con un agente Scion real y un actor humano (pregunta, intervención, corrección, evidencia, decisión y cierre mediante el handoff de WS28). Resultado esperado: un acta humana versionada en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/`, con guion, versión, comandos y resultado, que además resuelve `G_HUMAN_DELEGATE`. Repo dueño: graph_ui. Límites: no sustituir la integración por mocks ni confundir «completed» con «aprobación»; no bloquea WS31; depende de WS36 y WS30 y requiere G_EXEC y G_SCION; su promoción no está autorizada (requiere preflight task-only y fijar archivos/pills/evidencia).

## AMBIGUEDADES

Ninguna. Las menciones a WS28 y al guion tienen productor identificado (WS28 vía WS30; WS08 refina el guion sobre la matriz de cobertura), y la ausencia de contrato o permiso se resuelve con las reglas comunes de alcance.md. Los gates pendientes son intencionales.

## DRY-RUN

Un ejecutor futuro leería: `dag.yaml#node:WS37`, `task-ws37.md`, `validacion-humana.md`, `cobertura.md`, alcance.md, decisiones.md, el acta de WS30, la entrega de WS36, la autorización de `G_EXEC` en `autorizaciones/scion.md` y el probe de WS44 para `G_SCION`.

Comprobaría ambos gates antes de actuar: si faltan, se detiene, registra el hueco con repo dueño y no crea sustituto; la operación queda no disponible. Con gates satisfechos, prepararía el entorno Taller/Scion real, ejecutaría el recorrido UF06 (bundle, dispatch, seguimiento, pregunta, respuesta humana, corrección, evidencia, revisión y cierre por handoff WS28), registraría observaciones y fallos sin convertirlos en aprobación, y redactaría el acta con actor humano, versión/commit, guion, resultados y soportes.

Cambios previstos: alta del acta y su commit atómico en graph_ui bajo el `output_scope`; ninguna mutación de producto. Validación esperada: acta enlazada y versionada, gates verificados, recorrido completado por la persona sin rutas memorizadas ni correcciones verbales, y ausencia de mocks. Dependencias consumidas: WS36 (adaptador/revisión), WS30 (protocolo manual validado), G_EXEC y G_SCION. Errores esperados: gate sin resolver, API/permiso ausente o fallo de recorrido; cada uno bloquea el gate y abre corrección en el repo/superficie correspondiente sin inventar causalidad.

## FUTURO

WS44 produce el probe de G_SCION; el solicitante/designee resuelve G_EXEC; la persona firmante del acta resuelve G_HUMAN_DELEGATE; WS38 documenta el resultado; la promoción a tarea la decide quien autoriza, previo preflight task-only.
