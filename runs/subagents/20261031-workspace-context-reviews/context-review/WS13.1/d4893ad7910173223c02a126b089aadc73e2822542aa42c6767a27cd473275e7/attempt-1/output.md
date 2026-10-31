## REFORMULACION

**Propósito:** revisar WS13.1 como encargo de planificación: lector de documento, contexto y enlaces dentro del workspace documental.

**Resultado:** delta de solo lectura en `graph_ui`: Markdown sin modelo legible, panel de contexto con identidad/relaciones/origen, seguimiento de enlaces, Code local y foco por documento/nodo compartido entre texto, graph y code, sin abrir copias ni crear un workspace paralelo.

**Repo:** `graph_ui`, en `frontends/mindmap/views/workspace/document/` y `tests/`, con rutas de lectura fijadas por el contrato WS11.

**Límites:** depende de WS11 y del gate `G_UI_READ`; no requiere índices nuevos ni ejecución autorizada. Puede ser implementación nueva o cierre/evidencia del ticket workspace draft, según el acta WS11. Promoción no autorizada.

## AMBIGUEDADES

Ninguna.

Las condiciones abiertas —representaciones soportadas, relaciones, rutas, foco y elección entre delta o ticket draft— remiten a WS11 o al catálogo WS09, que el propio nodo nombra. La ausencia de contrato se cubre con las reglas comunes de alcance, y los detalles de archivos, pruebas y textos quedan para el TaskDoc de promoción.

## DRY-RUN

**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS13.1 y bloques de contrato vecinos; `task-ws13-1.md`; contrato WS11 cuando exista; catálogo WS09; acta `G_UI_READ`; ticket workspace draft y Board de `graph_ui`; `shell/registry.js`.

**Cambios previstos:** implementar en `graph_ui` el delta de lectura en el `output_scope` declarado: render de Markdown sin modelo, panel de contexto, navegación por enlaces preservando origen, Code local y foco compartido entre representaciones; añadir pruebas. Si el acta WS11 opta por integrar el ticket draft, cerrar/evidenciar ese ticket en vez de duplicarlo. No crear índices, documentos compartidos ni otro workspace.

**Dependencias:** WS11 produce contrato y acta; `G_UI_READ` sigue pendiente y bloquea el despacho. WS09 y la matriz WS06 llegan de forma transitiva. No se detecta dependencia faltante o sobrante.

**Validaciones futuras:** aceptación de WS13.1 (Markdown legible; panel con identidad, relaciones y origen; enlace y alternancia preservando origen; foco compartido; sin conocer ID; sin copia); confirmación de no índices nuevos; solo lectura; cierre de `G_UI_READ`; preflight y TaskDoc de promoción.

## FUTURO

- WS11 entrega contrato de navegación/identidad y acta que decide delta nuevo o integración del ticket draft.
- WS07 designa al responsable de `graph_ui`; ese actor acepta `G_UI_READ`.
- WS09 fija las representaciones soportadas.
- WS13.2 y WS13.3 aportan explorador y pestañas/historia.
- Un humano decide la promoción; WS16 valida con el corpus WS40.
