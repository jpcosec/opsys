## REFORMULACION
**Propósito:** precisar el índice y la convención del manual documental, incluyendo capítulos conceptuales, un ejemplo fijo y etiquetas de disponibilidad, reutilizando el manual CLI existente.

**Resultado:** `borradores/manual.md` actualizado como estructura editorial verificable.

**Repo dueño:** `deskops`.

**Límites:** solo planificación/documentación; no implementar UI ni escribir pasos o capturas ficticios; no modificar otros outputs; requiere `G_PRODUCT`; la promoción no está autorizada.

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (WS10 y contratos de WS02/WS07/WS09/WS31), guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/manual.md`, auditoría WS02 y, de forma transitiva, WS03/WS04.

**Cambios previstos:** editar únicamente `borradores/manual.md`: precisar índice, convención por capítulo, criterios de las etiquetas disponible/propuesto/bloqueado y referencia al ejemplo fijo; enlazar el manual CLI sin duplicarlo.

**Dependencias:** WS02 y WS07; WS03/WS04 llegan transitivamente según el propio nodo. `G_PRODUCT` debe estar resuelto por WS07.

**Validaciones futuras:** contraste con la auditoría WS02–WS04; etiquetas verificables y reutilizables por WS09; ausencia de pasos/capturas ficticios; coherencia con `alcance.md` y `brief.md`. No se ejecuta nada.

## FUTURO
WS07 y el humano resuelven P01–P09, incluido P08 —ejemplo fijo— y `source_mode`; sin ese registro no pasa `G_PRODUCT`. WS02 produce la auditoría base; WS03/WS04 aportan datos transitivos. WS09 consumirá las definiciones de estado. WS31 publicará el manual probado.
