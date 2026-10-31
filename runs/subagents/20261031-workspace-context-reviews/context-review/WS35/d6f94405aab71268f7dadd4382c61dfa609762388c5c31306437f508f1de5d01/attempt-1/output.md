REFORMULACION
Propósito: revisar WS35 como encargo de planificación para una vista de lectura de ejecución y trazabilidad. Resultado: UI en `graph_ui` que muestra mensajes, resultados y decisiones bajo intento/tarea, enlaza fuentes y abre evidencia en el lector WS13, sin traducir `completed` en aprobado/cerrado. Repo: `graph_ui`; salida en `frontends/mindmap/views/workspace/execution/` y `tests/`. Límites: lectura; no mutaciones, dispatch, cierre ni aprobación; sujeto a `G_SCION` y `G_UI_READ`; archivos, pruebas y textos concretos quedan al TaskDoc de promoción.

AMBIGUEDADES
1. «Lectura tarea-intento-conversación-resultados-decisión» frente a «Cada mensaje, resultado y decisión se muestra bajo su intento y tarea». No se define qué hacer con «conversación»: nivel de agrupación, metadato o simple origen. Obligaría a inventar su representación y si se prueba.
2. «Cada mensaje… se muestra bajo su intento y tarea» contradice WS33.1: «un mensaje … sin intento resoluble no se vincula y registra la procedencia como hueco». Obligaría a inventar si esos mensajes se ocultan, se muestran aparte o bajo qué criterio.
3. «decisión de WS32/WS33» no precisa si la decisión viene de WS32, de WS33.2 o de ambos, ni cómo se muestra una decisión sin intento. Obligaría a inventar el mapeo y la aceptación de ese caso.

DRY-RUN
Lecturas: `task-ws35.md`, contratos de WS33.1/WS33.2, WS27 y WS11/12, y reglas de alcance. Cambios previstos: vista de ejecución y tests dentro de `output_scope`; sin ejecución real. Dependencias: WS33 y WS27; WS13 vía WS27 para evidencia; gates `G_SCION` y `G_UI_READ` por delta. Validaciones futuras: agrupación y enlaces, apertura de evidencia en el lector, no equivalencia `completed`=aprobado/cerrado; escenarios exactos en TaskDoc.

FUTURO
WS44 produce probe/contrato `G_SCION`; WS33.1/WS33.2 producen vínculos y decisión; WS27 diff/evidencia; WS13 lector; el receptor de `graph_ui` emite acta `G_UI_READ` del delta; la promoción fija TaskDoc, archivos y pruebas.
