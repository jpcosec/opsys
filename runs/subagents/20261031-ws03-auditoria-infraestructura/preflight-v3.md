## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`, auditoría de solo lectura, verificable fila por fila, del estado actual de persistencia, concurrencia, referencias, búsquedas y notaciones en `sldb`, `pron` y `spec2viz`.

**Alcance:** cinco capacidades, una sección por capacidad, una fila por repo y mecanismo, columnas capacidad/repo/ubicación/operación expuesta/estado/evidencia. Estados: comprobado, ausente, hueco, con definiciones operativas dadas. Mecanismos nombrados (CAS, locks de archivo/DB, índices, renderers, ViewDoc) son hipótesis a comprobar, no hechos. ViewDoc se busca por nombre exacto; si no aparece, se registra ausente con el comando y se reporta lo existente sin asumir equivalencia.

**Repo/rutas:** lectura en `../sldb`, `../pron`, `../spec2viz`; Kimun no se lee ni entra al universo. Escritura únicamente en el entregable y en `runs/subagents/20261031-ws03-auditoria-infraestructura/` (`commands.log`, `result-summary.md`, y `tester-result-summary.md` por el Tester).

**Límites:** solo lectura fuera del entregable; sin commits ni closeout (Executor); sin modificar código, otro repo, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas de otros. Fuera de alcance WS05 Scion, contratos nuevos e implementación. Encabezado con fecha, HEAD completo por repo leído y líneas de `git status --short`; carpeta sin git se declara sin git; archivo de evidencia sucio agrega SHA-256. Lo no comprobado se marca «no comprobado» con causa.

## AMBIGUIDADES

1. «referencias documentales» — no hay definición operativa. Obligaría a inventar qué cuenta como referencia (rutas, IDs, enlaces, citas) y su granularidad.
2. «fuente/payload de documentos» — no se define la distinción fuente vs payload. Obligaría a inventar el criterio de separación.
3. «notaciones = notaciones y renderers de spec2viz» — no se enumeran las notaciones. Obligaría a inventar el conjunto a auditar (¿todas las halladas?, ¿solo las de ViewDoc?).
4. «qué existe en su lugar» (ViewDoc) — alcance difuso. Obligaría a inventar el radio de búsqueda y el criterio de reporte, aunque el texto prohíbe asumir equivalencia.
5. Formato de «fecha» y de `commands.log` no especificado. Obligaría a inventar formato (impacto bajo).
6. Directorio de ejecución de las validaciones (`build_plan.py`, `validate_plan.py`, `context_review.py` con rutas relativas) no indicado. Obligaría a inventar el cwd.

Tareas futuras asignadas (no lagunas): verificación por Tester independiente, commits/closeout del Supervisor, consumo por WS06 y WS08-12, exclusión de WS05 Scion.

## DRY-RUN

**Fuentes a leer:** el task file; `cierre.md`, `dag.yaml`, `brief.md`, `activation.md`, `context-review.md`; las cuatro pills; luego `../sldb`, `../pron`, `../spec2viz`.

**Entregable:** `infraestructura.md` (encabezado + filas), `commands.log`, `result-summary.md`.

**Comandos posteriores (sin ejecutar):** `git -C ../sldb rev-parse HEAD`; `git -C ../sldb status --short | wc -l` (ídem `pron`, `spec2viz`); `rg -n "ViewDoc" ../sldb ../pron ../spec2viz`; `rg -n -i "cas|lock|revision|hash" ...`; `rg -n -i "index|search|query" ...`; `rg -n -i "render|notation" ../spec2viz`; `git -C <repo> status --short -- <archivo>` y `sha256sum` si está sucio; validaciones del bloque Validation.

**Resultado esperado:** encabezado con HEAD y conteos por repo; filas comprobado/ausente/hueco con archivo:línea o salida; ViewDoc ausente o localizado con comando; validaciones en verde; muestreo del Tester documentado.
