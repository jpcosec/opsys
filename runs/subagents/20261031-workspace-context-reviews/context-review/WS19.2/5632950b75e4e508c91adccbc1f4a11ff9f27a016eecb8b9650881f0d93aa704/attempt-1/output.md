## REFORMULACION

**Propósito:** planificar la edición de relaciones —alta y baja— solo para las permitidas por el contrato de operaciones de WS12, sin definir semántica de relaciones dentro del componente.

**Resultado esperado:** en `graph_ui`, una vista/componente de relaciones que persiste altas y bajas mediante API real y before-image, confirma el cambio tras recargar y rechaza con error visible una relación no permitida o una revisión obsoleta.

**Repo dueño:** `graph_ui`, con salida en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por el contrato WS12 y `tests/`. Modo de integración: delta sobre ticket existente o ticket atómico, nunca duplicado paralelo.

**Límites:** depende de WS12; requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. G_HUMAN_READ bloquea el uso de mutaciones en UI, no el desarrollo ni pruebas aisladas de API. No se autoriza promoción.

## AMBIGUEDADES

Ninguna. El contrato que define qué relaciones y endpoints están permitidos tiene productor nombrado (WS12), y las reglas comunes de ejecución fijan qué hacer si falta: detenerse y registrar el hueco, sin crear sustituto. La aceptación es comprobable —persistencia tras recarga y rechazo con error visible—; los textos exactos y escenarios detallados corresponden al TaskDoc de promoción. Las dependencias, gates y repo están declarados.

## DRY-RUN

**Lecturas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md` y el nodo WS19.2 con sus aristas y gates en `dag.yaml`.

**Cambios previstos:** ninguno en esta revisión. En ejecución futura: componente de alta/baja de relaciones en `frontends/mindmap/views/workspace/relations/`, llamadas a endpoints del contrato WS12 y pruebas en `tests/`.

**Dependencias:** contrato técnico y whitelist de operaciones de WS12; gates G_WRITE_CONTRACT y G_UI_WRITE por delta; G_HUMAN_READ antes de habilitar mutaciones en UI.

**Validaciones futuras:** alta y baja persisten y se confirman tras recargar; relación no permitida y revisión obsoleta se rechazan con error visible; pruebas API aisladas pueden avanzar antes del acta humana de lectura.

## FUTURO

WS12 debe publicar la whitelist y el contrato de operaciones aplicable a relaciones. WS16 resuelve G_HUMAN_READ. La recepción por delta registra G_UI_WRITE y G_WRITE_CONTRACT en el repo receptor. La promoción fijará archivos, pills, átomos, evidencia y preflight. Nada de esto está autorizado ni ejecutado.
