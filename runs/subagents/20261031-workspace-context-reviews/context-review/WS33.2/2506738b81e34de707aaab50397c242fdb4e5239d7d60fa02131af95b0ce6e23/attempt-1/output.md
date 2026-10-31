## REFORMULACION
**Propósito:** encargo de implementación para registrar una decisión humana explícita —aprobar o pedir corrección— asociada a un intento y, por él, a su tarea.
**Resultado:** registro con actor humano, referencia al intento y a la tarea, y resultado explícito; la corrección exige texto. `completed` del agente nunca equivale a aprobación.
**Repo dueño:** `deskops`.
**Límites:** solo escribe la decisión mediante la operación que fije WS12; no escribe estados `validado` ni `cerrado` de deskops; no promueve el nodo (`promotion: not_authorized`).

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas consideradas:** guía de revisión, brief, alcance, decisiones, cobertura, reconciliación, nodo WS33.2, contratos de sus vecinos y gate `G_SCION`.
**Cambios previstos:** ninguno durante esta revisión. En una ejecución futura: registro de decisión, modelos/reportes, tests y adaptador conforme al contrato WS12.
**Dependencias:** WS12 —transitiva vía WS32— para actor y operación; WS32 para identidad del intento; WS33.1 para vínculos de mensajes/resultados; `G_SCION` mediante WS44.
**Validaciones futuras:** decisión registrada con actor, intento, tarea y resultado; corrección con texto; `completed` del agente no registrado como aprobado; contrato ausente registrado como hueco con dueño, sin sustituto.

## FUTURO
WS12 fija el contrato y la operación de registro. WS32 produce la identidad del intento. WS33.1 aporta vínculos de mensajes y resultados. WS44 resuelve `G_SCION`. El humano decide el resultado de la revisión y la aceptación por delta. El TaskDoc de promoción fija archivos, casos de prueba y textos, dentro de esta aceptación. WS06 integra el delta sin duplicar trabajo.
