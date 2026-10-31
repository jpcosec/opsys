## REFORMULACION

**Propósito:** inventariar el trabajo de UI existente en `../UIs/graph_ui` y reconciliar los nodos del plan con tareas, entradas de Board o commits ya existentes, además del SPEC externo y cualquier encargo entregado al ejecutor.

**Resultado:** `auditoria/ui.md`, con correspondencias, estados observados, hashes y hallazgos del SPEC.

**Repo dueño:** `deskops`. **Límites:** solo lectura sobre graph_ui; no cambia tareas, Board ni código externo; no implementa; promoción no autorizada. Depende de WS01.

## AMBIGUEDADES

1. «mapear nodos de este plan a deltas existentes (tarea o entrada del Board de graph_ui, o commit que ya lo implementa)» junto con «Hash = SHA256 del archivo de tarea». Obliga a inventar qué `path` y qué hash corresponden a una entrada de Board sin archivo de tarea o a un commit, porque la regla de hash solo cubre archivos de tarea.

2. «identificar sesiones y solapamientos sin cambiar sus tareas». La aceptación no incluye sesiones ni solapamientos y no define qué cuenta como solapamiento. Obliga a inventar el criterio, la evidencia exigible y si ese inventario forma parte del resultado o es solo contexto.

3. «mapear nodos de este plan a deltas existentes». No acota si son todos los nodos o solo los relacionados con UI/graph_ui; el título dice «UI» pero el alcance no lo limita. Obliga a inventar el subconjunto de nodos que debe mapearse y permite exceder el alcance de `auditoria/ui.md`.

## DRY-RUN

**Lecturas previstas:** WS01 (`brief.md`), documentos del plan y `dag.yaml`; `../UIs/graph_ui` (Board, tareas, código); `git status` y paneles herdr; `/home/jp/proyectos/softfactory_spec/SPEC.md`; encargo aportado, si existe.

**Cambios previstos:** crear o actualizar únicamente `auditoria/ui.md`.

**Dependencias:** WS01 y acceso de lectura a graph_ui y al SPEC externo.

**Validaciones futuras:** cada tarea externa con path, estado, hash y alcance; SPEC reconciliado con coincidencias, discrepancias y ausencias, path y hash; registro explícito de ausencia de encargo; ningún cambio en tareas/Board de graph_ui.

## FUTURO

WS06 consume la correspondencia para proponer la matriz por repo dueño en `reconciliacion.md`. WS07 designa responsables; WS11/12 obtienen aceptaciones. La persona confirma P01/P02 y demás decisiones abiertas. WS04 no aprueba deltas ni habilita implementación.
