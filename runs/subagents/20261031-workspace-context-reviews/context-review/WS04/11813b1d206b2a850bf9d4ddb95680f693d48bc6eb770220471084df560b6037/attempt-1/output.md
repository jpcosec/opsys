## REFORMULACION

Propósito: auditar la UI y el trabajo en curso de graph_ui y reconciliarlos con este plan. Resultado: `auditoria/ui.md` con tareas externas (path, estado, hash, alcance), sesiones/solapamientos, reconciliación del SPEC externo y tabla de mapeo de nodos graph_ui. Repo dueño: deskops. Límites: leer graph_ui y SPEC sin cambiar tareas, Board ni código; no notificar ni despachar; partir de HEAD/Board y commits a1b2b22/f16fcd1/134a665.

## AMBIGUEDADES

1. «mapear a deltas existentes los nodos de este plan que toquen graph_ui (tarea o entrada del Board de graph_ui, o commit que ya lo implementa)» / «Tabla de mapeo para cada nodo graph_ui». No se define qué cuenta como “tocar graph_ui”: ¿solo nodos con `owner_repo: graph_ui`, o también los que prueban, consumen o condicionan graph_ui desde deskops/sldb? Obliga a inventar el perímetro de la tabla y arriesga omitir nodos o incluir otros fuera del encargo.

2. «reconciliar también el SPEC externo (coincidencias, discrepancias y ausencias frente a este plan, con path y hash)» junto a «Hash = SHA256 del archivo de tarea». La regla de hash solo cubre archivos de tarea; para el SPEC no fija algoritmo ni objeto exacto. Obliga a decidir cómo calcular ese hash y, por tanto, qué evidencia exacta quedará registrada.

3. «Sesión = trabajo en curso observable en Board, git status o paneles herdr». “herdr” no aparece definido en brief, alcance ni glosario. Obliga a inventar cómo observar esos paneles o cómo declarar su ausencia sin saber si existían.

## DRY-RUN

Lecturas previstas: Board y `desk/tasks/` de graph_ui; git log/status y commits citados; código y rutas de UI; SPEC externo; brief, alcance, decisiones, reconciliacion y dag. Cambios previstos: solo crear/actualizar `auditoria/ui.md`; ningún cambio en graph_ui ni en tareas. Dependencias: WS01 (brief) y existencia legible de graph_ui/SPEC. Validaciones futuras: cada tarea externa con path/estado/hash/alcance; cada solapamiento; reconciliación SPEC con path y hash; tabla por nodo graph_ui con base/delta/ticket o ausencia; ausencia de sesión registrada.

## FUTURO

WS06 consumirá `auditoria/ui.md` para la matriz de reconciliacion.md. WS11/12 registrarán aceptación por delta. El solicitante puede aportar un encargo explícito durante la ejecución y validar el inventario. Nada de ello altera este nodo.
