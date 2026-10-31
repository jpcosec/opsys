## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md` como auditoría de solo lectura, verificable fila por fila, del estado actual de persistencia/fuente-payload, concurrencia/locks, referencias documentales, búsquedas/índices y notaciones/renderers de spec2viz, incluyendo el alcance real de ViewDoc.

**Alcance:** una sección por capacidad y, dentro, filas por repo y mecanismo con columnas capacidad, repo, ubicación, operación expuesta, estado (`comprobado`/`ausente`/`hueco`) y evidencia. Se auditan `../sldb`, `../pron` y `../spec2viz`; Kimun queda fuera del universo y no se lee. Los mecanismos nombrados (CAS, locks, índices) son hipótesis a comprobar, no hechos. Se registran también filas para mecanismos ausentes.

**Repo y límites:** el Executor solo escribe el entregable y evidencia en `runs/subagents/20261031-ws03-auditoria-infraestructura/`; no hace commits, no corre closeout y no modifica código, otros repos, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas de otros. Supervisor valida/commitea/cierra; Tester independiente muestrea filas.

## AMBIGUEDADES

1. «Rutas de lectura: ../sldb, ../pron, ../spec2viz». No se declara la base de esas rutas relativas. Obligaría a inventar si son relativas a `deskops`, al repo dueño o al run; una ruta inexistente se confundiría con ausencia de mecanismo.
2. «ViewDoc: buscar el nombre exacto en los tres repos; si no aparece se registra ausente con el comando usado». No define mayúsculas/minúsculas, variantes (`viewdoc`, `View Doc`) ni si “nombre exacto” cubre archivos, símbolos y comentarios. Obligaría a inventar el criterio de búsqueda y, por tanto, el de ausencia.
3. «Si un archivo citado como evidencia está sucio, se agrega su SHA-256 para fijar lo leído». No define “sucio” (¿`git status` del repo de origen?), ni dónde va el hash (encabezado, fila o `commands.log`). Obligaría a inventar formato y alcance.
4. «Hash = SHA-256 de los bytes del archivo». No dice qué archivos exigen hash: ¿solo evidencia sucia, el entregable, `commands.log`, todos los citados? Obligaría a inventar el inventario de hashes.
5. «Operación expuesta = comando CLI, ruta HTTP o función pública importable». No fija convención de “pública importable” por lenguaje. Obligaría a inventar qué símbolos cuentan.

No hay ambigüedad sobre roles, límites de escritura ni exclusión de Kimun. WS02–04, WS05, WS06, WS08–12 y WS13+ son tareas futuras asignadas, no lagunas de este encargo.

## DRY-RUN

**Fuentes a leer:** task doc, `cierre.md`, `brief.md`, pills y rituales enlazados; luego, en solo lectura, archivos de `../sldb`, `../pron` y `../spec2viz` relacionados con documentos/payload, CAS/revisión/hash, locks, referencias, índices/búsquedas y renderers/notaciones.

**Entregable:** `infraestructura.md` con encabezado (fecha, HEAD completo y líneas de `git status --short` por repo leído; “sin git” si aplica), secciones por capacidad y filas con evidencia `archivo:línea` o salida de comando. Evidencia: `commands.log` y `result-summary.md`.

**Comandos posteriores (sin ejecutar):** `git -C ../sldb rev-parse HEAD`; `git -C ../sldb status --short | wc -l`; equivalentes para pron/spec2viz; `grep -RIn --exclude-dir=.git 'ViewDoc' ../sldb ../pron ../spec2viz`; greps de CAS/lock/índice/renderer; `sha256sum` de archivos sucios citados; `test -s` del entregable; `build_plan.py --check`; `validate_plan.py --check`; `context_review.py status`. **Resultado esperado:** documento no vacío, filas clasificadas sin inferencias, comandos trazados y checks de plan en verde; el Tester muestrea filas contra la fuente citada.
