REFORMULACION
- **Propósito**: dotar al workspace de una vista de inbox que permita leer mensajes del desk y registrar acuse (ack) o respuesta local, usando solo operaciones autorizadas por el contrato WS12.
- **Resultado**: UI en `graph_ui` que muestra mensajes, persiste el ack tras recargar junto al mensaje origen y, solo si WS12 define la operación, registra respuesta local; en caso contrario la declara no disponible. No crea tareas implícitas ni cron de triage.
- **Repo dueño**: `graph_ui` (`output_base: graph_ui:repository_root/`), con salida en `frontends/mindmap/views/workspace/inbox/`, endpoints autorizados por WS12 y `tests/`.
- **Límites**: mismo desk, sin envío interdesk; ack ≠ aprobación; permisos del contrato aplicados; mutaciones de UI sujetas a `G_HUMAN_READ`; desarrollo y pruebas aisladas de API pueden avanzar sin acta humana de lectura.

AMBIGUEDADES
Ninguna. La ausencia de contrato para “respuesta local” está cubierta por la propia aceptación (“solo si el contrato WS12 define esa operación, y si no se declara no disponible”), y el resto de resultados y comprobaciones son verificables sin inventar alcance.

DRY-RUN
- **Lecturas**: guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS25.1 y bloques de contrato de WS12/WS25, sin revisarlos como nodos.
- **Cambios previstos**: implementar la vista de inbox, el flujo de ack y, condicionado a WS12, la respuesta local; añadir pruebas en `tests/`. Sin ejecutar.
- **Dependencias**: contrato WS12 (canal, whitelist, permisos, revisión, efectos); `G_WRITE_CONTRACT` por delta; `G_HUMAN_READ` antes de habilitar mutaciones en UI; `G_UI_WRITE` con acta por delta; corpus WS40 para validación humana cuando exista.
- **Validaciones futuras**: ack persistente tras recarga mostrando el mensaje origen; respuesta disponible o declarada no disponible según WS12; no creación de tarea implícita ni cron; permisos aplicados; preflight task-only y TaskDoc de promoción.

FUTURO
- WS12 publica whitelist/contrato y recibo técnico por delta.
- WS16 produce el acta de `G_HUMAN_READ`.
- El receptor P01 en `graph_ui` produce el acta de `G_UI_WRITE` para este delta.
- La promoción, aún no autorizada, fijará archivos, textos y casos de prueba en el TaskDoc.
- WS25 cierra cuando cumplan WS25.1 y WS25.2; la aceptación de UF02 queda según cobertura.
