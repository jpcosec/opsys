REFORMULACION
Propósito: encargo de implementación en graph_ui que amplía el workspace integrado (a1b2b22) con lectura de documento/fuente, contexto, enlaces y foco, como delta conciliado.
Resultado: Markdown modelado y no modelado con render de lectura y fuente cruda íntegra; panel con identidad, relaciones del contrato WS11 y ruta de origen; seguir enlaces y alternar texto/graph/code preservando origen; foco por documento compartido entre representaciones.
Repo: graph_ui; output_scope `frontends/mindmap/views/workspace/` y `tests/`.
Límites: solo lectura, sin índices nuevos, sin workspace paralelo, sin mapeo texto→código inventado, rutas según WS11; depende de WS11 y requiere G_UI_READ por delta.

AMBIGUEDADES
1. «Seleccionar en Code, texto o graph actualiza ese foco y las demás representaciones del mismo documento lo comparten» contradice «Compartir foco solo donde exista correspondencia real de origen definida WS11; no inventar mapeo texto→código». Si WS11 no define correspondencia Code↔texto, el ejecutor debe inventar el mapeo o incumplir la aceptación.
2. «No depender de conocer un ID» exige abrir documentos sin ID, pero el explorador que lo permite es WS13.2, que `depends_on: [WS11, WS13.1]`. El ejecutor tendría que inventar una ruta de selección o adelantar trabajo de un nodo dependiente.

DRY-RUN
Lecturas: nodo WS13.1, aristas WS11/WS13/WS13.2/WS13.3, gate G_UI_READ, guía, brief, alcance, decisiones, cobertura, reconciliación y referencia externa.
Cambios previstos: delta de lectura en graph_ui bajo `views/workspace/` y tests; no modificar el plan ni otros repos.
Dependencias: contrato WS11 (identidad/origen/foco/enlaces/lectura multidesk), catálogo WS09 transitivo, recibo G_UI_READ por delta, base a1b2b22.
Validaciones futuras: Markdown no modelado con render+fuente, panel de contexto, enlaces preservando origen y foco compartido; acta externa del delta. Nada ejecutado.

FUTURO
WS11 produce el contrato de navegación y el mapa de recepción; el solicitante P01/receptor emite el acta G_UI_READ del delta. WS13.2 aporta el explorador; WS13.3 pestañas/divisiones; WS09 el catálogo de representaciones; la promoción fija TaskDoc, archivos y pruebas.
