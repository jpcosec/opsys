## REFORMULACION

**Propósito:** agrupar la integración del lector workspace: documento/fuente de solo lectura, contexto, enlaces, pestañas/historia, foco, explorador de documentos modelados y no modelados, y dos documentos lado a lado.

**Resultado:** agregado no ejecutable; se cumple cuando WS13.1, WS13.2 y WS13.3 cumplen su aceptación. No produce una salida directa propia.

**Repo dueño:** `graph_ui`.

**Límites:** solo lectura; reutilizar el workspace integrado a1b2b22, el registro `shell/registry.js` y las rutas del host; no requerir índices nuevos, no crear otro workspace independiente, no duplicar implementación y no promover sin autorización. `G_UI_READ` es por delta.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas:** guía de revisión, nodo WS13, brief, alcance, decisiones, reconciliación, cobertura y gate `G_UI_READ`; los bloques de nodos vecinos se usan solo como contexto, no se revisan.
- **Cambios previstos:** ninguno.
- **Dependencias:** contrato WS11; hijos WS13.1–WS13.3; recibos `G_UI_READ` por delta.
- **Validaciones futuras:** aceptación de cada hijo y, por tanto, cierre del agregado; verificación de que cada delta tenga su recibo externo. Sin ejecución.

## FUTURO

WS11 debe fijar identidad, rutas, foco, enlaces y APIs de lectura. WS13.1–WS13.3 implementan y prueban sus deltas. El receptor P01 en `graph_ui` produce el acta de `G_UI_READ` por delta concreto; la matriz WS06 llega de forma transitiva. El TaskDoc de promoción fijará archivos y pruebas concretas. La implementación no está autorizada por este nodo.
