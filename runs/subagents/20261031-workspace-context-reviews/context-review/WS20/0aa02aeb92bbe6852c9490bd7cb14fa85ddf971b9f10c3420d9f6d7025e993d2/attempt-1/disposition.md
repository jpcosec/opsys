# Executor comparison — WS20, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION

**Propósito:** verificar si sldb ya ofrece guardado reversible de documentos raw-source y, si falta total o parcialmente, completarlo sin duplicar productor. **Resultado:** API pública de extracción/validación/guardado con revisión y preservación de campos protegidos, más tests de roundtrip, conflicto, recuperación tras fallo y campos protegidos; al promoverse, WS20 se convierte en la tarea propia en sldb que produce G_SOURCE. **Repo dueño:** sldb. **Límites:** solo `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`; no sobrescribir Markdown desde browser; si la capacidad existe, no duplicar código; si es parcial, completar solo lo faltante y reprobar todo el contrato.

##

## Hallazgos/disposición contra intención

Comparación aceptada: propósito/resultado/repo/límites coinciden con contrato; dry-run enumera fuentes, cambio futuro/hijos, dependencias y aceptación comprobable sin ejecutar. Futuro asigna APIs/actas/permisos a productores reales; no convierte decisiones base ni commit existente en aprobación de delta. Ninguna ambigüedad no resuelta. La aceptación procede del contenido completo, no APTO.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
