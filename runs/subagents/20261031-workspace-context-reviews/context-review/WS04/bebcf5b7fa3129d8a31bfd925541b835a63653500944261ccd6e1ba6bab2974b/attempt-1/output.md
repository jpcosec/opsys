## REFORMULACION
**Propósito:** inventariar la UI de `graph_ui` y reconciliar el trabajo en curso para mapear los nodos de este plan que toquen `graph_ui` a tareas, entradas del Board, deltas o commits existentes; detectar sesiones y solapamientos; y reconciliar el SPEC externo.

**Resultado:** `auditoria/ui.md` en el repo `deskops`, con tablas de tareas externas, solapamientos, mapeo por nodo y reconciliación del SPEC.

**Repo dueño:** `deskops`. **Fuentes:** `../UIs/graph_ui` (Board, tareas, código, git) y `/home/jp/proyectos/softfactory_spec/SPEC.md`.

**Límites:** no cambiar tareas ni sesiones; las sesiones son coordinación, no autoridad privada; un commit solo prueba base citada, no aceptación ampliada; no ejecutar acciones del plan.

## AMBIGUEDADES
1. **“reconciliar también el SPEC externo (coincidencias, discrepancias y ausencias frente a este plan, con path y hash)”**: la aceptación define “Hash = SHA256 del archivo de tarea”, pero no define el algoritmo ni el objeto del hash para el SPEC externo —archivo completo, extracto o commit—. Obligaría al ejecutor a inventar qué hashear y cómo verificarlo.

## DRY-RUN
**Lecturas previstas:** `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, `dag.yaml`, SPEC externo, Board/tareas/código de `graph_ui`, `git status`/HEAD y commits `a1b2b22`, `f16fcd1`, `134a665`; paneles `herdr` para sesiones.

**Cambios previstos:** crear o actualizar `deskops:desk/drawer/plans/workspace-documental/auditoria/ui.md`. Sin cambios en tareas de `graph_ui`.

**Dependencias:** WS01 aporta brief/glosario; acceso de lectura a `graph_ui` y al SPEC externo.

**Validaciones futuras:** cada tarea externa con path, estado, hash y alcance; cada solapamiento; tabla por nodo `graph_ui`; reconciliación del SPEC con path y hash; registro de encargo aportado o de su ausencia; ninguna modificación de tareas.

## FUTURO
WS06 consumirá `auditoria/ui.md` para la matriz de correspondencia por repo. WS07 verificará el recibo de WS01. El solicitante puede aportar el “encargo” al ejecutar o confirmar que no hubo. La promoción fijará archivos, pills y TaskDoc; la aceptación de deltas corresponde al receptor P01, no a este nodo.
