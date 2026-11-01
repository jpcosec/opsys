## REFORMULACION

WS31 es un nodo ejecutable de documentación en el repo `deskops`. Su propósito es publicar el manual documental básico probado: `docs/workspace-user-manual.md`, capturas en `docs/assets/workspace-user-manual/` y átomos vinculados en `desk/atoms/`. Debe partir del índice de `borradores/manual.md` (WS10) y de lo demostrado en el acta de WS30 y la publicación de WS43. Límites: no implementa UI ni valida producto; incluye Scion solo como capítulo propuesto hasta WS38; personalización e impacto no bloquean el manual básico; no atomiza permisos ni aceptación técnica inexistente.

## AMBIGUEDADES

ninguna

## DRY-RUN

Lecturas: `borradores/manual.md` de WS10; `decisiones.md`; `contratos/navegacion.md`, `contratos/operaciones.md` y otros contratos inventariados por WS11/WS12; acta WS30 en `graph_ui`; acta de publicación WS43 en `deskops`; evidencias de WS29/G_HUMAN_MODEL si se mencionan; manual y átomos existentes.

Cambios previstos: crear o actualizar `docs/workspace-user-manual.md` con el índice, capturas reales y limitaciones; añadir assets; dejar un átomo por cada Pxx vigente y por cada contrato, enlazado al manual con fuente declarada. Etiquetas: Scion propuesto; modelos e impacto propuestos salvo evidencia. Gates: `G_HUMAN_MANUAL` debe estar satisfecho por el acta de WS30.

Errores: si falta un acta o contrato, detenerse y registrar el hueco con repo dueño; si falta evidencia WS29, no bloquear el manual básico y mantener el capítulo propuesto. Validación esperada: links resolubles, etiquetas coherentes con actas/commits y `atom→doc` verificable; un tester independiente comprueba esos criterios antes del cierre.

## FUTURO

WS38 añadirá los capítulos de delegación después de WS31. WS29 y `G_HUMAN_MODEL` podrán cambiar etiquetas de capítulos opcionales. La aprobación humana del manual la aporta el acta de WS30 (`G_HUMAN_MANUAL`); la publicación real del desk, el acta de WS43.
