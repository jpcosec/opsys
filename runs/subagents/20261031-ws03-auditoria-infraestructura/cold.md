## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md` como auditoría de solo lectura, verificable fila por fila, del estado actual de `sldb`, `pron` y `spec2viz`: fuente/payload, concurrencia real (CAS por revisión/hash, locks de archivo o DB), referencias documentales, búsquedas/índices/consultas expuestas y alcance real de ViewDoc. Lo no comprobado se marca «no comprobado» con causa; no se infiere.

**Alcance:** lectura de `../sldb`, `../pron`, `../spec2viz` y documentos del plan; escritura únicamente del entregable y de `runs/subagents/20261031-ws03-auditoria-infraestructura/` (`commands.log`, `result-summary.md`). Sin commits, sin closeout, sin modificar código, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas de otros. WS05 Scion, contratos nuevos e implementación quedan fuera.

**Repo:** `deskops` (cwd) con lectura cruzada a los tres repos citados. **Límites:** Kimun no es fuente de decisión; keine inferencia; la auditoría no sustituye WS02/04/06/08–12, que son tareas futuras ya asignadas por `cierre.md`, no lagunas de este encargo.

## AMBIGUEDADES

1. Título «persistencia, consultas y **notaciones**» vs Scope, que solo menciona «alcance real ViewDoc». Obligaría a inventar qué notaciones auditar (layout, notación de grafo, serialización).
2. «verificable fila por fila» sin esquema de filas: no se define columnas, granularidad (archivo/módulo/API) ni formato. Obligaría a inventar la estructura del entregable.
3. «control de concurrencia real de sldb/pron: CAS por revisión/hash, locks de archivo o DB; **a auditar**»: no aclara si CAS es hecho conocido o hipótesis a comprobar; inventaría el estado de partida.
4. «encabezado con ... **universo auditado**» no delimita qué archivos/módulos entran; obligaría a inventar cobertura.
5. Validation exige `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status`, pero el Executor «no escribe en desk/ salvo [entregable]» y «no corre closeout»; no se dice quién los ejecuta ni si esos scripts escriben. Obligaría a inventar el reparto Executor/Tester.
6. «Kimun solo referencia» frente a «Kimun no se usa como fuente de decisión»: no aclara si se permite leerlo; obligaría a inventar el permiso.

## DRY-RUN (sin ejecutar)

**Fuentes a leer:** TaskDoc WS03, `rituals/execution|testing|closeout.md`, pills 001/005/007 y la de fases, `cierre.md`, `brief.md`, `dag.yaml`, `context-review.md`, `activation.md`; luego README/specs y código de `sldb`, `pron`, `spec2viz`.

**Entregable:** `infraestructura.md` (fecha, HEAD por repo, universo, filas) + `commands.log` + `result-summary.md`.

**Comandos a correr después:** `git -C ../sldb rev-parse HEAD` (ídem pron/spec2viz), `ls`/`rg` sobre fuentes, payloads y tests de concurrencia/búsqueda/ViewDoc; `test -s` del entregable; scripts `--check`/`status`. **Esperado:** hash por repo, filas con evidencia citada o «no comprobado», validaciones verdes reportadas por quien corresponda.
