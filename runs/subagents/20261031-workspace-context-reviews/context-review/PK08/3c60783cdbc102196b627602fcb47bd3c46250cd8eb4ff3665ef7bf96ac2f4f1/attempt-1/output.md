## REFORMULACION
Propósito: revisar PK08 como encargo de planificación del ramal Scion opcional, definido como agrupación sin ejecución propia. Resultado: determinar si PK08 se entiende y si su cierre es comprobable; `review_completion` exige revisión vigente de cada hijo directo o bloqueo externo con responsable, verificado con `context_review.py status`. Repo dueño: `deskops`. Límites: no ejecuta tareas ni añade aristas; no autoriza dispatch, mensajes, permisos Scion ni acceso real; no duplica el pipeline Scion; no convierte permisos de núcleo en dispatch; las validaciones futuras se describen, no se ejecutan.

## AMBIGUEDADES
1. Cita: PK08 scope: «WS05 inventario y WS44 probe con operador/acceso designados producen G_SCION». Contradice WS05: «WS05 no produce G_SCION; el probe y sus reintentos son responsabilidad explícita de WS44», y `G_SCION.produced_by: WS44`. Obliga a inventar si el inventario WS05 satisface, alimenta o no produce `G_SCION`, y quién es responsable del gate.

## DRY-RUN
Lecturas: nodo PK08, guía, brief, alcance, decisiones, cobertura y contratos vecinos ya suministrados; sin herramientas. Cambios previstos: ninguno en producto ni en el plan; una revisión efectiva solo dejaría `disposition.md` en el intento, no ejecutado aquí. Dependencias: revisiones de WS32–WS38 y WS44; WS44 depende de WS05/WS07 y `G_PRODUCT`; `G_SCION`/`G_EXEC` pendientes. Validaciones futuras: estado de `context_review.py`, vigencia de hashes/dispositions de hijos, evidencia del probe WS44 y acta WS37.

## FUTURO
WS05 produce el inventario; WS44 ejecuta el probe read-only y produce evidencia de `G_SCION`; el solicitante designa operador/acceso y registra `autorizaciones/scion.md`; un humano externo resuelve `G_EXEC`; WS37 produce acta humana; WS38 publica el capítulo. Nada de eso se decide en esta revisión.
