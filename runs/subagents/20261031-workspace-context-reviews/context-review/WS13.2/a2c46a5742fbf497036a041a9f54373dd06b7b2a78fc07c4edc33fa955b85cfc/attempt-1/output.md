## REFORMULACION

**Propósito:** revisar WS13.2 como encargo de planificación, no como producto ni ejecución.
**Resultado:** explorador en `graph_ui` para abrir documentos modelados del store y Markdown no modelado del desk, usando rutas de lectura del contrato WS11, sin IDs ni índices nuevos.
**Repo:** `graph_ui`, salida en `frontends/mindmap/views/workspace/explorer/` y `tests/`.
**Límites:** depende de WS11 y WS13.1; requiere `G_UI_READ`; no autoriza promoción ni código.

## AMBIGUEDADES

1. «al añadir un documento al store temporal de prueba, aparece sin cambiar código»
   No fija si «aparece» significa en el árbol ya abierto, tras recarga manual o por refresco automático, ni si el mismo criterio aplica a Markdown no modelado del desk. El ejecutor tendría que inventar la semántica de actualización y el alcance de esa comprobación.

## DRY-RUN

**Lecturas previstas:** nodo WS13.2; aristas WS11 y WS13.1; gates `G_UI_READ`; guía, brief, alcance, decisiones, cobertura y reconciliación.
**Cambios previstos:** implementar el explorador dentro del `output_scope`; consumir rutas de lectura definidas por WS11; añadir pruebas en `tests/`.
**Dependencias:** WS11 debe cerrar contrato y acta `G_UI_READ`; WS13.1 aporta lectura/foco; `G_UI_READ` sigue pendiente y no se presume satisfecho.
**Validaciones futuras:** abrir un documento modelado y uno no modelado sin conocer ID ni usar índices nuevos; comprobar aparición de un documento añadido al store temporal sin cambio de código; ejecutar pruebas del explorador. Nada se ejecuta ahora.

## FUTURO

WS11 produce contrato de navegación, identidad y rutas de lectura, y el acta `G_UI_READ` con el responsable de `graph_ui` designado por WS07. WS13.1 entrega la superficie de lectura/foco. El TaskDoc de promoción fijará archivos, escenarios y textos exactos. La matriz WS06 llega transitivamente por WS11/WS12. La promoción y cualquier aceptación humana quedan fuera de este nodo.
