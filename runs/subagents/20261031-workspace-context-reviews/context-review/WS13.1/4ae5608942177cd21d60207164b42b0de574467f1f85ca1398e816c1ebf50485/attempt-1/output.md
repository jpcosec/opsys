## REFORMULACION
**Propósito:** entregar en `graph_ui` la lectura de documento/fuente, panel de contexto, enlaces y selección compartida texto/graph/code. **Resultado:** lector read-only con foco por documento/nodo y origen preservado. **Repo:** `graph_ui`, como delta o integración en el ticket workspace draft según acta WS11. **Límites:** mantener rutas del host, no exigir índices nuevos ni crear otro workspace independiente.

## AMBIGUEDADES
1. «Markdown sin modelo legible»: no define qué evidencia demuestra “legible” ni la representación mínima exigida. Obligaría a inventar el criterio de aceptación y la prueba.
2. «La selección por documento/nodo fija el foco del documento abierto»: no precisa qué foco resulta al seleccionar el documento completo —frente a un nodo— ni cómo se refleja en texto/graph/code. Obligaría a inventar la semántica de foco a nivel documento.

## DRY-RUN
- **Lecturas:** guía, brief, alcance, decisiones, cobertura, reconciliación y nodo WS13.1; sin herramientas ni ejecución.
- **Cambios previstos:** ninguno en esta revisión. Al promover/ejecutar: `frontends/mindmap/views/workspace/document/` y `tests/`, con rutas de lectura del contrato WS11.
- **Dependencias:** WS11 y su acta `G_UI_READ`; catálogo WS09 vía WS11; ticket workspace draft en `graph_ui`; designación del responsable receptor por WS07.
- **Validaciones futuras:** comprobar lectura sin modelo, panel con identidad/relaciones/origen, enlaces, alternancia texto/graph/code, foco compartido sin copia, ausencia de índices nuevos y evidencia del gate. Promoción aún no autorizada: exige preflight y TaskDoc.

## FUTURO
WS11 decide contrato, acta de aceptación e integración con el ticket draft; el responsable de `graph_ui` acepta el delta; WS09 aporta el catálogo de representaciones; la promoción fija TaskDoc, archivos y pruebas; el humano resuelve P01/P07 cuando corresponda.
