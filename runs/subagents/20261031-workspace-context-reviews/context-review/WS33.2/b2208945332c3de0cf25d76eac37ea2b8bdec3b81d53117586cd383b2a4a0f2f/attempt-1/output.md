## REFORMULACION

**Propósito:** registrar una decisión humana explícita —aprobar o pedir corrección— sobre un intento Scion, con actor humano identificado por el contrato WS12, asociada al intento y, por él, a su tarea.

**Resultado:** un registro de decisión con actor, referencia al intento y a la tarea, y resultado explícito; si es “pedir corrección”, con su texto. El nodo no escribe estados de deskops como validado/cerrado, ni acepta `completed` del agente como aprobación.

**Repo dueño:** `deskops`, con salidas en `runtime/` (adaptador definido por contrato), modelos/reportes y tests.

**Límites:** solo escribe la decisión mediante la operación que fije el contrato WS12; si falta, se registra hueco con dueño. No ejecuta cierre, validación ni sustituye la decisión humana. Depende de WS32 y WS33.1 y requiere G_SCION.

## AMBIGUEDADES

ninguna

## DRY-RUN

**Lecturas previstas:** guía de revisión, brief, alcance, decisiones, nodo WS33.2, aristas WS32/WS33/WS33.1 y gate G_SCION.

**Cambios previstos, sin ejecutar:** adaptador de registro en `runtime/`, modelos/reportes y pruebas; alta de la decisión por la operación del contrato WS12. No se modifica el estado de la tarea ni se escribe closeout/testing.

**Dependencias:** WS32 aporta identidad de intento y relación con tarea; WS33.1 vincula mensajes/resultados; WS12, transitivamente vía WS32/G_WRITE_CONTRACT, fija operación y campos; G_SCION debe resolverse por WS44; WS07 identifica actores receptores.

**Validaciones futuras:** comprobar que el registro contiene actor humano, referencia al intento y a su tarea, y resultado aprobar/pedir corrección; que “pedir corrección” incluye texto; que `completed` del agente no se registra como aprobado; y que, si falta el contrato WS12, se detiene y se registra el hueco con repo dueño.

## FUTURO

WS12 produce la operación/campos de escritura; WS32 y sus hijos fijan identidad de intento y vínculo con tarea; WS33.1 aporta deduplicación y procedencia de mensajes/resultados; WS44 resuelve G_SCION con probe real; WS07 designa operador y actores. La promoción fijará archivos, escenarios y textos de prueba. El estado validado/cerrado lo escriben testing y closeout de deskops; Scion reporta `completed`. La decisión humana concreta la adopta la persona en ejecución, no este revisor.
