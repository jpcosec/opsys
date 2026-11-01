REFORMULACION
Propósito: implementar en `graph_ui` la autoría explícita de un TaskDoc desde un candidato del drawer, incluyendo evidencia declarada, dependencias y binding de contexto/pills. Resultado: sobre un TaskDoc real, el candidato queda autorado con esos elementos vinculados y visibles tras recargar, sin editar `status` para avanzar; toda operación Git sin contrato o dueño queda en handoff explícito y no disponible. Repo dueño: `graph_ui` (`frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12, `tests/`). Límites: usar solo operaciones/endpoints que autorice WS12; G_HUMAN_READ habilita el uso de mutaciones en UI, aunque desarrollo/pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos; promoción no autorizada; no inventar API, permisos ni efectos.

AMBIGUEDADES
Ninguna.

DRY-RUN
Un ejecutor futuro leería `dag.yaml`, el contrato WS12, las salidas de WS22, el TaskDoc de promoción, el corpus WS40 y el estado de gates. Crearía o modificaría vistas, formularios y pruebas bajo `.../authoring/` y `tests/`: cargar el candidato drawer, declarar evidencia/dependencias/pills mediante endpoints WS12, persistir y volver a renderizar el TaskDoc; no escribiría `status`. Consumiría WS12 (whitelist, canal público y precondiciones), WS22 (mismo TaskDoc, selección y links), G_CLOSEOUT satisfecho, G_WRITE_CONTRACT verificado para este delta, G_UI_WRITE por recibo del delta y G_HUMAN_READ antes del uso de mutaciones UI. Errores: endpoint o contrato ausente → detener, registrar hueco con repo dueño y handoff/no disponible; conflicto o fallo de guardado → mostrarlo sin alterar `status`; operación Git sin contrato → handoff. Validación esperada: UF04 sobre TaskDoc real, evidencia/dependencias/pills visibles tras recargar y `status` sin cambios; pruebas aisladas con store temporal.

FUTURO
WS12 produce contrato, whitelist y endpoints autorizados; WS22 aporta representación del TaskDoc y links; WS16 produce el acta G_HUMAN_READ; el receptor P01 emite el acta G_UI_WRITE por delta; el TaskDoc de promoción fija archivos, pills/átomos/evidencia exactos y preflight task-only; WS26.2 añade enrutamiento y capa lista en Board.
