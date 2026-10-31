## REFORMULACION
**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`, auditoría de solo lectura, verificable fila por fila, sobre persistencia, consultas y notaciones en `../sldb`, `../pron`, `../spec2viz`.
**Alcance:** universo por capacidad (fuente/payload, conflictos/concurrencia, referencias documentales, búsquedas/índices, notaciones/ViewDoc); columnas capacidad, repo, ubicación, operación expuesta, estado (comprobado/ausente/hueco), evidencia. Encabezado con fecha, HEAD completo y nº de líneas de `git status --short` por repo leído. CAS/locks son hipótesis. Kimun fuera de universo.
**Repo:** `deskops`; rutas de lectura relativas a él; solo se escribe el entregable y evidencia en `runs/subagents/20261031-ws03-auditoria-infraestructura/` (`commands.log`, `result-summary.md`).
**Límites:** sin commits, sin closeout, sin tocar otros repos, `desk/` (salvo entregable), `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas de otros. Executor escribe; Supervisor valida/commitea/cierra; Tester muestrea.

## AMBIGUEDADES
1. «por cada repo realmente leído» — no fija umbral de “leído” (¿basta `rev-parse`/`ls`, o exige abrir archivos?). Obliga a inventar criterio.
2. «cantidad de líneas de `git status --short`» — no aclara si cuenta líneas de salida (incluye `?? dir/` como una) o entradas; obliga a elegir.
3. «todas las que spec2viz expone por CLI» + «por la ayuda de cada CLI» — no define cómo invocar la CLI en solo lectura (¿instalada, `python -m`, `--help`?). Obliga a inventar método.
4. «Función pública importable = símbolo sin guion bajo en un módulo del paquete» — no delimita “el paquete” (raíz, `__init__`, distribución). Obliga a inventar frontera.
5. «ViewDoc… si no aparece se registra ausente con el comando usado» — no dice si apariciones en tests/docs/comentarios cuentan. Obliga a decidir criterio.
6. «Si un archivo citado como evidencia está sucio, se agrega su SHA-256» — “sucio” depende de git; no cubre archivo fuera de git o repo sin git.
7. «Un límite se describe como se observa, sin definirlo en abstracto» — suficiencia no verificable; obliga a inventar el nivel de detalle.
Tareas futuras asignadas (no lagunas): commits/closeout del Supervisor, muestreo del Tester, consumo por WS06/WS08-12.

## DRY-RUN
**Fuentes a leer:** `activation.md`, `cierre.md`, `dag.yaml`, `brief.md`, `context-review.md`, pills referenciadas; solo lectura en `../sldb`, `../pron`, `../spec2viz` (excluyendo `.venv`, `node_modules`). No leer Kimun.
**Entregable:** `infraestructura.md` (encabezado + secciones/filas), `commands.log`, `result-summary.md`.
**Comandos después (no ejecutados):**
- `git -C ../sldb rev-parse HEAD` y `git -C ../sldb status --short | wc -l` (ídem pron, spec2viz) → HEAD y conteo; carpeta sin git declarada.
- `grep -rIn ViewDoc …` y `grep -rIni ViewDoc …` → coincidencias o ausencia registrada con comando.
- `--help`/`python -m … --help` de cada CLI → notaciones y operaciones expuestas.
- `sha256sum` de archivos sucios citados → hash fijado.
- `test -s …`, `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status` → existencia y checks OK.
**Esperado:** auditoría con filas comprobadas por archivo:línea/salida, ausencias registradas y huecos citados; ninguna inferencia marcada como comprobada.
