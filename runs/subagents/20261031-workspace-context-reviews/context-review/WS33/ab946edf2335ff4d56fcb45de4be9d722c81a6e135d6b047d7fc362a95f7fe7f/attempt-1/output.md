REFORMULACION
- Propósito: agrupar la vinculación de mensajes/resultados al intento y el registro de decisión humana explícita, con deduplicación y procedencia, como backend documental.
- Resultado: agregado de salidas de WS33.1 y WS33.2; se cumple cuando ambos hijos cumplen su aceptación. Los dependientes siguen dependiendo de WS33.
- Repo: deskops.
- Límites: no editor UI; no tocar tablas Scion; no ejecutar dispatch/reply; promoción no autorizada (`promotion: not_authorized`); requiere G_SCION.

AMBIGUEDADES
ninguna.
El agregado no ejecuta trabajo propio: el resultado, la deduplicación y la aceptación comprobable están delegados en WS33.1/WS33.2. G_SCION pendiente tiene productor nombrado (WS44) y no obliga a inventar.

DRY-RUN
- Lecturas: `dag.yaml#node:WS33`, hijos WS33.1/WS33.2 y guía; brief, alcance, decisiones, cobertura y reconciliación; `task_file` referenciado.
- Cambios previstos: ninguno en esta revisión. La promoción futura solo podría preparar el TaskDoc; no está autorizada.
- Dependencias: WS32, WS11, WS33.1, WS33.2; G_SCION no verificado, producido por WS44; contrato de actor/operación por WS12.
- Validaciones futuras: aceptación de ambos hijos; dedup por Hub/proyecto/conversación/mensaje e intento/fuente; procedencia de no vinculados; decisión con actor humano, intento y tarea, resultado aprobar/pedir corrección; `completed` no equivale a aprobado; ausencia de tablas Scion.

FUTURO
- WS44/operador designado produce G_SCION.
- WS32 y WS33.1 producen identidad de intento, referencias y resultados deduplicados.
- WS33.2 registra la decisión humana según la operación que fije WS12.
- El responsable humano decide promoción y recepción por delta; no hay aprobación de implementación en este nodo.
