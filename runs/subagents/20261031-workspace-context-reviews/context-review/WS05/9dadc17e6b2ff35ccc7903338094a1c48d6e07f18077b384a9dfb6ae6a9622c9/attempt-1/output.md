# Revisión WS05 — Inventariar identidad y API Scion

## REFORMULACION
Propósito: inventariar, sin ejecutar, la identidad y la API pública de Scion leyendo código y documentación. Resultado: `auditoria/scion.md` que separa slug/agente/intento/dispatch/mensaje/conversación y permisos, señala campos internos fuera de la API pública y marca capabilities requeridas por nodos posteriores. Repo dueño: `deskops`, con lectura del repo `scion` (`../scion`). Límites: solo lectura de runtime/templates/RunDoc, SDK/endpoints documentados o exportados y configuración sin secretos; no contacta endpoints vivos, no usa credenciales, no crea agentes ni envía mensajes ni modifica configuración; no produce G_SCION (eso es WS44).

## AMBIGUEDADES
1. «marca qué capabilities requieren WS32 y WS33». WS33 no aparece definido en el input (solo WS32, WS32.1, WS32.2). El ejecutor tendría que inventar qué nodo es WS33 y qué capacidades necesita para poder marcarlas.
2. «Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33; si no las mapea por nodo, WS44 se detiene y registra el hueco» frente a la aceptación de WS05, que obliga a «marca qué capabilities requieren WS32 y WS33». El ejecutor debe inventar si el mapeo por nodo es obligatorio para cerrar WS05 o si su ausencia es admisible y solo bloquea aguas abajo.
3. «Lee código y documentación en deskops y en el repo scion (../scion)». No consta en el input responsable ni autorización de lectura de ese repo; el ejecutor tendría que asumir acceso y que esa ruta es la fuente autoritativa frente a copias vendorizadas.

## DRY-RUN
Lecturas previstas: `deskops` (runtime, templates, modelo RunDoc), código y documentación de `../scion` (endpoints/SDK documentados o exportados), configuración sin secretos. Cambios previstos: crear `auditoria/scion.md` bajo el paquete del plan. Dependencias: solo WS01; sin gates requeridos (G_SCION no lo produce este nodo). Validaciones futuras: WS32/WS32.1/WS32.2 consumen el mapeo de capabilities; WS44 ejecuta el probe real que satisface G_SCION.

## FUTURO
WS44 ejecuta el probe read-only y produce G_SCION o registra el hueco. WS32.1/WS32.2 implementan intento y manifiesto. WS07 designa operador Scion y responsables de repo. Las propuestas P01/P02/P04/P07/P09 quedan pendientes de decisión humana; ninguna se resuelve aquí.
