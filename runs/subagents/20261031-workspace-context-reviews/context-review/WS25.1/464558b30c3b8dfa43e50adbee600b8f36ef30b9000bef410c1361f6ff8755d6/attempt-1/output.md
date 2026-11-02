REFORMULACION
WS25.1 es un encargo de planificación (`implementation`, repo `graph_ui`) para una UI que lea mensajes del inbox, registre `ack` y, solo si el contrato WS12 define esa operación, una respuesta local en el mismo desk. Resultado: vista y operaciones en `frontends/mindmap/views/workspace/inbox/` más `tests/`, usando el canal autorizado por WS12 y el punto de admisión WS48. Límites: sin envío interdesk, `ack` no es aprobación, sin tarea implícita ni cron de triage; `promotion: not_authorized`. Depende de WS12 y WS48; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

AMBIGUEDADES
ninguna

DRY-RUN
Nodo no agregado; se ejecutaría como implementación. Lecturas previas: contrato WS12 sobre lectura/ack/respuesta y permisos; mecanismo de admisión WS48; formato real de `desk/inbox/`; vista existente y TaskDoc de promoción. Cambios previstos: listar/abrir mensajes en la vista inbox; botón/acción de ack que invoque la operación WS12 pasando por WS48; respuesta local solo si WS12 la define, con declaración de no disponible en caso contrario; pruebas en `tests/`. Dependencias: WS12 aporta operaciones y precondiciones; WS48 aporta admisión previa a mutaciones; G_HUMAN_READ habilitaría uso de mutaciones en UI; G_UI_WRITE y G_WRITE_CONTRACT se evaluarían por delta. Validaciones futuras: ack persiste tras recarga mostrando el mensaje origen; respuesta no disponible si falta contrato; no se crea tarea ni cron; permisos aplicados. Errores: contrato/API ausente → detenerse y registrar hueco con repo dueño, sin sustituto; admisión denegada → lectura/handoff con causa. Sin ejecutar nada.

FUTURO
WS12 debe publicar las secciones de operaciones y permisos aplicables; WS48 debe proveer la admisión; WS16 produce el acta G_HUMAN_READ; el receptor P01 en `graph_ui` produce el acta G_UI_WRITE por delta; WS12/G_WRITE_CONTRACT verifica el contrato técnico; la promoción decide el TaskDoc. Nada de esto es ambigüedad del nodo.
