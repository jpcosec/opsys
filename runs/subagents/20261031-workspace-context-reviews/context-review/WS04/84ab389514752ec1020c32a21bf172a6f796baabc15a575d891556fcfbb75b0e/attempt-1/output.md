REFORMULACION  
Propósito: inventariar y reconciliar el trabajo UI en curso de `graph_ui` para el plan documental. Resultado: `auditoria/ui.md` con tareas externas (path, estado observado, hash SHA256 y alcance), correspondencias de nodos que tocan `graph_ui`, solapamientos entre sesiones y reconciliación del SPEC externo y encargo aportado. Repo dueño: `deskops`. Límites: solo lectura de Board/tareas/código de `graph_ui`, `git status`, paneles herdr y SPEC; no cambia tareas, Board ni código; no ejecuta; promoción no autorizada.

AMBIGUEDADES  
1. «mapear a deltas existentes los nodos de este plan que toquen graph_ui»: no define qué significa “tocar” (owner_repo, mención textual, archivos afectados). Obliga a inventar el universo de nodos incluidos.  
2. «Cada tarea externa con path, estado observado, hash y alcance» y «Hash = SHA256 del archivo de tarea»: una «entrada del Board» puede no tener archivo de tarea; obliga a inventar un path/hash o una regla de exclusión.  
3. «archivos reclamados por dos sesiones»: no define cómo se registra una reclamación ni cómo atribuir cambios de `git status` o herdr a una sesión; obliga a inventar evidencia de autoría.  
4. «reconciliar también el SPEC externo … frente a este plan»: no fija granularidad ni si “plan” comprende brief, alcance, dag y demás documentos; obliga a inventar la matriz de comparación.

DRY-RUN  
Lecturas previstas: Board, tareas y código de `graph_ui`; `git status`; paneles herdr; SPEC; documentos del plan; encargo aportado. Cambios previstos: solo `auditoria/ui.md`; ninguno en `graph_ui`. Dependencia: WS01. Validaciones futuras: SHA256 por archivo de tarea, fila por tarea externa, solapamientos con evidencia, SPEC con path/hash, registro de ausencia de encargo y respeto de `output_scope`.

FUTURO  
WS06 consumirá la matriz; WS07 designará responsables; WS11/12 aceptarán alcance; el humano podrá entregar encargo y resolver Pxx; la promoción exigirá TaskDoc/preflight. Un faltante de contrato o acceso se registra y detiene según `alcance.md`.
