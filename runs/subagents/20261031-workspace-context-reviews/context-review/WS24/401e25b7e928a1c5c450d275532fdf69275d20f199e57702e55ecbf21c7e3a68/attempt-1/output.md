# REFORMULACION

**Propósito:** integrar conocimiento y grafo local reutilizando el gráfico existente y una vista genérica de documento registrada en `shell/registry.js`, cubriendo átomos/protoátomos/crossroads (WS02/WS09), materializaciones, pills, clasificación y vecindad.
**Resultado:** navegación ida/vuelta por fuentes y backlinks; Markdown no modelado visible y navegable con su ruta de origen; clasificación (tipo y tags) y vecindad de hasta 2 hops; sin renderer nuevo obligatorio por clase.
**Repo:** graph_ui.
**Límites:** depende de WS13 (lector/explorador, vía sus hijos) y WS09 (catálogo); API de grafo y tags provienen de WS03/WS11; ViewDoc WS18 es opcional y no bloquea; G_UI_READ por delta; reutiliza a1b2b22 sin duplicar implementación.

# AMBIGUEDADES

1. «preservar Code local del workspace integrado a1b2b22 que identifique el acta WS11» — no dice qué debe mostrar Code respecto de un acta de WS11 (referencia, enlace, contenido) ni cómo comprobarlo; obligaría a inventar el requisito y su aceptación.
2. «La vista muestra la clasificación (tipo y tags)» frente a «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare» — para el soporte no modelado (Markdown sin modelo), que la aceptación exige visible, no hay tipo/tags; obligaría a inventar qué mostrar y cómo verificarlo.

# DRY-RUN

- **Lecturas previstas:** `dag.yaml#WS24`, `#edge:WS13`, `#edge:WS09`; brief, alcance, decisiones, cobertura, reconciliacion; en promoción, `auditoria/infraestructura.md` (WS03) y contrato WS11.
- **Cambios previstos:** `frontends/mindmap/views/workspace/graph/`, `views/workspace/node/workspace-view.js` (panel Context), `shell/registry.js`, `tests/`.
- **Dependencias:** WS13 (agregado, hijos WS13.1/13.2/13.3), WS09; transitivas WS11/WS03; G_UI_READ per-delta pendiente (intencional).
- **Validaciones futuras:** navegación ida/vuelta con backlinks; soporte no modelado visible con ruta de origen; clasificación y vecindad ≤2 hops; ausencia de renderer por clase. Sin ejecutar.

# FUTURO

- Acta G_UI_READ del delta concreto: la produce el receptor del repo dueño / solicitante P01; no se inventa aquí.
- TaskDoc de promoción fija archivos exactos, escenarios de prueba y textos de pantalla.
- Conexión condicional de ViewDoc WS18 tras G_SPEC_VIEW.
- Matriz de reconciliación WS06 al promover; validación manual en WS30.
