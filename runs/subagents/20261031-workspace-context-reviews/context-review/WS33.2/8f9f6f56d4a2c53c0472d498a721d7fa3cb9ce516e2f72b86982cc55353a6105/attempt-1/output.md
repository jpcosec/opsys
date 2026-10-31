## REFORMULACION
Propósito: registrar una decisión humana explícita sobre un intento Scion, sin inferirla del estado `completed` del agente. Resultado: registro con actor humano, referencia al intento y a su tarea, y resultado explícito aprobar o pedir corrección, con texto obligatorio en este último caso. Repo dueño: `deskops`. Límites: el nodo no escribe estados `validated`/`closed` ni el `completed` de Scion; solo registra la decisión mediante la operación que fije el contrato WS12. Si falta, corresponde hueco con dueño, sin sustituto.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Lecturas previstas, sin ejecutar: nodo WS33.2, agregados WS33/WS32, WS33.1, gates y fuentes suministradas. Cambios previstos por el ejecutor: adaptador en `runtime/`, modelos/reportes y tests en `deskops` para registrar la decisión; no UI ni estados de cierre. Dependencias: WS32 y WS33.1; `G_SCION`; contrato/operación WS12 —transitivo por WS32— y `G_WRITE_CONTRACT`. Validaciones futuras: decisión con actor humano, intento/tarea, resultado explícito y texto de corrección cuando aplique; `completed` nunca como aprobación; comportamiento repetido/idempotente según contrato; prueba con store temporal o corpus WS40.

## FUTURO
WS12 define la operación y la identificación del actor; WS44 resuelve `G_SCION`; WS07 designa al operador Scion. La promoción/TaskDoc fija archivos, escenarios y textos. El humano emite la decisión y, si procede, el texto de corrección. WS33 cierra cuando cumplen sus hijos. `testing` y `closeout` de `deskops` gestionan los estados que este nodo no escribe.
