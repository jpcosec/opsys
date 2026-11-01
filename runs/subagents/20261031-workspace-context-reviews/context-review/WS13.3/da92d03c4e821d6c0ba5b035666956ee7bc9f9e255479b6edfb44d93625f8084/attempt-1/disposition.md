# Disposición WS13.3, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Pestañas, dos documentos lado a lado, foco e historia, disposición local por sesión (P07), repo graph_ui, depende de WS11 y WS13.1: coincide.

**Ambigüedades.**

1. «Volver sigue el orden inverso de navegación» (qué apila historia, pila global o por división). Clase: `detalle de promoción`. caso de prueba detallado dentro de una aceptación comprobable («volver conservando foco e historia»); el scope fija foco, origen y que cambiar de pestaña/división no altera el foco guardado.
2. el nodo no nombra el selector de documentos y no depende de WS13.2. Clase: `detalle de promoción`. la aceptación solo exige abrir dos documentos y alternar; cómo se abren en la prueba (enlaces WS13.1, rutas WS11 o catálogo base a1b2b22) lo fija el TaskDoc sin exigir WS13.2. Ver promotion-notes.md.
