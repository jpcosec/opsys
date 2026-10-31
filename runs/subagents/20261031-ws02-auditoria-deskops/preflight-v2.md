## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/deskops.md`, auditoría de solo lectura del estado actual, verificable fila por fila, con secciones A (comandos y métodos), B (modelos), C (archivos) y D (cierre).

**Alcance:** una fila por superficie —archivo, comando público o modelo registrado— de las categorías enumeradas; operaciones públicas completas por fila; estados comprobado/no comprobado con causa; anexo `file-inventory.tsv` con `path`, `sha256`, `modelo o «no modelado»`.

**Repo:** este checkout; se lee `deskops/`, `desk/`, `runs/subagents/` y `.sldb`. Encabezado con fecha, HEAD completo y rutas sucias por repo leído.

**Límites:** solo se escribe `desk/drawer/plans/workspace-documental/auditoria/deskops.md` y evidencia en `runs/subagents/20261031-ws02-auditoria-deskops/`. El Executor no hace commits ni closeout; no modifica código, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas de otros. Fuera de alcance: WS05 Scion, contratos nuevos, implementación.

## AMBIGUEDADES

1. **Ubicación de `DeskopsOperations`.** Cita: «por método público sin guion bajo de DeskopsOperations». No se indica módulo ni ruta; si no aparece en el código, obligaría a inventar dónde buscarla o a declararla ausente sin criterio.
2. **Consulta de vinculación archivo-modelo.** Cita: «Un archivo es modelado si el store lo vincula a un modelo». No se especifica comando ni estructura de `.sldb` para leer ese vínculo; obligaría a inventar un método de consulta o a asumir que `sldb models list` basta.
3. **Ruta de «fases».** Cita: «desk/issues, desk/faq, desk/crossroads y fases se registran comprobando si existen». No se da path; obligaría a asumir `desk/fases` u otra ubicación.
4. **Alcance de «repo» en el encabezado.** Cita: «por cada repo realmente leído su HEAD completo y cantidad de rutas sucias». No aclara si `deskops/` y `desk/` son el mismo repo o repos distintos; obligaría a decidir el agrupamiento.
5. **Entidades de «coincidencia por ruta exacta».** Cita: «Coincidencia por ruta exacta.» No dice entre qué se compara; obligaría a asumir que es `path` del archivo frente a la ruta vinculada por el store.
6. **Criterio de «método público».** Cita: «método público sin guion bajo de DeskopsOperations». No aclara si incluye heredados, estáticos o propiedades; obligaría a fijar un criterio no dado.

## DRY-RUN

**Fuentes que leería:** el archivo de tarea; `deskops/cli/registry.py`; definición de `DeskopsOperations`; árbol de `desk/` y `runs/subagents/`; store `.sldb`; estado Git del checkout.

**Entregable:** `auditoria/deskops.md` con encabezado y tablas A–D; `runs/subagents/20261031-ws02-auditoria-deskops/file-inventory.tsv`; `commands.log`; `result-summary.md`.

**Comandos posteriores (solo lectura):** `git rev-parse HEAD`, `git status --porcelain`, `sldb models list --store .sldb`, `sha256sum` sobre archivos y anexo, listado de `desk/`, inspección de `registry.py` y de `DeskopsOperations`, `deskops --help` y `deskops closeout --help` si existen. **Resultado esperado:** filas con ubicación, operaciones, efecto, estado y evidencia; anexo TSV íntegro; resumen por categoría con conteos y hash del anexo; huecos marcados «no comprobado» con causa. No se ejecuta nada en este dictamen.
