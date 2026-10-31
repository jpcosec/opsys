## REFORMULACION
**Propósito:** comprobar si sldb ya ofrece guardado reversible de documentos raw-source; si no, completarlo sin duplicar mecanismos existentes.

**Resultado:** API pública de extracción/validación/guardado con revisión y preservación de campos protegidos, más tests de roundtrip, conflicto, recuperación tras fallo y campos protegidos. Si la capacidad existe, bastan los tests; si falta, se implementa en sldb mediante tarea aceptada en `G_SLDB_WRITE`.

**Repo:** `sldb`, con alcance en `src/sldb/api/documents/; src/sldb/cli/serve/; tests/`.

**Límites:** no sobrescribir Markdown desde browser; no duplicar código si la capacidad ya existe.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** nodo WS20, arista WS12, gates `G_SLDB_WRITE`, `G_WRITE_CONTRACT` y `G_SOURCE`, `source_mode`, guía, brief, alcance y decisiones.

**Cambios previstos:** si la capacidad existe, añadir/ajustar tests en `tests/`; si falta, implementar en `src/sldb/api/documents/` y/o `src/sldb/cli/serve/` con tests. No se ejecuta nada.

**Dependencias:** WS12 debe producir `G_SLDB_WRITE` y `G_WRITE_CONTRACT`; el nodo solo se habilita con `source_mode=editable`. Si falta contrato/API/permiso, se registra el hueco y la operación queda no disponible.

**Validaciones futuras:** roundtrip sin pérdida de campos/secciones, conflicto, recuperación tras fallo, campos protegidos y API pública; revisión de contrato para `G_SOURCE`.

## FUTURO
- WS07/humano debe resolver P04 y fijar `source_mode`; mientras siga `pending`, WS20 no se habilita.
- WS12 produce la whitelist, campos protegidos, canal/actor y accepted task de `G_SLDB_WRITE`.
- La promoción de WS20 exige preflight y TaskDoc; no está autorizada.
- `G_SOURCE`, producido por WS20, habilita el consumo posterior por WS21.
- WS16/WS30 realizarán validaciones de entrega posteriores, no de este encargo.
