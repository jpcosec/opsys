## REFORMULACION
WS25.2 encarga implementar en `graph_ui` la captura interna con destino elegido explícitamente por la persona: candidato de drawer o protoátomo. El resultado es una captura que persiste tras recargar, conserva un origen tipado —ruta o mensaje—, no crea tarea implícita y aplica los permisos del contrato WS12. Repo dueño: `graph_ui`; alcance: `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. Límites: no crear API/modelo por reflejo; el canal de drawer está pendiente de WS12; G_HUMAN_READ solo habilita uso de mutaciones en UI, no bloquea desarrollo ni pruebas aisladas de API; promoción no autorizada.

## AMBIGUEDADES
Ninguna. Los huecos nombrados —canal de drawer, representación del origen, permisos— tienen productor explícito en WS12 y regla de parada en `alcance.md`; los textos, archivos y escenarios detallados quedan al TaskDoc de promoción.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml`, el contrato WS12 (`contratos/operaciones.md`), la whitelist de operaciones/campos y la API SLDB/Deskops existente; inspeccionaría la captura actual en `frontends/mindmap/views/workspace/capture/` y sus tests. Previsto: añadir selección de destino, acción/formulario de captura, referencia tipada de origen, llamada al endpoint autorizado, manejo de colisión no silenciosa y pruebas separadas por destino. Dependencias: WS12 -> G_WRITE_CONTRACT; G_UI_WRITE por delta; G_HUMAN_READ para uso de UI. Si falta canal, contrato, dato o permiso: detenerse y registrar el hueco con repo dueño, sin sustituto. Validación esperada: persistencia tras recarga en cada destino probado, origen ruta/mensaje visible, ausencia de tarea implícita, permisos aplicados y colisión controlada. No se ejecuta nada.

## FUTURO
WS12 produce el contrato, la whitelist y el canal o hueco; WS16 produce el acta G_HUMAN_READ; el receptor P01 en `graph_ui` produce el acta G_UI_WRITE del delta; el TaskDoc de promoción fija archivos, textos y escenarios; la persona responsable decide la aceptación.
