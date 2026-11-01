## REFORMULACION
Encargo: comprobar si `sldb` ya ofrece guardado raw-source reversible por API pública y, si falta o es parcial, completarlo sin duplicar código. Resultado: API pública y tests de roundtrip, conflicto, recuperación tras fallo y campos protegidos; produce `G_SOURCE`. Repo dueño: `sldb`, con `output_scope` en `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`. Límites: conserva solo raw-source; la precondición de escritura de payload por campos es un hueco separado de WS45 y no se espera; no sobrescribir Markdown desde browser; habilitado solo con `source_mode=editable`; promoción no autorizada; no crear segundo productor.

## AMBIGUEDADES
ninguna

## DRY-RUN
No es agregado: es un nodo de implementación ejecutable cuando se autorice la promoción. Un ejecutor futuro, con `source_mode=editable` y los gates `G_SLDB_WRITE` y `G_WRITE_CONTRACT` resueltos para WS20, leería el contrato WS12 —incluida la precondición de guardado raw-source—, el acta de recepción en `sldb` y el código/tests existentes en `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`. Contrastaría la capacidad existente con toda la aceptación: si satisface `G_SOURCE`, añadiría o verificaría los tests exigidos sin duplicar código; si falta o es parcial, implementaría solo lo faltante en esas rutas y añadiría tests. No consumiría WS45. Errores previstos: contrato o recibo ausente → detenerse y registrar hueco con repo dueño; conflicto → precondición falla y buffer recuperable; fallo tras escritura → recuperación sin pérdida; campo protegido → preservado o rechazado; roundtrip con diferencias → test falla. Validación esperada: tests de roundtrip, conflicto, recuperación y campos protegidos en verde, `G_SOURCE` satisfecho y ausencia de código duplicado.

## FUTURO
WS12 fija la precondición raw-source y emite `G_WRITE_CONTRACT` por delta. El receptor humano P01 emite el acta `G_SLDB_WRITE` en `sldb` al preparar/promover el delta. La promoción —hoy no autorizada— fija archivos, escenarios y evidencia en el TaskDoc. WS45 cubre la precondición de payload por campos. WS21 consume `G_SOURCE` y `G_PAYLOAD_PRECONDITION`. WS16 valida después las mutaciones de UI.
