REFORMULACION
Propósito: revisar WS25.2 como encargo de planificación: captura interna con destino elegido explícitamente —candidato de drawer o protoátomo— sin exigir tarea. Resultado: el nodo se entiende y su aceptación es comprobable; no se implementa. Repo dueño: graph_ui; `output_scope`: `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. Límites: no revisar los bloques edge vecinos, no ejecutar, no aprobar Pxx ni evaluar producto; WS12/WS16 y los gates son dependencias, no carencias del nodo.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS25.2 y contratos vecinos solo como contexto. Cambios previstos: ninguno. Dependencias: WS12 aporta contrato, capabilities y representación del origen; WS16 resuelve `G_HUMAN_READ`; aplican `G_UI_WRITE` y `G_WRITE_CONTRACT`. Validaciones futuras: para cada destino, persistencia tras recarga, origen ruta y mensaje registrado y mostrado, ausencia de tarea implícita y permisos del contrato; prueba separada de drawer y protoátomo.

FUTURO
WS12 fija whitelist, canal, efectos y representación del origen; si falta, la regla común obliga a detenerse y registrar el hueco. WS16 y el humano resuelven `G_HUMAN_READ`. La promoción/TaskDoc fijará archivos, pills y pruebas detalladas; `G_UI_WRITE`, `G_WRITE_CONTRACT` y la aceptación humana quedan fuera de este nodo.
