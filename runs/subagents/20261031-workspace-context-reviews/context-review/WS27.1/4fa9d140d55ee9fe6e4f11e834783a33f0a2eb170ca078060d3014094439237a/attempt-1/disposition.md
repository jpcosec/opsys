# Disposición WS27.1, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Diff Git e historial read-only por repo y tarea, una sección por repo alcanzado por TaskDoc.files, sin escribir ni revertir, sin integridad de store (WS29), repo graph_ui, depende de WS13 y WS12: coincide.

**Ambigüedades.**

1. «Base: commits listados en TaskDoc.references»: qué diff se muestra cuando hay commits (por commit, rango, working tree). Clase: `detalle de promoción`. caso límite: cualquiera de las lecturas cumple la aceptación («Diff real e historial read-only acotados al repo y tarea», una sección por repo) porque el scope ya acota por commits de references y rutas de files; el TaskDoc fija la comparación. Ver promotion-notes.md.
2. rutas nuevas/no trackeadas o repo sin HEAD. Clase: `detalle de promoción`. caso de prueba; la regla común es «ruta sin repo resoluble queda no disponible, no adivinar»; el tratamiento de untracked lo fija el TaskDoc.
