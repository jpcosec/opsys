## REFORMULACION
Encargo: definir e implementar en graph_ui la presentación de errores de lectura y modo degradado del lector, como delta sobre el workspace integrado. Resultado: el panel afectado muestra referencia rota, documento ausente, modelo no importable, backend caído, fuente no editable y fallo CDN, sin borrar historial, pestañas ni foco, y sin fingir vacío; un reintento manual recupera el estado. Repo: graph_ui; salida en `frontends/mindmap/views/workspace/errors/` más `tests/`. Límites: solo lectura/error, sin empaquetado offline; depende de WS13, del contrato de lectura WS11 y del gate G_UI_READ por delta; no autoriza promoción.

## AMBIGUEDADES
1. «Errores distinguidos por la respuesta de la API, según contrato WS11», frente a «backend caído» y «Fallos de CDN visibles como límite actual». Si no hay respuesta de API, no existe respuesta que distinga backend o CDN caídos; obliga a inventar detección, criterio de aceptación y relación con el contrato WS11.
2. «Leer Markdown existente cuando el soporte lo permita». No define qué soporte ni condición verificable; obliga a inventar qué Markdown es legible y si incluye fuente raw, lo que excedería `output_scope` y ya corresponde a WS13.1/WS20.
3. «tras reintento manual recuperar conexión sin perder pestañas, foco ni historia». No aclara si «conexión» es backend, CDN o ambas, ni cómo se comprueba la recuperación; obliga a inventar el escenario y la evidencia de aceptación.
4. «fuente no editable» figura entre los errores, pero P04 admite read-only y editable solo tras API reversible; obliga a decidir si se muestra como error, como límite o como estado read-only.

## DRY-RUN
Lecturas previstas: `dag.yaml` (WS15.1, WS13, gates), guía, brief, alcance, decisiones, cobertura y reconciliación. Cambios previstos: módulo de errores/degradación y pruebas en graph_ui; no tocar el contrato WS11 ni otros repos. Dependencias: WS13/WS13.1, contrato WS11 transitivo y acta G_UI_READ. Validaciones futuras: pruebas por tipo de error, reintento conservando pestañas/foco/historia, simulación de CDN no disponible y no regresión de lectura. Sin ejecución.

## FUTURO
WS13/WS13.1 producen lectura y estado; WS11, el contrato de rutas y errores; el receptor humano P01 emite el acta G_UI_READ de este delta; el TaskDoc de promoción fija archivos, pills, textos y casos de prueba; WS16 valida sobre corpus WS40; WS15.2 cubre el proyecto sin desk; WS06 reconcilia sin duplicar implementación.
