REFORMULACION
Propósito: revisar WS23 como encargo de planificación, no implementarlo. Resultado esperado: una vista de procedimiento en `graph_ui` que represente `RitualDoc/StepDoc/lifecycle` sobre referencias reales, con pasos y fuentes navegables y transiciones solo representadas, no accionables. Repo dueño: `graph_ui`; salida acotada a `frontends/mindmap/views/workspace/procedure/; tests/`. Depende de WS13 y WS09; requiere `G_UI_READ`; pruebas sobre corpus WS40 o store temporal real. Límites: lectura; no escribe ni auto-marca estado; promoción no autorizada.

AMBIGUEDADES
Ninguna. El nodo define propósito, resultado, repo, límites, dependencias y aceptación comprobable; los detalles exactos quedan para la promoción/TaskDoc.

DRY-RUN
Lecturas: nodo WS23, guía, brief, alcance, decisiones, cobertura, reconciliación y contratos de aristas WS13/WS09. Cambios previstos: vista `procedure` y pruebas; sin mutación del estado en deskops. Dependencias: WS13 (lector/workspace), WS09 (catálogo de renderizaciones), `G_UI_READ` pendiente; WS40 o store temporal para pruebas. Validaciones futuras: abrir documentos/soporte, navegar pasos y fuentes, no auto-marcar pasos por leerlos, estado solo leído desde deskops y transiciones no accionables; después, WS30 y el gate. No se ejecuta nada.

FUTURO
WS11 o el humano designado resuelve `G_UI_READ`; WS09 entrega el catálogo; WS40 produce el corpus; la promoción, el TaskDoc y la autorización son decisión humana; WS30 valida manualmente.
