**REFORMULACION**

- **Propósito:** encargo de implementación en graph_ui para mostrar diff Git e historial read-only junto a una TaskDoc.
- **Resultado:** una sección por cada repo alcanzado por `TaskDoc.files`, con repo declarado, diff real e historial acotados a la tarea, sin escribir ni revertir.
- **Repo:** graph_ui; salida en `frontends/mindmap/views/workspace/diff/` y `tests/`.
- **Límites:** solo lectura; no muestra hallazgos de integridad del store (WS29); la asociación a intento llega en WS35; ruta sin repo resoluble queda no disponible; usa el contrato WS11 y campos del modelo TaskDoc de deskops; gate `G_UI_READ` por delta.

**AMBIGUEDADES**

1. «Base: commits listados en TaskDoc.references y rutas en TaskDoc.files (campos del modelo TaskDoc de deskops); sin commits, working tree contra HEAD limitado a esas rutas.» No define qué diff se muestra cuando sí hay commits: por commit, acumulado o contra el último referenciado. Obliga a inventar el resultado y deja incomprobable «Diff real».
2. «Historial baseline = commits de TaskDoc.references resolubles y ordenados por fecha de commit, limitados a TaskDoc.files». No aclara si se excluyen commits que no tocan esas rutas o si se muestran todos limitando solo el diff. Obliga a inventar el criterio de inclusión.
3. «commits de TaskDoc.references resolubles». No indica qué hacer con una referencia no resoluble —omitir, marcar o bloquear la sección—; solo hay regla para ruta sin repo. Obliga a inventar el manejo.

**DRY-RUN**

- **Lecturas previstas:** nodo WS27.1 y aristas WS27, WS13, WS12; gate `G_UI_READ`; brief, alcance, decisiones y cobertura; contrato WS11 y modelo TaskDoc al promocionar.
- **Cambios previstos:** crear la vista diff e historial en el `output_scope` y sus tests; ningún cambio de datos, Git ni store.
- **Dependencias:** WS13 para integración lectora; WS12 para contrato; WS11 para rutas/registry; `G_UI_READ` per-delta; corpus WS40 para validación.
- **Validaciones futuras:** diff/historial reales y read-only, una sección por repo, sin escritura/reversión ni hallazgos WS29; acta P01 del delta.

**FUTURO**

WS12 publica el contrato; WS11 fija rutas de lectura; WS13 integra el host; P01 emite la aceptación per-delta de `G_UI_READ`; WS29 cubre integridad; WS35 añade asociación a intento; la promoción fija archivos, pruebas y textos; WS40 aporta corpus.
