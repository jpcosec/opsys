REFORMULACION
Propósito: encargo de implementación en `graph_ui` para captura interna en el workspace, con destino elegido explícitamente —candidato de drawer o protoátomo— mediante operaciones autorizadas por WS12, sin exigir ni crear tarea.
Resultado: captura que persiste tras recargar en el destino elegido, registra y muestra un origen tipado (ruta o mensaje) y aplica los permisos del contrato; cada destino se prueba por separado.
Repo: `graph_ui`; salida en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`.
Límites: no crear tareas implícitas, no inventar operaciones fuera del contrato WS12, no diseñar el contrato ni ejecutar mutaciones no permitidas. Los gates pendientes son intencionales; la promoción no está autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, nodo WS25.2, gates y contratos vecinos; contrato WS12 cuando exista; código y endpoint reales de `graph_ui`.
Cambios previstos: UI de captura con selección explícita de destino; llamada a operaciones WS12; persistencia y representación del origen; pruebas en `tests/`.
Dependencias: WS12 produce contrato/whitelist y representación del origen; G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT son prerrequisitos pendientes; WS25 cierra como agregado al cumplir WS25.1 y WS25.2.
Validaciones futuras: persistencia tras recarga para drawer y protoátomo por separado; origen ruta y mensaje registrado y visible; ausencia de tarea implícita; permisos del contrato aplicados; recibos por delta de los gates. No se ejecuta nada.

FUTURO
WS12 debe publicar el contrato de operaciones y la representación tipada del origen. WS16 produce el acta de G_HUMAN_READ. El receptor P01 en `graph_ui` produce el acta G_UI_WRITE del delta concreto. La promoción exige TaskDoc, archivos/pills y preflight; el cierre de WS25 queda para el agregado.
