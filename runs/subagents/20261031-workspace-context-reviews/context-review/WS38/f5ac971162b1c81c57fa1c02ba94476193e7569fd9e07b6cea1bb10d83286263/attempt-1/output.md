## REFORMULACION

- **Propósito:** publicar en el manual la operación de delegación y la revisión trazable “tal como quedó en WS37”.
- **Resultado:** capítulos en `docs/workspace-user-manual.md` y átomos vinculados, con pasos que remiten al acta de WS37 y a operaciones reales, documentando fallos registrados e indicando que `G_EXEC` es necesario para operar.
- **Repo:** `deskops` (`owner_repo`, `output_base`).
- **Límites:** nodo de documentación; depende de WS37 y WS31; requiere `G_HUMAN_DELEGATE`; `promotion: not_authorized`; no ejecuta delegación ni sustituye el acta por mocks o aprobación.

## AMBIGUEDADES

ninguna

## DRY-RUN

- **Lecturas:** WS38, guía, brief, alcance, decisiones, cobertura y borrador de manual; sin herramientas.
- **Cambios previstos:** añadir capítulos de delegación/revisión trazable al manual y átomos vinculados; enlazar el acta de WS37.
- **Dependencias:** acta de WS37 y `G_HUMAN_DELEGATE`; manual básico de WS31; `G_EXEC` como requisito operativo citado, no ejecutado.
- **Validaciones futuras:** cada paso cita acta/operaciones reales; fallos del acta documentados; `G_EXEC` indicado; enlaces y átomos verificados; preflight de promoción y archivos exactos, fuera de esta revisión.

## FUTURO

WS37 produce el acta y la evidencia de `G_HUMAN_DELEGATE`; un humano resuelve ese gate. WS31 produce el manual básico previo. `G_EXEC` lo autoriza un humano externo. La promoción fijará archivos, átomos y evidencia exactos; si falta el acta, rige la regla común de detenerse y registrar el hueco.
