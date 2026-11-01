REFORMULACION

- **Propósito**: registrar una decisión humana explícita —aprobar o pedir corrección— asociada a un intento y, por él, a su tarea.
- **Resultado**: un registro con actor, referencia al intento y a la tarea, y resultado explícito; si es corrección, con su texto. `completed` del agente no puede registrarse como aprobación.
- **Repo dueño**: `deskops`.
- **Límites**: no escribe los estados de validación ni cierre; solo escribe la decisión mediante la operación que fije el contrato WS12. Si falta, hueco con dueño y parada según `alcance.md`.

AMBIGUEDADES

ninguna.

DRY-RUN

- **Lecturas**: `dag.yaml` (nodo WS33.2, gates y referencia externa Scion), guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `reconciliacion.md`.
- **Cambios previstos**: ninguno en esta revisión. En una ejecución futura, solo los que fijen el contrato WS12 y el TaskDoc de promoción; este nodo no está autorizado a promocionarse.
- **Dependencias**: WS32 y WS33.1; gates `G_SCION` (WS44) y `G_WRITE_CONTRACT` (WS12, evaluación por delta). WS12 llega también de forma transitiva por WS32.
- **Validaciones futuras**: prueba de registro con actor, referencias y resultado; corrección con texto obligatorio; verificación de que `completed` no equivale a aprobado; acta de recepción por delta en el repo receptor.

FUTURO

- **WS12** producirá la operación, campos, actor, errores y pruebas del contrato por delta.
- **WS44** producirá la evidencia de `G_SCION`; **WS32/WS33.1** producirán identidad de intento y vinculación de mensajes/resultados.
- **Promoción/TaskDoc** fijarán archivos exactos, modelo, escenarios de prueba y textos.
- **Humano responsable** aceptará el delta y su acta; `G_WRITE_CONTRACT` se recibirá solo para este alcance, sin aceptar otros deltas.
