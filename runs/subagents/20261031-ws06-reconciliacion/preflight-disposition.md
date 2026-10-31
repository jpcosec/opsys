# Comparación del coordinador — WS06, aceptada para despacho

Preflight y cold en procesos Pi nuevos, sin herramientas y con stdin DEVNULL (recibos en este run). Ambas reproducen objetivo, matriz por capacidad, grupo por repo dueño, reglas, roles y límites, y el efecto esperado sobre 25 revisiones. Ninguna propone tocar código, DAG ni aceptar deltas.

## Resoluciones, obligan a Executor y Tester
- Cobertura: los 63 nodos tienen fila en la tabla de cobertura. La segunda columna es un C-nn o «sin delta: <motivo>». «Ningún nodo queda sin fila» se refiere a esa tabla.
- `build_plan.py --check` debe pasar; no lee reconciliacion.md. `validate_plan.py --check` falla por las 25 revisiones, y eso es lo esperado.
- Clasificación admite un cuarto valor, «no adoptado», solo para frontends/workspace, que no es capacidad reutilizable aprobada: se cita lo observado y no se adopta.
- C-nn: numeración continua en orden de aparición en el documento.
- Ticket o delta destino: nombre del ticket si existe; si no, «nuevo delta: <nombre corto>». Solo graph_ui tiene tickets abiertos conocidos.
- Commit observado: el que cita la auditoría para esa fila, del repo de la fila, indicando repo cuando no sea obvio. Si la auditoría no cita uno, HEAD auditado de ese repo marcado como HEAD.
