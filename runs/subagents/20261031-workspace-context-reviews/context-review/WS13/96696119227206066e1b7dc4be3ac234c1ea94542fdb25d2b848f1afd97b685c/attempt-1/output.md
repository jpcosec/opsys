## REFORMULACION

**Propósito:** revisar si WS13, tal como está escrito, se entiende como encargo de planificación verificable, sin evaluar el producto ni ejecutar nada.

**Resultado:** nodo `aggregate` no ejecutable que agrupa WS13.1 (lectura de documento, contexto y enlaces), WS13.2 (explorador de documentos modelados/no modelados) y WS13.3 (pestañas, divisiones e historia). Su aceptación se satisface cuando sus hijos cumplen la suya.

**Repo dueño:** `graph_ui`, con integración `delta_or_existing_ticket` sobre el ticket workspace en draft.

**Límites:** documento/fuente solo lectura; mantener Code local y rutas del host; no requerir índices nuevos; reutilizar `shell/registry.js`; sin workspace paralelo; promoción no autorizada.

## AMBIGUEDADES

Ninguna.

Las posibles dudas quedan cubiertas por fuentes suministradas: el contrato de navegación e identidad lo produce WS11 («contratos/navegacion.md»), el gate `G_UI_READ` tiene resolver y evidencia definidos, y los detalles de archivos, textos y pruebas se delegan al TaskDoc de promoción. La elección entre implementar o conciliar el ticket draft queda nombrada en WS13.1 («Si el acta de WS11 eligió integrar el ticket draft…»).

## DRY-RUN

**Lecturas previstas:** nodo WS13 y aristas de WS11, WS13.1–3 y gate `G_UI_READ`; guía, brief, alcance, decisiones, cobertura, reconciliación y dag.

**Cambios previstos:** ninguno; esta revisión no modifica artefactos ni ejecuta código.

**Dependencias:** WS11 (contrato de navegación e identidad y acta `G_UI_READ`), WS13.1, WS13.2 y WS13.3; gate `G_UI_READ` pendiente de forma intencional.

**Validaciones futuras:** acta de aceptación del delta de lectura con responsable designado en WS07 y lista `scope_nodes`; aceptación individual de los tres hijos; preflight y TaskDoc de promoción con archivos, pruebas y evidencias.

## FUTURO

WS07 debe designar al responsable de `graph_ui`; WS11 debe producir el contrato y el acta de `G_UI_READ`. El humano resuelve P01/P07 y Autoriza o no la promoción. La promoción fija archivos y pruebas exactas. WS14, WS15, WS22, WS24, WS27, WS41 y demás dependientes consumen WS13 una vez cerrado.
