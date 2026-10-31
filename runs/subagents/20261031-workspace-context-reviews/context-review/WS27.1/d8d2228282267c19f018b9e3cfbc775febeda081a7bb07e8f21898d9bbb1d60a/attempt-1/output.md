REFORMULACION
- Propósito: revisar si WS27.1 está bien planteado como encargo de planificación, sin evaluar producto ni ejecutar.
- Resultado: vista read-only de diff Git e historial junto a la TaskDoc, acotada a repo y tarea, con una sección por repo alcanzado por `TaskDoc.files`.
- Repo: `graph_ui`; salida en `frontends/mindmap/views/workspace/diff/` y `tests/`.
- Límites: sin escritura ni reversión; fuera asociación a intento (WS35) y hallazgos de integridad del store (WS29). Depende de WS13/WS12 y `G_UI_READ` pendiente; candidato no autorizado.

AMBIGUEDADES
1. «Se muestra una sección por cada repo alcanzado por TaskDoc.files, con el repo declarado.» No se indica dónde ni quién declara el repo, ni cómo derivarlo de las rutas. Obligaría a inventar el campo, formato y criterio de agrupación.
2. «commits listados en TaskDoc.references» no precisa cómo distinguir commits de otras referencias ni el formato esperado (hash, repo, tipo). Obligaría a inventar el criterio de selección y validación de referencias.
3. «Diff Git e historial read-only» y «sin commits, working tree contra HEAD limitado a esas rutas» no fijan el alcance del historial sin commits ni si incluye solo las rutas o todos los commits referenciados. Obligaría a inventar el rango y contenido del historial.

DRY-RUN
- Lecturas: guía, brief, alcance, decisiones, cobertura y nodo WS27.1 con sus aristas, sin herramientas.
- Cambios previstos: ninguno en esta revisión. Una promoción futura implementaría solo la vista de diff en el scope declarado y pruebas.
- Dependencias: WS13 y WS12; `G_UI_READ` pending; rutas de lectura por contrato WS11; WS35 y WS29 quedan fuera.
- Validaciones futuras: diff/historial reales y read-only, secciones por repo declarado, ausencia de escritura/reversión y de hallazgos de integridad.

FUTURO
WS12 debe producir la capability exacta de lectura Git; WS11, las rutas; la promoción fijará TaskDoc, archivos, pruebas y evidencia. Un humano resuelve `G_UI_READ` y las decisiones Pxx. WS35 añade asociación a intento y WS29, integridad del store.
