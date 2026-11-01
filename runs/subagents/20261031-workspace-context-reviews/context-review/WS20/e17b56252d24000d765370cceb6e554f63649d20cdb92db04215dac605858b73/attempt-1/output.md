## REFORMULACION
WS20 es un nodo `implementation` del repo `sldb`. Su encargo es verificar primero si ya existe guardado reversible de documentos raw-source mediante API pública, con revisión y preservación de campos protegidos; si la capacidad falta o es parcial, completar solo lo faltante o implementarla en `sldb`. Resultado esperado: API pública y pruebas de roundtrip, conflicto, recuperación tras fallo y campos protegidos, produciendo `G_SOURCE`. Repo dueño: `sldb`; `output_scope`: `src/sldb/api/documents/`, `src/sldb/cli/serve/`, `tests/`. Límites: solo raw-source; la precondición de escritura de payload por campos es WS45 y no se espera; no sobrescribir Markdown desde browser; si la capacidad existe, no duplicar código; promover WS20 como tarea propia en `sldb` con el mismo recibo `G_SLDB_WRITE`.

## AMBIGUEDADES
Ninguna. Las referencias a contrato, revisión, campos protegidos y precondición tienen productor nombrado —WS12— y las ausencias se rigen por «Reglas comunes de ejecución». Los detalles de pruebas y archivos quedan al TaskDoc de promoción.

## DRY-RUN
Un ejecutor futuro leería `desk/drawer/tasks/workspace-documental/task-ws20.md`, el contrato WS12 (`contratos/operaciones.md`), los recibos de `G_SLDB_WRITE`/`G_WRITE_CONTRACT` para WS20 y el código existente en `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`. Contrastaría la capacidad real contra toda la aceptación y `G_SOURCE`. Si existe y cumple, solo añadiría/ajustaría pruebas; si es parcial, completaría lo faltante y repetiría todo el contrato; si falta, implementaría en `sldb` mediante la tarea propia aceptada, sin segundo productor.

Consumiría WS12 y sus gates por delta; no esperaría WS45. Validaría roundtrip sin pérdida de campos/secciones, conflicto con la precondición raw-source fijada por WS12, recuperación tras fallo, campos protegidos y ausencia de sobrescritura desde browser. Si falta contrato, API, dato o recibo, se detendría y registraría el hueco con repo dueño, sin sustituto. Produciría `G_SOURCE` pendiente de revisión de contrato.

## FUTURO
P01/receptor de `sldb` emite el acta concreta de `G_SLDB_WRITE`; WS12 fija el contrato y la precondición raw-source; WS45 cubre aparte la precondición de payload. WS21 consumirá `G_SOURCE` solo en variante editable. La promoción y validación final corresponden a otro nodo/humano.
