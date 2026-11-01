REFORMULACION
Propósito: revisar PK03 como encargo de planificación que agrupa lector útil y descubrimiento temprano, no como implementación. Resultado sustantivo: paquete cerrado cuando sus hijos produzcan lector read-only con explorador de documentos modelados/no modelados, foco/historia, Code/grafo, búsqueda navegable con estados, errores/orientación, corpus Taller con dos desks y repo sin desk, lectura entre desks y acta humana WS16 con mediciones P08 de apertura/búsqueda/arranque. Repo dueño: deskops; los hijos implementan en graph_ui. Límites: agrupación sin ejecución propia ni autorización de tareas/aristas; no edición, Changes ni Scion; no guardado (WS30); revisión de comprensión no acredita producto.

AMBIGUEDADES
ninguna.

DRY-RUN (hipotético, sin ejecutar)
Prerrequisitos externos: WS11 (navegación/identidad) y WS08 (user-flows) habilitan WS13. WS13 recibe ese contrato y entrega workspace read-only con explorador, dos documentos, foco/historia y Code/grafo; WS14 consume WS13 y la API de búsqueda para resultados y tres estados; WS15 consume WS13 para errores y orientación sin desk. WS40, con WS11/WS08, genera corpus Taller, manifiesto y commits temporales. WS41 consume WS13/WS11/WS40 para lectura segura del segundo desk. WS16 consume WS14, WS15, WS08, WS40 y WS41; ejecuta recorrido humano integrado, registra acta y mide apertura/búsqueda/arranque. Validación integrada: regenerar Taller, abrir ambos desks y el repo sin desk, navegar con foco/historia, buscar con estados, comprobar errores y lectura cruzada, y contrastar acta. No se ejecuta ahora.

FUTURO
WS11/WS08 producen contrato y user-flows; WS13/14/15/40/41 producen artefactos y manifiesto; WS16 y el humano P01/P08 deciden aceptación, acta y correcciones. G_HUMAN_READ y recibos por delta pertenecen a otros nodos/actores.
