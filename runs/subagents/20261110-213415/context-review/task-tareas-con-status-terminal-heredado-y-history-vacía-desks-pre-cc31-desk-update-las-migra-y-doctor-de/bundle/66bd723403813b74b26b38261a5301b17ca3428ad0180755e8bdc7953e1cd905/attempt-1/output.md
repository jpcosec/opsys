## REFORMULACION

Propósito: corregir d1 (no hay vía de migración para tareas pre-CC31 con status terminal heredado y `history` vacía) y d2 (doctor y `desk update` caen enteros ante el primer documento inválido). Resultado: `deskops desk update --apply` migra las tareas heredadas según la tabla de d1 (superseded → `history [superseded]`; closed/resolved/done/complete/cancelled → `current_node ''`; deferred/candidate → `current_node ''`), reporta una línea por campo cambiado y deja como hallazgo, sin escribir, lo que no puede decidir; doctor y `desk update` listan los inválidos uno por uno y siguen. Repo: deskops (archivos del TaskDoc). Límites: no relajar el validador salvo `cancelled` en `LEGACY_RESOLVED_STATUSES`; no tocar desks de AntonIA; gramática CLI intacta. Es un nodo ejecutable (task.debug), no agregado; no liga pills ni átomos.

## AMBIGUEDADES

1. "las cinco formas de la reproducción del gateway" (Validation) frente a b6: "las 5 tareas ... más una cancelled y una closed". ¿El test de reproducción cubre 5 o 7 fixtures? Obligaría a inventar el alcance de la tabla probada.
2. "migra las tareas ... y reporta las que no puede decidir" frente a b9, que fija veredicto solo para doctor: "una tarea inválida es un error (exit distinto de 0...)". No se dice el exit code de `desk update --apply` cuando solo reporta indecidibles; habría que inventar 0 o 1.
3. "una segunda corrida no cambia nada" frente a b4: "línea de migración ... por cada campo cambiado". ¿La segunda corrida imprime cero líneas o repite el reporte? Obligaría a inventar la salida idempotente.
4. b1 define "una sugerencia fija" para los hallazgos de migración; b9 solo pide para doctor "una línea por documento". ¿La línea de doctor incluye también la sugerencia fija? Habría que inventarlo.

## DRY-RUN

Lecturas: `TaskDoc`/`lifecycle_errors`, seeds de `deskops/data/lifecycle/`, `desk.py`, `workspace.py` (`_task_type_migration_plan`, `pending_task_type_migration`), `doctor_findings.py`, `services/closure.py`, `closeout.py`, `tests/`, `docs/operator-manual.md`, `CHANGELOG.md`. Cambios previstos: helper que lee frontmatter, aplica la tabla con `history` vacía y `current_node` no vacío (b7 incluido), escribe por `desk_transaction`/`sldb replace_text`, revalida con el modelo y revierte si sigue inválida; reporte b4; en doctor y `desk update`, recorrido por documento capturando `ValidationError` como hallazgo; fixtures b6; doc y CHANGELOG (Fixed). Dependencias: `sldb replace_text`, tabla de ciclo de vida, guarda `pgrep`/`TMPDIR` (b3). Validaciones futuras: las cinco de Validation más los 4 pasos de b2.

## FUTURO

El coordinador corre los 4 pasos del workflow en clon limpio y abre la nota a sldb (b5); los dueños de AntonIA y demás desks ejecutan `desk update --apply`; queda revisable sumar `cancelled` a `LEGACY_RESOLVED_STATUSES` y como hipótesis si `sldb stores check` aborta en el primer documento inválido.
