## REFORMULACION
**Propósito:** comprobar si sldb ya ofrece guardado raw-source reversible por API pública; si existe, basta con pruebas; si falta, completarlo sin duplicar código. **Resultado:** G_SOURCE con API pública y tests de roundtrip, conflicto, recuperación y campos protegidos. **Repo:** sldb (`src/sldb/api/documents/`, `src/sldb/cli/serve/`, `tests/`). **Límites:** no sobrescribir Markdown desde browser; depende de WS12 y de G_SLDB_WRITE/G_WRITE_CONTRACT; solo con `source_mode=editable`; promoción no autorizada.

## AMBIGUEDADES
1. «Si falta, se implementa en sldb mediante tarea propia aceptada en G_SLDB_WRITE» frente a `output_scope: src/sldb/api/documents/; src/sldb/cli/serve/; tests/`. No queda fijado si WS20 modifica directamente esos archivos o solo prepara una tarea para otro ejecutor; tampoco si esa tarea exige un recibo nuevo o reutiliza el de WS20. Obliga a inventar el modo de ejecución y la relación con G_SLDB_WRITE.
2. «Primero verificar capacidad existente» y «Si la capacidad existe, esos tests bastan». No define qué cuenta como capacidad existente frente a una parcial (por ejemplo, extracción sin roundtrip o guardado sin revisión). Obliga a inventar el umbral que decide entre verificar y completar.

## DRY-RUN
**Lecturas previstas:** nodo WS20, gates G_SLDB_WRITE/G_WRITE_CONTRACT/G_SOURCE, edge WS12, decisiones P04/P05 y reglas comunes de alcance. **Cambios previstos:** inspeccionar la API/CLI existente en sldb; si procede, añadir o completar guardado raw-source con revisión y campos protegidos; añadir tests de roundtrip, conflicto, fallo y campos protegidos. **Dependencias:** WS12 debe aportar whitelist/campos y contrato por delta; G_SLDB_WRITE antes de WS20; G_SOURCE lo produce WS20. **Validaciones futuras:** pruebas con store temporal real, prueba de no pérdida al reextraer, conflicto y recuperación; acta de G_SOURCE con commit verificable. Sin ejecutar nada.

## FUTURO
WS12 produce el contrato y la whitelist; P01 acepta el delta en sldb; la promoción fija TaskDoc, archivos y pruebas; WS21/30/31 consumen G_SOURCE. La decisión de promocionar y el preflight quedan fuera de este nodo.
