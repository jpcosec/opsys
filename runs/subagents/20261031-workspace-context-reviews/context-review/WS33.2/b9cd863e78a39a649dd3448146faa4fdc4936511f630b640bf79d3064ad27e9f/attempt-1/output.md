## REFORMULACION
**Propósito:** registrar una decisión humana sobre un intento Scion, vinculándola a su tarea.  
**Resultado:** registro con actor humano, referencia al intento y resultado explícito “aprobar” o “pedir corrección” —esta última con texto—.  
**Repo dueño:** `deskops`, con salidas en `runtime/`, modelos/reportes y `tests/`.  
**Límites:** no escribe estados `validado`/`cerrado` de deskops; no convierte `completed` del agente en aprobación; solo escribe mediante la operación que fije WS12; no ejecuta código.  
**Dependencias:** WS32, WS11, WS33.1; gate `G_SCION`.

## AMBIGUEDADES
1. «asociada al intento y, por él, a su tarea»  
   Ningún contrato suministrado define explícitamente cómo se resuelve la tarea desde el intento; la aceptación solo exige «referencia al intento», no a la tarea. El ejecutor tendría que inventar el campo, relación o consulta intento→tarea, o decidir que basta el intento.

2. «depends_on: - WS32 - WS11 - WS33.1»  
   WS11 entrega un contrato de navegación e identidad documental, pero WS33.2 no indica qué artefacto de WS11 consume para registrar decisiones, intentos o tareas. Obliga a inventar el vínculo o a aceptar una dependencia que solo bloquea.

## DRY-RUN
**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS33.2 y contratos vecinos WS32/WS11/WS33.1.  
**Cambios previstos:** adaptador de registro de decisión según operación WS12; persistencia de actor, intento y resultado; prueba negativa de que `completed` no equivale a aprobado.  
**Dependencias:** WS32 y WS33.1 para identidad/vinculación del intento; WS12 —transitiva vía WS32— para la operación; `G_SCION` para acceso Scion.  
**Validaciones futuras:** preflight de promoción, TaskDoc con archivos/pruebas, prueba de decisión aprobar/pedir corrección y verificación de no escritura de estados deskops.

## FUTURO
WS07 designa actor humano y receptor; WS12 fija la operación concreta; WS32/WS33.1 aportan identidad y vínculo del intento; WS44 produce `G_SCION`; la promoción fija archivos y pruebas; una persona decide las Pxx pendientes.
