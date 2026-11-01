REFORMULACION

WS20 es un nodo de implementación en sldb que verifica si ya existe guardado raw-source reversible por API pública y, si falta, completa solo lo faltante. Resultado: documento raw-source extraído, validado y guardado con revisión esperada y campos protegidos; no sobrescribe Markdown desde browser, conserva solo raw-source y deja fuera la precondición de payload por campos de WS45. Repo dueño: sldb. Límite: source_mode editable; no duplica código ni crea segundo productor; se promueve como tarea propia aceptada en G_SLDB_WRITE. No es agregado.

AMBIGUEDADES

ninguna.

DRY-RUN

Un ejecutor futuro leería el input, `task_file`, el nodo WS20, el contrato WS12, código/API y tests actuales de sldb, y los recibos G_SLDB_WRITE/G_WRITE_CONTRACT. Primero auditaría la capacidad existente contra toda la aceptación/G_SOURCE. Si cumple, añadiría o completaría tests sin duplicar código; si falta o es parcial, implementaría lo faltante solo en `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`, mediante tarea sldb aceptada. Cambios previstos: extracción/validación/guardado raw-source con precondición fijada por WS12 y protección de campos; nunca escritura Markdown desde browser ni precondición de payload de WS45. Dependencias: WS12 debe fijar precondición raw-source y whitelist; ambos gates deben tener recibo del delta. Si falta contrato/API/permiso, se detiene y registra hueco con dueño, sin sustituto. Validación: pruebas públicas de roundtrip, conflicto, recuperación tras fallo y campos protegidos; guardar y reextraer sin pérdida; evidencia G_SOURCE con commit/blob. Errores esperados: conflicto por precondición y fallo recuperable declarado.

FUTURO

WS12 produce representación/precondición raw-source y whitelist; WS45 produce la precondición de escritura de payload por campos; el receptor P01/sldb decide y emite el acta G_SLDB_WRITE por delta; la promoción humana autoriza convertir WS20 en tarea sldb. WS20, al ejecutarse, producirá G_SOURCE; WS21 y consumidores editables esperan ese recibo.
