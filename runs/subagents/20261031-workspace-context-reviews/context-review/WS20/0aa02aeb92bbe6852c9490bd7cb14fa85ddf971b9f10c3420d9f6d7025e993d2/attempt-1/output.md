## REFORMULACION

**Propósito:** verificar si sldb ya ofrece guardado reversible de documentos raw-source y, si falta total o parcialmente, completarlo sin duplicar productor. **Resultado:** API pública de extracción/validación/guardado con revisión y preservación de campos protegidos, más tests de roundtrip, conflicto, recuperación tras fallo y campos protegidos; al promoverse, WS20 se convierte en la tarea propia en sldb que produce G_SOURCE. **Repo dueño:** sldb. **Límites:** solo `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`; no sobrescribir Markdown desde browser; si la capacidad existe, no duplicar código; si es parcial, completar solo lo faltante y reprobar todo el contrato.

## AMBIGUEDADES

Ninguna. Los elementos que podrían parecer huecos tienen productor o resolución explícita:

1. «con revisión y preservación de campos protegidos»: qué campos son protegidos lo fija el contrato WS12, dependencia declarada y scope_nodes de G_WRITE_CONTRACT; no obliga a inventar.
2. «se implementa en sldb mediante tarea propia aceptada en G_SLDB_WRITE» / «WS20 se convierte en esa tarea propia»: la segunda frase aclara que no hay segundo productor ni tarea paralela.
3. «Capacidad existente significa que satisface todos los requisitos»: define el criterio de comprobación; no queda a criterio del ejecutor.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (nodo WS20, gates G_SLDB_WRITE/G_WRITE_CONTRACT/G_SOURCE), `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md` (P04) y `cobertura.md` (UF03/UF04). **Cambios previstos, sin ejecutar:** inventariar API/tests existentes en sldb; si existe capacidad completa, añadir o completar solo tests; si falta, implementar en `src/sldb/api/documents/` y `tests/`; tocar CLI solo si el contrato lo exige. **Dependencias:** contrato WS12 y recibo humano G_SLDB_WRITE por delta; G_SOURCE queda producido por este nodo. **Validaciones futuras:** roundtrip sin pérdida de campos/secciones, conflicto con revisión esperada, recuperación tras fallo, campos protegidos, ausencia de sobrescritura Markdown desde browser; preflight de promoción y TaskDoc.

## FUTURO

WS12 produce el contrato de operaciones; el receptor humano P01 emite el acta G_SLDB_WRITE al preparar/promover el delta; el TaskDoc de promoción fija archivos, escenarios y textos; WS21 consume G_SOURCE y permanece bloqueado hasta que WS20 lo produzca. Nada de esto es ambigüedad del encargo.
