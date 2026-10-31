## REFORMULACION

**Propósito:** implementar en `graph_ui` la captura interna con destino elegido explícitamente por la persona usuaria —candidato de drawer o protoátomo— usando únicamente operaciones permitidas por el contrato WS12, sin exigir ni crear tarea.

**Resultado:** UI y endpoints en `frontends/mindmap/views/workspace/capture/` y `tests/`, con cada destino probado por separado. Una captura debe persistir tras recargar, conservar un origen tipado —ruta o mensaje— y mostrarlo, sin tarea implícita. Permisos del contrato aplicados.

**Repo dueño:** `graph_ui`.

**Límites:** no se autoriza promoción; no hay commits ni closeout; no se diseñan canales ausentes; no se exceden las operaciones del contrato WS12. Desarrollo y pruebas aisladas de API pueden avanzar sin acta humana, pero las mutaciones en UI requieren `G_HUMAN_READ`.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** nodo WS25.2, padre WS25, arista WS12, gates `G_HUMAN_READ`/`G_UI_WRITE`/`G_WRITE_CONTRACT`, guía, brief, alcance y decisiones.

**Cambios previstos:** componentes de captura bajo `frontends/mindmap/views/workspace/capture/`; integración con endpoints autorizados por WS12; pruebas en `tests/`.

**Dependencias:** contrato WS12 y sus recibos por delta. `G_HUMAN_READ` lo produce WS16; `G_UI_WRITE` y `G_WRITE_CONTRACT` se evalúan por efecto concreto, no como aceptación conjunta. WS25.1 es hermano, no prerrequisito de WS25.2.

**Validaciones futuras:** para cada destino, capturar, recargar y comprobar persistencia, origen ruta/mensaje visible y ausencia de tarea; verificar permisos del contrato; obtener los recibos técnicos y el acta humana exigidos antes de habilitar mutaciones en UI.

## FUTURO

- **WS12:** publica la whitelist de operaciones, campos, actor, revisión, efectos y errores aplicables a captura, y emite los recibos por delta.
- **WS16:** produce el acta humana de lectura que habilita el uso de mutaciones en UI.
- **Promoción:** el TaskDoc fija archivos exactos, pills, átomos y evidencia, y ejecuta el preflight limitado a tarea.
- **Persona responsable P01:** acepta el delta concreto en el repo receptor.
- **WS25.1:** aporta, por separado, la integración de mensaje/ack; no define esta captura.
