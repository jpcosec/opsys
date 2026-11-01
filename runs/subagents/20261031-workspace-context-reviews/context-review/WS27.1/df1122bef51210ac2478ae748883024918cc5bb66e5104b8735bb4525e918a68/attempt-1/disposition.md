# Disposición WS27.1, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Diff e historial read-only por repo y tarea, sección por repo alcanzado por TaskDoc.files, sin integridad de store, repo graph_ui, depende de WS13 y WS12: coincide.

**Ambigüedades.**

1. «ordenados por fecha de commit» sin sentido. Clase: `detalle de promoción`. detalle de presentación que no afecta la aceptación; lo fija el TaskDoc.
2. commits resolubles pero ninguno toca `TaskDoc.files`, o `files` vacío. Clase: `detalle de promoción`. caso de prueba; el scope acota el historial a files y para cero commits indica qué hacer; el resto lo fija el TaskDoc (ver promotion-notes.md, que además cubre qué diff se muestra con commits).
3. referencias no resolubles. Clase: `no es ambigüedad`. el scope usa «commits de TaskDoc.references resolubles»: solo esos entran al historial; advertir u omitir es presentación.
