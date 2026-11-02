REFORMULACION
WS20 es un nodo de implementación en `sldb`: verificar si ya existe guardado raw-source reversible por API pública, con revisión y preservación de campos protegidos; si existe y cumple, bastan pruebas; si falta o es parcial, completar solo lo faltante sin duplicar. Resultado esperado: API y tests de roundtrip, conflicto, recuperación y campos protegidos que producen `G_SOURCE`. Límites: no sobrescribir Markdown desde browser, solo raw-source, la precondición de payload por campos es WS45, promoción no autorizada, y requiere `source_mode=editable`.

AMBIGUEDADES
1. «tests de roundtrip, conflicto, recuperación tras fallo y campos protegidos»: no se define qué evidencia observable constituye «recuperación tras fallo» (¿buffer recuperable, reintento, ausencia de pérdida?). Además, la evidencia de `G_SOURCE` enumera «tests roundtrip/conflicto/campos protegidos» y omite recuperación. El ejecutor tendría que inventar el criterio de recuperación y decidir si este integra o no el gate.

DRY-RUN
No es agregado. Lecturas: contrato WS12 (`contratos/operaciones.md`) para revisión esperada y campos protegidos; recibos `G_SLDB_WRITE` y `G_WRITE_CONTRACT` referidos a WS20; código existente en `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`; parámetro `source_mode`. Cambios previstos: inventariar la capacidad real contra la aceptación; si cumple, añadir solo pruebas; si falta o es parcial, implementar extracción/validación/guardado raw-source y sus pruebas dentro del `output_scope`. Dependencias: precondición raw-source fijada por WS12; WS45 no se espera. Errores: si falta contrato, API o permiso, detenerse y registrar el hueco en `sldb`, sin crear sustituto. Validación esperada: pruebas de roundtrip, conflicto, recuperación y campos protegidos; evidencia `G_SOURCE` con commit verificable; recibo `G_SLDB_WRITE`. La promoción sigue no autorizada.

FUTURO
WS12 produce la representación de la precondición y la whitelist de campos. El solicitante P01 emite el recibo `G_SLDB_WRITE` por delta; un humano autoriza la promoción. WS45 produce aparte la precondición de payload; WS21 la consume. WS07 mantiene `source_mode`.
