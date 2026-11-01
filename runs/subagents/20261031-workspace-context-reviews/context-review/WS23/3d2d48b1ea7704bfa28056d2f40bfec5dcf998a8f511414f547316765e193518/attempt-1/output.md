REFORMULACION
Propósito: entregar en graph_ui una vista de solo lectura que represente RitualDoc/StepDoc/lifecycle como procedimiento navegable. Resultado: renderer bajo `frontends/mindmap/views/workspace/procedure/` que abre documentos y soportes, muestra pasos/fuentes y transiciones declaradas, sin escribir estado ni ofrecer avance. Repo dueño: graph_ui; pruebas en `tests/` sobre corpus WS40 o store temporal real. Límites: no marcar pasos por lectura, no inventar progreso sin campo/API real identificado por WS02/WS09/WS11, no controles mutantes, no sustituir contratos ausentes; depende de WS13 y WS09 y exige recibo G_UI_READ por delta.

AMBIGUEDADES
ninguna

DRY-RUN
Nodo ejecutable, no agregado. Lecturas: nodo y contratos WS11/WS09, código WS13 (`workspace_routes.py`, `views/workspace/`, registro de vistas), rutas de lectura deskops para RitualDoc/StepDoc/lifecycle, corpus WS40 o store temporal y tests existentes. Cambios: crear renderer y pruebas; enlazarlo desde el lector mediante el punto de registro existente; consumir solo lecturas; abrir documentos/soporte con navegación WS11; dejar pasos inertes salvo campo/API real; dibujar transiciones origen/destino/condición declarados sin POST ni avance. Dependencias/gates: WS13 con hijos cumplidos, WS09 y G_UI_READ con acta externa; si falta contrato/API, detener y registrar hueco sin sustituto. Errores: documento o soporte ausente se muestra como lectura fallida, sin inventar contenido; no hay peticiones de escritura. Validación: tests de navegación, ausencia de auto-marcado, transiciones no accionables y cero write requests; store temporal o WS40.

FUTURO
El receptor P01 emite el recibo G_UI_READ del delta; WS09/WS11 entregan catálogo y contrato; la promoción —hoy no autorizada— fija TaskDoc, archivos y escenarios; WS30 valida el flujo con una persona. Si aparece un hueco, decide el dueño del repo o del contrato.
