REFORMULACION
WS47 es un nodo de implementación en sldb: producir una guarda para que la edición por campos que termina en `save_document_payload` no pierda contenido no declarado (HO-07 del contrato WS12, 6.7). Entrega inventario y pruebas focalizadas; toca `src/sldb/api/documents/` y `src/sldb/cli/serve/` solo para la guarda, y `tests/`. Límites: no amplía WS45, no cambia la creación, no resuelve el gap de prevalidación del inbox de sldb —si toca el mismo código, serie— y no admite workaround de Deskops.

AMBIGUEDADES
1. «reutiliza ese criterio antes de crear otro» (scope) frente a «sin inventar otro criterio» (acceptance). Si las comprobaciones de la guarda de deskops edit no cubren el caso, el ejecutor debe decidir si puede crear otro criterio o detenerse; ambas frases se contradicen.
2. «con un piso de detección, que son las comprobaciones de la guarda de deskops edit (_write_doc) leídas en fuente». No se enumeran qué comprobaciones forman el piso ni cómo se traducen a `save_document_payload`; el ejecutor tendría que inventar el subconjunto aplicable y su correspondencia. («se reutilizan donde apliquen» añade la misma indefinición para `refuse_structural_noise` y `refuse_undeclared_frontmatter`).

DRY-RUN
Lecturas: contrato WS12 (6.7/HO-07), `save_document_payload`, `create_document`, `track_document_file`, `refuse_*`, guarda `_write_doc` de deskops edit y tests de sldb. Cambios: inventario con ruta/símbolo/commit; guarda en las rutas autorizadas; pruebas en `tests/`. Dependencias: WS12 debe entregar el contrato; `G_SLDB_WRITE` (acta P01 por delta) y `G_WRITE_CONTRACT` deben estar; si falta contrato, API, dato o permiso, detener y registrar hueco. Errores esperados: `expected` obsoleto 409; update con pérdida rechazado con error observable y sin cambios; creación sin cambios. Validación futura: pruebas reales focalizadas, declaración de pérdidas no detectadas y casos deshabilitados; sin merge ni restauración.

FUTURO
WS12 fija HO-07, el canal y la representación; P01 emite el acta `G_SLDB_WRITE` del delta; WS19.1, WS19.2 y el recorrido directo de WS26.1 no habilitan edición con contenido no declarado hasta que WS47 pase. La promoción sigue no autorizada y exige TaskDoc/preflight; no hay aprobación de implementación/API.
