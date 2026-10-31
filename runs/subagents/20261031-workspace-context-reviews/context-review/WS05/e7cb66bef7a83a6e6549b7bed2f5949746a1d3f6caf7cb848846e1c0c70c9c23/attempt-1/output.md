## REFORMULACION
Propósito: inventariar la identidad y la API pública de Scion (runtime/templates/RunDoc y endpoints/SDK documentados o exportados) y separar slug, agente, intento, dispatch, mensaje, conversación y permisos. Resultado: `auditoria/scion.md` bajo `desk/drawer/plans/workspace-documental/`. Repo dueño: deskops (con lectura del repo `../scion`). Límites: sin tocar tablas ni funciones internas, sin endpoints vivos ni credenciales, sin crear agentes, enviar mensajes ni modificar configuración; no produce G_SCION.

## AMBIGUEDADES
1. «endpoints/SDK documentados o exportados; no tablas ni funciones internas» — no fija qué fuente manda si documentación y exports discrepan, ni qué cuenta como «exportado» frente a interno. Obliga a inventar el criterio de admisibilidad, del que depende la aceptación («los campos internos que no figuren en la API pública definida en el scope»).
2. «marca qué capabilities requieren WS32 y WS33» — WS33 no aparece definido en las fuentes suministradas (solo WS32 y sus hijos). Obliga a inventar qué consume WS33 para clasificar cada capability.
3. «puede leer configuración sin secretos y no muestra tokens» — no indica rutas de configuración admisibles, qué claves son secretas ni cómo se evidencia la redacción. Obliga a inventar política de redacción y su prueba; sin ella el límite permite arrastrar credenciales al inventario.
4. «separar slug/agente/intento/dispatch/mensaje/conversación» — «conversación» no está en el glosario del brief, a diferencia de intento/RunDoc/manifiesto. Obliga a inventar su frontera respecto a mensaje.

## DRY-RUN
Lecturas: brief/glosario y alcance (límites), dag.yaml (nodo y aristas), código/documentación pública en deskops y `../scion`. Cambios previstos: crear `auditoria/scion.md` con taxonomía, permisos y marcas hacia WS32/WS33. Dependencias: WS01 (brief autosuficiente) como prerrequisito; WS44 consume el inventario pero el gate G_SCION sigue `unverified`. Validaciones futuras: revisión de aceptación (seis conceptos separados, campos internos señalados fuera de API pública, capabilities marcadas); ninguna ejecución en este nodo.

## FUTURO
WS07 designa operador Scion y su acceso read-only; WS44 ejecuta el probe real y produce G_SCION; WS32.1 fija la semántica de `confirmed`; el TaskDoc de promoción fija archivos y formato exactos del inventario; el solicitante humano resuelve P01/P09 y cualquier cambio de alcance.
