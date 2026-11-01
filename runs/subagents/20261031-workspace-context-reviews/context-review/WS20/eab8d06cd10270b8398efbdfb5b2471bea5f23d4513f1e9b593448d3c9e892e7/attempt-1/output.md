REFORMULACION
Propósito: verificar si sldb ya puede extraer, validar y guardar documentos raw-source por API pública con revisión, o completar solo lo faltante. Resultado: API pública y pruebas de roundtrip, conflicto, recuperación y campos protegidos, sin duplicar capacidad existente. Repo dueño: sldb. Límites: solo raw-source; no sobrescribir Markdown desde browser; la precondición de payload por campos queda en WS45; no se crea un segundo productor; promoción no autorizada.

AMBIGUEDADES
Ninguna. Las ramas “verificar o completar”, el criterio de capacidad suficiente, la precondición fijada por WS12, el acta externa de G_SLDB_WRITE y la exclusión de WS45 están delimitados. Los escenarios concretos y archivos exactos corresponden al TaskDoc de promoción.

DRY-RUN
Lecturas previstas: nodo WS20 en `dag.yaml`, guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, y contratos/gates WS12, G_SLDB_WRITE, G_WRITE_CONTRACT y G_SOURCE. Cambios previstos: ninguno en esta revisión; al promoverse, inspeccionar `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`; añadir pruebas o código faltante solo si la capacidad no satisface toda la aceptación; no tocar UI ni duplicar código existente. Dependencias: contrato WS12 para la precondición raw-source y revisión; acta por delta de G_SLDB_WRITE; G_WRITE_CONTRACT verificado por efecto; `source_mode=editable`. Validaciones futuras: roundtrip sin pérdida, conflicto con la precondición de WS12, recuperación tras fallo, preservación de campos protegidos, preflight task-only y enlace de evidencia/commit.

FUTURO
WS12 fija la representación de la precondición raw-source. El receptor P01 emite el acta de G_SLDB_WRITE al preparar/promover el delta. El TaskDoc de promoción fija archivos, escenarios y textos. Un humano acepta G_SOURCE. WS45 produce por separado la precondición de escritura de payload por campos.
