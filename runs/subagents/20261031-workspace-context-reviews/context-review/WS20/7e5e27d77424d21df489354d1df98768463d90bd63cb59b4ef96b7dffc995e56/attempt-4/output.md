REFORMULACION
Propósito: comprobar si sldb ya ofrece guardado raw-source reversible y, solo si falta, completarlo. Resultado: API pública con roundtrip, conflicto, recuperación tras fallo y preservación de campos protegidos, más tests y G_SOURCE. Repo dueño: sldb, con output_scope en `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`. Límites: no sobrescribir Markdown desde browser, no duplicar código si la capacidad existe, y el nodo solo aplica con `source_mode=editable`.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas previstas, sin ejecutar: contrato y gates de WS12 (`G_SLDB_WRITE`, `G_WRITE_CONTRACT`), resolución de P04/`source_mode`, reglas de alcance, corpus WS40 y APIs/tests existentes en sldb. Cambios previstos: si la capacidad existe, solo tests de roundtrip, conflicto, recuperación y campos protegidos; si falta, implementación acotada al output_scope y a la tarea aceptada en sldb. Dependencias: WS12 debe haber emitido contrato, gates e identidad del responsable sldb; el corpus WS40 respalda validaciones. Validaciones futuras: guardar y reextraer sin pérdida de campos/secciones, rechazo por conflicto, recuperación tras fallo, campos protegidos intactos y revisión de contrato para G_SOURCE.

FUTURO
WS07 resuelve P04 y fija `source_mode`; WS12 produce el contrato, la whitelist por campo/operación y los gates, además de identificar al responsable sldb. El TaskDoc de promoción fija archivos exactos, escenarios y evidencias. La promoción requiere autorización humana; WS16/WS30 validan después lectura/edición según el modo elegido.
