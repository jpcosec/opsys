REFORMULACION
Propósito: verificar si sldb ya ofrece guardado reversible de documento raw-source y, si no, completar solo lo faltante. Resultado: API pública que extrae/valida y guarda raw-source con revisión/precondición y campos protegidos, más pruebas de roundtrip, conflicto, recuperación tras fallo y campos protegidos; si la capacidad existente cumple todo, bastan los tests. Repo dueño: sldb; rutas permitidas: `src/sldb/api/documents/`, `src/sldb/cli/serve/`, `tests/`. Límites: no sobrescribir Markdown desde browser; conservar solo raw-source; la precondición de payload por campos es WS45 y no se espera; no crear segundo productor; promoción no autorizada; solo aplica con `source_mode=editable`.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: nodo WS20 y gates G_SLDB_WRITE/G_WRITE_CONTRACT/G_SOURCE; guía, brief, alcance, decisiones, cobertura; contrato WS12 cuando exista; API y tests actuales de sldb. Cambios previstos: ninguno aún; tras verificar, solo tests si la capacidad es completa, o implementación de lo faltante dentro del `output_scope` y repetición de todo el contrato si es parcial. Dependencias: contrato/precondición raw-source de WS12; acta humana G_SLDB_WRITE por delta; G_WRITE_CONTRACT por efecto; `source_mode` editable. Validaciones futuras: roundtrip sin pérdida de campos/secciones; conflicto con la precondición que fije WS12; recuperación tras fallo; campos protegidos; API pública; el TaskDoc de promoción fija archivos y escenarios.

FUTURO
WS12 produce el contrato y la precondición raw-source. El receptor P01 emite el acta G_SLDB_WRITE del delta. WS45 produce la precondición de escritura de payload por campos. La promoción/TaskDoc fija archivos, pills y pruebas; G_SOURCE queda producido por WS20 y su recepción se verifica por delta. Nada se ejecuta ni se autoriza aquí.
