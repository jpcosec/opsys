## REFORMULACION
- **Propósito**: publicar en el manual documental los capítulos de delegación ya demostrados, incluyendo instrucciones de uso, evidencia real y límites.
- **Resultado**: `docs/workspace-user-manual.md` actualizado con instrucciones runtime, capturas/operaciones reales, revisión trazable, contratos y autorización documentados; átomos vinculados en `desk/atoms/`.
- **Repo dueño**: `deskops`, con `output_base: deskops:repository_root/`.
- **Límites**: nodo de documentación; no implementa ni valida delegación. Depende de WS31 y WS37; `G_HUMAN_DELEGATE` está pendiente y `promotion: not_authorized`.

## AMBIGUEDADES
1. **«mantención de contratos y autorización documentadas»**: no identifica qué contratos ni qué autorización deben documentarse —¿la evidencia de `G_HUMAN_DELEGATE`, contratos de API, política de escritura?—. Obligaría a inventar la lista de contratos y el criterio de autorización exigible.
2. **«instrucciones runtime y revisión trazable»**: no concreta qué superficies, operaciones ni artefacto de trazabilidad cubren las instrucciones. Aunque WS37 aporta el acta, el ejecutor tendría que inventar qué operaciones documentar y cómo registrar la trazabilidad.
3. **«con lo que funciona y fallos demostrados»**: no define qué fallos deben publicarse ni su fuente exacta dentro de la evidencia de WS37. Obligaría a inventar el inventario y el nivel de detalle de fallos.

## DRY-RUN
- **Lecturas previstas**: `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/manual.md`, nodo WS38 y contratos de WS31/WS37; acta de WS37 en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md`; manual publicado por WS31.
- **Cambios previstos**: redactar capítulo(s) de delegación en `docs/workspace-user-manual.md`, incorporar capturas/operaciones reales, documentar contratos/autorización y vincular átomos.
- **Dependencias**: WS31 publicado, WS37 con acta válida y `G_HUMAN_DELEGATE` satisfecho.
- **Validaciones futuras**: contraste de instrucciones contra evidencia real, ausencia de mocks, links/átomos verificados, autorización y contratos referenciados, y preflight de promoción con archivos/pills/átomos/evidencia precisos.

## FUTURO
WS37 produce el acta y satisface `G_HUMAN_DELEGATE`; WS31 entrega el manual básico. Una persona decide la promoción de WS38 y autoriza su ejecución; el nodo no se ejecuta en esta revisión.
