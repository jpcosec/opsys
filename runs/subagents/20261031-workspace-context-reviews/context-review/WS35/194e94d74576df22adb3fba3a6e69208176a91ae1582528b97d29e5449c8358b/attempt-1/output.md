## REFORMULACION
**Propósito:** revisar WS35 como encargo de planificación para una vista de solo lectura de trazabilidad de ejecución en el workspace.  
**Resultado:** mostrar mensajes, resultados y decisiones bajo su intento y tarea, enlazando cada uno a su fuente y abriendo evidencia en el lector, sin traducir `completed` a aprobado/cerrado.  
**Repo:** `graph_ui`, salida en `frontends/mindmap/views/workspace/execution/; tests/`.  
**Límites:** no incluye dispatch/reply ni aprobación; depende de WS33 y WS27; requiere G_SCION y G_UI_READ.

## AMBIGUEDADES
1. «Lectura tarea-intento-conversación-resultados-decisión» incluye **conversación**, pero la aceptación solo exige mostrar mensajes, resultados y decisiones «bajo su intento y tarea». Obligaría a inventar si debe existir un nivel visual de conversación, agruparse por ella o ignorarse.
2. «Cada mensaje, resultado y decisión se muestra bajo su intento y tarea; cada uno enlaza a su fuente» no fija qué hacer con elementos sin intento, tarea o fuente. Obligaría a inventar si se ocultan, se muestran como “sin vínculo” o producen error.

## DRY-RUN
**Lecturas:** guía, brief, alcance, decisiones, cobertura, nodo WS35, contratos vecinos WS33/WS27/WS36 y gates G_SCION/G_UI_READ.  
**Cambios previstos:** implementar la vista y sus tests en `graph_ui`; ningún cambio de backend, despacho ni aprobación.  
**Dependencias:** WS33 (incluye WS33.1/WS33.2), WS27 (incluye WS27.1/WS27.2), WS13 vía WS27, contrato WS11 para G_UI_READ y WS44 para G_SCION.  
**Validaciones futuras:** pruebas de que cada mensaje/resultado/decisión aparece bajo intento y tarea, enlaza su fuente y abre evidencia en WS13; verificación negativa de que `completed` no equivale a aprobado/cerrado; recibo G_UI_READ por delta y probe G_SCION antes de consumir la API.

## FUTURO
WS44 debe producir el probe de G_SCION; el receptor de `graph_ui` debe emitir el acta G_UI_READ del delta concreto; WS33 y WS27 deben entregar datos y evidencia; WS13 debe ofrecer el lector; la promoción y el TaskDoc quedan a decisión humana. WS36 consumirá esta vista, pero no forma parte de este nodo.
