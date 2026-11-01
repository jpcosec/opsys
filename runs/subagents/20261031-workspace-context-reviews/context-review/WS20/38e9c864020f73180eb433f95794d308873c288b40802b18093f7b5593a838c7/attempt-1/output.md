## REFORMULACION

**Propósito:** verificar si sldb ya puede guardar un documento raw-source de forma reversible por API pública; si no, completar solo lo faltante. **Resultado:** capacidad existente probada o implementación mínima con tests de roundtrip, conflicto, recuperación y campos protegidos, publicando G_SOURCE. **Repo dueño:** sldb. **Límites:** `output_scope` acotado a `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`; no sobrescribir Markdown desde browser; conservar solo raw-source; la precondición de escritura de payload es un hueco separado de WS45, no de este nodo; promoción no autorizada.

## AMBIGUEDADES

ninguna

## DRY-RUN

- **Lecturas previstas:** contrato de WS12 (`contratos/operaciones.md` cuando exista), código y tests actuales de sldb en `api/documents/` y `cli/serve/`, y definición de campos protegidos producida por WS12/modelos auditados.
- **Cambios previstos:** primero comprobar capacidad existente; si satisface toda la aceptación, añadir solo pruebas. Si falta o es parcial, implementar únicamente lo faltante dentro de `output_scope` y volver a probar el contrato completo. No duplicar código ni crear un segundo productor.
- **Dependencias:** WS12 debe fijar la precondición de guardado raw-source usada en pruebas de conflicto; G_SLDB_WRITE requiere acta humana por delta; G_WRITE_CONTRACT se verifica por delta para WS20. WS20 no espera a WS45.
- **Validaciones futuras:** roundtrip guardar/extraer sin pérdida de campos ni secciones; conflicto; recuperación tras fallo; campos protegidos; API pública; acta de recepción en sldb. La aceptación no se ejecuta aquí.

## FUTURO

- WS12 produce el contrato técnico y la precondición raw-source; WS45 produce, por separado, la precondición de escritura de payload.
- El humano P01 emite el acta G_SLDB_WRITE del delta concreto en sldb.
- La promoción fija TaskDoc, archivos exactos, pruebas detalladas y evidencia; si falta capacidad, WS20 se convierte en la tarea propia aceptada en sldb.
- WS21 queda consumidor bloqueado por G_SOURCE y G_PAYLOAD_PRECONDITION.
