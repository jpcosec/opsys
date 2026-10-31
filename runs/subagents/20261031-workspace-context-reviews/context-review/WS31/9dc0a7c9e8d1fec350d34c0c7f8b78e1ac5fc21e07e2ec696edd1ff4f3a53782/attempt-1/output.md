## REFORMULACION

**Propósito:** publicar un manual documental básico que recoja navegación, edición, captura, trabajo manual y revisión ya demostrados. **Resultado:** `docs/workspace-user-manual.md`, `docs/assets/workspace-user-manual/` y átomos vinculados en `desk/atoms/`. **Repo dueño:** `deskops`. **Límites:** no publicar como disponibles capacidades no demostradas; Scion queda como capítulo propuesto hasta WS38; personalización/impacto se etiquetan o comprueban sin bloquear el manual básico; no se atomizan Pxx pendientes; no se ejecuta nada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** nodo WS31 y gates en `dag.yaml`; guía de revisión; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`; `borradores/manual.md`; contratos de vecinos WS30, WS10, WS43, WS38 y entradas de gates. **Cambios previstos:** crear/actualizar el manual, su directorio de assets y átomos enlazados; sin cambios de código ni de otros repos. **Dependencias:** acta y gate de WS30 (`G_HUMAN_MANUAL`), índice/convención de WS10, acta de publicación de WS43; contratos de WS11/WS12 de forma transitiva; WS29/WS39 solo condicionalmente para capítulos extras. **Validaciones futuras:** que cada instrucción remita a un acta; etiquetas, links y `atom->doc` verificados; ningún Pxx pendiente atomizado; Scion marcado propuesto; capturas y limitaciones coherentes con las actas; nada se ejecuta en esta revisión.

## FUTURO

WS30 debe producir el acta humana y satisfacer `G_HUMAN_MANUAL`; WS43 debe producir el acta de publicación y el commit correspondiente; WS38 añadirá después los capítulos verificados de delegación. La persona responsable debe resolver las Pxx y aprobar los gates aplicables. La promoción fijará archivos, pills, átomos, evidencia y preflight task-only; WS29/WS39 y `G_HUMAN_MODEL` solo condicionan capítulos no básicos.
