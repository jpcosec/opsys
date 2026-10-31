REFORMULACION

Propósito: añadir al workspace una revisión read-only de cambios Git de una tarea. Resultado: diff e historial por repo, usando commits de `TaskDoc.references` y rutas de `TaskDoc.files`; sin commits, working tree contra HEAD sobre esas rutas; una sección por repo. Repo dueño: graph_ui; salida en `frontends/mindmap/views/workspace/diff/` y `tests/`. Límites: solo lectura, sin mutar ni revertir; la asociación a intento es de WS35; integridad del store es de WS29; requiere G_UI_READ y contratos de WS11/WS12.

AMBIGUEDADES

1. «sin ejecutar ni revertir nada» frente a «Diff real e historial read-only»: prohibir "ejecutar" literalmente impide invocar Git para obtener el diff. Obligaría a inventar qué invocaciones de lectura están permitidas y por qué canal.

2. «Diff real e historial read-only acotados al repo y tarea»: no define extensión del historial (rango, profundidad, filtro por rutas, renames). Obligaría a inventar sus límites.

3. «Base: commits listados en TaskDoc.references»: no indica cómo distinguir commits de otras referencias (documentos, URLs) ni qué hacer con hashes inexistentes o clones shallow. Obligaría a inventar filtro y comportamiento de fallo.

4. «Se muestra una sección por cada repo alcanzado por TaskDoc.files, con el repo declarado»: falta la regla ruta→repo y dónde se declara el repo. Obligaría a inventar resolución y fuente de declaración.

5. «working tree contra HEAD limitado a esas rutas»: sin regla para archivos no rastreados ni repos sin HEAD. Obligaría a inventar inclusión y degradación.

6. «junto a la TaskDoc»: `depends_on` solo nombra WS13/WS12; ningún nodo listado garantiza el panel TaskDoc donde montar. Obligaría a inventar el punto de montaje o asumir una vista existente.

DRY-RUN

Lecturas futuras: DAG, TaskDoc (references/files), contrato WS11, whitelist de lectura Git WS12, acta G_UI_READ. Cambios previstos: vista diff/historial y tests en el `output_scope`; no ejecutados. Dependencias: WS13, WS12; G_UI_READ pendiente (intencional). Validaciones futuras: diff real, secciones por repo, ausencia de mutaciones y de hallazgos WS29; pruebas sobre store temporal real o corpus WS40.

FUTURO

WS11 produce rutas de lectura y G_UI_READ; WS12 registra la capability de lectura Git; WS35 añade asociación a intento; WS29 cubre integridad; WS07/G_PRODUCT resuelven P01 y el solicitante designa responsables. La promoción fijará archivos, escenarios y textos.
