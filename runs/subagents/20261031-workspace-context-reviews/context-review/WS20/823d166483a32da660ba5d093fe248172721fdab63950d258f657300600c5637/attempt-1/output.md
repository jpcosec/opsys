## REFORMULACION

WS20 es un nodo de implementación en `sldb`, habilitado solo con `source_mode=editable`, que debe comprobar si ya existe guardado reversible de documentos raw-source mediante API pública, con revisión y preservación de campos protegidos. Si la capacidad existe y satisface toda la aceptación y G_SOURCE, bastan las pruebas; si falta o es parcial, se completa solo lo faltante en una única tarea de `sldb` aceptada en G_SLDB_WRITE. Resultado: API pública y pruebas de roundtrip, conflicto, recuperación tras fallo y campos protegidos. Repo: `sldb`, con cambios limitados a `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`. Límites: conservar solo raw-source; no sobrescribir Markdown desde browser; la precondición de payload por campos corresponde a WS45; no duplicar código existente ni crear otro productor.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Un ejecutor leería el contrato WS12 (`contratos/operaciones.md`), comprobaría los recibos G_WRITE_CONTRACT y G_SLDB_WRITE para WS20 e inspeccionaría la API, CLI y pruebas existentes en `sldb`. Si falta contrato o acta, se detendría y registraría el hueco con repo dueño, sin crear sustituto. Cambios previstos: exponer o completar el guardado raw-source con la precondición fijada por WS12, extracción/validación, protección de campos y buffer recuperable; añadir pruebas de roundtrip sin pérdida, conflicto, recuperación y campos protegidos. Si la capacidad ya cumple todo, solo añadiría pruebas y evidencia, sin duplicar código. No tocaría la precondición de payload de WS45 ni otros repos. Validación esperada: ejecutar la suite sobre un store temporal real o el corpus WS40 y reunir evidencia para G_SOURCE.

## FUTURO

WS12 debe publicar el contrato y la precondición raw-source; el receptor humano P01 debe emitir el acta G_SLDB_WRITE del delta. La promoción fijará TaskDoc, archivos y pruebas concretas. WS45 producirá por separado la precondición de payload. La evidencia de WS20 alimentará G_SOURCE y, junto con G_PAYLOAD_PRECONDITION, condicionará al consumidor WS21 en variante editable.
