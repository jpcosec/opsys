## REFORMULACION
- **Propósito:** nodo agregado WS15 para cubrir errores de lectura, modo degradado y orientación de proyecto sin desk.
- **Resultado:** no ejecutable por sí mismo; se considera cumplido cuando WS15.1 y WS15.2 cumplen su aceptación.
- **Repo dueño:** `graph_ui`.
- **Límites:** salidas agregadas de WS15.1/WS15.2; depende de WS13; requiere `G_UI_READ`; sin cambios propios fuera de sus hijos.

## AMBIGUEDADES
ninguna.

## DRY-RUN
- **Lecturas previstas:** nodo WS15 en `dag.yaml`, guía de revisión, brief, alcance, decisiones y reconciliación.
- **Cambios previstos:** ninguno directo en WS15 por ser `aggregate`; las modificaciones corresponden a WS15.1 y WS15.2.
- **Dependencias:** WS13, WS15.1 y WS15.2; `G_UI_READ` con evaluación `per_delta`.
- **Validaciones futuras:** comprobar aceptación de ambos hijos; verificar recibo por delta de `G_UI_READ`; no exigir aceptación conjunta de otros nodos ni otros deltas. No ejecutar nada.

## FUTURO
- WS15.1 y WS15.2 producen las implementaciones y pruebas de error/degradación y orientación sin desk.
- WS11 produce los recibos `G_UI_READ` por delta concreto.
- WS16 realiza la validación humana de lectura y diagnóstico.
- WS06/promoción integra el delta en tarea receptora o tarea atómica; el TaskDoc fija archivos, pruebas y textos dentro de la aceptación.
- El responsable humano decide la aceptación; este nodo no la sustituye.
