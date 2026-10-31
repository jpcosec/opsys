# Executor comparison — WS20

State: requires_contract_correction_rereview

## Reformulación examinada

## REFORMULACION
**Propósito:** comprobar si sldb ya ofrece guardado raw-source reversible por API pública; si existe, basta con pruebas; si falta, completarlo sin duplicar código. **Resultado:** G_SOURCE con API pública y tests de roundtrip, conflicto, recuperación y campos protegidos. **Repo:** sldb (`src/sldb/api/documents/`, `src/sldb/cli/serve/`, `tests/`). **Límites:** no sobrescribir Markdown desde browser; depende de WS12 y de G_SLDB_WRITE/G_WRITE_CONTRACT; solo con `source_mode=editable`; promoción no autorizada.

##

## Comparación con intención / hallazgos

1 WS20 se convierte en tarea propia sldb mismo delta/recibo al promover, no segundo productor. 2 existente debe cumplir TODO G_SOURCE; parcial solo completar faltantes y volver a probar contrato entero.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
