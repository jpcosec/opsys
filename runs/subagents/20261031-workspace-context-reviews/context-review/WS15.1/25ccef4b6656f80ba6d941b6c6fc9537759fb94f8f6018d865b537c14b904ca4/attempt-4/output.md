## REFORMULACION

**Propósito:** encargar la implementación, en el workspace documental, de la presentación de errores de lectura y del modo degradado.

**Resultado:** errores distinguidos (referencia rota, documento ausente, modelo no importable, backend caído, fuente no editable, fallo CDN) mostrados en el panel afectado; reintento manual que recupera conexión sin perder pestañas, foco ni historia; test que cubre el fallo CDN.

**Repo:** `graph_ui`, con salida en `frontends/mindmap/views/workspace/errors/`, rutas de lectura del contrato WS11 y `tests/`.

**Límites:** depende de WS13 y del gate G_UI_READ; no incluye empaquetado offline; integración como delta o ticket existente, sin duplicado paralelo; promoción no autorizada.

## AMBIGUEDADES

ninguna.

## DRY-RUN

**Lecturas previstas:** nodo WS15.1, vecino WS13 y gate G_UI_READ en `dag.yaml`; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `reconciliacion.md`. En una ejecución futura: contrato WS11, registro de vistas del shell y APIs de lectura.

**Cambios previstos:** módulo de errores en `frontends/mindmap/views/workspace/errors/`, integración en el panel afectado y pruebas; sin borrar historial, foco ni pestañas.

**Dependencias:** WS13 aporta lector, tabs e historia; G_UI_READ pendiente, resuelto por WS11; contrato de rutas y errores de WS11; `source_mode` de P04.

**Validaciones futuras:** distinción de errores según respuesta de API, reintento manual sin pérdida de estado, test de fallo CDN y validación WS16. El gate G_UI_READ debe satisfacerse antes de despachar.

## FUTURO

WS11 produce el contrato de lectura/errores y resuelve G_UI_READ; WS07 identifica al responsable de `graph_ui`; el humano resuelve P04; WS16 valida el conjunto; la promoción fijará archivos, pruebas y textos de pantalla. WS15.2 cubre la orientación sin desk. Nada de esto se ejecuta aquí.
