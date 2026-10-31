REFORMULACION
- **Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/deskops.md` como auditoría de solo lectura, verificable fila por fila, del estado actual de Deskops.
- **Alcance:** una fila por superficie: cada archivo de las categorías enumeradas bajo `desk/`, cada comando público/método de `DeskopsOperations` y cada modelo registrado que sirva esas superficies. Cada fila lista todas sus operaciones públicas, sin duplicar por comando. Distingue modelado (modelo registrado en store) de Markdown no modelado; cubre firmas, efectos Git y cierre. Dato pasivo: path/hash o listado read-only. Lo no comprobado se marca «no comprobado» con causa; no se infiere.
- **Repo:** este checkout; lectura de `deskops/`, `desk/` y `.sldb` local. Encabezado con fecha, HEAD y universo auditado.
- **Límites:** solo se escribe la auditoría y evidencia en `runs/subagents/20261031-ws02-auditoria-deskops/`. No código, otros repos, `dag.yaml`, `reconciliacion.md`, Board ajeno, tareas de otros, implementación ni WS05. El Executor no hace commits ni corre closeout.

AMBIGUEDADES
1. «Modelos y Markdown no modelado» / «Modelado = tiene modelo registrado en el store; Markdown no modelado = el resto». Si un Markdown está modelado, no queda claro si se inventaría como archivo, como modelo, en ambas filas o se excluye. Obligaría a inventar el criterio y podría duplicar filas.
2. «encabezado con fecha, commit HEAD de cada repo leído y universo auditado». En un checkout con árbol sucio, HEAD no identifica por sí solo el estado leído. Obligaría a decidir si añadir `git status`, hashes de archivos u otra referencia; el texto no lo fija.
3. «hash/listado read-only» no especifica algoritmo ni formato de hash. Obligaría a elegir uno y a inventar el formato de evidencia aceptable.

No son lagunas: preflight/cold review, Tester independiente, commit/closeout y las validaciones `build_plan.py`, `validate_plan.py` y `context_review.py` son tareas o gates futuros asignados; WS05, contratos nuevos e implementación están fuera de alcance.

DRY-RUN
- **Fuentes a leer:** taskdoc, `cierre.md`, `brief.md`, `dag.yaml`, activación, rituales, pills, código en `deskops/`, árbol `desk/` de categorías enumeradas y store `.sldb`.
- **Entregable:** `auditoria/deskops.md` con encabezado y filas; `commands.log` y `result-summary.md` en el run.
- **Comandos después:** `git rev-parse HEAD`; `git status --short` si se adopta; `find`/`rg --files` para inventario; `rg` para comandos y métodos; `sldb models list`; ayuda de `deskops` solo lectura. Luego validaciones: `test -s ...`, `python build_plan.py --check`, `python validate_plan.py --check`, `python context_review.py status`.
- **Resultado esperado:** listados y firmas citables; auditoría no vacía; checks de plan en exit 0/sin errores; estado de contexto coherente. El Tester independiente muestrea filas y deja su summary. No se ejecutó nada.
