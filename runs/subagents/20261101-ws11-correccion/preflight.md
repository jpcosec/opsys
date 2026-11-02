## REFORMULACION

- **Objetivo:** corregir en una pasada `contratos/navegacion.md` (puntos A–F y cuatro decisiones root) y una sola celda de F18a en `vistas.md`; dejar `result-summary.md` con resolución por punto y tabla por fila C/H.
- **Alcance:** leer `review-source.md` completo (prevalece); abrir cada cita de cada fila C y H y seguir cadenas de llamada; aplicar A–F; cotejar todas las filas, no muestra.
- **Repo:** `/home/jp/proyectos/SLDB_1/deskops`. Superficies: `desk/drawer/plans/workspace-documental/contratos/navegacion.md`, `.../borradores/vistas.md`, `runs/subagents/20261101-ws11-correccion/result-summary.md`.
- **Límites:** no tocar `dag.yaml`, helper, validadores, fuentes comunes, otros contratos, código, repos hermanos ni auditorías; sin commits, revisiones ni tests; sin preguntar; decisión de producto no cubierta se expone, no se improvisa.

## AMBIGUEDADES

1. «Cotejar todas las filas C y H» — no define ubicación ni numeración de filas; obligaría a inventar el mapeo fila↔sección.
2. «una celda de F18a en ... vistas.md» — no identifica la celda; habría que inferirla de `review-source.md`.
3. «Sin commits, revisiones ni tests» vs Validation «Tester independiente» y «revisión fresca» — contradicción; obliga a decidir si el ejecutor lanza revisores o solo los espera.
4. «revisión root del parche congelado antes de registrar o revisar» — «parche congelado» y su procedimiento no definidos.
5. «WS09 renovada solo si vistas.md cambió» — WS09 no se describe en el encargo.
6. «clave de sesión de modelado con alias además de Model:name» — sintaxis del alias no especificada.
7. «E7 muestra la causa recibida» — E7 no identificado en el texto.
8. «comprobación al ejecutar consumidores» (C) — mecanismo de comprobación no concreto.
9. «build --check, validate --check y status en verde» frente a «No tocar validadores» — ambiguo si ejecutar cuenta como tocar.

## DRY-RUN

1. Abrir `review-source.md` y `navegacion.md` completos.
2. Localizar tablas C y H; por fila abrir cita y cadenas (`parse_links`, `split_anchor`, `doc_status`, `notation-view.js:356`, `shell/registry.js:16`).
3. Editar `navegacion.md`: §3.3, §4, §5.4, §6, §7, §8, §10, H-03…H-06, H-09, H-14, H-16; retirar «doc_status no escribe»; fijar input de aliases y clave de sesión.
4. `vistas.md`: cambiar solo la celda F18a indicada.
5. Crear `result-summary.md` con A–F, cuatro decisiones, tabla C/H, no leído y producto pendiente.
6. Verificar con los cuatro comandos de Validation.

**Errores esperables:** cita inexistente, fila sin código localizable, contradicción con límites. **Resultado esperado:** contrato corregido y summary trazable, sin tocar dag ni validadores.
